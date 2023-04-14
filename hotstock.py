# -*- coding: utf-8 -*-
"""
@Time ： 2022/12/9 12:59
@Auth ： Tiger
@File ：hotstock.py
@IDE ：PyCharm
@Motto:Build My Dream
"""
import time

import MySQLdb
import requests
import  json
# from spider import InsertData
headers={'Content-Type': 'application/json',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36'
}
# data={"question":"个股热度","perpage":50,"page":1,"secondary_intent":"stock","log_info":"{\"input_type\":\"typewrite\"}","source":"Ths_iwencai_Xuangu","version":"2.0","query_area":"","block_list":"","add_info":"{\"urp\":{\"scene\":1,\"company\":1,\"business\":1},\"contentType\":\"json\",\"searchInfo\":true}","rsh":"Ths_iwencai_Xuangu_yl3bd25h5xtdfl0n41crs4grbkqg23pr"}
url="https://xueqiu.com/service/screener/screen?category=CN&exchange=sh_sz&areacode=&indcode=&order_by=follow7d&order=desc&page=1&size=50&only_count=0&current=&pct=&follow7d=0_50000&follow7dpct=0_49900"
res =requests.get(url, headers=headers)
# print(res.content)
# content=res.content
data=json.loads(res.content)
# print(data)
print(data['data']['list'])
stocks=data['data']['list']

conn = MySQLdb.connect(host='localhost', user='root', passwd='root', db='test', port=3306)  # 链接数据库
cur = conn.cursor()

def InsertData(TableName, dict):
    try:

        COLstr = ''  # 列的字段
        ROWstr = ''  # 行字段

        ColumnStyle = ' VARCHAR(20)'
        for key in dict.keys():
            COLstr = COLstr + ' ' + key + ColumnStyle + ','
            ROWstr = (ROWstr + '"%s"' + ',') % (dict[key])

        # 判断表是否存在，存在执行try，不存在执行except新建表，再insert
        try:
            # cur.execute("SELECT * FROM  %s" % (TableName))
            cur.execute("INSERT INTO %s VALUES (%s)" % (TableName, ROWstr[:-1]))

        except:
            cur.execute("CREATE TABLE %s (%s)" % (TableName, COLstr[:-1]))
            cur.execute("INSERT INTO %s VALUES (%s)" % (TableName, ROWstr[:-1]))
        conn.commit()


    except:
        print("error")


now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
date = now[0:10]
print( date)


for stock in stocks:
    dict = {}
    list = []
    dict['ts_code']=stock['symbol']
    dict['name'] = stock['name']
    dict['date_exchange']=stock['pct']
    dict['price']=stock['current']
    dict['follow7d']=stock['follow7d']
    dict['follow7dpct']=stock['follow7dpct']
    dict['date']=date

    print(stock['name'])
    InsertData("hot_Stocks",dict)

cur.close()
conn.close()

