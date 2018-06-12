# _*_ coding: utf-8 _*_
"""
工具箱
"""
import datetime
from datetime import timedelta


class Tools(object):
    def __init__(self):
        pass

    # 判断某个日期是否是工作日
    @staticmethod
    def check_workday(date):
        """
        :param date: datetime.datetime
        :return: BOOL
        """
        td = date.weekday()
        if td < 5:
            return True
        return False

    # 判断某个日期是否是工作日str
    @staticmethod
    def check_workday_str(date):
        """
        :param date: "2018-06-11"
        :return: BOOL
        """
        td = datetime.datetime.strptime(date, "%Y-%m-%d").weekday()
        if td < 5:
            return True
        return False

    # 获取某个日期前n个工作日(不包含当日)
    @staticmethod
    def get_n_workday(num=3, date=datetime.datetime.now().strftime('%Y-%m-%d')):
        day_list = list()
        # day_list.append(date)
        date = datetime.datetime.strptime(date, "%Y-%m-%d")
        while len(day_list) < num:
            date = date + timedelta(days=-1)
            if Tools.check_workday(date):
                date_str = date.strftime('%Y-%m-%d')
                day_list.append(date_str)
        return day_list

    # 判断某个时间是否是交易时间
    @staticmethod
    def check_working_hours(ntime):
        """
        :param ntime: datetime.datetime
        :return: BOOL
        """
        td = ntime.weekday()
        if td < 5:
            hour = ntime.hour
            minute = ntime.minute
            f_min = hour * 60 + minute
            if 570 <= f_min <= 690 or 780 <= f_min <= 900:
                return True
        return False


if __name__ == '__main__':
    a = Tools.get_n_workday()
    print(a)
