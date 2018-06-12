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

    # 获得一支股票的历史行情数据
    @staticmethod
    def get_his_stock_data(code):
        """
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
        :return:
        """
        ts.get_hist_data(code)


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
    s.load_data()
    # res = s.sort_by_column('gpr', False)
    # print(res.loc[:, ['gpr', 'code']])
    res = s.get_all_600_code()
    print(res)
    print('len -> {}'.format(len(res)))


if __name__ == '__main__':
    main()
