# -*- coding: utf-8 -*-

from django.urls import path
from sk_optional.views import *


urlpatterns = [
    path('datashow/', DataShowViewSet.as_view(), name='数据查询'),
    path('slowcow/', SlowCowViewSet.as_view(), name='慢牛'),
    path('analysisshow/', AnalysisShowViewSet.as_view(), name='慢牛展示'),
    path('industry/', IndustryViewSet.as_view(), name='行业'),
]
