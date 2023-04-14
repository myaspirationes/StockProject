import tushare as ts
import openpyxl
import matplotlib.pyplot as plt
#import mpl_finance as mpf
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import matplotlib.ticker as ticker
import MySQLdb
import datetime
from sqlalchemy import create_engine

import time


# 查询出所有的股票信息插入表中

pro = ts.pro_api('a0045b3469b1b145fb57a7b97467a49fd7deecdd299c21b6d9a5f64a',33)

engine_ts = create_engine('mysql://root:root@127.0.0.1:3306/test?charset=utf8&use_unicode=1')
df = pro.stock_basic() #股票池基本信息
# res = df.to_sql('stock_basic', engine_ts, index=False, if_exists='append', chunksize=5000)
res = df.to_sql('stock_basic', engine_ts, index=False, if_exists='replace')

time.sleep(10)

update_tscode="UPDATE stock_basic SET ts_code = CONCAT( SUBSTRING_INDEX(ts_code, '.', -1),SUBSTRING_INDEX(ts_code, '.', 1))"

connect = MySQLdb.connect("localhost", "root", "root", "test", charset='utf8')
cursor = connect.cursor()

try:

    cursor.execute(update_tscode)
    connect.commit()



except mysql.connector.Error as error:
    print("error:{}".format(error))

cursor.close()
connect.close()


#
# #每日插入交易数据
# today= time.strftime('%Y%m%d',time.localtime(time.time()))#接口所需参数格式
# print(today)
# df=pro.daily(trade_date=today)
# print(df)
# res = df.to_sql('trade_details_2022', engine_ts, index=False, if_exists='append', chunksize=5000)
#格式化日期
# now_time=datetime.datetime.now()
# print(now_time.strftime("%Y%m%d"))
# print((now_time+datetime.timedelta(days=-1)).strftime("%Y%m%d")) #获取后一天
#
# begin_date=(now_time+datetime.timedelta(days=-1)).strftime("%Y%m%d")#获取后一天
# last_date=now_time.strftime("%Y%m%d")
# print(begin_date)
# print(last_date)

# #查询出均价
# ts_code='000777'
# sql5 = "select avg (tt.close) avg5 ,tt.ts_code,tt.trade_date from (select t.close,t.ts_code ,t.trade_date from trade_details_2022 t where t.ts_code={} and " \
#        " t.trade_date<={} order by t.trade_date  desc  limit 5)as tt".format( ts_code ,today)
#
# df = pd.read_sql_query(sql5, engine_ts)
# print(df)
# avge=pd.DataFrame(df)
# print(avge.get('avg (tt.close)'))
# res = df.to_sql('break_3_lines', engine_ts, index=False, if_exists='append', chunksize=5000)

# #查询并计算5日、10日、20日、30日均线值
#         sqlfive =  "select avg (tt.close) avg5 ,tt.ts_code,tt.trade_date from (select t.close,t.ts_code ,t.trade_date from trade_details_2022 t where t.ts_code={} and " \
#        " t.trade_date<={} order by t.trade_date  desc  limit 5)as tt".format( stock_code ,trade_day)
#         df5 = pd.read_sql_query(sqlfive, engine_ts)
#         # print(df5)
#         average5 = pd.DataFrame(df5)
#         avg5= average5.get('avg5')#获取到5日均值
#         print('5日线值：%s'%avg5)
#         # print(avg5)
#         # print(type(float(avg5)))
#         # print(type(today['open']))
#
#         sql10 = "select avg (tt.close) from (select t.close from trade_details_2022 t where t.ts_code={} and " \
#                 " t.trade_date<={} order by t.trade_date  desc  limit 10)as tt".format(stock_code ,trade_day)
#         df10 = pd.read_sql_query(sql10, engine_ts)
#
#         # print(df10)
#         average10 = pd.DataFrame(df10)
#         avg10=average10.get('avg (tt.close)')#获取到10日均值
#         print('10日线值：%s'%avg10)
#
#
#         sql20 = "select avg (tt.close) from (select t.close from trade_details_2022 t where t.ts_code={} and " \
#                 " t.trade_date<={} order by t.trade_date  desc  limit 20)as tt".format(stock_code ,trade_day)
#         df20 = pd.read_sql_query(sql20, engine_ts)
#         average20 = pd.DataFrame(df20)
#         avg20=average20.get('avg (tt.close)')#获取到20日均值
#         print('20日线值：%s'%avg20)
#
#
#         sql30 = "select avg (tt.close) from (select t.close from trade_details_2022 t where t.ts_code={} and " \
#                 " t.trade_date<={} order by t.trade_date  desc  limit 30)as tt".format(stock_code ,trade_day)
#         df30 = pd.read_sql_query(sql30, engine_ts)
#         average30 = pd.DataFrame(df30)
#         avg30=average30.get('avg (tt.close)')#获取到30日均值
#         print('30日线值：%s'%avg30)
#
#
#
#
#         if (today['open']<float(avg5) and today['open']<float(avg10) and today['open']<float(avg20))and(today['close']>float(avg5) and today['close']>float(avg10) and today['close']>float(avg20)):
#             res = df5.to_sql('break_3_lines', engine_ts, index=False, if_exists='append', chunksize=5000)
#             print("********************===  抓到一个了!  ===**********************")



#获取当年1月1日至今的交易日期
# trade_cal = pro.trade_cal(is_open='1', start_date='20220916', end_date='20220923')
# print(trade_cal)
#
# trade_days=trade_cal.cal_date#获取交易日期对象中的日期
# print(trade_days)
# list(trade_days)
# for trade_day in trade_days:
#     df=pro.daily(trade_date=trade_day)
#     # print(df)
#     res = df.to_sql('trade_details_2022_all', engine_ts, index=False, if_exists='append', chunksize=5000)
