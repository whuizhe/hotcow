# -*- coding: utf-8 -*-

from django.urls import path
from .views import *


urlpatterns = [
    path('codeinfo/', BasisDataViewSet.as_view(), name='基础数据'),
    path('historydeals/', HistoryDealsViewSet.as_view(), name='拉取历史交易'),
    path('mainflowscurr/', MainFlowsCurrViewSet.as_view(), name='当天行情数据'),
    path('mainflows/', MainFlowsViewSet.as_view(), name='历史资金流向'),
]
