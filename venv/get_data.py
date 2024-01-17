# -*- coding: utf-8 -*-
"""
@Time ： 2023/5/16 11:51
@Auth ： Tiger
@File ：get_data.py
@IDE ：PyCharm
@Motto:Coding is nothing
"""

import requests, json
import MySQLdb
import time


now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
date = now[0:10]


header = {  # 浏览器伪装
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36'
}
# 連漲放量
url='https://data.eastmoney.com/dataapi/xuangu/list?st=CHANGE_RATE&sr=-1&ps=150&p=1&sty=SECUCODE%2CSECURITY_CODE%2CSECURITY_NAME_ABBR%2CNEW_PRICE%2CCHANGE_RATE%2CVOLUME_RATIO%2CHIGH_PRICE%2CLOW_PRICE%2CPRE_CLOSE_PRICE%2CVOLUME%2CDEAL_AMOUNT%2CTURNOVERRATE%2CUPPER_LARGE_VOLUME&filter=(UPPER_LARGE_VOLUME%3D%221%22)&source=SELECT_SECURITIES&client=WEB'

response= requests.get(url, headers=header)
# print(response.content)
json_data= response.json()
print(json_data['result']['data'])
stock_info=json_data['result']['data']
print(len(stock_info))

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


    except MySQLdb.Error as e :
        print("Mysql Error %d: %s" % (e.args[0], e.args[1]))


if __name__ == '__main__':
    for stock in stock_info:
        # print(stock['SECURITY_NAME_ABBR'])
        dict = {}
        list = []
        dict['ts_code'] = stock['SECURITY_CODE']
        dict['name'] = stock['SECURITY_NAME_ABBR']
        dict['tv_rate'] = stock['TURNOVERRATE']
        dict['v_ratio'] = stock['VOLUME_RATIO']

        dict['date'] = date

        InsertData("high_pv_Stock", dict)

    delete_sql = "delete  from high_pv_Stock where ts_code like '68%' "
    delete_8 = "delete  from high_pv_Stock where ts_code like '8%'"

    try:
        cur.execute(delete_sql)
        cur.execute(delete_8)
        conn.commit()
    except MySQLdb.Error as error:
        print("Error:{}".format(error))
        # 发生错误时回滚
        conn.rollback()

    cur.close()
    conn.close()



    # day_3 = json_data_3['data']['diff']












