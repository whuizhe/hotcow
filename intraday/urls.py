# -*- coding: utf-8 -*-

from django.urls import path
from .views import *


urlpatterns = [
    path('turnover/', TradingVoViewSet.as_view(), name='盘中成交量分析'),
]
