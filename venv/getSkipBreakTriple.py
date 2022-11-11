import tushare as ts
import mplfinance as mpf
import pandas as pd
import numpy as np
import MySQLdb
from sqlalchemy import create_engine
import time,copy
import datetime

# pro = ts.pro_api('a0045b3469b1b145fb57a7b97467a49fd7deecdd299c21b6d9a5f64a',33)# 备用token ，防止接口调用次数用完
pro = ts.pro_api('4ddd47790cce532bde92ebdd220de5116d99b7155386f37dbabb7228',50)
now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
date = now[0:10]  # 获得查询日期用于插入数据库
print("今天的日期：{}. 开始时间：{}".format(date,now))


# 设置开始和结束时间
now_time = datetime.datetime.now()
last_date = now_time.strftime("%Y%m%d")
begin_date = (now_time + datetime.timedelta(days=-10)).strftime("%Y%m%d")  # 十天之内必有交易日

trade_cal = pro.trade_cal(exchange='', start_date=begin_date, end_date=last_date)#获取最近十天中的交易日
#print(trade_cal)
pre_tradeday=trade_cal['pretrade_date']#前一个交易日，字典集合
# print(pre_tradeday)
latest_tradeday=pre_tradeday[10]#字典中取值，最近的前一个交易日


# last_tradeday=pre_tradeday[9]
# print(latest_tradeday)
# print(last_tradeday)


#begin_date = (now_time + datetime.timedelta(days=-1)).strftime("%Y%m%d")  # 获取前一天，这里有一个bug，交易日不一定是昨天

# 链接数据库方法一：
connect = MySQLdb.connect("localhost", "root", "root", "test", charset='utf8')
cursor = connect.cursor()
# 链接数据库方法二：
engine_ts = create_engine('mysql://root:root@127.0.0.1:3306/test?charset=utf8&use_unicode=1')
# ts.set_token('a0045b3469b1b145fb57a7b97467a49fd7deecdd299c21b6d9a5f64a')
ts.set_token('4ddd47790cce532bde92ebdd220de5116d99b7155386f37dbabb7228')

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

arrays = get_codes.keys()
arrays = list(arrays)
#arrays=arrays[::-1]# 哈哈 ，一次网络异常终止，造成后面1300个没有处理，如是倒序来取值调接口一次
#arrays=arrays[250:]# 哈哈 ，一次网络异常终止，造成后面1300个没有处理，如是倒序来取值调接口一次
# print(len(arrays))  #长度是 ：4296

