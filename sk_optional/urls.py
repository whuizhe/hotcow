# -*- coding: utf-8 -*-

from django.urls import path
from sk_optional.views import *


urlpatterns = [
    path('historydeals/', HistoryDealsViewSet.as_view(), name='拉取历史交易'),
    path('mainflows/', MainFlowsViewSet.as_view(), name='拉取资金流向'),
    path('datashow/', DataShowViewSet.as_view(), name='数据查询'),
    path('slowcow/', SlowCowViewSet.as_view(), name='慢牛'),
    path('analysisshow/', AnalysisShowViewSet.as_view(), name='慢牛展示'),
    path('industry/', IndustryViewSet.as_view(), name='行业'),
]
