import dataFetch
import myDb
from datetime import datetime
import pandas

def data_convert(date_str):
    return str(datetime.strptime(date_str, '%Y%m%d').strftime('%Y-%m-%d'))


def hs300_insert():
    """
    沪深300成分股入库
    :return:
    """
    hs300 = dataFetch.get_hs300s()
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
    return


def hist_daily_insert():
    """
    历史复权数据入库
    :return:
    """
    dataFetch.hist_daily_insert('bfq')
    dataFetch.hist_daily_insert('qfq')
    dataFetch.hist_daily_insert('hfq')

    return


if __name__ == '__main__':
    # 历史日线数据
    # hist_daily_insert()
    # 历史分时数据
    dataFetch.hist_tick_insert()

