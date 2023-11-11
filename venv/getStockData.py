import requests
# import tushare
import  time,datetime
import openpyxl
import MySQLdb
from sqlalchemy import create_engine




conn = MySQLdb.connect(host='localhost', user='root', passwd='root', db='test', port=3306)  # 链接数据库
cur = conn.cursor()
# 获取时间戳 timestamp

#https://xueqiu.com/service/screener/screen?category=CN&exchange=sh_sz&areacode=&indcode=&order_by=symbol&order=desc&page=1&size=30&only_count=0&current=&pct=3_15&chgpct=3_10&pct_current_year=-67.34_577.96&mc=103309550_2317421139462&fmc=25076621_2317421139462&_=1662726491205
# url = f'https://xueqiu.com/service/screener/screen?category=CN&exchange=sh_sz&areacode=&indcode=&order_by=symbol&order=desc&page=1&size=5000&only_count=0&current=&pct=-10_20&chgpct=1_20&pct_current_year=-67.34_577.96&mc=103309550_2317421139462&fmc=25076621_2317421139462&amount=0_5523516959.15&volume=0_857274007&tr=0_70.17&_='+tss
# url = f'https://stock.xueqiu.com/v5/stock/screener/quote/list.json?page=1&size=5019&order=desc&orderby=code&order_by=symbol&market=CN&type=sh_sz'
# # 伪装
# https://xueqiu.com/service/screener/screen?category=CN&exchange=sh_sz&areacode=&indcode=&order_by=symbol&order=desc&page=1&size=30&only_count=0&current=&pct=3_15&chgpct=3_10&pct_current_year=-67.34_577.96&mc=103309550_2317421139462&fmc=25076621_2317421139462&_=1662726491205


def get_web_data(page_number):
    data_list_all = []
    t = int(time.time() * 1000)
    tss = str(t)
    headers = {
        # 浏览器伪装
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36',
        # 'cookie': 's=by1260v9g1; device_id=02a63e1623b278ea03ee553f73eff1de; _ga=GA1.2.1457744673.1667647235; bid=82e905d9bf5243f721705a93f8473182_lacbo8g6; xq_is_login=1; u=7849836942; xq_a_token=a0c918ef7cb2ccdd88e22ea9e453e724fc1ad1bf; xqat=a0c918ef7cb2ccdd88e22ea9e453e724fc1ad1bf; xq_id_token=eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJ1aWQiOjc4NDk4MzY5NDIsImlzcyI6InVjIiwiZXhwIjoxNjgwODQ5OTEwLCJjdG0iOjE2NzgyNTc5MTA4MjEsImNpZCI6ImQ5ZDBuNEFadXAifQ.Aa9R0bm6YUggEiYJ11qNnloPo2kTITmY2sbKqBosbxi_B2qUmyw--c4HMAbplhNfqnAbbcEZZAm5LJUBp6Ad2MYCLgxRjankirN-yJj99SFci2tNjavCC2z6D6sqsNZsOurkz02ZJg10ih259Z_ahBeobWCnXGD4mGc1UnkmI6wnEVYBmH14egtWbM8ZGtrIWXPBz2Hw8Y9eLlkPhDgF7DCXPbAWi869WYmsch2uhOrWSXMIY_chrTQFdtLdxGMfy8CVQSXQXFXRbGv2Np6WCgHZASLuWW2LvwZbOh5hs3eDUxJ3JaZn3Wmam6DmNTGCGOs_AYXW9FQ9pfyuYuTpvw; xq_r_token=23a5a32fcc2c0b9462bd35ac4d2e5624fec2c9bf; Hm_lvt_1db88642e346389874251b5a1eded6e3=1677554272,1677718964,1678065068,1678257912; snbim_minify=true; is_overseas=0; Hm_lpvt_1db88642e346389874251b5a1eded6e3=1678289711'
        'cookie':'s=by1260v9g1; device_id=02a63e1623b278ea03ee553f73eff1de; __utmz=1.1667647235.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); _ga=GA1.2.1457744673.1667647235; bid=82e905d9bf5243f721705a93f8473182_lacbo8g6; xq_is_login=1; u=7849836942; xq_a_token=2182a2544e6935519a0c592559bc6b63f96635d2; xqat=2182a2544e6935519a0c592559bc6b63f96635d2; xq_id_token=eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJ1aWQiOjc4NDk4MzY5NDIsImlzcyI6InVjIiwiZXhwIjoxNjg1MDIyMzIxLCJjdG0iOjE2ODI0MzAzMjE4NzAsImNpZCI6ImQ5ZDBuNEFadXAifQ.rCkwbSpP84TNLyzZIv4qSzcYoCkt0XoxmLntOrq4pb49JOuT9oLMN0b4EL24YfcbubAu7jG7oSzmRtS9tT8MnqR9jsW0-UvBJejuxmHKeRtDoyAirF5J3B5UnXPyccvyXNRk288qofbc7M2tGG6Al1bwZNRYy2vr7CeH2Lh5A6KvmzomVXLbC_v_lcFoIMZFgCxM8aAIFsMfg0K6CtejonGqfznvnyUqSvKkpgNhtrvBfoVMb2_TUbsOp9jt2Jv1k5XF2n8SOtbOraqkzBTuxahNSrsfWvPxmmy4rcrNMloa4HcHOZZygKmY-3r6pqzK0mSkt0Syys66NX3ogVzhag; xq_r_token=425b89164b64c7bf8124cedd69f2b34064e476da; acw_tc=2760827016825039672516977e05d6c39099346cfd6f0832bc8d45c2d8fced; __utma=1.1457744673.1667647235.1681120990.1682504050.25; __utmc=1; __utmt=1; Hm_lvt_1db88642e346389874251b5a1eded6e3=1681906222,1681956412,1682430323,1682504050; is_overseas=0; snbim_minify=true; __utmb=1.2.10.1682504050; Hm_lpvt_1db88642e346389874251b5a1eded6e3=1682504087'
    }

    for page_number in range(1,page_number):
        url = f'https://xueqiu.com/service/screener/screen?category=CN&exchange=sh_sz&areacode=&indcode=&order_by=symbol&order=desc&page={page_number}&size=200&only_count=0&current=&pct=-10_20&chgpct=1_20&pct_current_year=-67.34_577.96&mc=103309550_2317421139462&fmc=25076621_2317421139462&amount=0_5523516959.15&volume=0_857274007&tr=0_70.17&_='+tss
        # url = f'https://xueqiu.com/service/screener/screen?category=CN&exchange=sh_sz&areacode=&indcode=&order_by=symbol&order=desc&page=1&size=5000&only_count=0&current=&pct=-10_20&chgpct=1_20&pct_current_year=-67.34_577.96&mc=103309550_2317421139462&fmc=25076621_2317421139462&amount=0_5523516959.15&volume=0_857274007&tr=0_70.17&_=' + tss
        # url=f'https://stock.xueqiu.com/v5/stock/screener/quote/list.json?page=1&size=5000&order=desc&orderby=percent&order_by=percent&market=CN&type=sh_sz'
        print(url)
        time.sleep(3)
        response = requests.get(url, headers=headers)
        print(response.content)
        json_data = response.json()
        # print(json_data)

        data_list = json_data['data']['list']
        print(len(data_list))
        data_list_all.extend(data_list)
        print(len(data_list_all))
    return  data_list_all



