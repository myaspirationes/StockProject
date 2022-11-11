import requests
# import tushare
import  time
import openpyxl
import MySQLdb
from sqlalchemy import create_engine

# 获取时间戳 timestamp
t=int(time.time()*1000)
tss=str(t)
#https://xueqiu.com/service/screener/screen?category=CN&exchange=sh_sz&areacode=&indcode=&order_by=symbol&order=desc&page=1&size=30&only_count=0&current=&pct=3_15&chgpct=3_10&pct_current_year=-67.34_577.96&mc=103309550_2317421139462&fmc=25076621_2317421139462&_=1662726491205
url = f'https://xueqiu.com/service/screener/screen?category=CN&exchange=sh_sz&areacode=&indcode=&order_by=symbol&order=desc&page=1&size=5000&only_count=0&current=&pct=-10_20&chgpct=1_20&pct_current_year=-67.34_577.96&mc=103309550_2317421139462&fmc=25076621_2317421139462&amount=0_5523516959.15&volume=0_857274007&tr=0_70.17&_='+tss
# # 伪装
# 1662727329985
# 1662727477808
headers = {
    # 浏览器伪装
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36'
}
response = requests.get(url, headers=headers)
#print(response.content)
json_data = response.json()
# print(json_data)

data_list = json_data['data']['list']

conn = MySQLdb.connect(host='localhost', user='root', passwd='root', db='test', port=3306)  # 链接数据库
cur = conn.cursor()

def InsertData(TableName, dic):
    try:

        COLstr = ''  # 列的字段
        ROWstr = ''  # 行字段

        ColumnStyle = ' VARCHAR(20)'
        for key in dic.keys():
            COLstr = COLstr + ' ' + key + ColumnStyle + ','
            ROWstr = (ROWstr + '"%s"' + ',') % (dic[key])

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
    # dic = {'股票代码': 'SZ301318', '股票名字': '维海德', '当前价': 50.89, '当日振幅': 9.74, '流通市值': 837723496, '总市值': 3532376680, '当日成交量': 2659468, '当日成交额': 133216430.89, '涨跌幅/%': 6.13, '年初至今/%': -20.51, '成交量': 2659468, '成交额': 133216430.89, '换手率/%': 16.16}
    for i in data_list:
        dit = {}
        list = []

        dit['股票代码'] = i['symbol']
        dit['股票名字'] = i['name']
        dit['当前价'] = i['current']
        dit['当日振幅'] = i['chgpct']
        dit['流通市值'] = i['fmc']
        dit['总市值'] = i['mc']
        dit['当日成交量'] = i['volume']
        dit['当日成交额'] = i['amount']
        # dit['涨跌额'] = i['chg']

        dit['涨跌幅/%'] = i['pct']
        dit['年初至今/%'] = i['pct_current_year']
        dit['成交量'] = i['volume']
        dit['成交额'] = i['amount']
        dit['换手率/%'] = i['tr']
        # dit['成交额/流通值'] =(i['tr']i['fmc'])
        # dit['市盈率TTM'] = i['pe_ttm']
        # dit['股息率/%'] = i['dividend_yield']
        # dit['市值'] = i['market_capital']

        # print(dit)
        InsertData('xueqiu_stockinfo', dit)

    cur.close()
    conn.close()





  

  



