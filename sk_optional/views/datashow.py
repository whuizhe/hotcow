# -*- coding: utf-8 -*-
"""历史交易"""
import requests
import datetime
from django.conf import settings
from django.views.generic import View
from django.shortcuts import render, redirect

from extends import Base, trading_day
from basicdata.models import StockInfo, StockPrice
from sk_optional.models import MyChoiceData

__all__ = ['DataShowViewSet', 'AnalysisShowViewSet']


class DataShowViewSet(View):
    """历史交易"""

    def get(self, request):
        """GET请求"""
        data = request.GET
        if data and 'code' in data:
            code_data = []
            code_query = Base(StockPrice, **{'code': data['code'], 'trading_day__in': trading_day(9)}).findfilter()
            for i in code_query:
                code_data.append({
                    'open': i.open,
                    'close': i.close,
                    'high': i.high,
                    'low': i.low,
                    'average': i.average,
                    'trading_day': i.trading_day,
                    'hand_number': round(i.hand_number * i.average / 1000000, 2),
                    'turnover_rate': f'{round(i.hand_number / (i.sk_info.circulate_equity * 1000000) * 100, 2)}%',
                    'bidding_rate': f'{round(i.bidding_rate * 100, 0)}%',
                    'main_amount': i.main_amount,
                    'loose_amount': i.loose_amount,
                })

            code_info = Base(StockInfo, **{'db_status': 1, 'code': data['code']}).findfilter()
            if code_info:
                code = f'{str(code_info[0].exchange).lower()}{data["code"]}'
                context = {
                    'param': code_data,
                    'code': data['code'],
                    'code_name': code_info[0].name,
                    'flow_data': self.money_flow(code),
                    'total_flow': self.total_flow(code)
                }
                return render(request, 'sk_optional/datashow.html', context)

        return render(request, 'sk_optional/datashow.html', {'code_name': '无数据,请输入正确的代码'})

    @staticmethod
    def money_flow(code):
        flow_data = {
            'time_data': [],
            'main': {  # 主力
                'into': [],
                'out': []
            },
            'retail': {  # 散户
                'into': [],
                'out': []
            }
        }
        url = f'http://stock.gtimg.cn/data/view/ggdx.php?t=2&q={code}&r=0.6197422606657409'
        url_open = requests.get(url)
        url_info = url_open.text
        if url_info:
            money_flow = url_info.replace(';', '').split('=')[1].replace('"', '').split('~')
            for i in money_flow:
                if ':' in i:
                    index = money_flow.index(i)
                    flow_data['time_data'].append(i.split('^')[0][:-3])
                    flow_data['retail']['into'].append(float(money_flow[index - 1]))
                    flow_data['retail']['out'].append(float(money_flow[index - 2]))
                    flow_data['main']['into'].append(float(money_flow[index - 4]))
                    flow_data['main']['out'].append(float(money_flow[index - 5]))
        flow_data['time_data'].reverse()
        flow_data['retail']['into'].reverse()
        flow_data['retail']['out'].reverse()
        flow_data['main']['into'].reverse()
        flow_data['main']['out'].reverse()

        return flow_data

    def total_flow(self, code):
        total_data = {}
        url = f'{settings.QT_URL2}r=0.8545316768155392&q=ff_{code}'
        url_open = requests.get(url)
        url_info = url_open.text
        if url_info:
            total_flow = url_info.replace(';', '').split('=')[1].replace('"', '').split('~')
            total_data['into'] = [int(float(total_flow[1])), int(float(total_flow[5]))]
            total_data['out'] = [int(float(total_flow[2])), int(float(total_flow[6]))]
        return total_data


class AnalysisShowViewSet(View):
    """分析数据展示"""

    def get(self, request, code):
        """GET请求"""
        code_info = Base(StockInfo, **{'db_status': 1, 'my_choice': 1}).findfilter()
        my_code_data = Base(MyChoiceData, **{
            'sk_info_id__in': [i.id for i in code_info],
            'trading_day': datetime.date.today()
        }).findfilter()
        context = {
            'param': my_code_data,
        }
        print(context)
        return render(request, 'sk_optional/analysisshow.html', context)

    def post(self, request, code):
        Base(StockInfo, **{'db_status': 1, 'code': code}).update({'my_choice': 1})
        return redirect('/skoptional/analysisshow/')

    def delete(self, request, code):
        Base(StockInfo, **{'db_status': 1, 'code': code}).update({'my_choice': 0})
        return redirect('/skoptional/analysisshow/')