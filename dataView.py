import db_data as data
import matplotlib.pyplot as plt

import tushare_data


def money_flow_statistic_view():
    """
    小单成交比例统计折线图
    :return:
    """
    hs300_daily_info = tushare_data.get_index_daily('000300.SH')
    hs300_daily_info = hs300_daily_info.loc[hs300_daily_info['trade_date'] > '20180630']
    money_flow_statistic = data.get_money_flow_statistic()
    fig, (ax0, ax1) = plt.subplots(nrows=2)
    ax1.plot(money_flow_statistic['trade_date'], money_flow_statistic['small_total_rate'])
    ax1.grid(True)
    ax1.set_xlabel('trade_date')
    ax1.set_ylabel('small_trade_rate')
    fig.autofmt_xdate(rotation=90)

    ax0.plot(hs300_daily_info['trade_date'], hs300_daily_info['close'])
    ax0.grid(True)
    ax0.set_xlabel('trade_date')
    ax0.set_ylabel('close')
    plt.show()