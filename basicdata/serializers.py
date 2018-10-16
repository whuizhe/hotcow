# -*- coding: utf-8 -*-
"""
应用序列化器
显示全部字段 fields = '__all__'
"""

from .models import *
from rest_framework import serializers


class StockPriceSerializer(serializers.ModelSerializer):
    """基础应用"""

    class Meta:
        """表中要显示的字段"""
        model = StockPrice
        fields = '__all__'
