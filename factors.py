"""
因子分析函数
"""
import db_data


def is_quantile_qth(code, date=None, n=5, q=0.2):
    """
    当前近N天交易量是否位于前q分位以内，默认近两年
    :param code 股票代码
    :param date 起始日期
    :param q 分位数
    :param n 近几天
    当前交易量是否处于上四分位以内
    :return:
    """
    hist_data = db_data.get_vol_stocks(ts_code=code, trade_date=date)
    quantitles_qth = hist_data['vol'].quantile(q)

    return code, (hist_data['vol'].tail(n).values < quantitles_qth).all()