# codint=utf-8

import re
import redis
import uuid
import time
import datetime
import requests

class ChooseHot(object):
    """筛选"""

    def __init__(self):
        self.code_list = []
        self.token = '655d50949a8f53665db0d0266d338b56b5bd8a3976ba1ac9134fe684'
        self.qt_url1 = 'http://qt.gtimg.cn/q='
        self.ts_url = 'http://api.tushare.pro'
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:62.0) Gecko/20100101 Firefox/62.0'
        }
        self.conn_redis = redis.StrictRedis(host='127.0.0.1', password='blcmdb', db=3)

    def all_code(self):
        """获取所有代码"""
        req_params = {
            'api_name': 'stock_basic',
            'token': self.token,
            'params': {'list_status': 'L'},
            'fields': ['ts_code', 'name', 'list_date']
        }
        get_code = requests.post(self.ts_url, json=req_params)
        code_info = get_code.json()
        return code_info['data']['items']

    def basis_screening(self):
        """基础筛选"""
        screening_data = {}
        all_code = self.all_code()
        times_number = 100
        for num in range(0, len(all_code) // times_number + 1):
            code = ''
            for i in all_code[num * times_number:times_number * (num + 1) - 1]:
                if 'ST' in i[1]:
                    continue
                code_split = str(i[0]).split('.')
                screening_data[code_split[0]] = {
                    'info': {
                        'code': code_split[1].lower() + code_split[0],
                        'name': i[1],
                        'concept': [],
                        '上市时间': i[2],
                    },
                    'data': {}
                }
                code += f's_{code_split[1].lower() + code_split[0]},'
            open_url = requests.get(self.qt_url1 + code, timeout=120)
            code_list = re.findall('".*"', open_url.text)
            for c in code_list:
                code_price_info = c.replace('"', '').split('~')
                if int(code_price_info[-3]) >= 9000 and float(code_price_info[-1]) <= 260:  # 交易额 and 市值
                    jet_lag = (
                            datetime.datetime.now() -
                            datetime.datetime.strptime(screening_data[code_price_info[2]]['info']['上市时间'], "%Y%m%d")
                    ).days
                    if jet_lag <= 365:
                        new = 1
                    else:
                        new = 0
                    screening_data[code_price_info[2]]['info']['次新'] = new
                else:
                    screening_data.pop(code_price_info[2])
        if screening_data:
            self.conn_redis.set('code_list', str(screening_data))

    def query_concept(self, code: str):
        """所属概念"""
        url = f'http://web.ifzq.gtimg.cn/stock/relate/data/plate?code={code}'
        open_url = requests.get(url)
        concept_info = open_url.json()
        if concept_info['code'] == 0:
            print(concept_info)

    def quert_concept_ths(self):
        """同花顺概念"""
        concept_dict = eval(self.conn_redis.get('code_list'))
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
                        for i in list(set(concept_code)):
                            if i not in concept_dict:
                                continue
                            concept_dict[i]['info']['concept'].append(find_name[0][1])
        if concept_dict:
            self.conn_redis.set('code_list', str(concept_dict))

    def code_quert_concept_ths(self, concept_code, page):
        """
        同花顺概念code查询
        :param concept_code: 概念码
        :param page: 页码
        :return:
        """
        url = f'http://q.10jqka.com.cn/gn/detail/field/264648/order/' \
              f'desc/page/{page}/ajax/1/code/{concept_code}'
        uuid.uuid4()
        self.headers['Cookie'] = f'v=AjYeLmkTcR-28gV7m1wn7E9pgW05V3oCzJmvNKAfIkm0HtifCOfKoZwr_MJz;'
        open_url = requests.get(url, headers=self.headers)
        if open_url.status_code == 200:
            url_info = open_url.text
            print(url_info)
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

a = ChooseHot().quert_concept_ths()
