"""
描述本地数据库表属性
"""
from sqlalchemy import Column, String, Sequence, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.mysql import FLOAT, INTEGER
from sqlalchemy.orm import sessionmaker


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
    return session.query(IndexStocks).all()
