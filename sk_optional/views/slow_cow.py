# -*- coding: utf-8 -*-
"""慢牛"""
import json
import re
import requests
import datetime
from django.conf import settings
from django_redis import get_redis_connection
from rest_framework.response import Response
from rest_framework.views import APIView

from extends import Base, ts_api
from basicdata.models import *

__all__ = ['SlowCowViewSet', 'MainFlowsViewSet']


class SlowCowViewSet(APIView):
    """慢牛"""
    connection_redis = get_redis_connection()

    def get(self, request):
        """GET请求"""

        today = datetime.date.today()
        trading_day = ts_api(
            api_name='trade_cal',
            params={
                'is_open': 1,
                'start_date': (today - datetime.timedelta(days=30)).strftime('%Y%m%d'),
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
                    self.connection_redis.rpush(
                        'SlowCow_List',
                        json.dumps({'sid': i.id, 'td': td, 'td_last': td_last})
                    )

        return Response({'SlowCow': 'data update node'})

    def post(self, request):
        data = request.data
        if data:
            self.close_day(data['sid'], data['td'], data['td_last'])

        return Response({'SlowCow': 'data update node'})

    def close_day(self, sid, td, td_last):
        """收盘数据"""
        code_one = Base(StockInfo, **{'db_status': 1}).findone(sid)
        url = f'{settings.QT_URL1}appstock/app/fqkline/get?_var=kline_dayqfq&param=' \
              f'{str(code_one.exchange).lower()}{code_one.code},day,{td},,320,qfq'
        url_open = requests.get(url)
        url_info = url_open.text
        history_data = json.loads(url_info.split('=')[1])
        # 获取分价表
        day_data = []
        if 'qfqday' in history_data['data'][str(code_one.exchange).lower() + code_one.code]:
            day_data = history_data['data'][str(code_one.exchange).lower() + code_one.code]['qfqday']
        elif 'day' in history_data['data'][str(code_one.exchange).lower() + code_one.code]:
            day_data = history_data['data'][str(code_one.exchange).lower() + code_one.code]['day']
        if day_data:
            for price in day_data:
                if not Base(StockPrice, **{'code': code_one.code, 'trading_day': price[0]}).findfilter():
                    add_price = {
                        'sk_info_id': code_one.id,
                        'code': code_one.code,
                        'trading_day': price[0],
                        'open': float(price[1]),
                        'close': float(price[2]),
                        'high': float(price[3]),
                        'low': float(price[4]),
                        'hand_number': eval(price[5])
                    }
                    Base(StockPrice, **add_price).save_db()

        self.ma_day(str(code_one.exchange).lower(), code_one.code, td_last)

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


class MainFlowsViewSet(APIView):
    """资金流向"""

    def get(self, request):
        """GET请求"""
        sk_all = Base(StockInfo, **{'db_status': 1}).findfilter()
        code_list = []
        for i in sk_all:
            code_list.append(f'{i.exchange}{i.code}'.lower())
        times_number = 100
        for num in range(0, len(code_list) // times_number + 1):
            url = f"{settings.QT_URL3}data/view/ggdx.php?t=3&d=18&q=" \
                  f"{','.join(code_list[num * times_number:times_number * (num + 1)])}"
            url_open = requests.get(url)
            url_info = url_open.text
            url_data = url_info.replace(';', '').replace('\'', '').split('\n')
            for code in url_data:
                amount_data = code.split('=')
                amount_date = amount_data[1].split('~')
                amount_dict = {}
                for i in amount_date:
                    if '^' in i:
                        index = amount_date.index(i)
                        amount_dict[i.split('^')[0]] = (
                            float(amount_date[index - 2]),
                            float(amount_date[index - 1])
                        )
                code_price = Base(StockPrice, **{'code': amount_data[0].split('_')[-1][2:]}).findfilter()
                if code_price:
                    for price in code_price:
                        if price.main_amount == 0 or not price.main_amount and str(
                                price.trading_day) in amount_dict:
                            price.main_amount = amount_dict[str(price.trading_day)][0]
                            price.loose_amount = amount_dict[str(price.trading_day)][1]
                            price.save()
        return Response({'SlowCow': 'data update node'})
