# -*- coding: utf-8 -*-
"""行业"""
import re
import requests
import datetime
from django.core.cache import cache
from django.conf import settings
from rest_framework.response import Response
from rest_framework.views import APIView

from extends import Base, trading_day
from basicdata.models import StockPrice


class IndustryViewSet(APIView):
    """行业行情分析"""
    analysis_data = {
        '连板': {},
    }
    trading_day = []


    def get(self, request):
        """行业行情分析"""
        data = request.GET
        if data and 'time' in data:
            industry_name = cache.get(f'industry_coce_cache_{data["time"]}')
        else:
            industry_name = {}
            url = f"{settings.QT_URL3}data/view/bdrank.php?&t=02/averatio&p=1&o=0&l=30&v=list_data"
            url_info1 = self._open_url(url)
            if url_info1:
                code_info1 = url_info1.split("data:'")[1].replace("'};", '').replace('qt', 'hz')
                # 行业祥情
                url = f"{settings.QT_URL2}q={code_info1}&r=11192163"
                url_info2 = self._open_url(url)
                if url_info2:
                    industry_list = re.findall('".*"', url_info2)
                    for i in industry_list:
                        industry_info = str(i).replace('"', '').split('~')
                        industry_name[industry_info[0]] = {
                            'name': industry_info[1],
                            'no.1': industry_info[11],
                            'new_code': []
                        }
                    # 行业各股
                    for i in code_info1.split(','):
                        url = f"{settings.QT_URL3}data/index.php?appn=rank&t={i.replace('bkhz', 'pt')}" \
                              f"/chr&p=1&o=0&l=6&v=list_data"
                        url_info3 = self._open_url(url)
                        if url_info3:
                            # 资金数据
                            code_info = url_info3.split("data:'")[1].replace("'};", '')
                            for code in code_info.split(','):
                                read_code = cache.get(f'cache_code_info_{code[:2]}~{code[2:]}')
                                if read_code:
                                    if read_code['new'] == 1:
                                        industry_name[i[4:]]['new_code'].append(read_code)
            cache.set(f'industry_coce_cache_{datetime.date.today()}', industry_name, timeout=None)
        return Response({"Industry": {"param": industry_name}})

    def _continuous_rise(self):
        """连续上涨"""
        td = trading_day(6)
        url = f'{settings.QT_URL3}data/view/dataPro.php?t=2&p=3'
        url_info = self._open_url(url)
        find_code = re.findall("'.*'", url_info)
        if find_code:
            code_list = str(find_code[0]).replace("'", '').split('^')
            for i in code_list:
                code_query = Base(StockPrice, **{'code': str(i).split('~')[0][2:], 'trading_day__in': td}).findfilter()
                print(str(i).split('~')[0][2:])
                print(code_query)
                print([i.average for i in code_query])
                print(i)
                return None

    def _accelerated(self):
        """突放量"""
        url = f'{settings.QT_URL3}data/view/dataPro.php?t=7&p=1'
        url_info = self._open_url(url)

        return None

    def _open_url(self, url):
        """请求url"""
        url_open = requests.get(url)
        if url_open.status_code == 200:
            url_info = url_open.text
            return url_info
        else:
            return None

