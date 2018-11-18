# -*- coding: utf-8 -*-

from django.urls import path
from .views import *


urlpatterns = [
    path('codeinfo/', BasisDataViewSet.as_view(), name='基础数据同步'),
    path('historydeals/', HistoryDealsViewSet.as_view(), name='同步历史交易'),
    path('mainflowscurr/', MainFlowsCurrViewSet.as_view(), name='同步当天资金流向'),
    path('mainflows/', MainFlowsViewSet.as_view(), name='同步历史资金流向'),
    path('concept/', ConceptViewSet.as_view(), name='基础概念同步'),
    path('dealdetail/', DealDetailViewSet.as_view(), name='成交分笔明细'),
]
