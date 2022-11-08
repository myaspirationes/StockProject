#  MY  TOKEN :  a0045b3469b1b145fb57a7b97467a49fd7deecdd299c21b6d9a5f64a
import tushare as ts
import openpyxl
import matplotlib.pyplot as plt
import mplfinance as mpf
import matplotlib.pyplot as plt
import pandas as pd
import time
import datetime
import matplotlib.ticker as ticker
from sqlalchemy import create_engine

#df = ak.stock_zh_a_daily(symbol="sz002714", start_date="20201103", end_date="20210118",adjust="qfq")
# dfr =ts.get_hist_data(code="sz002714", start="20201103", end="20210118")
# print(dfr)
pro = ts.pro_api('a0045b3469b1b145fb57a7b97467a49fd7deecdd299c21b6d9a5f64a',33)





# ddf = pro.daily(ts_code='000001.SZ', start_date='20220701', end_date='20220718')

# sdf = pro.query('daily', ts_code='600519.SH', start_date='20220201', end_date='20220712')
# now_time = datetime.datetime.now()
# last_date = now_time.strftime("%Y%m%d")
# begin_date = (now_time + datetime.timedelta(days=-10)).strftime("%Y%m%d")  # 获取前一天，这里有一个bug，交易日不一定是昨天
#
# print(now_time,last_date)
# #获取交易日期
# ts.set_token('a0045b3469b1b145fb57a7b97467a49fd7deecdd299c21b6d9a5f64a')
# #df = ts.pro_bar(ts_code='000777.SZ', start_date='20220801', end_date='20220920', ma=[5, 10, 20,30])
#
# trade_cal = pro.trade_cal(exchange='', start_date=begin_date, end_date=last_date)
# print(trade_cal)
# pre_tradeday=trade_cal['pretrade_date'][10]
# print(type(pre_tradeday))
# print(pre_tradeday)
# list(pre_tradeday)
# print(pre_tradeday[-1:])  #获取交易日期

engine_ts = create_engine('mysql://root:root@127.0.0.1:3306/test?charset=utf8&use_unicode=1')
#获取A股每日筹码平均成本和胜率情况
# df_cost_winRate = pro.cyq_perf(ts_code='002945.SZ', start_date='20220901', end_date='20221010')
# res = df_cost_winRate.to_sql('cyq_perf', engine_ts, index=False, if_exists='append', chunksize=5000)
#获取A股每日筹码分布情况，提供各价位占比
# df_cost_pnt = pro.cyq_chips(ts_code='002945.SZ', start_date='20221010', end_date='20221010')
# res = df.to_sql('cyq_chips', engine_ts, index=False, if_exists='append', chunksize=5000)
#每日涨跌停,炸板股票信息
df = pro.limit_list_d(trade_date='20221010')
res = df.to_sql('raising_decline_limit', engine_ts, index=False, if_exists='append', chunksize=5000)


print(res)
# print((df.ma5)[0])
# print((df.ma10)[0])
# print((df.ma20)[0])
#print((df.ma30)[0])


# print (ddf)
# ddf.to_excel("牧原股份.xlsx")

#创建绘图的基本参数
# fig=plt.figure(figsize=(12, 8))
# ax=fig.add_subplot(111)

#获取刚才的股票数据
#df = pd.read_excel("牧原股份.xlsx")
#mpf.candlestick2_ochl(ax, df["open"], df["close"], df["high"], df["low"], width=0.6, colorup='green',colordown='red',alpha=1.0)
#显示出来
#plt.show()


#将股票时间转换为标准时间，不带时分秒的数据
def date_to_num(dates):
    num_time = []
    for date in dates:
        date_time = datetime.strptime(date, '%Y-%m-%d')
        num_date = date2num(date_time)
        num_time.append(num_date)
    return num_time

#创建绘图的基本参数
# fig=plt.figure(figsize=(12, 8))
# ax=fig.add_subplot(111)

#获取刚才的股票数据
# df = pd.read_excel("牧原股份.xlsx")
#
# mpf.candlestick2_ochl(ax, df["open"], df["close"], df["high"], df["low"], width=0.6, colorup='r',colordown='green',alpha=1.0)
# df['date'] = pd.to_datetime(df['trade_date'])
# df['date'] = df['date'].apply(lambda x: x.strftime('%Y-%m-%d'))
# def format_date(x, pos=None):
#     if x < 0 or x > len(df['date']) - 1:
#         return ''
#     return df['date'][int(x)]
# ax.xaxis.set_major_formatter(ticker.FuncFormatter(format_date))
# plt.setp(plt.gca().get_xticklabels(), rotation=45, horizontalalignment='right')
# #显示出来
# plt.show()
