# -*- coding: utf-8 -*-
"""盘中成交量分析"""
import re
import asyncio
import aiohttp
import datetime
from collections import OrderedDict
from django.conf import settings
from django.core.cache import cache
from rest_framework.response import Response
from rest_framework.views import APIView

from extends import Base
from basicdata.models import TradingDay
from sk_optional.models import MyChoice, MyChoiceData


__all__ = ['TradingVoViewSet']


class TradingVoViewSet(APIView):
    """
    盘中成交量分析
    S 卖盘
    B 买盘
    M 中性盘
    """

    def get(self, request):
        data = request.GET
        if Base(TradingDay, **{'day': datetime.date.today()}).findfilter():
            my_code = Base(MyChoice, **{'db_status': 1}).findfilter()
            if not data:
                tasks = []
                for i in my_code:
                    tasks.append(self._constantly_deal(i.code))

                if tasks:
                    asyncio.set_event_loop(asyncio.new_event_loop())  # 创建新的协程
                    loop = asyncio.get_event_loop()
                    loop.run_until_complete(asyncio.wait(tasks))
                    loop.close()
            elif data and 'save' in data:
                for i in my_code:
                    if not Base(MyChoiceData, **{
                        'my_choice_id': i.id,
                        'trading_day': datetime.date.today()
                    }).findfilter():
                        add_data = self._trading_volume(i.code, i.id)
                        Base(MyChoiceData, **add_data).save_db()
            elif data and 'shishi' in data:
                shishi_data = {}
                for i in my_code:
                    shishi_data[i.code] = self._trading_volume(i.code)
                return Response(shishi_data)

        return Response({"BasisData": {"Status": 1, "msg": "Basis data update node"}})

    @staticmethod
    async def fetch(sessions, url):
        async with sessions.get(url) as response:
            return await response.text()

    async def _constantly_deal(self, code):
        """时时成交"""
        redis_key = f'constantly_deal_{code}_{datetime.date.today()}_cache'
        read_cache = cache.get(redis_key)
        if not read_cache:
            read_cache = OrderedDict()
            read_cache['number'] = 0
            read_cache['data'] = OrderedDict()

        for i in range(read_cache['number'], 100):
            url = f'{settings.QT_URL3}data/index.php?appn=detail&action=data&c={code}&p={i}'
            async with aiohttp.ClientSession() as session:
                url_info = await self.fetch(session, url)
                if url_info:
                    deal_info = re.search('\".*\"', url_info)
                    for m in deal_info.group().replace('"', '').split('|'):
                        ms = m.split('/')
                        read_cache['data'][ms[1]] = ms
                else:
                    read_cache['number'] = i - 1

        cache.set(redis_key, read_cache, timeout=3 * 24 * 60 * 60)
        return None

    def _trading_volume(self, code, sid: int = 0):
        redis_key = f'constantly_deal_{code}_{datetime.date.today()}_cache'
        read_cache = cache.get(redis_key)
        z_buy = 0  # 主买
        z_sell = 0  # 主卖
        da_dan = 0  # 大单
        zhong_dan = 0  # 中单
        xiao_dan = 0  # 小单
        liu_ru = 0  # 流入
        liu_chu = 0  # 流出
        zhong_xing = 0  # 中性
        for keys in read_cache['data']:
            # 主买卖
            if eval(read_cache['data'][keys][3]) >= 0.02:
                z_buy += eval(read_cache['data'][keys][5])
            elif eval(read_cache['data'][keys][3]) <= -0.02:
                z_sell += eval(read_cache['data'][keys][5])
            # 大中小单
            if eval(read_cache['data'][keys][5]) >= 500000:
                da_dan += eval(read_cache['data'][keys][5])
            elif 200000 <= eval(read_cache['data'][keys][5]) < 500000:
                zhong_dan += eval(read_cache['data'][keys][5])
            else:
                xiao_dan += eval(read_cache['data'][keys][5])
            # 流出入
            if read_cache['data'][keys][-1] == 'B':
                zhong_xing += eval(read_cache['data'][keys][5])
            elif read_cache['data'][keys][-1] == 'S':
                liu_ru += eval(read_cache['data'][keys][5])
            else:
                liu_chu += eval(read_cache['data'][keys][5])
        add_data = {
            'trading_day': datetime.date.today(),
            'trading_data': {
                'z_buy': z_buy / 10000,
                'z_sell': z_sell / 10000,
                'da_dan': da_dan / 10000,
                'zuong_dan': zhong_dan / 10000,
                'xiao_dan': xiao_dan / 10000,
                'zhong_xing': zhong_xing / 10000,
                'liu_ru': liu_ru / 10000,
                'liu_chu': liu_chu / 10000,
                'total': (zhong_dan + xiao_dan + da_dan) / 10000
            }
        }
        if sid != 0:
            add_data['my_choice_id'] = sid
            add_data['deal_data'] = read_cache['data']

        return add_data
