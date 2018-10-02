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


class StockInfo(models.Model):
    """应用节点监控数据"""

    id = models.AutoField(primary_key=True, blank=False, auto_created=True)
    db_status = models.IntegerField(verbose_name='数据状态', default=1, blank=False)
    exchange = models.CharField(verbose_name='交易所', max_length=8, blank=False)
    code = models.CharField(verbose_name='代码', max_length=6, blank=False)
    name = models.CharField(verbose_name='名称', max_length=32, blank=False)
    total_equity = models.FloatField(verbose_name='总股本', default=0, blank=False)
    listed_time = models.DateTimeField(auto_now_add=False, auto_now=False, blank=True)
    new = models.IntegerField(verbose_name='次新', default=0, blank=False)
    concept = JSONField(verbose_name='概念', blank=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True, blank=True)

    class Meta:
        db_table = "stock_info"
