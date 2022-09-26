import tushare as ts
import openpyxl
import matplotlib.pyplot as plt
import mpl_finance as mpf
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import matplotlib.ticker as ticker

import MySQLdb

from sqlalchemy import create_engine

import time
import datetime

now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
date = now[0:10] #获得查询日期用于插入数据库
print(date)
#设置开始和结束时间
now_time=datetime.datetime.now()
begin_date=(now_time+datetime.timedelta(days=-1)).strftime("%Y%m%d")#获取后一天
last_date=now_time.strftime("%Y%m%d")
# 链接数据库方法一：
connect = MySQLdb.connect("localhost", "root", "root", "test", charset='utf8')
cursor = connect.cursor()
#链接数据库方法二：
engine_ts = create_engine('mysql://root:root@127.0.0.1:3306/test?charset=utf8&use_unicode=1')
ts.set_token('a0045b3469b1b145fb57a7b97467a49fd7deecdd299c21b6d9a5f64a')

# df = ak.stock_zh_a_daily(symbol="sz002714", start_date="20201103", end_date="20210118",adjust="qfq")
#从接口拿数据
pro = ts.pro_api('a0045b3469b1b145fb57a7b97467a49fd7deecdd299c21b6d9a5f64a', 33)
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

#股票代码存入excel
get_codes = dict(zip(df_basic.ts_code.values, df_basic.industry.values))
exceldata = pd.DataFrame(get_codes.keys())
exceldata.to_excel("scanerStocks.xlsx")
# print(get_codes.keys())
# print(type(get_codes.keys()))
#代码每500个一组，规避接口500个每分钟的限制
arrays = []
arrays = get_codes.keys()
arrays = list(arrays)
array1 = arrays[0:500]
array2 = arrays[501:1001]
array3 = arrays[1002:1502]
array4 = arrays[1503:2003]
array5 = arrays[2004:2504]
array6 = arrays[2505:3005]
array7 = arrays[3006:3506]
array8 = arrays[3507:4007]
array9 = arrays[-500:]
# print("第一批：")
# print(array1)
# print(len(array1))
#测试是否每列500个
# data = pd.read_excel("500.xlsx")
# data.insert(0, '甲', array1)
# data.insert(1, '乙', array2)
# data.insert(2, '丙', array3)
# data.insert(3, '丁', array4)
# data.insert(4, '戊', array5)
# data.insert(5, '己', array6)
# data.insert(6, '庚', array7)
# data.insert(7, '辛', array8)
# data=pd.DataFrame(data)
# data.to_excel("500.xlsx", sheet_name='Sheet1', index=False, header=True)

#从接口拉取第一批500个股票的数据
for array in array1:
    stock_dat = pro.daily(ts_code=array, start_date=begin_date, end_date=last_date)
    print(stock_dat)
    for kl_index in np.arange(1, stock_dat.shape[0]):
        # today今天的股票信息
        # yesterday 昨天的股票信息

        today = stock_dat.iloc[kl_index - 1]  # 若版本提示已经弃用 可使用loc或iloc替换
        yesterday = stock_dat.iloc[kl_index]
        yesterday = yesterday.copy()

        today = today.copy()
        print("-----")
        #print(today)

        stock_code=today['ts_code'][0:7]
        trade_day=today['trade_date']
        #print(trade_day)
        print(stock_code)
        # print('----yesterday')
        # print(yesterday)
        # 思考：成交量是昨日3-5倍以上
        Multiples = round(today.vol / yesterday.vol, 2)#交易量倍数保留2位小数
        # print(times)
        #=======================>第一个if：筛选成交量3倍的股票
        if (today['pct_chg'] > 0) and (today['close']>today['open'])and (Multiples >= 2.5):
            print('$$$$$$$$$$==  3倍  =============>')
            print(today.ts_code)
            print(today.trade_date)
            print(Multiples)

        # 使用两种方法存入数据库
        #1.符合条件的存入详细信息表中，、
            todayfor = stock_dat[stock_dat.trade_date == today.trade_date]
            yesterdayfor = stock_dat[stock_dat.trade_date == yesterday.trade_date]
            print(todayfor)
            res = todayfor.to_sql('three_times_vol_detail', engine_ts, index=False, if_exists='append', chunksize=5000)
            res = yesterdayfor.to_sql('three_times_vol_detail', engine_ts, index=False, if_exists='append', chunksize=5000)

        #2.存入3倍表中
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


        #=======================>第二个if：筛选跳空的stocks
        skip_stock_code = []
        jump_threshold = 0.05 #超过5分钱
        if (today['pct_chg'] > 0) and ((today.low - yesterday.high) > jump_threshold):
            skip_stock_code.append(today.ts_code)
            print('$$$$$$$$$$=====  跳空  ==========>')
            print(skip_stock_code)
            name=today.name

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


        #========================>第三个if：一阳三线的股票 存入数据库（sql计算5,10,20日均线速度太慢了）

        df = ts.pro_bar(ts_code=today['ts_code'], start_date='20220801', end_date=last_date, ma=[5, 10, 20, 30])
        # print(df)
        # print(df.ma5)
        lines_5=(df.ma5)[0]
        # print(lines_5)

        if(today['open']<(df.ma5)[0] and today['open']<(df.ma10)[0] and today['open']<(df.ma20)[0]and(today['close']>(df.ma5)[0] and today['close']>(df.ma10)[0] and today['close']>(df.ma20)[0])):
            sql_three_lines = "insert ignore into  break_3_lines (ts_code,trade_date,avg5) value (%s,%s,%s)"
            param = (today.ts_code, date,lines_5)

            try:
                # 执行sql语句
                cursor.execute(sql_three_lines, param)
                print("Add To Database  Success")
                # 提交到数据库执行
                connect.commit()
            except:
                # 发生错误时回滚
                connect.rollback()

            print("********************===  抓到一个 一阳三线 了!====>>> %s ===**********************"%today.ts_code)
