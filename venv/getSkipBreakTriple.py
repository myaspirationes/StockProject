import tushare as ts
import mpl_finance as mpf
import pandas as pd
import numpy as np
import MySQLdb
from sqlalchemy import create_engine
import time
import datetime

pro = ts.pro_api('a0045b3469b1b145fb57a7b97467a49fd7deecdd299c21b6d9a5f64a',33)

now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
# print(now)
date = now[0:10]  # 获得查询日期用于插入数据库
print(date)
# 设置开始和结束时间
now_time = datetime.datetime.now()
last_date = now_time.strftime("%Y%m%d")
begin_date = (now_time + datetime.timedelta(days=-10)).strftime("%Y%m%d")  # 十天之类必有交易日

trade_cal = pro.trade_cal(exchange='', start_date=begin_date, end_date=last_date)#获取最近十天中的交易日
# print(trade_cal)
pre_tradeday=trade_cal['pretrade_date']#前一个交易日，字典集合
# print(pre_tradeday)
latest_tradeday=pre_tradeday[10]#字典中取值，最近的前一个交易日

#begin_date = (now_time + datetime.timedelta(days=-1)).strftime("%Y%m%d")  # 获取前一天，这里有一个bug，交易日不一定是昨天
# print('pppppppppppp')
# print(begin_date)
# print(last_date)
# 链接数据库方法一：
connect = MySQLdb.connect("localhost", "root", "root", "test", charset='utf8')
cursor = connect.cursor()
# 链接数据库方法二：
engine_ts = create_engine('mysql://root:root@127.0.0.1:3306/test?charset=utf8&use_unicode=1')
ts.set_token('a0045b3469b1b145fb57a7b97467a49fd7deecdd299c21b6d9a5f64a')

# df = ak.stock_zh_a_daily(symbol="sz002714", start_date="20201103", end_date="20210118",adjust="qfq")
# 从接口拿数据
#pro = ts.pro_api('a0045b3469b1b145fb57a7b97467a49fd7deecdd299c21b6d9a5f64a', 33)
df_basic = pro.stock_basic(exchange='', list_status='L')

# print(df_basic)
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

#print(get_codes.keys())

# arrays = []
arrays = get_codes.keys()
arrays = list(arrays)
# print(len(arrays))  长度是 ：4296

time.sleep(1)
i = 0

for array in arrays:
    stock_dat = pro.daily(ts_code=array, start_date=latest_tradeday, end_date=last_date)#start_date 是前一个交易日，不一定是自然日
    i = i + 1
    print('已调用接口次数：%s'%i)
    print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    # print(stock_dat)

    # if (i % 500 == 0):
    #     print('已调用接口N个500次了，让tushare的接口踹口气~~~~~~~~~~~~~~~~~~')
    #     time.sleep(10)
    #     print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    #print(stock_dat.shape[0])
    for kl_index in np.arange(1, stock_dat.shape[0]):
        # today今天的股票信息
        # yesterday 昨天的股票信息

        today = stock_dat.iloc[kl_index - 1]  # 若版本提示已经弃用 可使用loc或iloc替换
        yesterday = stock_dat.iloc[kl_index]
        yesterday = yesterday.copy()

        today = today.copy()
        # print("-----")
        # print(today)

        stock_code = today['ts_code'][0:7]
        trade_day = today['trade_date']
        # print(trade_day)
        #print(stock_code)
        # print('----yesterday')
        # print(yesterday)
        # 思考：成交量是昨日3-5倍以上
        Multiples = round(today.vol / yesterday.vol, 2)  # 交易量倍数保留2位小数
        # print(times)
        # =======================>第一个if：筛选成交量3倍的股票
        if (today['pct_chg'] > 0) and (today['close'] > today['open']) and (Multiples >= 2.5):
            print('$$$$$$$$$$==  3倍  =============>')
            print(today.ts_code)
            print(today.trade_date)
            print(Multiples)

            # 使用两种方法存入数据库
            # 1.符合条件的存入详细信息表中，、
            todayfor = stock_dat[stock_dat.trade_date == today.trade_date]
            yesterdayfor = stock_dat[stock_dat.trade_date == yesterday.trade_date]
            print(todayfor)
            res = todayfor.to_sql('three_times_vol_detail', engine_ts, index=False, if_exists='append', chunksize=5000)
            res = yesterdayfor.to_sql('three_times_vol_detail', engine_ts, index=False, if_exists='append',
                                      chunksize=5000)

            # 2.存入3倍表中
            sql_three_times = "insert ignore into  three_times_vol (ts_code,times,date) value (%s,%s,%s)"
            param = (today.ts_code, Multiples, date)

            try:
                # 执行sql语句
                # cursor.execute(sql, skip_stock_code)
                cursor.execute(sql_three_times, param)

                # cursor.execute(sql2, skip_stock_code,date)

                print("Three Times  Stock Add To Database  Success")
                # 提交到数据库执行
                connect.commit()
            except:
                # 发生错误时回滚
                connect.rollback()

        # =======================>第二个if：筛选跳空的stocks
        skip_stock_code = []
        jump_threshold = 0.05  # 超过5分钱
        if (today['pct_chg'] > 0) and ((today.low - yesterday.high) > jump_threshold):
            skip_stock_code.append(today.ts_code)
            print('$$$$$$$$$$=====  跳空  ==========>')
            print(skip_stock_code)
            name = today.name

            # sql = "INSERT INTO skip_stock (ts_code) values(%s)"
            # sql2 = "INSERT INTO skip_stock values(%s,%s)"
            sql2 = "insert ignore into skip_stock (ts_code, date) VALUES (%s, %s)"
            val = (skip_stock_code, date)

            try:
                # 执行sql语句
                # cursor.execute(sql, skip_stock_code)
                cursor.execute(sql2, val)

                # cursor.execute(sql2, skip_stock_code,date)

                print("add success")
                # 提交到数据库执行
                connect.commit()
            except:
                # 发生错误时回滚
                connect.rollback()

        # ========================>第三个if：一阳三线的股票 存入数据库（sql计算5,10,20日均线速度太慢了）

        df = ts.pro_bar(ts_code=today['ts_code'], start_date='20220801', end_date=last_date, ma=[5, 10, 20, 30])
        # print(df)
        # print(df.ma5)
        lines_5 = (df.ma5)[0]
        # print(lines_5)

        if (today['open'] < (df.ma5)[0] and today['open'] < (df.ma10)[0] and today['open'] < (df.ma20)[0] and (
                today['close'] > (df.ma5)[0] and today['close'] > (df.ma10)[0] and today['close'] > (df.ma20)[0])):
            sql_three_lines = "insert ignore into  break_3_lines (ts_code,trade_date,avg5) value (%s,%s,%s)"
            param = (today.ts_code, date, lines_5)

            try:
                # 执行sql语句
                cursor.execute(sql_three_lines, param)
                print("Add To Database  Success")
                # 提交到数据库执行
                connect.commit()
            except:
                # 发生错误时回滚
                connect.rollback()

            print("********************===  抓到一个 一阳三线 了!====>>> %s ===**********************" % today.ts_code)
#
#
