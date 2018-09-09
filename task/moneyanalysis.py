# codint=utf-8

import re
import requests


class MoneyAnalysis(object):

    def __init__(self):
        self.qt_url = 'http://qt.gtimg.cn/q='

    def trading_list(self, code):
        """
        交易明细
        :param code: 代码
        1-5 100-500手
        6 800手
        7 1000手
        8 1500手
        9 2000手
        10 100W
        11 200W
        12 500W
        13 1000W
        """
        code_trading = {}
        url = 'http://stock.gtimg.cn/data/index.php?appn=dadan&action=summary&c='
        url_open = requests.get(url + code)
        if url_open.status_code == 200:
            url_info = url_open.text
            url_list = eval(url_info.split('=')[-1])
            code_trading[url_list[1]] = {

            }
            print(url_list[3][-1] + url_list[3][-2] + url_list[3][-3])
            print(url_list)

a = MoneyAnalysis()
a.trading_list('sz002072')