# -*- coding: utf-8 -*-
"""慢牛"""
import time
import requests
import datetime
import tushare as ts
from django.conf import settings
from rest_framework.response import Response
from rest_framework.views import APIView

from extends import Base
from basicdata.models import StockInfo


class SlowCowViewSet(APIView):
    """慢牛"""
    code_list = []
    qt_url1 = 'http://qt.gtimg.cn/q='
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:62.0) Gecko/20100101 Firefox/62.0'
    }

    def get(self, request):
        a = ts.pro_api(settings.TS_TOKEN)

        # sk_all = Base(StockInfo, **{'db_status': 1}).findfilter()
        # for i in sk_all:
        #     pass


        return Response({'SlowCow': [1, 2, 3]})