# -*- coding: utf-8 -*-
"""交易日"""
import datetime
from django.core.cache import cache

from extends import Base
from basicdata.models import TradingDay


def trading_day(days: int):
    """获取交易日列表"""
    trading_days = cache.get('trading_days_cache')
    if not trading_days:
        date_query = Base(TradingDay, **{'day__lte': datetime.date.today()}).findfilter()
        trading_days = [str(i.day) for i in date_query]
        trading_days.reverse()
        cache.set('trading_days_cache', trading_days, timeout=30 * 60 * 60)
    return trading_days[:days]
