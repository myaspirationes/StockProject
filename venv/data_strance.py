import MySQLdb
import time




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

    time.sleep(5)

    cursor.execute(sql_skip_triple)
    print("Add To Database  Success 2")

    time.sleep(5)
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



try:
    # 执行sql语句
    # cursor.execute(sql, skip_stock_code)
    cursor_django.execute(sql_django_dual_three)
    print("Add To Database  Success 1")

    time.sleep(5)

    cursor_django.execute(sql_django_skip_triple)
    print("Add To Database  Success 2")

    time.sleep(5)
    cursor_django.execute(sql_django_skip_times_lines)

    print("Add To Database  Success 3")
    # 提交到数据库执行
    connect.commit()
except:
    # 发生错误时回滚
    connect.rollback()

cursor_django.close()
connect_django.close()

cursor.close()
connect.close()