#
#
#
#         #
#         # #查询并计算5日、10日、20日、30日均线值
#         # sqlfive =  "select avg (tt.close) avg5 ,tt.ts_code,tt.trade_date from (select t.close,t.ts_code ,t.trade_date from trade_details_2022 t where t.ts_code={} and " \
#         #            " t.trade_date<={} order by t.trade_date  desc  limit 5)as tt".format( stock_code ,trade_day)
#         # df5 = pd.read_sql_query(sqlfive, engine_ts)
#         # # print(df5)
#         # average5 = pd.DataFrame(df5)
#         # avg5= average5.get('avg5')#获取到5日均值
#         # # print('5日线值：%s'%avg5)
#         # # print(avg5)
#         # # print(type(float(avg5)))
#         # # print(type(today['open']))
#         #
#         # sql10 = "select avg (tt.close) from (select t.close from trade_details_2022 t where t.ts_code={} and " \
#         #         " t.trade_date<={} order by t.trade_date  desc  limit 10)as tt".format(stock_code ,trade_day)
#         # df10 = pd.read_sql_query(sql10, engine_ts)
#         #
#         # # print(df10)
#         # average10 = pd.DataFrame(df10)
#         # avg10=average10.get('avg (tt.close)')#获取到10日均值
#         # # print('10日线值：%s'%avg10)
#         #
#         #
#         # sql20 = "select avg (tt.close) from (select t.close from trade_details_2022 t where t.ts_code={} and " \
#         #         " t.trade_date<={} order by t.trade_date  desc  limit 20)as tt".format(stock_code ,trade_day)
#         # df20 = pd.read_sql_query(sql20, engine_ts)
#         # average20 = pd.DataFrame(df20)
#         # avg20=average20.get('avg (tt.close)')#获取到20日均值
#         # # print('20日线值：%s'%avg20)
#         #
#         #
#         # # sql30 = "select avg (tt.close) from (select t.close from trade_details_2022 t where t.ts_code={} and " \
#         # #         " t.trade_date<={} order by t.trade_date  desc  limit 30)as tt".format(stock_code ,trade_day)
#         # # df30 = pd.read_sql_query(sql30, engine_ts)
#         # # average30 = pd.DataFrame(df30)
#         # # avg30=average30.get('avg (tt.close)')#获取到30日均值
#         # # print('30日线值：%s'%avg30)
#         #
#         #
#         #
#         #
#         # if (today['open']<float(avg5) and today['open']<float(avg10) and today['open']<float(avg20))and(today['close']>float(avg5) and today['close']>float(avg10) and today['close']>float(avg20)):
#         #     res = df5.to_sql('break_3_lines', engine_ts, index=False, if_exists='append', chunksize=5000)
#         #     print("********************===  抓到一个 一阳三线 了!  ===**********************")
#
#
#time.sleep(10)#规避接口500次/min的限制

