# -*- coding: utf-8 -*-
# 基础数据
"""
class Meta:
    指定表名
    db_table = ""
    模型中可排列的字段名称
    get_latest_by = ""
    在父对象中有序,可排序的
    order_with_respect_to = ""
    默认顺序 "a" 正序 "-a" 倒序,可多个字段["a","-b"]
    ordering = ""
    权限
    permissions = ('add', 'change', 'delete')
"""
from django_mysql.models import JSONField
from djongo import models as djongo_models
from django.db import models


class MyChoiceData(models.Model):
    """我的数据"""

    id = models.AutoField(primary_key=True, blank=False, auto_created=True)
    code = models.CharField(verbose_name='代码', max_length=11, blank=False)
    trading_day = models.DateField(auto_now_add=False, auto_now=True, blank=True)
    trading_data = JSONField(verbose_name='交易数据')
    deal_data = JSONField(verbose_name='分价数据')
    mongo_id = models.CharField(verbose_name='mongoid', max_length=64, blank=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True, blank=True)

    class Meta:
        db_table = "my_choice_data"

class TradingData(djongo_models.Model):
    """交易数据-Mongo"""

    code = djongo_models.CharField(verbose_name='code', max_length=16, blank=False)
    trading_day = djongo_models.DateField(auto_now_add=False, auto_now=True, blank=True)
    trading_list = djongo_models.ListField()
