# -*- coding: utf-8 -*-
"""
@Time ： 2023/5/22 20:11
@Auth ： Tiger
@File ：g.py
@IDE ：PyCharm
@Motto:Coding is nothing
"""
import lmproof
import requests
import qrcode
from PIL import Image
import random, string
import MySQLdb
import pywencai
from decimal import Decimal

from warnings import simplefilter

simplefilter(action="ignore", category=FutureWarning)


# import tabula,os


# def pdf_csv():
#     filename = input("Enter File Path: ")
#     df = tabula.read_pdf(filename, encoding='utf-8', spreadsheet=True, pages='1')
#
#     df.to_csv('output.csv')

def proofread(text):
    proofread = lmproof.load("en")
    correction = proofread.proofread(text)
    print("Original: {}".format(text))
    print("Correction: {}".format(correction))


def get_cookie():
    url = "https://weibo.com"
    response = requests.post(url)
    print(response.headers)

    # 获取cookies
    cookies = response.cookies
    print(cookies)

    print(requests.utils.dict_from_cookiejar(response.cookies))

    # 打印cookies
    # for cookie in cookies:
    #     print(f"{cookie.name}: {cookie.value}")


def post_request():
    url = "http://www.iwencai.com/gateway/urp/v7/landing/getDataList"
    headers = {"Content-Type": "application/x-www-form-urlencoded",
               "User_Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                             'Chrome/113.0.0.0 Safari/537.36 Edg/113.0.1774.50',
               "cookie": "other_uid=Ths_iwencai_Xuangu_yl3bd25h5xtdfl0n41crs4grbkqg23pr; ta_random_userid=qi1b8qi7o8; cid=393fb8a8bb2afb5caafe2425c54174d51668331053; cid=393fb8a8bb2afb5caafe2425c54174d51668331053; ComputerID=393fb8a8bb2afb5caafe2425c54174d51668331053; WafStatus=0; wencai_pc_version=1; v=AzHOtqWT8a10Sl25U3Hn9_8kQLbOHqIJT5dJqRNGL9oXJl8oW261YN_iWWmg"}
    data = {
        "query": "跳空高开",
        "urp_sort_way": "desc",
        "urp_sort_index": "最新涨跌幅",
        "page": "1",
        "perpage": "100",
        "addheaderindexes": "",
        "condition": [
            {"indexName": "跳空高开", "indexProperties": ["nodate 1", "交易日期 20230524"], "source": "new_parser",
             "type": "tech",
             "indexPropertiesMap": {"交易日期": "20230524", "nodate": "1"}, "reportType": "TRADE_DAILY",
             "dateType": "交易日期",
             "chunkedResult": "跳空高开", "valueType": "", "domain": "abs_股票领域", "uiText": "跳空高开", "sonSize": 0,
             "queryText": "跳空高开", "relatedSize": 0, "tag": "跳空高开"}],
        "codelist": "",
        "indexnamelimit": "",
        "logid": "c60660181c88bafc9772d42458afc386",
        "ret": "json_all",
        "sessionid": "c60660181c88bafc9772d42458afc386",
        "source": "Ths_iwencai_Xuangu",
        "date_range[0]": "20230524",
        "iwc_token": "",
        "urp_use_sort": "1",
        "user_id": "Ths_iwencai_Xuangu_yl3bd25h5xtdfl0n41crs4grbkqg23pr",
        "uuids[0]": "24087",
        "query_type": "stock",
        "comp_id": "6734520",
        "business_cat": "soniu",
        "uuid": "24087",

    }

    response = requests.post(url, headers=headers, data=data)

    print(response.status_code)
    print(response)


def num_code(length=6):
    """
    生成长度为length的 数字+字母 随机验证码
    :param length: 验证码长度
    :return: 验证码
    """

    return ''.join(random.choice(string.ascii_letters + string.digits) for i in range(0, length))


def qrcode_gen(url):
    # Define the URL you want to encode
    # url = "https://www.example.com"

    # Generate the QR code
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")

    # Add color to the QR code
    img = img.convert("RGBA")
    data = img.getdata()

    # Replace white pixels with your desired color
    new_data = []
    for item in data:
        if item[0] == 255 and item[1] == 255 and item[2] == 255:
            new_data.append((50, 120, 20, 155))  # Replace white with red
        else:
            new_data.append(item)

    img.putdata(new_data)

    # Save the colored QR code
    img.save("colored_qr.png")


