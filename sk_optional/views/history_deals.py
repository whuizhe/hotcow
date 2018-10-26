# -*- coding: utf-8 -*-
"""历史交易"""
import json
import re
import datetime
import asyncio
import aiohttp
from django.conf import settings
from django.core.cache import cache
from rest_framework.response import Response
from rest_framework.views import APIView

from extends import Base, trading_day
from basicdata.models import StockPrice

__all__ = ['HistoryDealsViewSet', 'MainFlowsViewSet']


class HistoryDealsViewSet(APIView):
    """历史交易"""

    def get(self, request):
        """GET请求"""
        data = request.GET
        td_last = trading_day(2)[0]
        sk_all = cache.iter_keys('cache_code_info_*')
        tasks = []
        if data and 'average' in data:
            for i in sk_all:
                code = cache.get(i)
                tasks.append(self._ma_day(code['exchange'], td_last))
        else:
            for i in sk_all:
                code = cache.get(i)
                tasks.append(self._close_day(code['sid'], code['exchange']))

        if tasks:
            asyncio.set_event_loop(asyncio.new_event_loop())  # 创建新的协程
            loop = asyncio.get_event_loop()
            loop.run_until_complete(asyncio.wait(tasks))
            loop.close()

        return Response({'HistoryDeals': 'data update node'})

    @staticmethod
    async def fetch(sessions, url):
        async with sessions.get(url) as response:
            return await response.text()

    async def _close_day(self, sid, code_name):
        """收盘数据"""
        url = f'{settings.QT_URL1}appstock/app/fqkline/get?_var=kline_dayqfq&param=' \
              f'{code_name},day,{datetime.date.today().strftime("%Y-%m-%d")},,320,qfq'
        async with aiohttp.ClientSession() as session:
            url_info = await self.fetch(session, url)
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

    async def _ma_day(self, code_name, trading_day):
        """日均线"""
        url = f'{settings.QT_URL3}data/index.php?appn=price&c={code_name}'
        async with aiohttp.ClientSession() as session:
            url_info = await self.fetch(session, url)
            price_query = re.findall('".*"', url_info)
            if price_query:
                price_distribute = str(price_query[0]).replace('"', '').split('^')
                if price_distribute:
                    average, hand_number, active_number, bidding_rate = 0, 0, 0, 0
                    for i in price_distribute:
                        i = str(i).split('~')
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
        data = request.GET
        tasks = []
        sk_all = cache.iter_keys('cache_code_info_*')
        if data and 'code' in data:
            for i in sk_all:
                code = str(i).split('_')[-1]
                url = f"{settings.QT_URL3}data/view/ggdx.php?t=2&r=0.8876465514316253" \
                      f"&q={code.replace('~', '')}"
                tasks.append(self._read_data(url=url, num_day='day', code=code.split('~')[-1]))
        else:
            code_list = []
            for i in sk_all:
                code_list.append(str(i).split('_')[-1].replace('~', ''))
            times_number = 100
            for num in range(0, len(code_list) // times_number + 1):
                url = f"{settings.QT_URL3}data/view/ggdx.php?t=3&d=5&q=" \
                      f"{','.join(code_list[num * times_number:times_number * (num + 1)])}"
                tasks.append(self._read_data(url=url, num_day='many_day'))

        asyncio.set_event_loop(asyncio.new_event_loop())  # 创建新的协程
        loop = asyncio.get_event_loop()
        loop.run_until_complete(asyncio.wait(tasks))
        loop.close()
        return Response({'MainFlows': 'data update node'})

    async def _read_data(self, url, num_day, **kwargs):
        async with aiohttp.ClientSession() as session:
            url_info = await HistoryDealsViewSet.fetch(session, url)
            if num_day == 'many_day':
                url_data = url_info.replace(';', '').replace('\'', '').split('\n')
                for code in url_data:
                    amount_data = code.split('=')
                    if len(amount_data) != 2:
                        continue
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
                            if str(price.trading_day) in amount_dict and\
                                    (price.main_amount == 0 or not price.main_amount):
                                    price.main_amount = amount_dict[str(price.trading_day)][0]
                                    price.loose_amount = amount_dict[str(price.trading_day)][1]
                                    price.save()
            else:
                url_data = url_info.replace(';', '')
                amount_data = url_data.split('=')[1].replace('"', '').split('~')
                Base(StockPrice, **{'code': kwargs.get('code'), 'trading_day': str(datetime.date.today())}).update({
                    'main_amount': amount_data[2],
                    'loose_amount': amount_data[5]
                })
