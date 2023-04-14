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
import MySQLdb

#df = ak.stock_zh_a_daily(symbol="sz002714", start_date="20201103", end_date="20210118",adjust="qfq")
# dfr =ts.get_hist_data(code="sz002714", start="20201103", end="20210118")
# print(dfr)


stock_list=[]
pro = ts.pro_api('a0045b3469b1b145fb57a7b97467a49fd7deecdd299c21b6d9a5f64a',33)

connect = MySQLdb.connect("localhost", "root", "root", "test", charset='utf8')
cursor = connect.cursor()
print(cursor)



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

# engine_ts = create_engine('mysql://root:root@127.0.0.1:3306/test?charset=utf8&use_unicode=1')
#获取A股每日筹码平均成本和胜率情况
# df_cost_winRate = pro.cyq_perf(ts_code='002945.SZ', start_date='20220901', end_date='20221010')
# res = df_cost_winRate.to_sql('cyq_perf', engine_ts, index=False, if_exists='append', chunksize=5000)
#获取A股每日筹码分布情况，提供各价位占比
# df_cost_pnt = pro.cyq_chips(ts_code='002945.SZ', start_date='20221010', end_date='20221010')
# res = df.to_sql('cyq_chips', engine_ts, index=False, if_exists='append', chunksize=5000)
#每日涨跌停,炸板股票信息
# df = pro.limit_list_d(trade_date='20221010')
# res = df.to_sql('raising_decline_limit', engine_ts, index=False, if_exists='append', chunksize=5000)
# print(res)

df_basic = pro.stock_basic(exchange='', list_status='L')

# print(type(df_basic))
# 筛选数据：剔除*st股，科创板，
df_basic = df_basic[df_basic['name'].apply(lambda x: x.find('*ST') < 0)]
df_basic = df_basic[df_basic['ts_code'].apply(lambda x: x.find('.BJ') < 0)]
df_basic = df_basic[df_basic['market'].apply(lambda x: x.find('科创板') < 0)]
# print(df_basic)


# print(df_basic.industry)
# df_basic = df_basic[(df_basic["industry"] == u"证券") | (df_basic["industry"] == u"全国地产")
#                     | (df_basic["industry"] == u"银行") | (df_basic["industry"] == u"水泥")
#                     | (df_basic["industry"] == u"保险") | (df_basic["industry"] == u"医疗保健")
#                     | (df_basic["industry"] == u"半导体") | (df_basic["industry"] == u"元器件")
#                     | (df_basic["industry"] == u"数字货币") | (df_basic["industry"] == u"汽车")
#                     | (df_basic["industry"] == u"医药") | (df_basic["industry"] == u"化工")
#                     ]


get_codes = dict(zip(df_basic.ts_code.values, df_basic.industry.values))

# print(get_codes.keys())

arrays = get_codes.keys()
arrays = list(arrays)
# arrays = arrays[3800:]
i = 0
for array in arrays:
    i = i + 1

# get stock data for the last 3 months
    print("%s,%s"%(array,i))


    if (i % 500 == 0):
        number = i // 500
        print(
            '**************************************************************************************已调用接口第 %s '
            '个500次了，让tushare的接口踹口气**********************************************' % number)
        time.sleep(10)
        print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))




    df = pro.daily(ts_code=array, start_date='20230101', end_date='20230412')
    # print(df)
    high = df['high'].max()
    low = df['low'].min()

    # print(high_date)
    # print(low_date)
    





    if high>=low*2.2:
        print(f'Highest price: {high}, Lowest price: {low}')
        high_date = df[df.iloc[:, 3] == high].iloc[:, 1].values[0]
        low_date = df[df.iloc[:, 4] == low].iloc[:, 1].values[0]
        print("high date is : {} ,low date is:{} ".format(high_date,low_date))
        times = round(high / low, 1)

        if high_date< low_date:

            times=0-times


        print(times)
        last_2w = array[-2:]
        # print(last_2w)
        pre_6w = array[0:6]
        # print(pre_6w)
        stock_code = last_2w + pre_6w  # 格式SH600600 或者SZ300300

        current_time = datetime.datetime.now()
        now = current_time.strftime("%Y-%m-%d %H:%M:%S")


        

        select_tscode="select * from test.triple_price where ts_code=%s"
        select_param=(stock_code,)



        update_ifexist="update test.triple_price set high=%s,high_date=%s,low=%s,low_date=%s,times=%s where ts_code=%s;"
        param_update = (high,high_date, low,low_date,times,stock_code)


        sql_three_times = "INSERT INTO test.triple_price (ts_code,  high,high_date, low,low_date,`date`, " \
                          "times) values (%s,%s,%s,%s,%s,%s,%s);"
        param_insert = (stock_code, high,high_date, low,low_date,now,times)

       

        try:
            cursor.execute(select_tscode, select_param)
            if cursor.fetchone() is None:
                cursor.execute(sql_three_times, param_insert)
                print("price  3 times  Add To Database  Success")

                update_ts_name = 'update test.triple_price,test.stock_basic set test.triple_price.name= test.stock_basic.name  ' \
                                 'where test.triple_price.ts_code=test.stock_basic.ts_code;'
                cursor.execute(update_ts_name)


            time.sleep(5)
            
            cursor.execute(update_ifexist,param_update)
            
            
            

            connect.commit()
        except mysql.connector.Error as error:
            # Catch the error and handle it appropriately
            print("Error: {}".format(error))
            connect.rollback()



cursor.close()
connect.close()





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
# def date_to_num(dates):
#     num_time = []
#     for date in dates:
#         date_time = datetime.strptime(date, '%Y-%m-%d')
#         num_date = date2num(date_time)
#         num_time.append(num_date)
#     return num_time

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
