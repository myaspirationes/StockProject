'''
Insert items into database
@author: hakuri
'''
import MySQLdb


def InsertData(TableName, dic):
    try:
        conn = MySQLdb.connect(host='localhost', user='root', passwd='root', db='test', port=3306)  # 链接数据库
        cur = conn.cursor()
        COLstr = ''  # 列的字段
        ROWstr = ''  # 行字段

        ColumnStyle = ' VARCHAR(20)'
        for key in dic.keys():
            COLstr = COLstr + ' ' + key + ColumnStyle + ','
            ROWstr = (ROWstr + '"%s"' + ',') % (dic[key])

            print(COLstr)
            print(COLstr[:-1])

        # 判断表是否存在，存在执行try，不存在执行except新建表，再insert
        try:
            cur.execute("SELECT * FROM  %s" % (TableName))
            cur.execute("INSERT INTO %s VALUES (%s)" % (TableName, ROWstr[:-1]))

        except:
            cur.execute("CREATE TABLE %s (%s)" % (TableName, COLstr[:-1]))
            cur.execute("INSERT INTO %s VALUES (%s)" % (TableName, ROWstr[:-1]))
        conn.commit()
        cur.close()
        conn.close()

    except:
        print("error")


if __name__ == '__main__':
    dic = {'股票代码': 'SZ301318', '股票名字': '维海德', '当前价': 50.89, '当日振幅': 9.74, '流通市值': 837723496, '总市值': 3532376680, '当日成交量': 2659468, '当日成交额': 133216430.89, '涨跌幅/%': 6.13, '年初至今/%': -20.51, '成交量': 2659468, '成交额': 133216430.89, '换手率/%': 16.16}

    InsertData('testtable', dic)