# -*- coding: utf-8 -*-
"""历史交易"""
import json
import re
import requests
import datetime
import asyncio
from django.conf import settings
from rest_framework.response import Response
from rest_framework.views import APIView

from extends import Base, ts_api
from basicdata.models import *

__all__ = ['HistoryDealsViewSet', 'MainFlowsViewSet']


class HistoryDealsViewSet(APIView):
    """历史交易"""
    today = datetime.date.today()

    def get(self, request):
        """GET请求"""
        trading_day = ts_api(
            api_name='trade_cal',
            params={
                'is_open': 1,
                'start_date': (self.today - datetime.timedelta(days=10)).strftime('%Y%m%d'),
                'end_date': self.today.strftime('%Y%m%d')
            },
            fields=['cal_date', 'is_open']
        )
        if trading_day:
            td_last = datetime.datetime.strftime(
                datetime.datetime.strptime(trading_day[-1][0], '%Y%m%d'), '%Y-%m-%d'
            )  # 最近历史交易日

            tasks = []
            asyncio.set_event_loop(asyncio.new_event_loop())  # 创建新的协程
            loop = asyncio.get_event_loop()
            sk_all = Base(StockInfo, **{'db_status': 1}).findfilter()
            for i in sk_all:
                if not Base(StockPrice, **{'code': i.code, 'trading_day': td_last}).findfilter():
                    code_name = str(i.exchange).lower() + i.code
                    tasks.append(asyncio.ensure_future(self.run(i.id, code_name)))
                    print(i.code)

            loop.run_until_complete(asyncio.wait(tasks))
            loop.close()

        return Response({'HistoryDeals': 'data update node'})

    async def run(self, sid, code_name):
        """运行"""
        await self.close_day(sid, code_name)

    def close_day(self, sid, code_name):
        """收盘数据"""
        url = f'{settings.QT_URL1}appstock/app/fqkline/get?_var=kline_dayqfq&param=' \
              f'{code_name},day,{self.today.strftime("%Y-%m-%d")},,320,qfq'
        url_open = requests.get(url)
        url_info = url_open.text
        history_data = json.loads(url_info.split('=')[1])
        # 获取分价表
        day_data = []
        if 'qfqday' in history_data['data'][code_name]:
            day_data = history_data['data'][code_name]['qfqday']
        elif 'day' in history_data['data'][code_name]:
            day_data = history_data['data'][code_name]['day']
        if day_data:
            for price in day_data:
                if not Base(StockPrice, **{'code': code_name[2:], 'trading_day': price[0]}).findfilter():
                    add_price = {
                        'sk_info_id': sid,
                        'code': code_name[2:],
                        'trading_day': price[0],
                        'open': float(price[1]),
                        'close': float(price[2]),
                        'high': float(price[3]),
                        'low': float(price[4]),
                        'hand_number': eval(price[5])
                    }
                    Base(StockPrice, **add_price).save_db()
                    self.ma_day(code_name, price[0])

    @staticmethod
    def ma_day(code_name, trading_day):
        """日均线"""
        url = f'{settings.QT_URL3}data/index.php?appn=price&c={code_name}'
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
            Base(StockPrice, **{'code': code_name[2:], 'trading_day': trading_day}).update({
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

        return Response({'MainFlows': 'data update node'})
