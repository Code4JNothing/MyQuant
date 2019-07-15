"""
描述本地数据库表属性
优化性能，可参考：
https://docs.sqlalchemy.org/en/13/faq/performance.html#i-m-inserting-400-000-rows-with-the-orm-and-it-s-really-slow
"""
from sqlalchemy import Column, String, Sequence, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.mysql import FLOAT, INTEGER
from sqlalchemy.orm import sessionmaker

import myDb

db = myDb.db_connect()
cursor = db.cursor()
Base = declarative_base()

# 初始化数据库连接:
engine = create_engine('mysql+mysqlconnector://root:mysql@localhost:3306/mystockdata')
DBSession = sessionmaker(bind=engine)
# 创建Session:
session: object = DBSession()


class DailyInfo(Base):
    """
    日线数据
    """
    __tablename__ = 'daily_info'
    id = Column(String(16), Sequence('user_id_seq'), primary_key=True)
    code = Column(String(6))
    trade_date = Column(String(10))
    open = Column(FLOAT(precision=10, scale=2))
    close = Column(FLOAT(precision=10, scale=2))
    high = Column(FLOAT(precision=10, scale=2))
    low = Column(FLOAT(precision=10, scale=2))
    pre_close = Column(FLOAT(precision=10, scale=2))
    pchange = Column(FLOAT(precision=10, scale=2))
    pct_change = Column(FLOAT(precision=10, scale=2))
    vol = Column(INTEGER(20))
    amount = Column(FLOAT(precision=10, scale=2))


def add_daily_info(id, code, trade_date, open, close, high, low, pre_close, pchange, pct_change, vol, amount):
    """
    插入股票日线数据
    :param id: code+trade_date,唯一索引
    :param code 股票代码
    :param trade_date:交易日
    :param open:开盘价
    :param close:收盘价
    :param high：最高价
    :param low：最低价
    :param pre_close:昨日收盘价
    :param pchange：今日涨跌额
    :param pct_change:今日涨跌幅
    :param vol：交易量
    :param amount：交易金额
    :return:
    """
    daily_info = DailyInfo(id=id, code=code, trade_date=trade_date, open=open, close=close, high=high, low=low,
                           pre_close=pre_close, pchange=pchange, pct_change=pct_change, vol=vol, amount=amount)
    session.add(daily_info)
    session.commit()


def hs30_daily_queryy():
    """
    查询沪深30股票分时数据
    :return:
    """
    return session.query(DailyInfo).all()


class IndexStocks(Base):
    """
    指数股票信息
    """
    __tablename__ = "index_stocks"
    code = Column(String(6), primary_key=True)
    date = Column(String(10))
    name = Column(String(255))
    weight = Column(FLOAT(precision=10, scale=2))


def add_index_stocks(code, date, name, weight):
    """
    股票信息插入
    :param code: 股票代码
    :param date: 指数时间
    :param name: 股票名称
    :param weight: 占指数权重
    :return:
    """
    index_stocks = IndexStocks(code=code, date=date, name=name, weight=weight)
    session.add(index_stocks)
    session.commit()


def hs30_queryy():
    """
    查询沪深30股票代码信息
    :return:
    """
    return session.query(IndexStocks).all()


class TickDate(Base):
    """
    分时成交数据
    """
    __tablename__ = 'tick_data'
    code = Column(String(6))
    date = Column(String(10))
    time = Column(String(8))
    price = Column(FLOAT(precision=10, scale=2))
    pchange = Column(FLOAT(precision=10, scale=2))
    volume = Column(INTEGER(20))
    amount = Column(FLOAT(precision=10, scale=2))
    type = Column(String(8))
    id = Column(String(40), primary_key=True)


def add_tick_date(code, date, time, price, pchange, volume, amount, type, id):
    """
    sqlalchemy 性能较差，考虑使用原生拼接产生sql
    """
    '''
    tick_data = TickDate(code=code, date=date, time=time, price=price, pchange=pchange, volume=volume, amount=amount,
                         type=type, id=id)
    session.add(tick_data)
    '''
    '''
    # 还是很慢
    engine.execute(TickDate.__table__.insert(), {"code": code, "date": date, "time": time, "price": price,
                                                 "change": pchange, "volume": volume, "amount": amount, "type": type,
                                                 "id": id})
    '''
    '''
    手工拼sql减少了sql语句的表结构的解析与sql的生成
    '''
    sql = "INSERT INTO tick_data(ID, CODE, DATE, TIME, PRICE, PCHANGE, VOLUME, AMOUNT, TYPE) VALUES (" \
          + '\'' + str(id) + '\'' + ',' \
          + '\'' + str(code) + '\'' + ',' \
          + '\'' + str(date) + '\'' + ',' \
          + '\'' + str(time) + '\'' + ',' \
          + '\'' + str(price) + '\'' + ',' \
          + '\'' + str(pchange) + '\'' + ',' \
          + '\'' + str(volume) + '\'' + ',' \
          + '\'' + str(amount) + '\'' + ',' \
          + '\'' + str(type) + '\'' \
          + ')'
    myDb.data_insert(db, cursor, sql)


class MoneyFlow(Base):
    """
    个股资金流向
    """
    __tablename__ = 'moneyflow'
    id = Column(String(14), primary_key=True)
    code = Column(String(6))
    date = Column(String(8))
    sell_sm_vol = Column(INTEGER(12))
    sell_sm_amt = Column(FLOAT(precision=14, scale=2))
    buy_sm_vol = Column(INTEGER(12))
    buy_sm_amt = Column(FLOAT(precision=14, scale=2))
    total_sell_vol = Column(INTEGER(12))
    total_sell_amt = Column(FLOAT(precision=14, scale=2))
    total_buy_vol = Column(INTEGER(12))
    total_buy_amt = Column(FLOAT(precision=14, scale=2))
    net_inflows_amt = Column(FLOAT(precision=14, scale=2))


def add_money_flow(id, code, date, sell_sm_vol, sell_sm_amt, buy_sm_vol, buy_sm_amt,
                   total_sell_vol, total_sell_amt, total_buy_vol, total_buy_amt, net_inflows_amt):
    """
    插入资金流量信息
    :param id:
    :param code: 股票代码
    :param date: 交易日期
    :param sell_sm_vol: 小单卖出手数
    :param sell_sm_amt: 小单卖出金额
    :param buy_sm_vol: 小单买入手数
    :param buy_sm_amt: 小单买入金额
    :param total_sell_vol: 总卖出手数
    :param total_sell_amt: 总卖出金额
    :param total_buy_vol: 总买入手数
    :param total_buy_amt: 总买入金额
    :param net_inflows_amt: 净流入金额
    :return:
    """
    moneyflow = MoneyFlow(id=id, code=code, date=date, sell_sm_vol= sell_sm_vol, sell_sm_amt=sell_sm_amt,
                          buy_sm_vol=buy_sm_vol, buy_sm_amt=buy_sm_amt, total_sell_vol=total_sell_vol,
                          total_sell_amt=total_sell_amt, total_buy_vol=total_buy_vol, total_buy_amt=total_buy_amt,
                          net_inflows_amt=net_inflows_amt)
    session.add(moneyflow)
    session.commit()


