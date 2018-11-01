# -*- coding: utf-8 -*-
"""基础数据获取"""
import re
import requests
import datetime
from django.conf import settings
from django.core.cache import cache
from rest_framework.response import Response
from rest_framework.views import APIView

from extends import Base, ts_api
from .models import StockInfo


class BasisDataViewSet(APIView):
    """基础数据"""
    # 次新的定义
    listed_day = 700
    code_list = []
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:62.0) Gecko/20100101 Firefox/62.0'
    }

    def get(self, request):
        all_code = ts_api(
            api_name='stock_basic',
            params={'list_status': 'L'},
            fields=['ts_code', 'name', 'list_date']
        )
        times_number = 100
        for num in range(0, len(all_code) // times_number + 1):
            code = ''
            for i in all_code[num * times_number:times_number * (num + 1)]:
                if 'ST' in i[1]:
                    continue
                code_split = str(i[0]).split('.')
                if not Base(StockInfo, **{'db_status': 1, 'code': code_split[0]}).findfilter():
                    listed_time = datetime.datetime.strptime(i[2], "%Y%m%d")
                    jet_lag = (
                            datetime.datetime.now() -
                            listed_time
                    ).days
                    if jet_lag <= self.listed_day:
                        new = 1
                    else:
                        new = 0
                    Base(StockInfo, **{
                        'db_status': 1,
                        'exchange': code_split[1],
                        'code': code_split[0],
                        'name': i[1],
                        'new': new,
                        'listed_time': datetime.datetime.strftime(listed_time, '%Y-%m-%d'),
                    }).save_db()
                code += f'{code_split[1].lower() + code_split[0]},'
            open_url = requests.get(settings.QT_URL2 + code, timeout=120)
            code_list = re.findall('".*"', open_url.text)
            for c in code_list:
                code_price_info = c.replace('"', '').split('~')
                query_code = Base(StockInfo, **{'db_status': 1, 'code': code_price_info[2]}).findfilter()
                if query_code:
                    jet_lag = (
                            datetime.date.today() -
                            query_code[0].listed_time
                    ).days
                    if jet_lag <= self.listed_day:
                        new = 1
                    else:
                        new = 0
                    query_code[0].new = new
                    query_code[0].name = code_price_info[1]
                    query_code[0].total_equity = round(float(code_price_info[-9]) / float(code_price_info[3]), 3)
                    query_code[0].circulate_equity = round(float(code_price_info[-10]) / float(code_price_info[3]), 3)
                    query_code[0].save()

            # 缓存数据到redis
            code_all = Base(StockInfo, **{'db_status': 1}).findfilter()
            for codes in code_all:
                code_dict = {
                    'exchange': f'{str(codes.exchange).lower()}{codes.code}',
                    'code': codes.code,
                    'circulate_equity': codes.circulate_equity,
                    'new': codes.new,
                    'sid': codes.id
                }
                cache.set(
                    f'cache_code_info_{str(codes.exchange).lower()}~{codes.code}',
                    code_dict,
                    timeout=24 * 60 * 60
                )

        return Response({"BasisData": {"Status": 1, "msg": "Basis data update node"}})
