# -*- coding: utf-8 -*-
"""基础数据获取"""
import re
import time
import requests
import datetime
from django.conf import settings
from rest_framework.response import Response
from rest_framework.views import APIView

from extends import Base
from .models import StockInfo


class BasisDataViewSet(APIView):
    """基础数据"""
    code_list = []
    qt_url1 = 'http://qt.gtimg.cn/q='
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:62.0) Gecko/20100101 Firefox/62.0'
    }

    def get(self, request):
        all_code = self.all_code()
        times_number = 100
        for num in range(0, len(all_code) // times_number + 1):
            code = ''
            for i in all_code[num * times_number:times_number * (num + 1) - 1]:
                if 'ST' in i[1]:
                    continue
                code_split = str(i[0]).split('.')
                if not Base(StockInfo, **{'db_status': 1, 'code': code_split[0]}).findfilter():
                    listed_time = datetime.datetime.strptime(i[2], "%Y%m%d")
                    jet_lag = (
                            datetime.datetime.now() -
                            listed_time
                    ).days
                    if jet_lag <= 365:
                        new = 1
                    else:
                        new = 0
                    Base(StockInfo, **{
                        'db_status': 1,
                        'exchange': code_split[1],
                        'code': code_split[0],
                        'name': i[1],
                        'new': new,
                        'listed_time': datetime.datetime.strftime(listed_time, '%Y-%m-%d'),
                    }).save_db()
                code += f's_{code_split[1].lower() + code_split[0]},'
            open_url = requests.get(self.qt_url1 + code, timeout=120)
            code_list = re.findall('".*"', open_url.text)
            for c in code_list:
                code_price_info = c.replace('"', '').split('~')
                query_code = Base(StockInfo, **{'db_status': 1, 'code': code_price_info[2]}).findfilter()
                if query_code:
                    query_code[0].total_equity = round(float(code_price_info[-1]) / float(code_price_info[3]), 3)
                    query_code[0].save()

        return Response({"BasisData": {"Status": 1, "msg": "Basis data update node"}})

    def all_code(self):
        """获取所有代码"""
        req_params = {
            'api_name': 'stock_basic',
            'token': settings.TS_TOKEN,
            'params': {'list_status': 'L'},
            'fields': ['ts_code', 'name', 'list_date']
        }
        get_code = requests.post(settings.TS_URL, json=req_params)
        code_info = get_code.json()
        return code_info['data']['items']

    @staticmethod
    def query_concept(code: str):
        """所属概念"""
        url = f'http://web.ifzq.gtimg.cn/stock/relate/data/plate?code={code}'
        open_url = requests.get(url)
        concept_info = open_url.json()
        if concept_info['code'] == 0:
            print(concept_info)

    def quert_concept_ths(self):
        """同花顺概念"""
        concept_dict = []
        url = "http://q.10jqka.com.cn/gn/"
        open_url = requests.get(url, headers=self.headers)
        if open_url.status_code == 200:
            find_concept = re.findall('<a href="http://q.10jqka.com.cn/gn/detail/code/.*</a>', open_url.text)
            for i in find_concept:
                find_name = re.findall(
                    '<a href="http://q.10jqka.com.cn/gn/detail/code/(\d+)/" target="_blank">(.*)</a>',
                    i
                )
                if find_name:
                    self.code_list = []
                    time.sleep(2)
                    concept_code = self.code_quert_concept_ths(find_name[0][0], 1)
                    if concept_code:
                        print(concept_code)
                        for c in list(set(concept_code)):
                            if c not in concept_dict:
                                continue
                            concept_dict[c]['info']['concept'].append(find_name[0][1])

    def code_quert_concept_ths(self, concept_code, page):
        """
        同花顺概念code查询
        :param concept_code: 概念码
        :param page: 页码
        :return:
        """
        url = f'http://q.10jqka.com.cn/gn/detail/field/264648/order/' \
              f'desc/page/{page}/ajax/1/code/{concept_code}'
        self.headers['Cookie'] = f'v=ApdyQuWBgEwgOATAzCzWcxZyIArg3Gs-RbDvsunEs2bNGLm48az7jlWAfwP6;'
        open_url = requests.get(url, headers=self.headers)
        if open_url.status_code == 200:
            url_info = open_url.text
            self.code_list += re.findall(
                '<td><a href="http://stockpage.10jqka.com.cn/(\d+)" target="_blank">.*</a></td>',
                url_info
            )
            if page == 1:
                all_page = re.findall(
                    '<a class="changePage" page="(\d+)" href="javascript:void\(0\);">尾页',
                    url_info
                )
                if all_page:
                    for pages in range(2, int(all_page[0]) + 1):
                        self.code_quert_concept_ths(concept_code, pages)
        return self.code_list
