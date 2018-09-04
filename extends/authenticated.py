# -*- coding: utf-8 -*-
"""权限认证"""
from rest_framework import exceptions
from django.core.cache import cache

from extends import Base


class Authenticated(object):
    """登录Token认证"""

    def has_permission(self, request, view):
        """
        用户登录认证
        """
        return True
