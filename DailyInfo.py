"""
利用SQLAlchemy查询数据并转换为DataFrame
"""
from sqlalchemy import Column, String, create_engine, Sequence
from sqlalchemy.orm import sessionmaker, query
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.mysql import FLOAT, INTEGER
import pandas as pd
Base = declarative_base()


class DailyInfo(Base):
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


# 初始化数据库连接:
engine = create_engine('mysql+mysqlconnector://root:mysql@localhost:3306/mystockdata')
DBSession = sessionmaker(bind=engine)

# 创建Session:
session = DBSession()
query_obj = session.query(DailyInfo).filter(DailyInfo.code == '600000')
data = pd.read_sql(query_obj.statement, engine)
print(data.head(10))
# 释放Session
session.close()