for array in array2:
    stock_dat = pro.daily(ts_code=array, start_date=begin_date, end_date=last_date)
    for kl_index in np.arange(1, stock_dat.shape[0]):
        # today今天的股票信息
        # yesterday 昨天的股票信息

        today = stock_dat.iloc[kl_index - 1]  # 若版本提示已经弃用 可使用loc或iloc替换
        yesterday = stock_dat.iloc[kl_index]
        yesterday = yesterday.copy()

        today = today.copy()
        # print("-----")
        #print(today)

        stock_code=today['ts_code'][0:7]
        trade_day=today['trade_date']
        #print(trade_day)
        print(stock_code)
        # print('----yesterday')
        # print(yesterday)
        # 思考：成交量是昨日3-5倍以上
        Multiples = round(today.vol / yesterday.vol, 2)#交易量倍数保留2位小数
        # print(times)
        #=======================>第一个if：筛选成交量3倍的股票
        if (today['pct_chg'] > 0) and (today['close']>today['open'])and (Multiples >= 2.5):
            print('$$$$$$$$$$==  3倍  =============>')
            print(today.ts_code)
            print(today.trade_date)
            print(Multiples)

        # 使用两种方法存入数据库
        #1.符合条件的存入详细信息表中，、
            todayfor = stock_dat[stock_dat.trade_date == today.trade_date]
            yesterdayfor = stock_dat[stock_dat.trade_date == yesterday.trade_date]
            print(todayfor)
            res = todayfor.to_sql('three_times_vol_detail', engine_ts, index=False, if_exists='append', chunksize=5000)
            res = yesterdayfor.to_sql('three_times_vol_detail', engine_ts, index=False, if_exists='append', chunksize=5000)

        #2.存入3倍表中
            sql_three_times = "insert into  three_times_vol (ts_code,times,date) value (%s,%s,%s)"
            param = (today.ts_code, Multiples, date)

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


        #=======================>第二个if：筛选跳空的stocks
        skip_stock_code = []
        jump_threshold = 0.05 #超过5分钱
        if (today['pct_chg'] > 0) and ((today.low - yesterday.high) > jump_threshold):
            skip_stock_code.append(today.ts_code)
            print('$$$$$$$$$$=====  跳空  ==========>')
            print(skip_stock_code)
            name=today.name

            # sql = "INSERT INTO skip_stock (ts_code) values(%s)"
            # sql2 = "INSERT INTO skip_stock values(%s,%s)"
            sql2 = "insert into skip_stock (ts_code, date) VALUES (%s, %s)"
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


        #========================>第三个if：一阳三线的股票 存入数据库（速度太慢了）

        df = ts.pro_bar(ts_code=today['ts_code'], start_date='20220801', end_date=last_date, ma=[5, 10, 20, 30])
        # print(df)
        # print(df.ma5)
        lines_5 = (df.ma5)[0]
    # print(lines_5)

        if (today['open'] < (df.ma5)[0] and today['open'] < (df.ma10)[0] and today['open'] < (df.ma20)[0] and (
            today['close'] > (df.ma5)[0] and today['close'] > (df.ma10)[0] and today['close'] > (df.ma20)[0])):
            sql_three_lines = "insert into  break_3_lines (ts_code,trade_date,avg5) value (%s,%s,%s)"
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

time.sleep(2)#规避接口500次/min的限制

