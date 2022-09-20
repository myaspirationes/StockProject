import requests
import tushare
import  time
import openpyxl


print((time.time()*1000))
t=int(time.time()*1000)
tss=str(t)
print(tushare.__version__)
#https://xueqiu.com/service/screener/screen?category=CN&exchange=sh_sz&areacode=&indcode=&order_by=symbol&order=desc&page=1&size=30&only_count=0&current=&pct=3_15&chgpct=3_10&pct_current_year=-67.34_577.96&mc=103309550_2317421139462&fmc=25076621_2317421139462&_=1662726491205
url = f'https://xueqiu.com/service/screener/screen?category=CN&exchange=sh_sz&areacode=&indcode=&order_by=symbol&order=desc&page=1&size=150&only_count=0&current=&pct=3_15&chgpct=3_10&pct_current_year=-67.34_577.96&mc=103309550_2317421139462&fmc=25076621_2317421139462&amount=0_5523516959.15&volume=0_857274007&tr=0_70.17&_='+tss
# 伪装
1662727329985
1662727477808
headers = {
    # 浏览器伪装
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36'
}
response = requests.get(url, headers=headers)
print(response.content)
json_data = response.json()
print(json_data)

data_list = json_data['data']['list']
for i in data_list:
  dit = {}
  dit['股票代码'] = i['symbol']
  dit['股票名字'] = i['name']
  dit['当前价'] = i['current']
  dit['当日振幅'] = i['chgpct']
  dit['流通市值'] = i['fmc']
  dit['总市值'] = i['mc']
  dit['当日成交量'] = i['volume']
  dit['当日成交额'] = i['amount']
  #dit['涨跌额'] = i['chg']

  dit['涨跌幅/%'] = i['pct']
  dit['年初至今/%'] = i['pct_current_year']
  dit['成交量'] = i['volume']
  dit['成交额'] = i['amount']
  dit['换手率/%'] = i['tr']
  #dit['成交额/流通值'] =(i['tr']i['fmc'])
  #dit['市盈率TTM'] = i['pe_ttm']
  #dit['股息率/%'] = i['dividend_yield']
  #dit['市值'] = i['market_capital']
  print(dit)
  
  