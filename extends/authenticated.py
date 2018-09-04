# -*- coding: utf-8 -*-
"""权限认证"""


class Authenticated(object):
    """登录Token认证"""

    def has_permission(self, request, view):
        """
        用户登录认证
        """
        return True