for array in array3:
    stock_dat = pro.daily(ts_code=array, start_date=begin_date, end_date=last_date)
    for kl_index in np.arange(1, stock_dat.shape[0]):
        # today今天的股票信息
        # yesterday 昨天的股票信息

        today = stock_dat.iloc[kl_index - 1]  # 若版本提示已经弃用 可使用loc或iloc替换
        yesterday = stock_dat.iloc[kl_index]
        yesterday = yesterday.copy()

        today = today.copy()
        # print("-----")
        #print(today)

        stock_code=today['ts_code'][0:7]
        trade_day=today['trade_date']
        #print(trade_day)
        print(stock_code)
        # print('----yesterday')
        # print(yesterday)
        # 思考：成交量是昨日3-5倍以上
        Multiples = round(today.vol / yesterday.vol, 2)#交易量倍数保留2位小数
        # print(times)
        #=======================>第一个if：筛选成交量3倍的股票
        if (today['pct_chg'] > 0) and (today['close']>today['open'])and (Multiples >= 2.5):
            print('$$$$$$$$$$==  3倍  =============>')
            print(today.ts_code)
            print(today.trade_date)
            print(Multiples)

        # 使用两种方法存入数据库
        #1.符合条件的存入详细信息表中，、
            todayfor = stock_dat[stock_dat.trade_date == today.trade_date]
            yesterdayfor = stock_dat[stock_dat.trade_date == yesterday.trade_date]
            print(todayfor)
            res = todayfor.to_sql('three_times_vol_detail', engine_ts, index=False, if_exists='append', chunksize=5000)
            res = yesterdayfor.to_sql('three_times_vol_detail', engine_ts, index=False, if_exists='append', chunksize=5000)

        #2.存入3倍表中
            sql_three_times = "insert into  three_times_vol (ts_code,times,date) value (%s,%s,%s)"
            param = (today.ts_code, Multiples, date)

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


        #=======================>第二个if：筛选跳空的stocks
        skip_stock_code = []
        jump_threshold = 0.05 #超过5分钱
        if (today['pct_chg'] > 0) and ((today.low - yesterday.high) > jump_threshold):
            skip_stock_code.append(today.ts_code)
            print('$$$$$$$$$$=====  跳空  ==========>')
            print(skip_stock_code)
            name=today.name

            # sql = "INSERT INTO skip_stock (ts_code) values(%s)"
            # sql2 = "INSERT INTO skip_stock values(%s,%s)"
            sql2 = "insert into skip_stock (ts_code, date) VALUES (%s, %s)"
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


        #========================>第三个if：一阳三线的股票 存入数据库（速度太慢了）
        df = ts.pro_bar(ts_code=today['ts_code'], start_date='20220801', end_date=last_date, ma=[5, 10, 20, 30])
        # print(df)
        # print(df.ma5)
        lines_5 = (df.ma5)[0]
        # print(lines_5)

        if (today['open'] < (df.ma5)[0] and today['open'] < (df.ma10)[0] and today['open'] < (df.ma20)[0] and (
                today['close'] > (df.ma5)[0] and today['close'] > (df.ma10)[0] and today['close'] > (df.ma20)[0])):
            sql_three_lines = "insert into  break_3_lines (ts_code,trade_date,avg5) value (%s,%s,%s)"
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

#time.sleep(10)#规避接口500次/min的限制

for array in array4:
    stock_dat = pro.daily(ts_code=array, start_date=begin_date, end_date=last_date)
    for kl_index in np.arange(1, stock_dat.shape[0]):
        # today今天的股票信息
        # yesterday 昨天的股票信息

        today = stock_dat.iloc[kl_index - 1]  # 若版本提示已经弃用 可使用loc或iloc替换
        yesterday = stock_dat.iloc[kl_index]
        yesterday = yesterday.copy()

        today = today.copy()
        # print("-----")
        #print(today)

        stock_code=today['ts_code'][0:7]
        trade_day=today['trade_date']
        #print(trade_day)
        print(stock_code)
        # print('----yesterday')
        # print(yesterday)
        # 思考：成交量是昨日3-5倍以上
        Multiples = round(today.vol / yesterday.vol, 2)#交易量倍数保留2位小数
        # print(times)
        #=======================>第一个if：筛选成交量3倍的股票
        if (today['pct_chg'] > 0) and (today['close']>today['open'])and (Multiples >= 2.5):
            print('$$$$$$$$$$==  3倍  =============>')
            print(today.ts_code)
            print(today.trade_date)
            print(Multiples)

        # 使用两种方法存入数据库
        #1.符合条件的存入详细信息表中，、
            todayfor = stock_dat[stock_dat.trade_date == today.trade_date]
            yesterdayfor = stock_dat[stock_dat.trade_date == yesterday.trade_date]
            print(todayfor)
            res = todayfor.to_sql('three_times_vol_detail', engine_ts, index=False, if_exists='append', chunksize=5000)
            res = yesterdayfor.to_sql('three_times_vol_detail', engine_ts, index=False, if_exists='append', chunksize=5000)

        #2.存入3倍表中
            sql_three_times = "insert into  three_times_vol (ts_code,times,date) value (%s,%s,%s)"
            param = (today.ts_code, Multiples, date)

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


        #=======================>第二个if：筛选跳空的stocks
        skip_stock_code = []
        jump_threshold = 0.05 #超过5分钱
        if (today['pct_chg'] > 0) and ((today.low - yesterday.high) > jump_threshold):
            skip_stock_code.append(today.ts_code)
            print('$$$$$$$$$$=====  跳空  ==========>')
            print(skip_stock_code)
            name=today.name

            # sql = "INSERT INTO skip_stock (ts_code) values(%s)"
            # sql2 = "INSERT INTO skip_stock values(%s,%s)"
            sql2 = "insert into skip_stock (ts_code, date) VALUES (%s, %s)"
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


        #========================>第三个if：一阳三线的股票 存入数据库（速度太慢了）
        df = ts.pro_bar(ts_code=today['ts_code'], start_date='20220801', end_date=last_date, ma=[5, 10, 20, 30])
        # print(df)
        # print(df.ma5)
        lines_5=(df.ma5)[0]
        # print(lines_5)

        if(today['open']<(df.ma5)[0] and today['open']<(df.ma10)[0] and today['open']<(df.ma20)[0]and(today['close']>(df.ma5)[0] and today['close']>(df.ma10)[0] and today['close']>(df.ma20)[0])):
            sql_three_lines = "insert into  break_3_lines (ts_code,trade_date,avg5) value (%s,%s,%s)"
            param = (today.ts_code, date,lines_5)

            try:
                # 执行sql语句
                cursor.execute(sql_three_lines, param)
                print("Add To Database  Success")
                # 提交到数据库执行
                connect.commit()
            except:
                # 发生错误时回滚
                connect.rollback()

            print("********************===  抓到一个 一阳三线 了!====>>> %s ===**********************"%today.ts_code)


