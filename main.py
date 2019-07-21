import tushare_data
import myDb
from datetime import datetime
import db_data


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
    # tushare_data.daily_today_insert('qfq')
    # 当日后复权数据
    # tushare_data.daily_today_insert('hfq')
    # 当日不复权数据
    # tushare_data.daily_today_insert('bfq')
    return


if __name__ == '__main__':
    # 历史日线
    # db_data.hs30s_daily_info_add()
    # 历史分时
    # db_data.tick_data_add()
    # 历史现金流量信息
    # db_data.add_money_flow()
    # 当日日线
    # db_data.hs30s_daily_info_add(today=True)
    # 当日分时
    # db_data.tick_data_add(today=True)
    # 历史个股现金流信息
    db_data.add_money_flow()
    # 当日个股现金流信息
    # db_data.add_money_flow_today()