# time.sleep(1)
i = 0
# print(i)
for array in arrays:
    stock_dat = pro.daily(ts_code=array, start_date=latest_tradeday, end_date=last_date)#start_date 是前一个交易日，不一定是自然日
    i = i + 1
    #print('已调用接口次数：%s'%i)
    # print(stock_dat)

    if (i % 500 == 0):
        number=i//500
        print('已调用接口第 %s 个500次了，让tushare的接口踹口气~~~~~~~~~~~~~~~~~~'%number)
        time.sleep(10)
        print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    #print(stock_dat.shape[0])
    for kl_index in np.arange(1, stock_dat.shape[0]):
        # today今天的股票信息
        # yesterday 昨天的股票信息

        today = stock_dat.iloc[kl_index - 1]  # 若版本提示已经弃用 可使用loc或iloc替换
        yesterday = stock_dat.iloc[kl_index]
        yesterday = yesterday.copy()

        today = today.copy()
        # print(today)

        stock_code = today['ts_code'][0:9]
        # print(stock_code)

        # last_2w = stock_code[-2:]
        # # print(last_2w)
        # pre_6w = stock_code[0:6]
        # # print(pre_6w)
        # stock_code = last_2w + pre_6w



        trade_day = today['trade_date']
        # print(trade_day)
        print(stock_code)
        # print(yesterday)
        # 思考：成交量是昨日3-5倍以上
        Multiples = round(today.vol / yesterday.vol, 2)  # 交易量倍数保留2位小数
        # print(times)
        # =======================>第一个if：筛选成交量3倍的股票
        if (today['pct_chg'] > 0) and (today['close'] > today['open']) and (Multiples >= 2.5):
            print('$$$$$$$$$$==  3倍  =============>')
            # print(today.ts_code)
            # print(today.trade_date)
            # print(Multiples)
            # print("stock code: {}  , trade date is: {}, multiples is {}" .format(stock_code,today.trade_date,Multiples))

            # 使用两种方法存入数据库
            # 1.符合条件的存入详细信息表中，、
            todayfor = stock_dat[stock_dat.trade_date == today.trade_date]
            yesterdayfor = stock_dat[stock_dat.trade_date == yesterday.trade_date]
            print(todayfor)
            # print(type(todayfor))

            res = todayfor.to_sql('three_times_vol_detail', engine_ts, index=False, if_exists='append', chunksize=5000)
            res = yesterdayfor.to_sql('three_times_vol_detail', engine_ts, index=False, if_exists='append',
                                      chunksize=5000)

            # 2.存入3倍表中
            last_2w = stock_code[-2:]
            # print(last_2w)
            pre_6w = stock_code[0:6]
            # print(pre_6w)
            tri_stock_code = last_2w + pre_6w #格式sh600600 或者sz300300
            print(tri_stock_code)

            sql_three_times = "insert ignore into  three_times_vol (ts_code,times,date) value (%s,%s,%s)"
            param = (tri_stock_code, Multiples, date)

            try:
                cursor.execute(sql_three_times, param)
                print("Three Times  Stock Add To Database  Success")
                connect.commit()
            except:
                connect.rollback()
        #
        # =======================>第二个if：筛选跳空的stocks
        skip_stock_code = []
        jump_threshold = 0.01  # 超过1分钱
        if (today['pct_chg'] > 0) and ((today.low - yesterday.high) > jump_threshold):
            deep_stock_code=copy.deepcopy(stock_code)
            last_2w = deep_stock_code[-2:]
            # print(last_2w)
            pre_6w = deep_stock_code[0:6]
            # print(pre_6w)
            stock_code_skip = last_2w + pre_6w  # 格式sh600600 或者sz300300



            skip_stock_code.append(stock_code_skip)
            print('$$$$$$$$$$=====  跳空  ==========>')
            print(skip_stock_code)
            # name = today.name

            # sql = "INSERT INTO skip_stock (ts_code) values(%s)"
            # sql2 = "INSERT INTO skip_stock values(%s,%s)"
            sql2 = "insert ignore into skip_stock (ts_code, date,today_low,pre_high,pct_chg) VALUES (%s,%s, %s, %s, %s)"
            val = (skip_stock_code, date,today.low,yesterday.high,today.pct_chg)

            try:
                cursor.execute(sql2, val)
                print("add success")
                connect.commit()                 # 提交到数据库执行
            except:
                connect.rollback()                  # 发生错误时回滚


        # ========================>第三个if：一阳三线的股票 存入数据库（sql计算5,10,20日均线速度太慢了）

        df = ts.pro_bar(ts_code=today['ts_code'], start_date='20220901', end_date=last_date, ma=[5, 10, 20, 30])
        # print(df.ma5)          #所有的五日线值
        #lines_5 = (df.ma5)[0]   #五日线值

        if (today['open'] < (df.ma5)[0] and today['open'] < (df.ma10)[0] and today['open'] < (df.ma20)[0] and (
                today['close'] > (df.ma5)[0] and today['close'] > (df.ma10)[0] and today['close'] > (df.ma20)[0])):

            deep_stock_code2 = copy.deepcopy(stock_code)
            last_2w = deep_stock_code2[-2:]
            # print(last_2w)
            pre_6w = deep_stock_code2[0:6]
            # print(pre_6w)
            stock_code_3lines = last_2w + pre_6w  # 格式sh600600 或者sz300300
            print(stock_code_3lines)

            sql_three_lines = "insert ignore into  break_3_lines (ts_code,trade_date,avg5) value (%s,%s,%s)"
            param = (stock_code_3lines, date, (df.ma5)[0])

            try:
                cursor.execute(sql_three_lines, param)                 # 执行sql语句
                print("Add To Database  Success")
                connect.commit()                  # 提交到数据库执行
            except:
                connect.rollback()                 # 发生错误时回滚

            print("********************===  抓到一个 一阳三线 了!====>>> %s ===**********************" % today.ts_code)



#
#
# sql_dual_triple="insert ignore into test.dual_three (dual_three.ts_code,`date`,times,name) select break_3_lines.ts_code, three_times_vol.`date`, three_times_vol.`times`, stock_basic.name from break_3_lines, stock_basic, three_times_vol where break_3_lines.ts_code = stock_basic.ts_code and break_3_lines.ts_code = three_times_vol.ts_code and three_times_vol.`date`=break_3_lines.trade_date"
# sql_skip_triple="insert ignore into test.skip_triple (skip_triple.ts_code,`date`,name) select skip_stock.ts_code, three_times_vol.`date`, stock_basic.name from skip_stock, stock_basic, three_times_vol where skip_stock.ts_code = stock_basic.ts_code and skip_stock.ts_code = three_times_vol.ts_code and skip_stock.`date`=three_times_vol.`date`"
# sql_skip_times_lines="insert ignore into test.skip_times_lines (skip_times_lines.`date`,name,ts_code) select dual_three.`date` , dual_three.name , skip_triple.ts_code from dual_three , skip_triple where dual_three.`date` = skip_triple.`date` and dual_three.ts_code = skip_triple.ts_code"
#
#



cursor.close()
connect.close()

#

