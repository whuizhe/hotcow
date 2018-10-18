# -*- coding: utf-8 -*-
"""历史交易"""
import datetime
from django.views.generic import View
from django.shortcuts import render

from extends import Base, ts_api
from basicdata.models import StockInfo, StockPrice

__all__ = ['DataShowViewSet']


class DataShowViewSet(View):
    """历史交易"""

    def get(self, request):
        """GET请求"""
        data = request.GET
        if data and 'code' in data:
            trading_day = ts_api(
                api_name='trade_cal',
                params={
                    'is_open': 1,
                    'start_date': (datetime.date.today() - datetime.timedelta(days=10)).strftime('%Y%m%d'),
                    'end_date': datetime.date.today().strftime('%Y%m%d')
                },
                fields=['cal_date', 'is_open']
            )
            if trading_day:
                trading_day = [
                    str(datetime.datetime.strptime(i[0], '%Y%m%d')).split(' ')[0] for i in trading_day[-15:]
                ]
            code_data = []
            code_query = Base(StockPrice, **{'code': data['code'], 'trading_day__in': trading_day}).findfilter()
            for i in code_query:
                code_data.append({
                    'open': i.open,
                    'close': i.close,
                    'high': i.high,
                    'low': i.low,
                    'average': i.average,
                    'trading_day': i.trading_day,
                    'hand_number': round(i.hand_number * i.average / 1000000, 2),
                    'turnover_rate': f'{round(i.hand_number / (i.sk_info.circulate_equity * 1000000) * 100, 2)}%',
                    'bidding_rate': f'{round(i.bidding_rate * 100, 0)}%',
                    'main_amount': i.main_amount,
                    'loose_amount': i.loose_amount,
                })


            code_info = Base(StockInfo, **{'db_status': 1, 'code': data['code']}).findfilter()
            context = {
                'param': code_data,
                'code': data['code'],
                'code_name': code_info[0].name
            }
            return render(request, 'sk_optional/datashow.html', context)

        return render(request, 'sk_optional/datashow.html')
