"""
利用SQLAlchemy查询数据并转换为DataFrame
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import pandas as pd
import datetime
import tables

# 初始化数据库连接:
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
        trade_date = (datetime.datetime.today() - datetime.timedelta(days=365*2)).strftime('%Y-%m-%d')
    if ts_code:
        query_obj = session.query(tables.DailyInfo.code, tables.DailyInfo.trade_date,
                                  tables.DailyInfo.vol).filter(tables.DailyInfo.code == ts_code,
                                                               tables.DailyInfo.trade_date > trade_date)\
            .order_by(tables.DailyInfo.trade_date)
        return pd.read_sql(query_obj.statement, engine)
    else:
        query_obj = session.query(tables.DailyInfo.code, tables.DailyInfo.vol,
                                  tables.DailyInfo.trade_date > trade_date if trade_date else '')
        return pd.read_sql(query_obj.statement, engine)


def db_session_close():
    # 释放Session
    return session.close()
