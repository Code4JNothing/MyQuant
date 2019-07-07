"""
利用SQLAlchemy查询数据并转换为DataFrame
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import pandas as pd
import tables

# 初始化数据库连接:
engine = create_engine('mysql+mysqlconnector://root:mysql@localhost:3306/mystockdata')
DBSession = sessionmaker(bind=engine)
# 创建Session:
session: object = DBSession()


def get_vol_stocks(ts_code=None):
    """
    获取股票代码、交易日期、交易量
    :param ts_code:股票代码，默认为零
    :return: DataFrame，获取股票的代码，交易日期，成交量
    """
    if ts_code:
        query_obj = session.query(tables.DailyInfo.code, tables.DailyInfo.trade_date,
                                  tables.DailyInfo.vol).filter(tables.DailyInfo.code == ts_code)
        return pd.read_sql(query_obj.statement, engine)
    else:
        query_obj = session.query(tables.DailyInfo.code, tables.DailyInfo.vol)
        return pd.read_sql(query_obj.statement, engine)


def db_session_close():
    # 释放Session
    return session.close()
