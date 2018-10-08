# -*- coding: utf-8 -*-
"""
从tushare获取数据
https://tushare.pro/document/2
"""
import requests
from django.conf import settings


def tushare_api(api_name: str, params: dict, fields: list):
    """
    从tushare获取数据
    :param api_name: 接口函数名
    :param params: 参数
    :param fields: 获取的字段列表
    :return:
    """
    req_params = {
        'api_name': api_name,
        'token': settings.TS_TOKEN,
        'params': params,
        'fields': fields
    }
    get_code = requests.post(settings.TS_URL, json=req_params)
    code_info = get_code.json()
    return code_info['data']['items']
