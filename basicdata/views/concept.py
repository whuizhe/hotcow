# -*- coding: utf-8 -*-
"""基础概念"""
import re
import requests
from django.conf import settings
from django.core.cache import cache
from rest_framework.response import Response
from rest_framework.views import APIView


__all__ = ['ConceptViewSet']


class ConceptViewSet(APIView):
    """基础概念"""

    def get(self, request):
        # 概念
        code_conecpt = {}
        url = f'{settings.QT_URL4}mstats/menu_childs.php?id=bd021185'
        url_open = requests.get(url)
        url_info = url_open.json()
        conecpt_dict = url_info
        for keys in conecpt_dict:
            if keys != 'bd_cpt':
                cpt_url = f'{settings.QT_URL3}data/index.php?appn=rank&t=' \
                          f'{conecpt_dict[keys]["clk"].replace("SS_", "")}/chr&p=3&o=0&l=1000&v=list_data'
                url_open = requests.get(cpt_url)
                code_query = url_open.text
                code_find = re.findall("data:'.*", code_query)
                if code_find:
                    code_info = str(code_find[0]).replace("'};", "").replace("data:'", "")
                    for code in code_info.split(','):
                        if code[2:] not in code_conecpt:
                            code_conecpt[code[2:]] = []
                        code_conecpt[code[2:]].append(conecpt_dict[keys]['t'])
        cache.set('code_conecpt_data_cache', code_conecpt, timeout=24 * 60 * 60)

        # 地域
        code_region = {}
        url = f'{settings.QT_URL4}mstats/menu_childs.php?id=bd033400'
        url_open = requests.get(url)
        url_info = url_open.json()
        region_dict = url_info
        for keys in region_dict:
            if keys != 'bd_rgn':
                rgn_url = f'{settings.QT_URL3}data/index.php?appn=rank&t=' \
                          f'{region_dict[keys]["clk"].replace("SS_", "")}/chr&p=3&o=0&l=1000&v=list_data'
                url_open = requests.get(rgn_url)
                code_query = url_open.text
                code_find = re.findall("data:'.*", code_query)
                if code_find:
                    code_info = str(code_find[0]).replace("'};", "").replace("data:'", "")
                    for code in code_info.split(','):
                        code_region[code[2:]] = region_dict[keys]['t']
        cache.set('code_region_data_cache', region_dict, timeout=24 * 60 * 60)
        return Response({"Concept": {"Status": 1, "msg": "Basis Concept data"}})
