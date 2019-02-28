# -*- coding: utf-8 -*-
"""行业"""
import re
import requests
import datetime
from django.core.cache import cache
from django.conf import settings
from rest_framework.response import Response
from rest_framework.views import APIView

from extends import Base, trading_day
from basicdata.models import StockPrice


class IndustryViewSet(APIView):
    """市场分析"""
    market_code = {
        'fangliang': [],
        'shangzhang': [],
        'gainian': {}
    }

    def get(self, request):
        """市场分析"""
        self._fangliang()
        self._shangzhang()
        self._gainian()

        return Response({'market_code': self.market_code})

    def _gainian(self):
        """概念"""
        url = f"{settings.QT_URL3}data/view/bdrank.php?&t=02/averatio&p=1&o=0&l=30&v=list_data"
        url_info1 = self._open_url(url)
        if url_info1:
            code_info1 = url_info1.split("data:'")[1].replace("'};", '').replace('qt', 'hz')
            # 行业祥情
            url = f"{settings.QT_URL2}q={code_info1}&r=11192163"
            url_info2 = self._open_url(url)
            if url_info2:
                industry_list = re.findall('".*"', url_info2)
                for i in industry_list:
                    industry_info = str(i).replace('"', '').split('~')
                    self.market_code['gainian'][industry_info[0]] = {
                        'name': industry_info[1],
                        'no.1': industry_info[11],
                        'new_code': []
                    }
                # 行业各股
                for i in code_info1.split(','):
                    url = f"{settings.QT_URL3}data/index.php?appn=rank&t={i.replace('bkhz', 'pt')}" \
                        f"/chr&p=1&o=0&l=6&v=list_data"
                    url_info3 = self._open_url(url)

                    find_code = re.findall("'.*'", url_info3)
                    if find_code:
                        gainian_code = find_code[0][:9][3:]
                        if gainian_code in self.market_code['gainian']:
                            self.market_code['gainian'][gainian_code]['new_code'].append(
                                [i[2:] for i in str(find_code[0]).replace("'", '').split('data:')[1].split(',')]
                            )
        return None

    def _shangzhang(self):
        """连续上涨"""
        url = f'{settings.QT_URL3}data/view/dataPro.php?t=2&p=3'
        url_info = self._open_url(url)
        find_code = re.findall("'.*'", url_info)
        if find_code:
            code_list = str(find_code[0]).replace("'", '').split('^')
            for code in code_list:
                self.market_code['shangzhang'].append((code.split('~')[0][2:], code.split('~')[1]))
        return None

    def _fangliang(self):
        """突放量"""
        url = f'{settings.QT_URL3}data/view/dataPro.php?t=7&p=1'
        url_info = self._open_url(url)
        find_code = re.findall("'.*'", url_info)
        if find_code:
            code_list = str(find_code[0]).replace("'", '').split('^')
            for code in code_list:
                self.market_code['fangliang'].append(code.split('~')[0][2:])
        return None

    def _open_url(self, url):
        """请求url"""
        url_open = requests.get(url)
        if url_open.status_code == 200:
            url_info = url_open.text
            return url_info
        else:
            return None
