# -*- coding: utf-8 -*-

from django.urls import path
from sk_optional.views import *


urlpatterns = [
    path('datashow/', DataShowViewSet.as_view(), name='获取腾讯时时交易量'),
    path('analysisshow/', AnalysisShowViewSet.as_view(), name='分笔交易数据展示'),
    path('industry/', IndustryViewSet.as_view(), name='行业行情分析'),
    path('energyhuigui/', EnergyHuiguiViewSet.as_view(), name='能量回归'),
]
