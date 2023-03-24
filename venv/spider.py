# -*- coding: utf-8 -*-
"""
@Time ： 2022/11/11 18:58
@Auth ： Tiger
@File ：spider.py
@IDE ：PyCharm
@Motto:Build My Dream
"""
import requests, json
import MySQLdb
import time

header = {  # 浏览器伪装
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36'
}

# 三日涨幅前50
url_3_days = f'https://push2.eastmoney.com/api/qt/clist/get?fid=f127&po=1&pz=50&pn=1&np=1&fltt=2&invt=2&ut=b2884a393a59ad64002292a3e90d46a5=&fs=m:0+t:6+f:!2,m:0+t:13+f:!2,m:0+t:80+f:!2,m:1+t:2+f:!2,m:1+t:23+f:!2,m:0+t:7+f:!2,m:1+t:3+f:!2&fields=f12,f14,f2,f127'
# 五日涨幅前50
url_5_days = f'https://push2.eastmoney.com/api/qt/clist/get?fid=f109&po=1&pz=50&pn=1&np=1&fltt=2&invt=2&ut=b2884a393a59ad64002292a3e90d46a5&fs=m:0+t:6+f:!2,m:0+t:13+f:!2,m:0+t:80+f:!2,m:1+t:2+f:!2,m:1+t:23+f:!2,m:0+t:7+f:!2,m:1+t:3+f:!2&fields=f12,f14,f2,f109'
# 十日涨幅前50
url_10_days = f'https://push2.eastmoney.com/api/qt/clist/get?fid=f160&po=1&pz=50&pn=1&np=1&fltt=2&invt=2&ut=b2884a393a59ad64002292a3e90d46a5&fs=m:0+t:6+f:!2,m:0+t:13+f:!2,m:0+t:80+f:!2,m:1+t:2+f:!2,m:1+t:23+f:!2,m:0+t:7+f:!2,m:1+t:3+f:!2&fields=f12,f14,f2,f160'
# 人气50
url_50_hot = "https://data.eastmoney.com/dataapi/xuangu/list?st=CHANGE_RATE&sr=-1&ps=50&p=1&sty=SECUCODE%2CSECURITY_CODE%2CSECURITY_NAME_ABBR%2CNEW_PRICE%2CCHANGE_RATE%2CVOLUME_RATIO%2CHIGH_PRICE%2CLOW_PRICE%2CPRE_CLOSE_PRICE%2CVOLUME%2CDEAL_AMOUNT%2CTURNOVERRATE%2CPOPULARITY_RANK&filter=(POPULARITY_RANK%3E0)(POPULARITY_RANK%3C%3D50)&source=SELECT_SECURITIES&client=WEB"

response_3_days = requests.get(url_3_days, headers=header)
# print(response_3_days.content)
json_data_3 = response_3_days.json()
# print(json_data_3['data']['diff'])
day_3 = json_data_3['data']['diff']

response_5_days = requests.get(url_5_days, headers=header)
json_data_5 = response_5_days.json()
day_5 = json_data_5['data']['diff']

response_10_days = requests.get(url_10_days, headers=header)
json_data_10 = response_10_days.json()
day_10 = json_data_10['data']['diff']

response_50_hot = requests.get(url_50_hot, headers=header)
json_hotdata_50 = json.loads(response_50_hot.content)
stock_list = json_hotdata_50['result']['data']
print(stock_list)

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


if __name__ == '__main__':
    now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    date = now[0:10]
    for i in day_3:
        dict = {}
        list = []
        dict['today_price'] = i['f2']
        dict['ts_code'] = i['f12']
        dict['name'] = i['f14']
        dict['change_3_days'] = i['f127']
        dict['date'] = date
        try:
            InsertData("change_three_days", dict)
            print("change_three _days ,add succes ")
        except:
            print("faild to add data  in  change_3_days")

    for i in day_5:
        dict = {}
        list = []
        dict['today_price'] = i['f2']
        dict['ts_code'] = i['f12']
        dict['name'] = i['f14']
        dict['change_5_days'] = i['f109']
        dict['date'] = date
        try:
            InsertData("change_five_days", dict)
            print("change_five_days,add success")
        except:
            print("faild to add data  in  change_5_days")
    for i in day_10:
        dict = {}
        list = []
        dict['today_price'] = i['f2']
        dict['ts_code'] = i['f12']
        dict['name'] = i['f14']
        dict['change_10_days'] = i['f160']
        dict['date'] = date

        try:
            InsertData("change_ten_days", dict)

            print("change_ten_days, add success")
        except:
            print("faild to add data  in  change_10_days")
    '''
    {'SECUCODE': '300359.SZ', 'SECURITY_CODE': '300359', 'SECURITY_NAME_ABBR': '全通教育', 'NEW_PRICE': 8.1,
     'CHANGE_RATE': 20, 'VOLUME_RATIO': 1.95, 'HIGH_PRICE': 8.1, 'LOW_PRICE': 6.59, 'PRE_CLOSE_PRICE': 6.75,
     'VOLUME': 1144869, 'DEAL_AMOUNT': 859250774.72, 'TURNOVERRATE': 18.08, 'POPULARITY_RANK': 21,
     'MAX_TRADE_DATE': '2022-12-23'}
    '''

    for stock in stock_list:
        dict = {}
        list = []
        dict['ts_code'] = stock['SECURITY_CODE']
        dict['name'] = stock['SECURITY_NAME_ABBR']
        dict['date'] = stock['MAX_TRADE_DATE']
        dict['trunover_rate'] = stock['TURNOVERRATE']
        dict['high'] = stock['HIGH_PRICE']
        dict['close_price'] = stock['NEW_PRICE']
        dict['pre_close'] = stock['PRE_CLOSE_PRICE']
        dict['change_rate'] = stock['CHANGE_RATE']
        dict['popularity_rate'] = stock['POPULARITY_RANK']
        try:
            InsertData("ths_50_hot", dict)
            print("ths_50_hot,add success")
        except:
            print("faild to add data in ths_50_hot")

    cur.close()
    conn.close()
