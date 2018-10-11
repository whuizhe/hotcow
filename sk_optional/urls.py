# -*- coding: utf-8 -*-
# 自选
from django.urls import path
from sk_optional.views import *


urlpatterns = [
    path('slowcow/', SlowCowViewSet.as_view(), name='慢牛'),
    path('mainflows/', MainFlowsViewSet.as_view(), name='资金流向'),
]
