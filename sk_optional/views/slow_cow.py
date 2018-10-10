# -*- coding: utf-8 -*-
"""慢牛"""
import json
import re
import requests
import datetime
from django.conf import settings
from rest_framework.response import Response
from rest_framework.views import APIView

from extends import Base, ts_api
from basicdata.models import *


class SlowCowViewSet(APIView):
    """慢牛"""

    def get(self, request):
        today = datetime.date.today()
        trading_day = ts_api(
            api_name='trade_cal',
            params={
                'is_open': 1,
                'start_date': (today - datetime.timedelta(days=10)).strftime('%Y%m%d'),
                'end_date': today.strftime('%Y%m%d')
            },
            fields=['cal_date', 'is_open']
        )
        if trading_day:
            td = datetime.datetime.strftime(
                datetime.datetime.strptime(trading_day[0][0], '%Y%m%d'), '%Y-%m-%d'
            )
            td_last = datetime.datetime.strftime(
                datetime.datetime.strptime(trading_day[-1][0], '%Y%m%d'), '%Y-%m-%d'
            )
            sk_all = Base(StockInfo, **{'db_status': 1}).findfilter()
            for i in sk_all:
                if not Base(StockPrice, **{'code': i.code, 'trading_day': td_last}).findfilter():
                    # 获取历史数据
                    url = f'{settings.QT_URL1}appstock/app/fqkline/get?_var=kline_dayqfq&param=' \
                          f'{str(i.exchange).lower()}{i.code},day,{td},,320,qfq'
                    url_open = requests.get(url)
                    url_info = url_open.text
                    history_data = json.loads(url_info.split('=')[1])
                    # 获取分价表
                    if 'qfqday' in history_data['data'][str(i.exchange).lower() + i.code]:
                        for price in history_data['data'][str(i.exchange).lower() + i.code]['qfqday']:
                            if not Base(StockPrice, **{'code': i.code, 'trading_day': price[0]}).findfilter():
                                add_price = {
                                    'sk_info_id': i.id,
                                    'code': i.code,
                                    'trading_day': price[0],
                                    'open': float(price[1]),
                                    'close': float(price[2]),
                                    'high': float(price[3]),
                                    'low': float(price[4]),
                                    'hand_number': eval(price[5])
                                }
                                Base(StockPrice, **add_price).save_db()
                self.ma_day(str(i.exchange).lower(), i.code, td_last)
        return Response({'SlowCow': 'data update node'})

    @staticmethod
    def ma_day(exchange, code, trading_day):
        """日均线"""
        code_price = Base(StockPrice, **{'code': code, 'trading_day': trading_day}).findfilter()
        if code_price and code_price[0].average == 0:
            url = f'{settings.QT_URL3}data/index.php?appn=price&c={exchange}{code}'
            url_open = requests.get(url)
            url_info = url_open.text
            price_query = re.findall('".*"', url_info)
            if price_query and price_query[0] != '""':
                price_data = price_query[0][1:-1]
                price_distribute = str(price_data).split('^')
                price_distribute = [i.split('~') for i in price_distribute]
                average, hand_number, active_number, bidding_rate = 0, 0, 0, 0
                for i in price_distribute:
                    average += float(i[0]) * eval(i[2])
                    hand_number += eval(i[2])
                    active_number += eval(i[1])
                Base(StockPrice, **{'code': code, 'trading_day': trading_day}).update({
                    'average': round(average / hand_number, 2),
                    'active_number': active_number,
                    'bidding_rate': round(active_number / hand_number, 2)
                })