def qrcode_logo(url):
    # 创建QRCode对象
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=1
    )

    qr.add_data(url)  # 添加信息，data_str为拟创建二维码中的信息字符串
    qr.make(fit=True)  # 生成二维码

    img = qr.make_image()  # 获取二维码图像
    img = img.convert("RGBA")  # 转换图像格式

    img_w, img_h = img.size  # 获取图像宽、高
    logopath = 'D:/BaiduNetdiskDownload/Python/StockProject/venv/milogo.jpeg'

    logo = Image.open(logopath)  # 打开logo图像，logopath为logo的文件名和路径

    factor = 4  # 比例因子，即logo宽度为二维码图像的1/4左右

    size_w = int(img_w / factor)  # logo宽
    size_h = int(img_h / factor)  # logo高

    logo_w, logo_h = logo.size  # 获取logo实际宽、高

    if logo_w > size_w:  # logo宽度小于等于size_w
        logo_w = size_w

    if logo_h > size_h:  # logo高度小于等于size_h
        logo_h = size_h

    logo = logo.resize((size_w, size_h), Image.ANTIALIAS)  # 缩放logo图片
    logo = logo.convert("RGBA")  # 转换logo格式

    w = int((img_w - logo_w) / 2)  # 计算粘贴位置
    h = int((img_h - logo_h) / 2)

    img.paste(logo, (w, h))  # 将logo粘贴到二维码图像

    img.save("qr.png")  # 保存二维码，"qr.png"为图片文件名


def get_3_lines():
    connect = MySQLdb.connect("localhost", "root", "root", "test", charset='utf8')
    cursor = connect.cursor()

    res = pywencai.get(question='一阳三线，非北京交易所', sort_key='股票代码', sort_order='asc')
    # print(res)
    # print(res.keys()[6])
    # print(res.keys()[7])
    # print(res.keys()[9])
    # print(res.keys()[8])

    date_symbol = res.keys()[7]
    date = date_symbol[-9:-1]
    print(date)
    date = date[:4] + "-" + date[4:6] + "-" + date[6:]
    # date='2023-12-18'

    # print(date)
    for i in range(0, res.shape[0]):

        name = res.iloc[i][1]
        print(name)
        ts_code = res.loc[i]['code']
        if ts_code[0] == "6":
            ts_code = "SH" + ts_code
        else:
            ts_code = "SZ" + ts_code

        price = res.iloc[i][3]

        sql_three_lines = "insert ignore into  break_3_lines (ts_code,trade_date,avg5) value (%s,%s,%s)"
        param = (ts_code, date, price)

        try:
            cursor.execute(sql_three_lines, param)  # 执行sql语句
            print(" Break_3_lines Add To Database  Success")
            connect.commit()  # 提交到数据库执行
        except:
            connect.rollback()  # 发生错误时回滚

    cursor.close()
    connect.close()


def get_skip():
    connect = MySQLdb.connect("localhost", "root", "root", "test", charset='utf8')
    cursor = connect.cursor()

    res = pywencai.get(question='最低价>前1日的最高价，非北京交易所', sort_key='股票代码', sort_order='asc')
    # print(res)
    date_symbol = res.keys()[4]
    date = date_symbol[-9:-1]
    # print(date)
    date = date[:4] + "-" + date[4:6] + "-" + date[6:]
    # date='2023-12-18'

    print(date)
    for i in range(0, res.shape[0]):

        name = res.loc[i][1]
        print(name)
        ts_code = res.loc[i]['code']
        if ts_code[0] == "6":
            ts_code = "SH" + ts_code
        else:
            ts_code = "SZ" + ts_code
        print(ts_code)
        chg = res.loc[i][3]
        chg = Decimal(chg).quantize(Decimal("0.01"), rounding="ROUND_HALF_UP")
        # print(chg)
        low_price = res.loc[i][4]
        low_price = Decimal(low_price).quantize(Decimal("0.01"), rounding="ROUND_HALF_UP")

        # print(low_price)
        high_price = res.loc[i][5]
        high_price = Decimal(high_price).quantize(Decimal("0.01"), rounding="ROUND_HALF_UP")

        # print(high_price)
        sql_three_lines = "insert ignore into  skip_stock (ts_code,date,name,today_low,pre_high,pct_chg) value (%s,%s,%s,%s,%s,%s)"
        param = (ts_code, date, name, low_price, high_price, chg)

        try:
            cursor.execute(sql_three_lines, param)  # 执行sql语句
            print("Add To skip_stock  Success")
            connect.commit()  # 提交到数据库执行
        except:
            connect.rollback()  # 发生错误时回滚

    cursor.close()
    connect.close()


