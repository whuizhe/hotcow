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
from django.db import models

from basicdata.models import StockInfo


class MyChoiceData(models.Model):
    """我的数据"""

    id = models.AutoField(primary_key=True, blank=False, auto_created=True)
    sk_info = models.ForeignKey(StockInfo, on_delete=None, related_query_name='sk_info_id')
    trading_day = models.DateField(auto_now_add=False, auto_now=True, blank=True)
    trading_data = JSONField(verbose_name='交易数据')
    deal_data = JSONField(verbose_name='分价数据')
    updated = models.DateTimeField(auto_now_add=False, auto_now=True, blank=True)

    class Meta:
        db_table = "my_choice_data"
