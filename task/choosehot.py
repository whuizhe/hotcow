# codint=utf-8

import re
import redis
import requests

class ChooseHot(object):
    """筛选"""

    def __init__(self):
        self.token = '655d50949a8f53665db0d0266d338b56b5bd8a3976ba1ac9134fe684'
        self.qt_url = 'http://qt.gtimg.cn/q='
        self.ts_url = 'http://api.tushare.pro'

    def all_code(self):
        """获取所有代码"""
        req_params = {
            'api_name': 'stock_basic',
            'token': self.token,
            'params': {'list_status': 'L'},
            'fields': ['ts_code']
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
                code_split = str(i[0]).split('.')
                code += f's_{code_split[1].lower() + code_split[0]},'
            open_url = requests.get(self.qt_url + code)
            code_list = re.findall('".*"', open_url.text)

            for i in code_list:
                if '~~' in i:
                    print(i)
                    return
                    code_info = str(i)[1:-2].split('~')
                    if float(code_info[-1]) <= 100 and 'ST' not in code_info[1] and int(code_info[-3]) >= 10000:
                        screening_data[code_info[2]] = {
                            'name': code_info[1],
                            'belongs': '',
                            'concept': self.query_concept(code_info[2])
                        }
        if screening_data:
            conn_redis = redis.StrictRedis(host='127.0.0.1', password='blcmdb', db=3)
            conn_redis.set('code_list', str(screening_data))


    def query_concept(self, code: str):
        """所属概念"""
        url = f'http://web.ifzq.gtimg.cn/stock/relate/data/plate?code={code}'
        open_url = requests.get(url)
        concept_info = open_url.json()
        if concept_info['code'] == 0:

            print(concept_info)




a = ChooseHot()
a.basis_screening()
