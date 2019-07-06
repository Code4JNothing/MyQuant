import numpy as np
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters
import dataFetch
import matplotlib.pyplot as plt

sql = "SELECT h.TRADE_DATE, h.vol FROM hfq_daily_info h where h.code = '600036' and h.trade_date > '2019-06-01'"

zhongguoyh = dataFetch.fetch_data_db(sql)
zhongguoyh = pd.DataFrame(list(zhongguoyh), columns=['trade_date', 'vol'])
c = zhongguoyh["vol"]
c = c - np.mean(c.values)


date = zhongguoyh["trade_date"]
values = pd.DataFrame({"zhongguoyh": c.values}, date)
sns.lineplot(data=values, palette="tab10", linewidth=2.5)
plt.show()