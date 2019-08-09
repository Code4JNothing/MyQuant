import tushare_data
import db_data
import dataView

def hist_daily_insert():
    """
    历史复权数据入库
    :return:
    """
    tushare_data.hist_daily_insert('bfq')
    tushare_data.hist_daily_insert('qfq')
    tushare_data.hist_daily_insert('hfq')

    return


def daily_insert():
    """
    当日复权数据入库
    :return:
    """
    # 当日前复权数据
    tushare_data.daily_today_insert('qfq')
    # 当日后复权数据
    # tushare_data.daily_today_insert('hfq')
    # 当日不复权数据
    # tushare_data.daily_today_insert('bfq')
    return


if __name__ == '__main__':
    # 历史个股现金流信息
    db_data.add_money_flow()
    # 历史股票现金流统计信息
    db_data.add_money_flow_statistic()
    # 当日个股现金流信息
    try:
        db_data.add_money_flow_today()
    except Exception as err:
        print(err)
    # 当日股票现金流统计信息
    try:
        db_data.add_money_flow_statistic(today=True)
    except Exception as err:
        print(err)
    dataView.money_flow_statistic_view()

