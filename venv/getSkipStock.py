# -*- coding: utf-8 -*-
"""
@Time ： 2022/12/6 20:47
@Auth ： Tiger
@File ：getSkipStock.py
@IDE ：PyCharm
@Motto:Build My Dream
"""

# 导入tushare
import tushare as ts

# 初始化pro接口
pro = ts.pro_api('a0045b3469b1b145fb57a7b97467a49fd7deecdd299c21b6d9a5f64a')
stock_dat = pro.daily(ts_code='000777', start_date='20221212', end_date='20221216')
# df = ts.pro_bar(ts_code='000756.SZ', adj='qfq', start_date='20221215', end_date='20221216')
print(stock_dat)

daily_all=ts.get_today_all()
print(daily_all)
# print(df.iloc[0])
# # 拉取数据
# df = pro.trade_cal(**{
#     "exchange": "",
#     "cal_date": "",
#     "start_date": "",
#     "end_date": "",
#     "is_open": "",
#     "limit": "",
#     "offset": ""
# }, fields=[
#     "exchange",
#     "cal_date",
#     "is_open",
#     "pretrade_date"
# ])
# print(df)


