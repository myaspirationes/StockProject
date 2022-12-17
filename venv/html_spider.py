# -*- coding: utf-8 -*-
"""
@Time ： 2022/11/23 11:52
@Auth ： Tiger
@File ：html_spider.py
@IDE ：PyCharm
@Motto:Build My Dream
"""

from bs4 import BeautifulSoup  # 网页解析
import os.path  # 文件操作
import urllib.request, urllib.error  # URL操作，获取网页数据

from requests_html import HTMLSession

import MySQLdb

price_list = []
connect = MySQLdb.connect(host='localhost', user='root', passwd='root', db='web_django', port=3306)
cur = connect.cursor()

# sql_delete="delete from web_django.sustained_higher_price where 1=1 "
# cur.execute(sql_delete)

session_for_volum = HTMLSession()
session_for_price = HTMLSession()
session_for_volum.encoding = 'utf-8'
session_for_price.encoding = 'utf-8'
sustained_higher_volum= session_for_volum.get('http://data.10jqka.com.cn/rank/cxfl/')
sustained_higher_price = session_for_price.get('http://data.10jqka.com.cn/rank/lxsz/')

sustained_higher_price.html.render()
sustained_higher_volum.html.render()

price_val = sustained_higher_price.html.find("tr")
# print(price_val)
for row in price_val:
    price_data = row.text
    price_list.append(price_data)
for i in range(2, len(price_list) - 1):
    price_cell = price_list[i]
    # print(type(price_cell))
    price_data = price_cell.split()
    ts_code = price_data[1]
    name = price_data[2]
    sustain_days = price_data[6]
    change = price_data[7]
    turnover_rate = price_data[8]
    industry = price_data[9]
    print(industry)

    try:


        sql = "INSERT INTO web_django.sustained_higher_price (name, ts_code, `change`, sustain_days, turnover_rate, industry, insert_time) VALUES(%s, %s, %s, %s, %s, %s, CURRENT_TIMESTAMP);"
        param = (name,ts_code,  sustain_days, change, turnover_rate, industry)
        cur.execute(sql, param)
        #             print("add success")

        connect.commit()
    except:
        connect.rollback()
    # print(price_data)

# print(price_list)
# # 获取表头
# q = sustained_higher_volum.html.find("th")
# list=[]
# tr_list=[]
# for item in q:
#     data=item.text
#     list.append(data)
#
# # print(list)
tbody_val = sustained_higher_volum.html.find("tr")
# for dd in tbody_val:
#     tr_data=dd.text
#     tr_list.append(tr_data)
#     for i in range (0,len(tr_list)-1):
#         td_data=tr_list[i]
#         datalist=tr_data.split()
#         print(datalist[1])


#
#
# # 空的列表用于加入新的数据
# tbody_id = []
# # e=[]
for tr in tbody_val:
    cols = tr.find('td')
    # 迭代cols中的元素，使用strip()方法剥离出每个元素的text
    col = [content.text.strip() for content in cols]
    print(col)
    try:
        ts_code = col[1]
        name = col[2]
        benchmark_volum_date = col[6]
        sustain_days = col[7]
        price_change = col[8]
        industry = col[9]
        print(industry)

        try:


            sql = "INSERT INTO sustained_higher_volum (name, ts_code, benchmark_volum_date, sustain_days, price_change, industry,insert_time) VALUES(%s, %s, %s, %s, %s, %s,CURRENT_TIMESTAMP)"
            param = (name, ts_code, benchmark_volum_date, sustain_days, price_change, industry)

            cur.execute(sql, param)
            print("add success")

            connect.commit()
        except:
            connect.rollback()



    except:
        pass

cur.close()
connect.close()
