# -*- coding: utf-8 -*-
"""能量回归"""
import json
import re
import datetime
from pymongo import MongoClient
from django.conf import settings
from django.core.cache import cache
from rest_framework.response import Response
from rest_framework.views import APIView

from extends import Base
from basicdata.models import StockPrice, TradingDay
from sk_optional.models import MyChoiceData


__all__ = ['EnergyHuiguiViewSet']


class EnergyHuiguiViewSet(APIView):
    """能量回归"""
    mongo_conn = MongoClient(settings.MONGO_CONN)
    collection = None

    def get(self, request):
        """能量回归"""
        db = self.mongo_conn.hotcow
        self.collection = db.trading_data


        return Response({'MainFlows': 'data update node'})


