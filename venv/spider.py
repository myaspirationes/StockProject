# -*- coding: utf-8 -*-
"""
@Time ： 2022/11/11 18:58
@Auth ： Tiger
@File ：spider.py
@IDE ：PyCharm
@Motto:Build My Dream
"""
import requests
import MySQLdb
import  time

now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
date = now[0:9]


# 三日涨幅前50
url_3_days=f'https://push2.eastmoney.com/api/qt/clist/get?fid=f127&po=1&pz=50&pn=1&np=1&fltt=2&invt=2&ut=b2884a393a59ad64002292a3e90d46a5=&fs=m:0+t:6+f:!2,m:0+t:13+f:!2,m:0+t:80+f:!2,m:1+t:2+f:!2,m:1+t:23+f:!2,m:0+t:7+f:!2,m:1+t:3+f:!2&fields=f12,f14,f2,f127'
# 五日涨幅前50
url_5_days=f'https://push2.eastmoney.com/api/qt/clist/get?fid=f109&po=1&pz=50&pn=1&np=1&fltt=2&invt=2&ut=b2884a393a59ad64002292a3e90d46a5&fs=m:0+t:6+f:!2,m:0+t:13+f:!2,m:0+t:80+f:!2,m:1+t:2+f:!2,m:1+t:23+f:!2,m:0+t:7+f:!2,m:1+t:3+f:!2&fields=f12,f14,f2,f109'
url_10_days=f'https://push2.eastmoney.com/api/qt/clist/get?fid=f160&po=1&pz=50&pn=1&np=1&fltt=2&invt=2&ut=b2884a393a59ad64002292a3e90d46a5&fs=m:0+t:6+f:!2,m:0+t:13+f:!2,m:0+t:80+f:!2,m:1+t:2+f:!2,m:1+t:23+f:!2,m:0+t:7+f:!2,m:1+t:3+f:!2&fields=f12,f14,f2,f160'
header={# 浏览器伪装
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36'
}
response_3_days=requests.get(url_3_days,headers=header)
# print(response.content)
json_data_3 = response_3_days.json()
# print(json_data['data']['diff'])
day_3=json_data_3['data']['diff']


response_5_days=requests.get(url_5_days,headers=header)
# print(response.content)
json_data_5 = response_5_days.json()
# print(json_data['data']['diff'])
day_5=json_data_5['data']['diff']


response_10_days=requests.get(url_10_days,headers=header)
# print(response.content)
json_data_10 = response_10_days.json()
# print(json_data['data']['diff'])
day_10=json_data_10['data']['diff']


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
        list=[]
        dict['today_price']=i['f2']
        dict['ts_code']=i['f12']
        dict['name']=i['f14']
        dict['change_3_days']=i['f127']
        dict['date']=date


        InsertData("change_three_days",dict)
    for i in day_5:
        dict = {}
        list=[]
        dict['today_price']=i['f2']
        dict['ts_code']=i['f12']
        dict['name']=i['f14']
        dict['change_5_days']=i['f109']
        dict['date']=date
        InsertData("change_five_days",dict)
    for i in day_10:
        dict = {}
        list=[]
        dict['today_price']=i['f2']
        dict['ts_code']=i['f12']
        dict['name']=i['f14']
        dict['change_10_days']=i['f160']
        dict['date']=date
        InsertData("change_ten_days",dict)

    cur.close()
    conn.close()




