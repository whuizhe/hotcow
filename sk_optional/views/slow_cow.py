# -*- coding: utf-8 -*-
"""慢牛"""
import datetime
from rest_framework.response import Response
from rest_framework.views import APIView

from extends import Base, ts_api
from basicdata.models import StockInfo, StockPrice
from basicdata.serializers import StockPriceSerializer

__all__ = ['SlowCowViewSet']


class SlowCowViewSet(APIView):
    """慢牛"""

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
            trading_day = [
                str(datetime.datetime.strptime(i[0], '%Y%m%d')).split(' ')[0] for i in trading_day[-15:]
            ]
            trading_day.reverse()
            code_dict = {
                's3': {},  # 上3天
                's2': {},  # 上2天
                'm': {},  # 满
                'x': {},  # 下,放量
            }
            code_all = Base(StockInfo, **{'db_status': 1}).findfilter()
            for i in code_all:
                ma_5, ma_10, day_data = 0, 0, {}
                code_info = Base(StockPrice, **{'sk_info_id': i.id, 'trading_day__in': trading_day}).findfilter()
                code_serializers = StockPriceSerializer(code_info, many=True)
                for day in code_serializers.data:
                    day_data[day['trading_day']] = day

                num = 0
                try:
                    if day_data[trading_day[num]]['close'] >= day_data[trading_day[num + 1]]['close']:
                        if day_data[trading_day[num + 1]]['close'] >= day_data[trading_day[num + 2]]['close']:
                            code_dict['s2'][i.code] = {

                            }
                            if day_data[trading_day[num + 2]]['close'] >= day_data[trading_day[num + 3]]['close']:
                                code_dict['s3'][i.code] = {

                                }
                except KeyError:
                    pass

            return Response({'SlowCow': code_dict})