#time.sleep(10)#规避接口500次/min的限制

for array in array5:
    stock_dat = pro.daily(ts_code=array, start_date=begin_date, end_date=last_date)
    for kl_index in np.arange(1, stock_dat.shape[0]):
        # today今天的股票信息
        # yesterday 昨天的股票信息

        today = stock_dat.iloc[kl_index - 1]  # 若版本提示已经弃用 可使用loc或iloc替换
        yesterday = stock_dat.iloc[kl_index]
        yesterday = yesterday.copy()

        today = today.copy()
        # print("-----")
        #print(today)

        stock_code=today['ts_code'][0:7]
        trade_day=today['trade_date']
        #print(trade_day)
        print(stock_code)
        # print('----yesterday')
        # print(yesterday)
        # 思考：成交量是昨日3-5倍以上
        Multiples = round(today.vol / yesterday.vol, 2)#交易量倍数保留2位小数
        # print(times)
        #=======================>第一个if：筛选成交量3倍的股票
        if (today['pct_chg'] > 0) and (today['close']>today['open'])and (Multiples >= 2.5):
            print('$$$$$$$$$$==  3倍  =============>')
            print(today.ts_code)
            print(today.trade_date)
            print(Multiples)

        # 使用两种方法存入数据库
        #1.符合条件的存入详细信息表中，、
            todayfor = stock_dat[stock_dat.trade_date == today.trade_date]
            yesterdayfor = stock_dat[stock_dat.trade_date == yesterday.trade_date]
            print(todayfor)
            res = todayfor.to_sql('three_times_vol_detail', engine_ts, index=False, if_exists='append', chunksize=5000)
            res = yesterdayfor.to_sql('three_times_vol_detail', engine_ts, index=False, if_exists='append', chunksize=5000)

        #2.存入3倍表中
            sql_three_times = "insert into  three_times_vol (ts_code,times,date) value (%s,%s,%s)"
            param = (today.ts_code, Multiples, date)

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


        #=======================>第二个if：筛选跳空的stocks
        skip_stock_code = []
        jump_threshold = 0.05 #超过5分钱
        if (today['pct_chg'] > 0) and ((today.low - yesterday.high) > jump_threshold):
            skip_stock_code.append(today.ts_code)
            print('$$$$$$$$$$=====  跳空  ==========>')
            print(skip_stock_code)
            name=today.name

            # sql = "INSERT INTO skip_stock (ts_code) values(%s)"
            # sql2 = "INSERT INTO skip_stock values(%s,%s)"
            sql2 = "insert into skip_stock (ts_code, date) VALUES (%s, %s)"
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


        #========================>第三个if：一阳三线的股票 存入数据库（速度太慢了）


        #========================>第三个if：一阳三线的股票 存入数据库（速度太慢了）
        df = ts.pro_bar(ts_code=today['ts_code'], start_date='20220801', end_date=last_date, ma=[5, 10, 20, 30])
        # print(df)
        # print(df.ma5)
        lines_5 = (df.ma5)[0]
        # print(lines_5)

        if (today['open'] < (df.ma5)[0] and today['open'] < (df.ma10)[0] and today['open'] < (df.ma20)[0] and (
                today['close'] > (df.ma5)[0] and today['close'] > (df.ma10)[0] and today['close'] > (df.ma20)[0])):
            sql_three_lines = "insert into  break_3_lines (ts_code,trade_date,avg5) value (%s,%s,%s)"
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

#time.sleep(10)#规避接口500次/min的限制

