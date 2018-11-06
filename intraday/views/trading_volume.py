# -*- coding: utf-8 -*-
"""盘中成交量分析"""
import re
import asyncio
import aiohttp
from datetime import date
from collections import OrderedDict
from django.conf import settings
from django.core.cache import cache
from rest_framework.response import Response
from rest_framework.views import APIView


__all__ = ['TradingVoViewSet']


class TradingVoViewSet(APIView):
    """盘中成交量分析"""

    def get(self, request):
        code_list = ['sz000669', 'sz300694', 'sz300508', 'sh603076', 'sz002356']
        tasks = []
        for i in code_list:
            tasks.append(self._constantly_deal(i))

        if tasks:
            asyncio.set_event_loop(asyncio.new_event_loop())  # 创建新的协程
            loop = asyncio.get_event_loop()
            loop.run_until_complete(asyncio.wait(tasks))
            loop.close()

        return Response({"BasisData": {"Status": 1, "msg": "Basis data update node"}})

    @staticmethod
    async def fetch(sessions, url):
        async with sessions.get(url) as response:
            return await response.text()

    async def _constantly_deal(self, code):
        """时时成交"""
        redis_key = f'constantly_deal_{code}_{date.today()}_cache'
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
