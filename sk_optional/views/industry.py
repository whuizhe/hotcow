# -*- coding: utf-8 -*-
"""行业"""
import re
import requests
from django.core.cache import cache
from django.conf import settings
from rest_framework.response import Response
from rest_framework.views import APIView


class IndustryViewSet(APIView):
    """行业"""
    trading_day = []

    def get(self, request):
        """GET请求"""
        # 领涨行业
        industry_name = {}
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
                    industry_name[industry_info[0]] = {
                        'name': industry_info[1],
                        'no.1': industry_info[11],
                        'new_code': []
                    }
                # 行业各股
                for i in code_info1.split(','):
                    url = f"{settings.QT_URL3}data/index.php?appn=rank&t={i.replace('bkhz', 'pt')}" \
                          f"/chr&p=1&o=0&l=6&v=list_data"
                    url_info3 = self._open_url(url)
                    if url_info3:
                        # 资金数据
                        code_info = url_info3.split("data:'")[1].replace("'};", '')
                        for code in code_info.split(','):
                            read_code = cache.get(f'cache_code_info_{code[:2]}~{code[2:]}')
                            if read_code:
                                if read_code['new'] == 1:
                                    industry_name[i[4:]]['new_code'].append(read_code)
        return Response({"Industry": {"param": industry_name}})

    def _open_url(self, url):
        """请求url"""
        url_open = requests.get(url)
        if url_open.status_code == 200:
            url_info = url_open.text
            return url_info
        else:
            return None
