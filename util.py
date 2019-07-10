"""
常用公共函数
"""
import datetime


def stock_code_change(code):
    """
    添加股票代码标识，如6000000.SH、0000001.SZ分表标识上证、深证
    :param code: 六位股票代码
    :return: 添加沪深标识后缀的股票代码
    """
    code = code.strip()
    if code.isdigit() and len(code) == 6:
        if str(code).startswith('6'):
            return str(code) + '.SH'
        else:
            return str(code) + '.SZ'


def data_start_end_future(date):
    """
    日期转换，输入%Y%m%d，返回两年前、半年后的日期
    :param date: 目标日期
    :return: list[...],元素格式%Y%m%d
    """
    dates = str(date).strip().split("-")
    start_date = (datetime.datetime(int(dates[0]), int(dates[1]), int(dates[2])) - datetime.timedelta(days=365 * 2))\
        .strftime('%Y-%m-%d')
    future = (datetime.datetime(int(dates[0]), int(dates[1]), int(dates[2])) + datetime.timedelta(days=182))\
        .strftime('%Y-%m-%d')
    return list([start_date, date, future])