for array in array6:
    stock_dat = pro.daily(ts_code=array, start_date=begin_date, end_date=last_date)
    for kl_index in np.arange(1, stock_dat.shape[0]):
        # today今天的股票信息
        # yesterday 昨天的股票信息

        today = stock_dat.iloc[kl_index - 1]  # 若版本提示已经弃用 可使用loc或iloc替换
        yesterday = stock_dat.iloc[kl_index]
        yesterday = yesterday.copy()

        today = today.copy()
        # print("-----")
        #print(today)

        stock_code=today['ts_code'][0:7]
        trade_day=today['trade_date']
        #print(trade_day)
        print(stock_code)
        # print('----yesterday')
        # print(yesterday)
        # 思考：成交量是昨日3-5倍以上
        Multiples = round(today.vol / yesterday.vol, 2)#交易量倍数保留2位小数
        # print(times)
        #=======================>第一个if：筛选成交量3倍的股票
        if (today['pct_chg'] > 0) and (today['close']>today['open'])and (Multiples >= 2.5):
            print('$$$$$$$$$$==  3倍  =============>')
            print(today.ts_code)
            print(today.trade_date)
            print(Multiples)

        # 使用两种方法存入数据库
        #1.符合条件的存入详细信息表中，、
            todayfor = stock_dat[stock_dat.trade_date == today.trade_date]
            yesterdayfor = stock_dat[stock_dat.trade_date == yesterday.trade_date]
            print(todayfor)
            res = todayfor.to_sql('three_times_vol_detail', engine_ts, index=False, if_exists='append', chunksize=5000)
            res = yesterdayfor.to_sql('three_times_vol_detail', engine_ts, index=False, if_exists='append', chunksize=5000)

        #2.存入3倍表中
            sql_three_times = "insert into  three_times_vol (ts_code,times,date) value (%s,%s,%s)"
            param = (today.ts_code, Multiples, date)

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


        #=======================>第二个if：筛选跳空的stocks
        skip_stock_code = []
        jump_threshold = 0.05 #超过5分钱
        if (today['pct_chg'] > 0) and ((today.low - yesterday.high) > jump_threshold):
            skip_stock_code.append(today.ts_code)
            print('$$$$$$$$$$=====  跳空  ==========>')
            print(skip_stock_code)
            name=today.name

            # sql = "INSERT INTO skip_stock (ts_code) values(%s)"
            # sql2 = "INSERT INTO skip_stock values(%s,%s)"
            sql2 = "insert into skip_stock (ts_code, date) VALUES (%s, %s)"
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


        #========================>第三个if：一阳三线的股票 存入数据库（速度太慢了）

        #========================>第三个if：一阳三线的股票 存入数据库（速度太慢了）
        df = ts.pro_bar(ts_code=today['ts_code'], start_date='20220801', end_date=last_date, ma=[5, 10, 20, 30])
        # print(df)
        # print(df.ma5)
        lines_5 = (df.ma5)[0]
        # print(lines_5)

        if (today['open'] < (df.ma5)[0] and today['open'] < (df.ma10)[0] and today['open'] < (df.ma20)[0] and (
                today['close'] > (df.ma5)[0] and today['close'] > (df.ma10)[0] and today['close'] > (df.ma20)[0])):
            sql_three_lines = "insert into  break_3_lines (ts_code,trade_date,avg5) value (%s,%s,%s)"
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

#time.sleep(10)#规避接口500次/min的限制

