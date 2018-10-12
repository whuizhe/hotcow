# -*- coding: utf-8 -*-
"""慢牛"""
from django_redis import get_redis_connection
from rest_framework.response import Response
from rest_framework.views import APIView

from extends import Base, ts_api
from basicdata.models import *

__all__ = ['SlowCowViewSet']


class SlowCowViewSet(APIView):
    """历史交易"""
    connection_redis = get_redis_connection()

    def get(self, request):
        """GET请求"""
        return Response({'SlowCow': 'data update node'})
