import tushare as ts
import matplotlib.pyplot as plt
#import mplfinance as mpf
import pandas as pd
import numpy as np
import matplotlib.ticker as ticker
import MySQLdb
from sqlalchemy import create_engine

pro = ts.pro_api('a0045b3469b1b145fb57a7b97467a49fd7deecdd299c21b6d9a5f64a', 33)
stock_dat = pro.daily(ts_code='000759.SZ', start_date='20220901', end_date='20220914')

engine_ts = create_engine('mysql://root:root@127.0.0.1:3306/test?charset=utf8&use_unicode=1')
#df = pro.stock_basic()#获取全部交易信息

print(type(stock_dat))
print(stock_dat[stock_dat.trade_date=='20220908'])
connect = MySQLdb.connect("localhost", "root", "root", "test", charset='utf8')
cursor = connect.cursor()

for kl_index in np.arange(1, stock_dat.shape[0]):
    # today今天的股票信息
    # yesterday 昨天的股票信息

    today = stock_dat.iloc[kl_index - 1]  # 若版本提示已经弃用 可使用loc或iloc替换
    yesterday = stock_dat.iloc[kl_index]
    yesterday = yesterday.copy()

    today = today.copy()
    # print("-----")
    # print(today)
    # print('----yesterday')
    # print(yesterday)
    # 思考：成交量是昨日3-5倍以上


    Multiples = round(today.vol / yesterday.vol, 2)  # 交易量倍数保留2位小数
    # print(times)

    if (today['pct_chg'] > 0) and (Multiples >= 2.5):
            print('$$$$$$$$$$===============>')
            print(today.ts_code)
            print(today.trade_date)
            print(Multiples)

            todayinfo=stock_dat[stock_dat.trade_date==today.trade_date] # 数据框DataFrame的 数据筛选
            yesterdayinfo=stock_dat[stock_dat.trade_date==yesterday.trade_date]
            print(todayinfo)
            res = todayinfo.to_sql('three_times_vol_detail', engine_ts, index=False, if_exists='append', chunksize=5000)
            res = yesterdayinfo.to_sql('three_times_vol_detail', engine_ts, index=False, if_exists='append', chunksize=5000)

            sql_three_times = "insert into  three_times_vol (ts_code,times,date) value (%s,%s,%s)"
            param = (today.ts_code, Multiples, today.trade_date)
            try:
            # 执行sql语句
            # cursor.execute(sql, skip_stock_code)
                cursor.execute(sql_three_times, param)

            # cursor.execute(sql2, skip_stock_code,date)

                print("Add To Database  Success")
            # 提交到数据库执行
                connect.commit()
            except:
            # 发生错误时回滚
                connect.rollback()
cursor.close()
connect.close()