# -*- coding: utf-8 -*-
"""数据库连接实例"""

from django.core import checks


class Base(object):

    def __init__(self, instance, limit=None, offset=None, using=None, order_by=None, **kwargs):
        """
        数据库公共方法
        :param instance: 实例
        :param limit: 结束值
        :param offset: 开始值
        :param using: 指定数据库
        :param order_by: 排序 -id 以id倒序排列
        :param kwargs type(dict) 查询条件

        __exact 精确匹配 字段__exact
        __iexact 不敏感大小写 字段__iexact
        __contains 模糊查询敏感大小写 字段__contains
        __in 包含查询 字段__in
        __gt 大于 字段__gt 例: id > 1
        __gte 大于 字段__gt 例: id >= 1
        __lt 小于 字段__lt 例: id < 1
        __lte 小于 字段__lte 例: id <= 1
        __startswith 区分大小写,开始位置匹配 例: LIKE 'Will%'
        __istartswith 不区分大小写，开始位置匹配 例: LIKE 'Will%'
        __endswith 区分大小写,结束位置匹配 例: LIKE '%Will'
        __iendswith 不区分大小写,结束位置匹配 例: LIKE '%Will'

        pk 表示主键
        """
        self.instance = instance
        self.limit = limit
        self.offset = offset
        self.using = using
        self.kwargs = kwargs
        self.order_by = order_by
        if self.offset and self.limit and self.offset >= self.limit:
            self.errord()

    @staticmethod
    def errord():
        """offset的值不能等于或大于limit"""
        return [checks.ERROR('offset的值不能等于或大于limit')]

    def findone(self, sid):
        """查询一条"""
        try:
            if self.using:
                return self.instance.objects.using(self.using).get(pk=sid)
            else:
                return self.instance.objects.get(pk=sid)
        except Exception:
            return None

    def findall(self):
        """查询所有"""
        if self.using:
            return self.instance.objects.using(self.using).all()[self.offset:self.limit]
        else:
            return self.instance.objects.all()[self.offset:self.limit]

    def findfilter(self):
        """满足条件"""
        # 包含
        if self.using and self.order_by:
            return self.instance.objects.using(self.using).filter(
                **self.kwargs
            ).order_by(self.order_by)[self.offset:self.limit]
        elif self.using:
            return self.instance.objects.using(self.using).filter(**self.kwargs)[self.offset:self.limit]
        elif self.order_by:
            return self.instance.objects.filter(**self.kwargs).order_by(self.order_by)[self.offset:self.limit]
        else:
            return self.instance.objects.filter(**self.kwargs)[self.offset:self.limit]

    def findexclude(self):
        """不满足条件"""
        # 不包含
        if self.using:
            return self.instance.objects.using(self.using).exclude(**self.kwargs)[self.offset:self.limit]
        else:
            return self.instance.objects.exclude(**self.kwargs)[self.offset:self.limit]

    def findfe(self):
        """精确和模糊查询"""
        # 包含和不包含
        if self.using:
            return self.instance.objects.using(self.using).filter(
                **self.kwargs['filter']
            ).exclude(['exclude'])[self.offset:self.limit]
        else:
            return self.instance.objects.filter(
                **self.kwargs['filter']
            ).exclude(['exclude'])[self.offset:self.limit]

    def db_count(self):
        """统计"""
        if self.using:
            return self.instance.objects.using(self.using).filter(**self.kwargs).count()
        else:
            return self.instance.objects.filter(**self.kwargs).count()

    def sql_raw(self, sql, *args):
        """实例下的SQL查询"""
        if args and self.using:
            return self.instance.objects.using(self.using).raw(sql, args)
        elif args and not self.using:
            return self.instance.objects.raw(sql, args)
        elif not args and self.using:
            return self.instance.objects.using(self.using).raw(sql)
        else:
            return self.instance.objects.raw(sql)

    @staticmethod
    def sql_custom(sql, *args, usings=None):
        from django.db import connections, connection
        """自定义SQL,不介助 实例"""
        if usings:
            cursor = connections[usings].cursor()
        else:
            cursor = connection.cursor()
        if args:
            cursor.execute(sql, args)
        else:
            cursor.execute(sql)
        desc = cursor.description
        return [
            dict(zip([col[0] for col in desc], row))
            for row in cursor.fetchall()
        ]

    def save_db(self):
        """save db"""
        if self.using:
            return self.instance.objects.using(self.using).create(**self.kwargs)
        else:
            return self.instance.objects.create(**self.kwargs)

    def batch_save(self, obj):
        """批量插入"""
        if self.using:
            return self.instance.objects.using(self.using).bulk_create(obj)
        else:
            return self.instance.objects.bulk_create(obj)

    def delete(self, sid):
        """del db"""
        if self.using:
            db_del = self.instance.objects.using(self.using).get(pk=sid)
            db_del.delete()
        else:
            db_del = self.instance.objects.using(self.using).get(pk=sid)
            db_del.delete()

    def update(self, update):
        """更新数据"""
        if self.using:
            return self.instance.objects.using(self.using).filter(**self.kwargs).update(**update)
        else:
            return self.instance.objects.filter(**self.kwargs).update(**update)