for array in array7:
    stock_dat = pro.daily(ts_code=array, start_date=begin_date, end_date=last_date)
    for kl_index in np.arange(1, stock_dat.shape[0]):
        # today今天的股票信息
        # yesterday 昨天的股票信息

        today = stock_dat.iloc[kl_index - 1]  # 若版本提示已经弃用 可使用loc或iloc替换
        yesterday = stock_dat.iloc[kl_index]
        yesterday = yesterday.copy()

        today = today.copy()
        # print("-----")
        #print(today)

        stock_code=today['ts_code'][0:7]
        trade_day=today['trade_date']
        #print(trade_day)
        print(stock_code)
        # print('----yesterday')
        # print(yesterday)
        # 思考：成交量是昨日3-5倍以上
        Multiples = round(today.vol / yesterday.vol, 2)#交易量倍数保留2位小数
        # print(times)
        #=======================>第一个if：筛选成交量3倍的股票
        if (today['pct_chg'] > 0) and (today['close']>today['open'])and (Multiples >= 2.5):
            print('$$$$$$$$$$==  3倍  =============>')
            print(today.ts_code)
            print(today.trade_date)
            print(Multiples)

        # 使用两种方法存入数据库
        #1.符合条件的存入详细信息表中，、
            todayfor = stock_dat[stock_dat.trade_date == today.trade_date]
            yesterdayfor = stock_dat[stock_dat.trade_date == yesterday.trade_date]
            print(todayfor)
            res = todayfor.to_sql('three_times_vol_detail', engine_ts, index=False, if_exists='append', chunksize=5000)
            res = yesterdayfor.to_sql('three_times_vol_detail', engine_ts, index=False, if_exists='append', chunksize=5000)

        #2.存入3倍表中
            sql_three_times = "insert into  three_times_vol (ts_code,times,date) value (%s,%s,%s)"
            param = (today.ts_code, Multiples, date)

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


        #=======================>第二个if：筛选跳空的stocks
        skip_stock_code = []
        jump_threshold = 0.05 #超过5分钱
        if (today['pct_chg'] > 0) and ((today.low - yesterday.high) > jump_threshold):
            skip_stock_code.append(today.ts_code)
            print('$$$$$$$$$$=====  跳空  ==========>')
            print(skip_stock_code)
            name=today.name

            # sql = "INSERT INTO skip_stock (ts_code) values(%s)"
            # sql2 = "INSERT INTO skip_stock values(%s,%s)"
            sql2 = "insert into skip_stock (ts_code, date) VALUES (%s, %s)"
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


        #========================>第三个if：一阳三线的股票 存入数据库（速度太慢了）

        #========================>第三个if：一阳三线的股票 存入数据库（速度太慢了）
        df = ts.pro_bar(ts_code=today['ts_code'], start_date='20220801', end_date=last_date, ma=[5, 10, 20, 30])
        # print(df)
        # print(df.ma5)
        lines_5 = (df.ma5)[0]
        # print(lines_5)

        if (today['open'] < (df.ma5)[0] and today['open'] < (df.ma10)[0] and today['open'] < (df.ma20)[0] and (
                today['close'] > (df.ma5)[0] and today['close'] > (df.ma10)[0] and today['close'] > (df.ma20)[0])):
            sql_three_lines = "insert into  break_3_lines (ts_code,trade_date,avg5) value (%s,%s,%s)"
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

#time.sleep(10)#规避接口500次/min的限制
for array in array8:
    stock_dat = pro.daily(ts_code=array, start_date=begin_date, end_date=last_date)
    for kl_index in np.arange(1, stock_dat.shape[0]):
        # today今天的股票信息
        # yesterday 昨天的股票信息

        today = stock_dat.iloc[kl_index - 1]  # 若版本提示已经弃用 可使用loc或iloc替换
        yesterday = stock_dat.iloc[kl_index]
        yesterday = yesterday.copy()

        today = today.copy()
        # print("-----")
        #print(today)

        stock_code=today['ts_code'][0:7]
        trade_day=today['trade_date']
        #print(trade_day)
        print(stock_code)
        # print('----yesterday')
        # print(yesterday)
        # 思考：成交量是昨日3-5倍以上
        Multiples = round(today.vol / yesterday.vol, 2)#交易量倍数保留2位小数
        # print(times)
        #=======================>第一个if：筛选成交量3倍的股票
        if (today['pct_chg'] > 0) and (today['close']>today['open'])and (Multiples >= 2.5):
            print('$$$$$$$$$$==  3倍  =============>')
            print(today.ts_code)
            print(today.trade_date)
            print(Multiples)

        # 使用两种方法存入数据库
        #1.符合条件的存入详细信息表中，、
            todayfor = stock_dat[stock_dat.trade_date == today.trade_date]
            yesterdayfor = stock_dat[stock_dat.trade_date == yesterday.trade_date]
            print(todayfor)
            res = todayfor.to_sql('three_times_vol_detail', engine_ts, index=False, if_exists='append', chunksize=5000)
            res = yesterdayfor.to_sql('three_times_vol_detail', engine_ts, index=False, if_exists='append', chunksize=5000)

        #2.存入3倍表中
            sql_three_times = "insert into  three_times_vol (ts_code,times,date) value (%s,%s,%s)"
            param = (today.ts_code, Multiples, date)

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


        #=======================>第二个if：筛选跳空的stocks
        skip_stock_code = []
        jump_threshold = 0.05 #超过5分钱
        if (today['pct_chg'] > 0) and ((today.low - yesterday.high) > jump_threshold):
            skip_stock_code.append(today.ts_code)
            print('$$$$$$$$$$=====  跳空  ==========>')
            print(skip_stock_code)
            name=today.name

            # sql = "INSERT INTO skip_stock (ts_code) values(%s)"
            # sql2 = "INSERT INTO skip_stock values(%s,%s)"
            sql2 = "insert into skip_stock (ts_code, date) VALUES (%s, %s)"
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


        #========================>第三个if：一阳三线的股票 存入数据库（速度太慢了）

        #========================>第三个if：一阳三线的股票 存入数据库（速度太慢了）
        df = ts.pro_bar(ts_code=today['ts_code'], start_date='20220801', end_date=last_date, ma=[5, 10, 20, 30])
        # print(df)
        # print(df.ma5)
        lines_5 = (df.ma5)[0]
        # print(lines_5)

        if (today['open'] < (df.ma5)[0] and today['open'] < (df.ma10)[0] and today['open'] < (df.ma20)[0] and (
                today['close'] > (df.ma5)[0] and today['close'] > (df.ma10)[0] and today['close'] > (df.ma20)[0])):
            sql_three_lines = "insert into  break_3_lines (ts_code,trade_date,avg5) value (%s,%s,%s)"
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

