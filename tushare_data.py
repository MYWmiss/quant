# _*_ coding: utf-8 _*_

import tushare as ts
import pandas as pd
import os


class StockInfo(object):
    def __init__(self):
        self.data_path = './data.csv'
        self.stock_data = None

    # 下载所有股票数据并保存到csv文件
    def download_data_and_save(self):
        """
        技术笔记:get_stock_basics用法
        code,代码
        name,名称
        industry,所属行业
        area,地区
        pe,市盈率
        outstanding,流通股本(亿)
        totals,总股本(亿)
        totalAssets,总资产(万)
        liquidAssets,流动资产
        fixedAssets,固定资产
        reserved,公积金
        reservedPerShare,每股公积金
        esp,每股收益
        bvps,每股净资
        pb,市净率
        timeToMarket,上市日期
        undp,未分利润
        perundp, 每股未分配
        rev,收入同比(%)
        profit,利润同比(%)
        gpr,毛利率(%)
        npr,净利润率(%)
        holders,股东人数
        """
        if os._exists(self.data_path):
            os.remove(self.data_path)
        res = ts.get_stock_basics()
        res.to_csv(path_or_buf=self.data_path, encoding='utf-8')

    # 从csv文件中读取数据
    def load_data(self):
        if not self.stock_data:
            self.stock_data = pd.read_csv(filepath_or_buffer=self.data_path, encoding='utf-8')
        return self.stock_data

    # 获得所有上交所主板股票代码
    def get_all_600_code(self):
        if isinstance(self.stock_data, pd.core.frame.DataFrame):
            codes = self.stock_data['code']
            res = list()
            for code in codes:
                code = str(code)
                if len(code) == 6 and code.startswith('6'):
                    res.append(code)
            return res
        else:
            print('WARN: load_data first !')
            return None

    # 根据某列排序
    def sort_by_column(self, keyword, ascending):
        """
        :param keyword: 按照哪个字段排序
        :param ascending: 是否递增
        :return:
        """
        if isinstance(self.stock_data, pd.core.frame.DataFrame):
            return self.stock_data.sort_values(by=keyword, ascending=ascending)
        else:
            print('WARN: load_data first !')


"""
技术笔记:
DataFrame选择数据
df.loc[[index],[colunm]] 通过标签选择数据
df.iloc[[index],[colunm]] 通过位置选择数据
df.ix[[index],[column]] 通过标签or位置选择数据
"""
"""
金融笔记:
000***是深交所主板
002***是深交所中小企业版
300***是深交所创业板
600***是上交所
"""


def main():
    s = StockInfo()
    # s.download_data_and_save()
    # s.load_data()
    # res = s.sort_by_column('gpr', False)
    # print(res.loc[:, ['gpr', 'code']])
    # res = s.get_all_600_code()
    # print(res)
    # print('len -> {}'.format(len(res)))


if __name__ == '__main__':
    main()
