"""
利用SQLAlchemy查询数据并转换为DataFrame
"""
import random
import tushare
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import pandas as pd
import datetime

import myDb
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


def hs30s_daily_info_add(today=False):
    """
    导入30支沪深300股票日线信息
    :return:
    """
    hs_code = tables.hs30_queryy()
    for row in hs_code:
        try:
            ts_code = util.stock_code_change(row.code)
            if today:
                start_date = datetime.datetime.now().strftime('%Y%m%d')
                end_date = datetime.datetime.now().strftime('%Y%m%d')
                daily = tushare.pro_bar(ts_code=ts_code, start_date=start_date, end_date=end_date)
                print("插入日线数据：st_code =", row.code, ' date =', end_date)
                pass
            else:
                daily = tushare.pro_bar(ts_code=ts_code)
                print("插入日线数据：st_code =", row.code)
            for index, daily_info in daily.iterrows():
                id = str(daily_info['ts_code'][:6]) + str(daily_info['trade_date'][:10]).replace('-', '')
                tables.add_daily_info(id=id, code=row.code, open=daily_info['open'], close=daily_info['close'],
                                      high=daily_info['high'], low=daily_info['low'], pre_close=daily_info['pre_close'],
                                      pchange=daily_info['change'], vol=daily_info['vol'], amount=daily_info['amount'],
                                      pct_change=daily_info['pct_chg'], trade_date=daily_info['trade_date'])
        except Exception as e:
            print(e)


def tick_data_add(today=False):
    """
    历史分时数据插入
    :return:
    """
    hs30s_daily_info = tables.hs30_daily_queryy()
    for row in hs30s_daily_info:
        if today:
            date = datetime.datetime.now().strftime('%Y%m%d')
        else:
            date = row.trade_date[:4] + '-' + row.trade_date[4:6] + '-' + row.trade_date[6:8]
        print("插入分时数据：st_code =", row.code, ' date =', date)
        try:
            if date <= '2017-12-32':
                continue
            df = tushare.get_tick_data(code=row.code, date=date, src='tt')
            if df is None:
                continue
            for index, tick in df.iterrows():
                id = row.code + row.trade_date + tick['time'] + str(random.randint(1, 10000)).zfill(5)
                tables.add_tick_date(code=row.code, date=row.trade_date, time=tick['time'], price=tick['price'],
                                     pchange=tick['change'], volume=tick['amount'], amount=tick['amount'],
                                     type=tick['type'], id=id)
            print("插入分时数据：", "st_code =", row.code, ' date =', date, "插入完成")
        except Exception as e:
            print(e)


def hs300_insert():
    """
    沪深300成分股入库
    :return:
    """
    hs300 = tushare_data.get_hs300s()
    db = myDb.db_connect()
    cursor = db.cursor()
    for index, row in hs300.iterrows():
        sql = "INSERT INTO INDEX_STOCKS (CODE, NAME, INDEX_TYPE, DATE, WEIGHT) VALUES(" \
              + '\'' + row['code'] + '\'' + ',' \
              + '\'' + row['name'] + '\'' + ',' \
              + '\'' + '300' + '\'' + ',' + '\'' \
              + str(row['date'])[:10] + '\'' + ',' \
              + '\'' + str(row["weight"]) + '\'' \
              + ')'
        myDb.data_insert(db, cursor, sql)
    db.close()
