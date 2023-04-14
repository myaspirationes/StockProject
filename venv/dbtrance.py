# -*- coding: utf-8 -*-
"""
@Time ： 2023/3/30 18:13
@Auth ： Tiger
@File ：dbtrance.py
@IDE ：PyCharm
@Motto:Coding is nothing
"""
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

connect_django = MySQLdb.connect("localhost", "root", "root", "web_django", charset='utf8')
cursor_django = connect.cursor()

sql_price_volume="insert into web_django.price_volume (ts_code, name, p_sustain_days, price_change, v_sustain_days, " \
                 "pct, turnover_rate, date)  select a.ts_code, a.name, a.sustain_days , a.price_change, " \
                 "b.sustain_days, b.change, b.turnover_rate, a.date from web_django.sustained_higher_volum a, " \
                 "web_django.sustained_higher_price b where a.ts_code = b.ts_code and a.date = b.date and a.date = current_date;"
sql_stock_info="insert ignore into web_django.stock_info(ts_code, name, price, chgpct, fmc, mc, volume, amount, changes, changes_this_year, current_volume, current_amount, tr, `date`, industry) select * from  test.xueqiu_stockinfo;"
try:
    cursor_django.execute(sql_price_volume)
    print("Add price_volume To web_django Database  Success ")
    time.sleep(3)

    cursor_django.execute(sql_stock_info)
    print("Add stock_info To web_django Database  Success ")


    # 提交到数据库执行
    connect.commit()
except:
    print("error ")

    connect.rollback()
cursor_django.close()
connect_django.close()

cursor.close()
connect.close()