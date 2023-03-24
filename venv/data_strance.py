import MySQLdb
import time

# #  添加industry 的值
# update stock_info, temp set stock_info.industry = temp.industry where stock_info.ts_code = temp.ts_code and stock_info.ts_code in (  select b.mid_id from (select stock_info.ts_code as mid_id from stock_info where stock_info.industry = '' ) b)
# #industry  更新给 stockinfo 表格中
# update test.xueqiu_stockinfo,test.stock_basic set  test.xueqiu_stockinfo.industry=  (select test.stock_basic.industry from test.stock_basic where xueqiu_stockinfo.ts_code=stock_basic.ts_code ) where test.xueqiu_stockinfo.ts_code= test.stock_basic.ts_code  ;
#
# # 数据迁移
# insert  into web_django.stock_info select * from test.xueqiu_stockinfo where test.xueqiu_stockinfo.date=curdate()

connect = MySQLdb.connect("localhost", "root", "root", "test", charset='utf8')
cursor = connect.cursor()

sql_dual_three="insert ignore into test.dual_three (dual_three.ts_code,`date`,times,name) select break_3_lines.ts_code, three_times_vol.`date`, three_times_vol.`times`, stock_basic.name from break_3_lines, stock_basic, three_times_vol where break_3_lines.ts_code = stock_basic.ts_code and break_3_lines.ts_code = three_times_vol.ts_code and three_times_vol.`date`=break_3_lines.trade_date"
sql_skip_triple="insert ignore into test.skip_triple (skip_triple.ts_code,`date`,name) select skip_stock.ts_code, three_times_vol.`date`, stock_basic.name from skip_stock, stock_basic, three_times_vol where skip_stock.ts_code = stock_basic.ts_code and skip_stock.ts_code = three_times_vol.ts_code and skip_stock.`date`=three_times_vol.`date`"
sql_skip_times_lines="insert ignore into test.skip_times_lines (skip_times_lines.`date`,name,ts_code) select dual_three.`date` , dual_three.name , skip_triple.ts_code from dual_three , skip_triple where dual_three.`date` = skip_triple.`date` and dual_three.ts_code = skip_triple.ts_code"


try:
    # 执行sql语句
    # cursor.execute(sql, skip_stock_code)
    cursor.execute(sql_dual_three)
    print("Add To Database  Success 1")

    time.sleep(2)

    cursor.execute(sql_skip_triple)
    print("Add To Database  Success 2")

    time.sleep(2)
    cursor.execute(sql_skip_times_lines)

    print("Add To Database  Success 3")
    # 提交到数据库执行
    connect.commit()
except:
    # 发生错误时回滚
    connect.rollback()



connect_django = MySQLdb.connect("localhost", "root", "root", "web_django", charset='utf8')
cursor_django = connect.cursor()




sql_django_dual_three="insert ignore into web_django.dual_three select * from test.dual_three"
sql_django_skip_triple="insert ignore into web_django.skip_triple select * from test.skip_triple"
sql_django_skip_times_lines="insert ignore into web_django.skip_times_lines select * from test.skip_times_lines"
sql_hot_stocks="INSERT ignore INTO web_django.hot_stocks (ts_code,name, date_exchange, price, follow7d, follow7dpct, `date`) select * from test.hot_stocks"

try:
    # 执行sql语句
    cursor_django.execute(sql_hot_stocks)
    print("Add hotstocks To web_django Database  Success ")

    time.sleep(1)

    cursor_django.execute(sql_django_dual_three)
    print("Add dual_three To web_django Database  Success ")

    time.sleep(1)


    cursor_django.execute(sql_django_skip_triple)
    print("Add skip_triple To web_django Database  Success")

    time.sleep(1)

    cursor_django.execute(sql_django_skip_times_lines)
    print("Add skip_times_lines To web_django Database  Success")
    time.sleep(3)


    # 提交到数据库执行
    connect.commit()
except:
    # 发生错误时回滚
    connect.rollback()



SQL_test_to_django_break3lines="insert ignore into web_django.break_three_lines (select * from test.break_3_lines)"
SQL_test_to_django_three_times_vol="insert ignore into web_django.three_times_vol (select * from test.three_times_vol)"
SQL_test_to_django_skip_stock="insert ignore into web_django.skip_stock (select * from test.skip_stock)"

try:
    # 执行sql语句
    # cursor.execute(sql, skip_stock_code)
    cursor_django.execute(SQL_test_to_django_break3lines)
    print("Add break3lines form test To web_django  Success ")

    time.sleep(1)

    cursor_django.execute(SQL_test_to_django_three_times_vol)
    print("Add three_times_vol form test To web_django  Success")

    time.sleep(1)
    cursor_django.execute(SQL_test_to_django_skip_stock)

    print("Add skip_stock form test To web_django  Success")
    # 提交到数据库执行
    connect.commit()
except:
    # 发生错误时回滚
    connect.rollback()

sql_change_3_days= "insert  ignore into web_django.change_three_days (today_price,ts_code,name,change_3_days,date)  select  today_price,ts_code,name,change_3_days,date from test.change_three_days"
sql_change_5_days= "insert  ignore into web_django.change_five_days (today_price,ts_code,name,change_5_days,date)  select * from test.change_five_days"
sql_change_10_days= "insert  ignore into web_django.change_ten_days (today_price,ts_code,name,change_10_days,date)  select * from test.change_ten_days"
sql_ths_hot_50="insert ignore into  web_django.ths_50_hot(ts_code, name, `date`, trunover_rate, high, close_price, pre_close, change_rate, popularity_rate) select ts_code, name, `date`, trunover_rate, high, close_price, pre_close, change_rate, popularity_rate from  test.ths_50_hot"

try:
    cursor_django.execute(sql_change_3_days)
    time.sleep(1)

    print("change 3 days trance success")
    cursor_django.execute(sql_change_5_days)
    time.sleep(1)
    print("change 5 days trance success")

    cursor_django.execute(sql_change_10_days)
    print("change 10 days trance success")
    connect.commit()

    cursor_django.execute(sql_ths_hot_50)
    print("ths_hot_50 add  success")
    connect.commit()

except:
    connect.rollback()


cursor_django.close()
connect_django.close()

cursor.close()
connect.close()