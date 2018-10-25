# -*- coding: utf-8 -*-
"""交易日"""
import datetime
import requests
from django.core.cache import cache
from django.conf import settings


def trading_day(days: int):
    """获取交易日列表"""
    trading_days = cache.get('trading_days_cache')
    if not trading_days:
        trading_days = []
        url = f'{settings.QT_URL3}data/view/ggdx.php?t=3&d=60&q=sz000001'
        url_open = requests.get(url)
        url_info = url_open.text
        url_list = url_info.split('=')[1].replace(';', '').replace('\'', '').split('~')
        for i in url_list:
            if '^' in i:
                trading_days.append(i.split('^')[0])
        url = f'{settings.QT_URL2}?q=marketStat'
        url_open = requests.get(url)
        url_info = url_open.text
        rec_day = url_info.split('=')[1].replace('"', '').split(' ')[0]
        if int(datetime.datetime.now().strftime('%H'))  >= 16:
            if rec_day not in trading_days:
                trading_days = [rec_day] + trading_days
        cache.set('trading_days_cache', trading_days, timeout=30 * 60 * 60)
    return trading_days[:days]
