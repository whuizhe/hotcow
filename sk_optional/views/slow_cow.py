# -*- coding: utf-8 -*-
"""慢牛"""
import datetime
from rest_framework.response import Response
from rest_framework.views import APIView

from extends import Base, ts_api
from basicdata.models import StockInfo, StockPrice

__all__ = ['SlowCowViewSet']


class SlowCowViewSet(APIView):
    """历史交易"""

    def get(self, request):
        """GET请求"""
        trading_day = ts_api(
            api_name='trade_cal',
            params={
                'is_open': 1,
                'start_date': (datetime.date.today() - datetime.timedelta(days=30)).strftime('%Y%m%d'),
                'end_date': datetime.date.today().strftime('%Y%m%d')
            },
            fields=['cal_date', 'is_open']
        )
        if trading_day:
            trading_day = [str(datetime.datetime.strptime(i[0], '%Y%m%d')).split(' ')[0] for i in trading_day[-10:]]
            code_all = Base(StockInfo, **{'db_status': 1}).findfilter()
            for i in code_all:
                code_info = Base(StockPrice, **{'sk_info_id': i.id, 'trading_day__in': trading_day}).findfilter()
                print(code_info)
                return Response({'SlowCow': {}})
