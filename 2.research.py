# _*_ coding: utf-8 _*_

import tushare as ts
import pandas as pd
import os
from tushare_data import StockInfo
from Tools import Tools


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

    # 获得上证所有股票的最近n天收盘价 （后期细分，行业股）
    def get_n(self):
        """
        """
        # 获得前三个工作日的日期
        day_list = Tools.get_n_workday()
        day_list.sort(reverse=False)
        res_day = day_list.pop()  # 结果
        factor_dat2 = day_list.pop()  # 因子2
        factor_dat1 = day_list.pop()  # 因子1

        stock_list = self.stock_data.get_all_600_code()
        for stock in stock_list:
            ts.get_hist_data(stock)

    # 获得一支股票n天的收盘价
    def get_n_close(self, code):
        ts.get_hist_data('600848')


def main():
    r = Research()
    r.initail()
    print(r.find_lucky_day())


if __name__ == '__main__':
    main()