# 返回列表中不重复的数
def get_undul_inlist():
    my_list = [1, 2, 3, 4, 5, 8, 6, 3, 5]
    nums = []

    while len(nums) < len(my_list):
        num = random.choice(my_list)
        # print(num)
        if num not in nums:
            nums.append(num)
            print(num)
    return num

    print("随机选择的数字为：", nums)


def get_triple_vol():
    connect = MySQLdb.connect("localhost", "root", "root", "test", charset='utf8')
    cursor = connect.cursor()

    res = pywencai.get(question='成交量>前面第1日的成交量*3，非北京交易所', sort_key='股票代码', sort_order='asc')
    # print(res)
    date_symbol = res.keys()[4]
    date = date_symbol[-9:-1]
    # print(date)
    date = date[:4] + "-" + date[4:6] + "-" + date[6:]
    # date='2023-12-18'

    print(date)

    for i in range(0, res.shape[0]):

        name = res.loc[i][1]
        print(name)
        ts_code = res.loc[i]['code']
        # print(ts_code)
        if ts_code[0] == "6":
            ts_code = "SH" + ts_code
        else:
            ts_code = "SZ" + ts_code
        print(ts_code)

        yesterday_vol = res.loc[i][5]
        # print(int(float(yesterday_vol)))
        today_vol = res.loc[i][4]
        # print(int(float(today_vol)))
        Multiples = round(int(float(today_vol)) / int(float(yesterday_vol)), 2)  # 交易量倍数保留2位小数
        # print(Multiples)
        sql_three_lines = "insert ignore into  three_times_vol (ts_code,times,date) value (%s,%s,%s)"
        param = (ts_code, Multiples, date)

        try:
            cursor.execute(sql_three_lines, param)  # 执行sql语句
            print("Add To three_times_vol  Success")
            connect.commit()  # 提交到数据库执行
        except MySQLdb.ProgrammingError as e:
            print(e)
            connect.rollback()  # 发生错误时回滚

    cursor.close()
    connect.close()


def get_limitUp_stocks():
    connect = MySQLdb.connect("localhost", "root", "root", "web_django", charset='utf8')
    cursor = connect.cursor()

    res = pywencai.get(question='今日涨停和涨停原因', sort_key='股票代码', sort_order='asc')
    # print(res)

    # for i in range(0, 19):
    #     print(res.keys()[i])
    #
    #     print(res.loc[0][i])

    date_symbol = res.keys()[4]
    date = date_symbol[-9:-1]
    # print(date)
    date = date[:4] + "-" + date[4:6] + "-" + date[6:]
    # date='2023-12-18'

    print(date)

    for i in range(0, res.shape[0]):

        name = res.loc[i][1]
        print(name)
        ts_code = res.loc[i]['code']
        # print(ts_code)
        if ts_code[0] == "6":
            ts_code = "SH" + ts_code
        else:
            ts_code = "SZ" + ts_code
        # print(ts_code)

        price = res.loc[i][2]
        # print(price)

        change = res.loc[i][3]
        # print(change)
        reason = res.loc[i][5]
        # print(reason)
        first_limit = res.loc[i][6]
        # print(first_limit)
        last_limit = res.loc[i][7]
        # print(last_limit)
        continuous_limit = res.loc[i][16]
        # print(continuous_limit)

        break_limit = res.loc[i][14]
        # print(break_limit)

        limit_type = res.loc[i][17]
        # print(limit_type)

        if ts_code[2] != 8 and ts_code[3] != 8 and not name.startswith(
                '*ST'):  # 科创板,*STDo you want to install the recommended 'Python' extension from ms-python for the Python language?和新三板不入库

            sql_limit_up = "insert ignore into  limit_up_stock (ts_code,name,date ,price,changes,reason,first_limit,last_limit,continuous_limit,break_limit,limit_type) value (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            param = (ts_code, name, date, price, change, reason, first_limit, last_limit, continuous_limit, break_limit,
                     limit_type)

            try:
                cursor.execute(sql_limit_up, param)  # 执行sql语句
                print("Add To limit_up_stock  Success")
                connect.commit()  # 提交到数据库执行
            except:
                connect.rollback()  # 发生错误时回滚

    cursor.close()
    connect.close()


