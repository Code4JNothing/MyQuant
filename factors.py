"""
因子分析函数
"""
import db_data


def is_quantile_4th(code, date=None, q=0.25):
    """
    当前交易量是否位于前q分位以内，默认近三年
    :param code 股票代码
    :param date 起始日期
    :param q 分位数
    当前交易量是否处于上四分位以内
    :return:
    """
    hist_data = db_data.get_vol_stocks(ts_code=code, trade_date=date)
    quantitles_4th = hist_data['vol'].quantile(q=q)
    return hist_data['vol'].tail(1) < quantitles_4th