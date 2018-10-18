# -*- coding: utf-8 -*-
"""历史交易"""
from django.views.generic import View
from django.shortcuts import render

from extends import Base
from basicdata.models import StockInfo, StockPrice

__all__ = ['DataShowViewSet']


class DataShowViewSet(View):
    """历史交易"""

    def get(self, request):
        """GET请求"""
        data = request.GET
        if data and 'code' in data:
            code_query = Base(StockPrice, **{'code': data['code']}).findfilter()
            context = {
                'param': code_query,
                'code': data['code']
            }
            return render(request, 'sk_optional/datashow.html', context)

        return render(request, 'sk_optional/datashow.html')