def get_renqi():
    # connect = MySQLdb.connect("localhost", "root", "root", "test", charset='utf8')
    # cursor = connect.cursor()

    res = pywencai.get(question='人气资金流入', sort_key='股票代码', sort_order='asc', loop=2)
    print(res)

    date_symbol = res.keys()[5]
    date = date_symbol[-9:-1]
    print(date)
    for i in range(0, res.shape[0]):

        name = res.loc[i][1]
        print(name)
        ts_code = res.loc[i]['code']
        if ts_code[0] == "6":
            ts_code = "SH" + ts_code
        else:
            ts_code = "SZ" + ts_code

        price = res.loc[i][3]
        #
        # sql_three_lines = "insert ignore into  break_3_lines (ts_code,trade_date,avg5) value (%s,%s,%s)"
        # param = (ts_code, date, price)
        #
        # try:
        #     cursor.execute(sql_three_lines, param)  # 执行sql语句
        #     print("Add To Database  Success")
        #     connect.commit()  # 提交到数据库执行
        # except:
        #     connect.rollback()  # 发生错误时回滚
    #
    # cursor.close()
    # connect.close()


def getCookies():
    url = f'https://stock.xueqiu.com/v5/stock/screener/quote/list.json?page=1&size=90&order=desc&order_by=percent' \
          f'&exchange=CN&market=CN&type=kcb'

    headers = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Mobile Safari/537.36 Edg/114.0.1823.51',
        'Referer': 'https://xueqiu.com/',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-US,en;q=0.9',
        'Connection': 'keep-alive'
    }

    response = requests.get(url, headers)
    print(response)

    cookie = response.cookies.get_dict()
    print(cookie)


def checkinV2():
    url = f'https://w1.v2free.net/user/checkin'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Mobile Safari/537.36 Edg/114.0.1823.51',
        'cookie': '_ga=GA1.1.2126236496.1658272726; _ga_NC10VPE6SR=GS1.1.1694675902.249.1.1694677231.0.0.0; uid=57247; email=myaspirations%40126.com; key=cf9d342ad786f0afda1c3cb9348fb94200adfc0ddc0d0; ip=1b7086e20d5ed55661f25d93b3a2337a; expire_in=1702533252; crisp-client%2Fsession%2Fa47ae3dd-53d8-4b15-afae-fb4577f7bcd0=session_9893b12b-5ec0-4e84-9297-2b469590de4d'

    }
    response = requests.post(url, headers)
    print(response)


def checkinHiFi():
    url = f'https://www.hifini.com/sg_sign.htm'
    headers = {
        'Referer': 'https://www.hifini.com/',
        'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Mobile Safari/537.36 Edg/114.0.1823.51',
        'cookie': 'bbs_token=i_2FId_2F4UOJEGe6hR00C7eHNkgyWRb2_2FteUAe4y0Kf2ghelcIbFRNW_2FuZs_2FCE0bjXGexYXVDtS9TFL2Qvhf_2F18UFHEpAE_3D; bbs_sid=rnovtri2pb63sg5pdenfskhcvm; Hm_lvt_4ab5ca5f7f036f4a4747f1836fffe6f2=1701489940,1701663611,1702208927,1702449353; Hm_lpvt_4ab5ca5f7f036f4a4747f1836fffe6f2=1702449370'
    }
    response = requests.post(url, headers)
    # response.encoding = response.apparent_encoding
    text = response.content.decode('utf-8', 'ignore')
    print(text)
    with open('HIFI.html', 'w') as fp:
        fp.write(text)

    # print(response.text)
    # print(response.json())


if __name__ == '__main__':
    url = "手机号：13817391487"
    # getCookies()
    # get_cookie()
    # qrcode_gen(url)
    # qrcode_logo(url)
    # get_cookie()
    # post_request()
    # print(num_code())
    # get_renqi()
    # proofread("YourNameIsJacky")

    get_3_lines()
    get_triple_vol()
    get_skip()
    get_limitUp_stocks()

    # get_undul_inlist()

    # #
    # checkinHiFi()
    # checkinV2()
