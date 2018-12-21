# -*- coding: utf-8 -*-
"""能量回归"""

import matplotlib.pyplot as plt
from pymongo import MongoClient
from bson.objectid import ObjectId
from django.conf import settings
from rest_framework.response import Response
from rest_framework.views import APIView

from extends import Base
from sk_optional.models import MyChoiceData
from intraday.views import TradingVoViewSet


__all__ = ['EnergyHuiguiViewSet']


class EnergyHuiguiViewSet(APIView):
    """能量回归"""
    mongo_conn = MongoClient(settings.MONGO_CONN2)

    def get(self, request):
        """能量回归"""
        db = self.mongo_conn.hotcow
        collection = db.trading_data
        code = '603081'
        trading_day = Base(MyChoiceData, **{
            'code': code,
            'trading_day__in': ['2018-12-17', '2018-12-18', '2018-12-19', '2018-12-20']
        }).findfilter()
        for i in trading_day:
            trading_query = collection.find_one(ObjectId(i.mongo_id))
            if trading_query:
                self.chart_show(trading_query)

        return Response({'MainFlows': 'data update node'})

    def chart_show(self, data):
        minutes_data = TradingVoViewSet.minutes_data(data['trading_list'])
        # 生成图表
        chart_data = {
            'bar': ['Total', 'liu_ru', 'liu_chu', 'z_buy', 'z_sell'],
            'keys': [],
            'liu_ru': [],
            'liu_chu': [],
            'z_buy': [],
            'z_sell': [],
            'Total': []
        }
        for i in minutes_data:
            chart_data['keys'].append(i)
            chart_data['liu_ru'].append(minutes_data[i]['liu_ru'])
            chart_data['liu_chu'].append(minutes_data[i]['liu_chu'])
            chart_data['z_buy'].append(minutes_data[i]['z_buy'])
            chart_data['z_sell'].append(minutes_data[i]['z_sell'])
            chart_data['Total'].append(minutes_data[i]['total'])

        plt.figure(figsize=(65, 16))
        for keys in chart_data['bar']:
            plt.bar(chart_data['keys'], chart_data[keys], label=keys)
        plt.xticks(rotation=45)
        plt.legend(loc='upper left', frameon=False)
        jingliu = round((sum(chart_data['liu_ru']) - sum(chart_data['liu_chu'])) / 10000, 2)
        zhumai1 = round(sum(chart_data['z_buy']) / 10000, 2)
        zhumai2 = round(sum(chart_data['z_sell']) / 10000, 2)
        totle = sum(chart_data['Total']) / 10000
        plt.title(
            f"{data['trading_day']} {data['code']} JL ({jingliu} {round(jingliu / totle, 2) * 100}%) "
            f"ZM ({round(zhumai1 - zhumai2, 2)} {round((zhumai1 - zhumai2) / totle, 2) * 100}%) ",
            fontsize='60'
        )
        plt.show()
