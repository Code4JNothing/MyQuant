"""
利用SQLAlchemy查询数据并转换为DataFrame
"""
import tushare
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import pandas as pd
import datetime
import tables
import tushare_data

# 初始化数据库连接:
import util

engine = create_engine('mysql+mysqlconnector://root:mysql@localhost:3306/mystockdata')
DBSession = sessionmaker(bind=engine)
# 创建Session:
session: object = DBSession()


def get_vol_stocks(ts_code=None, trade_date=None):
    """
    获取股票代码、交易日期、交易量，默认近两年
   :param ts_code:股票代码，默认为零
    :param trade_date:交易起始日期
    :return: DataFrame，获取股票的代码，交易日期，成交量
    """
    # 如日期为None则默认返回近三年数据
    if trade_date is None:
        trade_date = (datetime.datetime.today() - datetime.timedelta(days=365 * 2)).strftime('%Y-%m-%d')
    if ts_code:
        query_obj = session.query(tables.DailyInfo.code, tables.DailyInfo.trade_date,
                                  tables.DailyInfo.vol).filter(tables.DailyInfo.code == ts_code,
                                                               tables.DailyInfo.trade_date > trade_date) \
            .order_by(tables.DailyInfo.trade_date)
        return pd.read_sql(query_obj.statement, engine)
    else:
        query_obj = session.query(tables.DailyInfo.code, tables.DailyInfo.vol,
                                  tables.DailyInfo.trade_date > trade_date if trade_date else '')
        return pd.read_sql(query_obj.statement, engine)


def db_session_close():
    # 释放Session
    return session.close()


def hs30s_add():
    """
    导入30支沪深300股票基本权重信息
    :return:
    """
    try:
        hs30s = tushare_data.get_hs30s()
        print("导入沪深300成份股中30支股票")
        for index, row in hs30s.iterrows():
            tables.add_index_stocks(code=row['code'], date=str(row['date'])[:10], name=row['name'],
                                    weight=row['weight'])
        print("导入完成")
    except Exception as err:
        print("数据导入失败:", str(err))


def hs30s_daily_info_add():
    """
    导入30支沪深300股票日线信息
    :return:
    """
    hs_code = tables.hs30_queryy()
    for row in hs_code:
        ts_code = util.stock_code_change(row.code)
        daily = tushare.pro_bar(ts_code=ts_code)
        for index, daily_info in daily.iterrows():
            id = str(daily_info['ts_code'][:6]) + str(daily_info['trade_date'][:10]).replace('-', '')
            tables.add_daily_info(id=id, code=row.code, open=daily_info['open'], close=daily_info['close'],
                                  high=daily_info['high'], low=daily_info['low'], pre_close=daily_info['pre_close'],
                                  pchange=daily_info['change'], vol=daily_info['vol'], amount=daily_info['amount'],
                                  pct_change=daily_info['pct_chg'], trade_date=daily_info['trade_date'])