def InsertData(TableName, dic):

    try:


        COLstr = ''  # 列的字段
        ROWstr = ''  # 行字段

        ColumnStyle = ' VARCHAR(20)'
        for key in dic.keys():
            COLstr = COLstr + ' ' + key + ColumnStyle + ','
            ROWstr = (ROWstr + '"%s"' + ',') % (dic[key])
        print(ROWstr[:-1])
        # print(COLstr[:-1])

        # 判断表是否存在，存在执行try，不存在执行except新建表，再insert
        try:
            cur.execute("SELECT * FROM  %s" % (TableName))
            cur.execute("INSERT INTO %s VALUES (%s)" % (TableName, ROWstr[:-1]))

        except :

            cur.execute("CREATE TABLE %s  (%s) " % (TableName, COLstr[:-1]))
            cur.execute("INSERT INTO %s VALUES (%s) " % (TableName, ROWstr[:-1]))
        conn.commit()




    except MySQLdb.Error as e :
        print("Mysql Error %d: %s" % (e.args[0], e.args[1]))




if __name__ == '__main__':
    # dic = {'股票代码': 'SZ301318', '股票名字': '维海德', '当前价': 50.89, '当日振幅': 9.74, '流通市值': 837723496, '总市值': 3532376680, '当日成交量': 2659468, '当日成交额': 133216430.89, '涨跌幅/%': 6.13, '年初至今/%': -20.51, '成交量': 2659468, '成交额': 133216430.89, '换手率/%': 16.16}
    data_list_all=get_web_data(26)
    now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    date = now[0:10]
    for i in data_list_all:
        dit = {}
        list = []
        dit['ts_code'] = i['symbol']
        dit['name'] = i['name']
        dit['price'] = i['current']
        dit['chgpct'] = i['chgpct']
        dit['fmc'] = i['fmc']
        dit['mc'] = i['mc']
        dit['volume'] = i['volume']
        dit['amount'] = i['amount']
        dit['changes'] = i['pct']
        dit['changes_this_year'] = i['pct_current_year']
        dit['current_volume'] = i['volume']
        dit['current_amount'] = i['amount']
        dit['tr'] = i['tr']
        dit['date'] = date
        dit['industry']=''
        # dit['成交额/流通值'] =(i['tr']i['fmc'])
        # dit['市盈率TTM'] = i['pe_ttm']
        # dit['股息率/%'] = i['dividend_yield']
        # dit['市值'] = i['market_capital']

        # print(dit)
        InsertData('xueqiu_stockinfo_temp', dit)


    try:
        cur.execute("delete from  xueqiu_stockinfo_temp where  date != date=CURDATE() ")
        time.sleep(2)
        cur.execute("delete from  xueqiu_stockinfo_temp where  ts_code like 'BJ%'")
        time.sleep(2)
        cur.execute(
            "update xueqiu_stockinfo_temp  set fmc=round(fmc/100000000,2),mc=round(mc/100000000,2),\
            volume=round(volume/1000000 ,2),amount=round(amount/100000000,2) where  date=CURDATE();")
        time.sleep(5)
        cur.execute("update xueqiu_stockinfo_temp set xueqiu_stockinfo_temp.industry=(select \
        temp_industry.industry from  temp_industry  where 	xueqiu_stockinfo_temp.ts_code = temp_industry.ts_code) ")
        time.sleep(8)
        cur.execute(" insert into test.xueqiu_stockinfo select * from test.xueqiu_stockinfo_temp \
        where `date`= CURDATE();")
        conn.commit()
    except MySQLdb.Error as error:
        print("Error:{}".format(error))
        # 发生错误时回滚
        connect.rollback()



    cur.close()
    conn.close()





  

  