#time.sleep(10)#规避接口500次/min的限制

for array in array9:
    stock_dat = pro.daily(ts_code=array, start_date=begin_date, end_date=last_date)
    for kl_index in np.arange(1, stock_dat.shape[0]):
        # today今天的股票信息
        # yesterday 昨天的股票信息

        today = stock_dat.iloc[kl_index - 1]  # 若版本提示已经弃用 可使用loc或iloc替换
        yesterday = stock_dat.iloc[kl_index]
        yesterday = yesterday.copy()

        today = today.copy()
        # print("-----")
        #print(today)

        stock_code=today['ts_code'][0:7]
        trade_day=today['trade_date']
        #print(trade_day)
        print(stock_code)
        # print('----yesterday')
        # print(yesterday)
        # 思考：成交量是昨日3-5倍以上
        Multiples = round(today.vol / yesterday.vol, 2)#交易量倍数保留2位小数
        # print(times)
        #=======================>第一个if：筛选成交量3倍的股票
        if (today['pct_chg'] > 0) and (today['close']>today['open'])and (Multiples >= 2.5):
            print('$$$$$$$$$$==  3倍  =============>')
            print(today.ts_code)
            print(today.trade_date)
            print(Multiples)

        # 使用两种方法存入数据库
        #1.符合条件的存入详细信息表中，、
            todayfor = stock_dat[stock_dat.trade_date == today.trade_date]
            yesterdayfor = stock_dat[stock_dat.trade_date == yesterday.trade_date]
            print(todayfor)
            res = todayfor.to_sql('three_times_vol_detail', engine_ts, index=False, if_exists='append', chunksize=5000)
            res = yesterdayfor.to_sql('three_times_vol_detail', engine_ts, index=False, if_exists='append', chunksize=5000)

        #2.存入3倍表中
            sql_three_times = "insert into  three_times_vol (ts_code,times,date) value (%s,%s,%s)"
            param = (today.ts_code, Multiples, date)

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


        #=======================>第二个if：筛选跳空的stocks
        skip_stock_code = []
        jump_threshold = 0.05 #超过5分钱
        if (today['pct_chg'] > 0) and ((today.low - yesterday.high) > jump_threshold):
            skip_stock_code.append(today.ts_code)
            print('$$$$$$$$$$=====  跳空  ==========>')
            print(skip_stock_code)
            name=today.name

            # sql = "INSERT INTO skip_stock (ts_code) values(%s)"
            # sql2 = "INSERT INTO skip_stock values(%s,%s)"
            sql2 = "insert into skip_stock (ts_code, date) VALUES (%s, %s)"
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


        #========================>第三个if：一阳三线的股票 存入数据库（速度太慢了）

        #========================>第三个if：一阳三线的股票 存入数据库（速度太慢了）
        df = ts.pro_bar(ts_code=today['ts_code'], start_date='20220801', end_date=last_date, ma=[5, 10, 20, 30])
        # print(df)
        # print(df.ma5)
        lines_5 = (df.ma5)[0]
        # print(lines_5)

        if (today['open'] < (df.ma5)[0] and today['open'] < (df.ma10)[0] and today['open'] < (df.ma20)[0] and (
                today['close'] > (df.ma5)[0] and today['close'] > (df.ma10)[0] and today['close'] > (df.ma20)[0])):
            sql_three_lines = "insert into  break_3_lines (ts_code,trade_date,avg5) value (%s,%s,%s)"
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






connect.close()
# sdf.to_excel("allSkipStock.xlsx")
