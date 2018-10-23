# -*- coding: utf-8 -*-
"""慢牛"""
import datetime
from django.core.cache import cache
from rest_framework.response import Response
from rest_framework.views import APIView

from extends import Base, trading_day
from basicdata.models import StockInfo, StockPrice
from basicdata.serializers import StockPriceSerializer

__all__ = ['SlowCowViewSet']


class SlowCowViewSet(APIView):
    """慢牛"""
    trading_day = []
    code_dict = {
        'continuous_up': {},
        'zl': [],
        'zl_1': []
    }

    def get(self, request):
        """GET请求"""
        self.trading_day = trading_day(15)
        if self.trading_day:
            redis_keys = f'code_analysis_data_{datetime.date.today().strftime("%Y-%m-%d")}'
            read_cache = cache.get(redis_keys)
            if read_cache:
                return Response({'SlowCow': read_cache, 'trading_day': self.trading_day})
            code_all = Base(StockInfo, **{'db_status': 1}).findfilter()
            for i in code_all:
                day_data = self._read_data(sid=i.id)
                # 连接上涨
                self._continuous_up(day_data)
            # 主散流入
            self._trading_volume()
            # 量能分析
            self._quantity_energy()
            cache.set(
                redis_keys,
                self.code_dict,
                timeout=None
            )
            return Response({'SlowCow': self.code_dict, 'trading_day': self.trading_day})

    def _read_data(self, sid=None, code=None):
        """读取code数据"""
        day_data = {}
        if sid:
            code_info = Base(StockPrice, **{'sk_info_id': sid, 'trading_day__in': self.trading_day}).findfilter()
        else:
            code_info = Base(StockPrice, **{'code': code, 'trading_day__in': self.trading_day}).findfilter()
        code_serializers = StockPriceSerializer(code_info, many=True)
        for day in code_serializers.data:
            day_data[day['trading_day']] = day
        return day_data

    def _continuous_up(self, day_data):
        """连续上涨"""
        try:
            am5 = self._am(5, day_data)
            # 上涨 大于5日均线 交易量大于5kw
            if day_data[self.trading_day[0]]['close'] >= day_data[self.trading_day[1]]['close'] and \
                    day_data[self.trading_day[0]]['close'] >= am5 and \
                    day_data[self.trading_day[0]]['hand_number'] * day_data[self.trading_day[0]]['average'] >= 500000:
                for i in range(2, 21):
                    if day_data[self.trading_day[i - 1]]['close'] >= day_data[self.trading_day[i]]['close']:
                        if i not in self.code_dict['continuous_up']:
                            self.code_dict['continuous_up'][i] = []
                        self.code_dict['continuous_up'][i].append(day_data[self.trading_day[0]]['code'])
                        if i != 2:
                            for m in range(2, i):
                                if day_data[self.trading_day[0]]['code'] in self.code_dict['continuous_up'][m]:
                                    self.code_dict['continuous_up'][m].remove(day_data[self.trading_day[0]]['code'])
                    else:
                        break
        except KeyError:
            pass

    def _am(self, few_day: int, day_dat):
        """均线"""
        am = 0
        for i in range(0, few_day):
            am += day_dat[self.trading_day[i]]['average']
        return round(am / few_day, 2)

    def _quantity_energy(self):
        """量能分析"""
        pass

        # for keys in self.code_dict['continuous_up']:
        #     for code in self.code_dict['continuous_up'][keys]:
        #         day_data = self._read_data(code=code)


    def _trading_volume(self):
        """主散流入"""
        for keys in self.code_dict['continuous_up']:
            for code in self.code_dict['continuous_up'][keys]:
                day_data = self._read_data(code=code)
                main_amount, loose_amount, status = 0, 0, 1
                for i in self.trading_day[:int(keys)]:
                    if day_data[i]['main_amount'] < 0:
                        status = 0
                    main_amount += day_data[i]['main_amount']
                    loose_amount += day_data[i]['loose_amount']
                if main_amount <= 100 and code in self.code_dict['continuous_up']:
                    self.code_dict['continuous_up'].pop(code)
                    continue
                # 主力正向流入
                if status == 1:
                    self.code_dict['zl'].append({
                        'code': code,
                        'up': keys,
                    })
                    # 散户流出小于主力流入的0.6
                    if loose_amount < 0 and round(main_amount / (0 - loose_amount), 1) <= 0.6:
                        self.code_dict['zl_1'].append({
                            'code': code,
                            'up': keys,
                        })
