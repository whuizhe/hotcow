# -*- coding: utf-8 -*-

from django.urls import path
from sk_optional.views import *


urlpatterns = [
    path('historydeals/', HistoryDealsViewSet.as_view(), name='历史交易'),
    path('mainflows/', MainFlowsViewSet.as_view(), name='资金流向'),
    path('datashow/', DataShowViewSet.as_view(), name='数据展示'),
    path('slowcow/', SlowCowViewSet.as_view(), name='慢牛'),
]
