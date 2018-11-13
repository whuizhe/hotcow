# -*- coding: utf-8 -*-
"""历史交易"""
import datetime
import requests
import matplotlib.pyplot as plt
from django.conf import settings
from django.views.generic import View
from django.core.cache import cache
from django.shortcuts import render, redirect

from extends import Base, trading_day
from basicdata.models import StockInfo, StockPrice
from intraday.views import TradingVoViewSet


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

    def get(self, request):
        """GET请求"""
        data = request.GET
        if not data:
            code_info = Base(StockInfo, **{'db_status': 1, 'my_choice': 1}).findfilter()
            context = {
                'param': code_info,
            }
            return render(request, 'sk_optional/analysisshow.html', context)

        elif data and 'code' in data:
            if 'day' in data:
                redis_key = f'constantly_deal_{str(data["code"]).lower()}_{data["day"]}_cache'
            else:
                redis_key = f'constantly_deal_{str(data["code"]).lower()}_{datetime.date.today()}_cache'
            read_cache = cache.get(redis_key)
            if read_cache['data']:
                minutes_data = TradingVoViewSet.minutes_data(read_cache['data'])
                # 生成图表
                chart_data = {
                    'bar': ['Total', 'liu_ru', 'liu_chu', 'z_buy', 'z_sell'],
                    'keys': [],
                    'liu_ru': [],
                    'liu_chu': [],
                    'z_buy': [],
                    'z_sell': [],
                    'Total': []
                }
                for i in minutes_data:
                    chart_data['keys'].append(i)
                    chart_data['liu_ru'].append(minutes_data[i]['liu_ru'])
                    chart_data['liu_chu'].append(minutes_data[i]['liu_chu'])
                    chart_data['z_buy'].append(minutes_data[i]['z_buy'])
                    chart_data['z_sell'].append(minutes_data[i]['z_sell'])
                    chart_data['Total'].append(minutes_data[i]['total'])

                plt.figure(figsize=(65, 16))
                for keys in chart_data['bar']:
                    plt.bar(chart_data['keys'], chart_data[keys], label=keys)
                plt.xticks(rotation=45)
                plt.legend(loc='upper left', frameon=False)
                jingliu = round((sum(chart_data['liu_ru']) - sum(chart_data['liu_chu'])) / 10000, 2)
                zhumai1 = round(sum(chart_data['z_buy']) / 10000, 2)
                zhumai2 = round(sum(chart_data['z_sell']) / 10000, 2)
                totle = sum(chart_data['Total']) / 10000
                plt.title(
                    f"Jingliu ({jingliu} {round(jingliu / totle, 2) * 100}%) "
                    f"Zhumai ({round(zhumai1 - zhumai2, 2)} {round((zhumai1 - zhumai2)  / totle, 2) * 100}%) ",
                    fontsize='60'
                )
                plt.show()

                return redirect('/skoptional/analysisshow/')

        return redirect('/skoptional/analysisshow/')

    def post(self, request):
        code = str(request.body.decode()).split('=')[1]
        code_query = Base(StockInfo, **{'db_status': 1, 'code': code}).findfilter()
        if code_query:
            if code_query[0].my_choice == 1:
                code_query[0].my_choice = 0
            else:
                code_query[0].my_choice = 1
            code_query[0].save()

        return redirect('/skoptional/analysisshow/')
