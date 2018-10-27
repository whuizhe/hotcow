# -*- coding: utf-8 -*-
"""交易日"""
import datetime
from django.core.cache import cache

from .tushare_api import tushare_api


def trading_day(days: int):
    """获取交易日列表"""

    trading_days = cache.get('trading_days_cache')
    if not trading_days:
        trading_days = []
        requeys_data = tushare_api(
            api_name='trade_cal',
            params={
                'is_open': 1,
                'start_date': datetime.datetime.now().strftime('%Y0901'),
                'end_date': datetime.datetime.now().strftime('%Y%m%d'),
            },
            fields=['cal_date']
        )
        if requeys_data:
            for i in requeys_data:
                date_list = list(i[0])
                date_list.insert(4, '-')
                date_list.insert(7, '-')
                trading_days.append(''.join(date_list))
            trading_days.reverse()
            cache.set('trading_days_cache', trading_days, timeout=30 * 60 * 60)
    if trading_days:
        return trading_days[:days]
    else:
        return None
