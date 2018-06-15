# _*_ coding: utf-8 _*_

import tushare as ts
import pandas as pd
from pandas import Series, DataFrame
import os
from tushare_data import StockInfo
from Tools import Tools
import numpy as np


"""
调研一些想法
可调研的问题
1、是否周三是lucky day
2、所有股票，两个交易日的成交量和收盘价格对第三天的影响
3、单个股票，两个交易日的成交量和收盘价格对第三天的影响
"""


class Research(object):
    def __init__(self):
        self.stock_data = None

    # 加载数据
    def initail(self):
        self.stock_data = StockInfo()
        return self.stock_data.load_data()

########################################################################################################################
    # 调研幸运日
    def find_lucky_day(self):
        """
        计算方式
        1. 周三开盘价 - 周二收盘价
        2. 周三收盘价 - 周二收盘价
        """
        stock_list = self.stock_data.get_all_600_code()
        for stock in stock_list:
            ts.get_hist_data(stock)

########################################################################################################################
    # 统计get_all_3_close获得的数据中，涨跌情况几何
    def count_rise_fall(self):
        """
        结果： =。= 研究中断
        涨跌 -> 811
        涨涨 -> 123
        跌涨 -> 47
        跌跌 -> 439
        """
        data = pd.read_csv('./3_day.csv')
        r_f = 0
        r_r = 0
        f_r = 0
        f_f = 0
        for i in data:
            if np.nan not in list(data[i]):
                sum_1 = data[i][1] - data[i][0]
                sum_2 = data[i][2] - data[i][1]
                if sum_1 > 0:
                    if sum_2 > 0:
                        r_r += 1
                    else:
                        r_f += 1
                else:
                    if sum_2 > 0:
                        f_r += 1
                    else:
                        f_f += 1
        print('涨跌 -> {}'.format(r_f))
        print('涨涨 -> {}'.format(r_r))
        print('跌涨 -> {}'.format(f_r))
        print('跌跌 -> {}'.format(f_f))
        print('第一天涨，第二天也涨的概率 -> {}'.format(r_r/(r_f + r_r)))
        print('第一天跌，第二天涨的概率 -> {}'.format(f_r / (f_f + f_r)))

    # 获得上证所有股票的最近3天收盘价 （后期细分，行业股）
    def get_all_3_close(self):
        """
        """
        # 获得前三个工作日的日期
        day_list = Tools.get_n_workday()
        day_list.sort(reverse=False)

        stock_list = self.stock_data.get_all_600_code()
        f_res = None
        for stock in stock_list:
            res, flag = self.get_his_stock_data(stock, day_list)
            if flag:
                f_res = pd.concat([f_res, res], axis=1)
        f_res.to_csv('./3_day.csv', index=False)

    # 获得一支股票在date_list中的收盘价
    def get_his_stock_data(self, code, date_list):
        """
        技术笔记:get_hist_data用法
        【参数说明】
        code：股票代码，即6位数字代码，或者指数代码（sh=上证指数 sz=深圳成指 hs300=沪深300指数 sz50=上证50 zxb=中小板 cyb=创业板）
        start：开始日期，格式YYYY-MM-DD
        end：结束日期，格式YYYY-MM-DD
        ktype：数据类型，D=日k线 W=周 M=月 5=5分钟 15=15分钟 30=30分钟 60=60分钟，默认为D
        retry_count：当网络异常后重试次数，默认为3
        pause:重试时停顿秒数，默认为0
        【返回值说明】
        date：日期
        open：开盘价
        high：最高价
        close：收盘价
        low：最低价
        volume：成交量
        price_change：价格变动
        p_change：涨跌幅
        ma5：5日均价
        ma10：10日均价
        ma20:20日均价
        v_ma5:5日均量
        v_ma10:10日均量
        v_ma20:20日均量
        turnover:换手率[注：指数无此项]
        :param code:
        :return: res:收盘价 True:成功 False: 失败
        """
        # ts.get_hist_data('600848', start='2015-01-05', end='2015-01-09')
        start_date = date_list[0]
        end_date = date_list[-1]
        res = None
        try:
            res = ts.get_hist_data(code, start=start_date, end=end_date)
            res = res['close'].sort_index()
            res = res.to_frame(code)
            return res, True
        except Exception as e:
            print(e)
        return res, False
########################################################################################################################


def main():
    r = Research()
    # r.initail()  # 用到data.csv的时候要运行
    r.count_rise_fall()


if __name__ == '__main__':
    main()
