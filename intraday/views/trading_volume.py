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
from basicdata.models import TradingDay, StockInfo
from sk_optional.models import MyChoiceData


__all__ = ['TradingVoViewSet']


class TradingVoViewSet(APIView):
    """
    盘中成交量分析
    S 卖盘
    B 买盘
    M 中性盘
    """

    def get(self, request):
        query_day = Base(TradingDay, **{'day': datetime.date.today()}).findfilter()
        if query_day:
            # 抓取数据
            my_code = Base(StockInfo, **{'db_status': 1, 'my_choice': 1}).findfilter()
            tasks = []
            for i in my_code:
                tasks.append(self._constantly_deal(f'{i.exchange}{i.code}'.lower()))

            if tasks:
                asyncio.set_event_loop(asyncio.new_event_loop())  # 创建新的协程
                loop = asyncio.get_event_loop()
                loop.run_until_complete(asyncio.wait(tasks))
                loop.close()

            # 分析并保存到db
            trading_day = str(datetime.date.today())
            if int(datetime.datetime.now().strftime('%H')) <= 8:
                trading_day = Base(TradingDay).findone(query_day[0].id - 1).day
            for i in my_code:
                add_data = self._trading_volume(f'{i.exchange}{i.code}'.lower(), i.id)
                if not Base(MyChoiceData, **{
                    'sk_info_id': i.id,
                    'trading_day': trading_day
                }).findfilter():
                    Base(MyChoiceData, **add_data).save_db()
                else:
                    Base(MyChoiceData, **{
                        'sk_info_id': i.id,
                        'trading_day': trading_day
                    }).update({
                        'deal_data': add_data['deal_data'],
                        'trading_data': add_data['trading_data']
                    })
        return Response({"BasisData": {"Status": 1, "msg": "Trading Vo Node"}})

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
                        read_cache['data'][ms[1]] = (
                            eval(ms[0]),
                            eval(ms[2]),
                            eval(ms[3]),
                            eval(ms[4]),
                            eval(ms[5]),
                            ms[6]
                        )
                else:
                    read_cache['number'] = i - 1
                    break

        cache.set(redis_key, read_cache, timeout=3 * 24 * 60 * 60)
        return None

    def _trading_volume(self, code, sid: int = 0):
        """
        数据分析
        """
        redis_key = f'constantly_deal_{code}_{datetime.date.today()}_cache'
        read_cache = cache.get(redis_key)
        if read_cache:
            add_data = {
                'sk_info_id': sid,
                'deal_data': read_cache['data'],
                'trading_day': datetime.date.today(),
                'trading_data': {
                    'z_buy': 0,  # 主买,
                    'z_sell': 0,  # 主卖
                    'caoda_dan': 0,  # 超大单
                    'da_dan': 0,  # 大单
                    'zhong_dan': 0,  # 中单
                    'xiao_dan': 0,  # 小单
                    'zhong_xing': 0,  # 中性盘,
                    'liu_ru': 0,  # 流入
                    'liu_chu': 0,  # 流出
                    'total': 0,
                }
            }

            for keys in read_cache['data']:
                # 主买卖
                if eval(read_cache['data'][keys][3]) >= 0.02:
                    add_data['trading_data']['z_buy'] += eval(read_cache['data'][keys][5]) / 10000
                elif eval(read_cache['data'][keys][3]) <= -0.02:
                    add_data['trading_data']['z_sell'] += eval(read_cache['data'][keys][5]) / 10000

                # 超大中小单
                if eval(read_cache['data'][keys][5]) >= 5000000:
                    add_data['trading_data']['caoda_dan'] += eval(read_cache['data'][keys][5]) / 10000
                if eval(read_cache['data'][keys][5]) >= 500000:
                    add_data['trading_data']['da_dan'] += eval(read_cache['data'][keys][5]) / 10000
                elif 200000 <= eval(read_cache['data'][keys][5]) < 500000:
                    add_data['trading_data']['zhong_dan'] += eval(read_cache['data'][keys][5]) / 10000
                else:
                    add_data['trading_data']['xiao_dan'] += eval(read_cache['data'][keys][5]) / 10000

                # 流出入
                if read_cache['data'][keys][-1] == 'B':
                    add_data['trading_data']['liu_ru'] += eval(read_cache['data'][keys][5]) / 10000
                elif read_cache['data'][keys][-1] == 'S':
                    add_data['trading_data']['liu_chu'] += eval(read_cache['data'][keys][5]) / 10000
                else:
                    add_data['trading_data']['zhong_xing'] += eval(read_cache['data'][keys][5]) / 10000

                # 总量
                add_data['trading_data']['total'] += eval(read_cache['data'][keys][5]) / 100000000
            return add_data
        return None
