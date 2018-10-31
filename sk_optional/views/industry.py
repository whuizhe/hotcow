# -*- coding: utf-8 -*-
"""行业"""
import datetime
from django.core.cache import cache
from django.conf import settings
from rest_framework.response import Response
from rest_framework.views import APIView

from extends import Base, trading_day
from basicdata.models import StockPrice
from basicdata.serializers import StockPriceSerializer

__all__ = ['IndustryViewSet']


class IndustryViewSet(APIView):
    """慢牛"""
    trading_day = []


    def get(self, request):
        """GET请求"""
        # 领涨行业
        url = f"{settings.QT_URL3}data/view/bdrank.php?&t=01/averatio&p=1&o=0&l=40&v=list_data"
        # 行业祥情
        url = f"{settings.QT_URL3}q=bkhz012029,&r=11192163"
        # 行业各股
        url = f"{settings.QT_URL3}data/index.php?appn=rank&t=pt012029/chr&p=1&o=0&l=40&v=list_data"
        # 资金数据
        url = f"{settings.QT_URL2}q=ff_sh600425,ff_sh600585,ff_sz000789,ff_sz000877,ff_sh600668,ff_sh600801,ff_sh600883,ff_sh600720,ff_sz000672,ff_sh600802,ff_sh600449,ff_sz002233,ff_sh601992,ff_sh600326,ff_sz000401,ff_sz000935,ff_sz000546,ff_sh600881&r=466867552"
