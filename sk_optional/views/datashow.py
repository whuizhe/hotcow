# -*- coding: utf-8 -*-
"""历史交易"""
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from django.conf import settings
from rest_framework.response import Response
from rest_framework.views import APIView

from extends import Base
from basicdata.models import *

__all__ = ['DataShowViewSet']


class DataShowViewSet(APIView):
    """历史交易"""

    def get(self, request):
        """GET请求"""
        data = request.GET
        if data and 'code' in data:
            xs = []
            ys = []
            code_query = Base(StockPrice, **{'code': data['code']}).findfilter()
            for i in code_query:
                xs.append(i.trading_day)
                ys.append(i.average)
            # plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
            # plt.gca().xaxis.set_major_locator(mdates.DayLocator())
            plt.plot(xs, ys, label='MA1')
            plt.xlabel('交易日')
            plt.ylabel('价格')
            plt.legend()
            plt.gcf().autofmt_xdate()
            plt.show()

        return Response({'DataShow': ''})
