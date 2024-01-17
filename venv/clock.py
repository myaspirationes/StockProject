# -*- coding: utf-8 -*-
"""
@Time ： 2023/6/4 8:56
@Auth ： Tiger
@File ：clock.py
@IDE ：PyCharm
@Motto:Coding is nothing
"""
import tkinter as tk
import time
import datetime


# 按日期返回星期几
def get_week_day(date):
    # 用一个字典建立对应关系
    dict1 = {
        0: '星期一',
        1: '星期二',
        2: '星期三',
        3: '星期四',
        4: '星期五',
        5: '星期六',
        6: '星期天',
    }
    # 取得日期对应的星期几的索引
    day = date.weekday()
    # 返回汉字的索引
    return dict1[day]


# 每1秒钟修改一下clock_label,date_label显示值
def show_time():
    # 取得当天星期几
    week_day = get_week_day(datetime.datetime.now())
    # 取得现在日期和星期数
    str_date = time.strftime('%Y{}%m{}%d{}').format('年', '月', '日') + week_day
    # 取得当前时间
    str_time = time.strftime('%H:%M:%S %p').format('年', '月', '日')
    # 设置变量date_str的值
    date_str.set(str_date)
    # 设置变量time_str的值
    time_str.set(str_time)
    # 设置clock_label控件每显示1000ms调用一次show_time()函数
    date_label.after(1000, show_time)


if __name__ == '__main__':
    # 生成根窗口
    win = tk.Tk()
    # 设置窗口标题
    win.title('电子时钟')
    # 设置窗口像素
    win.geometry('380x160')
    # 生成一个字符型变量，此变量与clock_label的text属性值绑定
    time_str = tk.StringVar()
    # 生成一个字符型变量，此变量与date_label的text属性值绑定
    date_str = tk.StringVar()
    # 其中textvariable=date_str将控件的text属性与变量date_str的值绑定在一起，形成联动
    date_label = tk.Label(win, textvariable=date_str, bg='black', fg='white', font=('Arial', 20), width=70, height=2)
    # 其中textvariable=time_str将控件的text属性与变量time_str的值绑定在一起，形成联动
    clock_label = tk.Label(win, textvariable=time_str, bg='black', fg='white', font=('Arial', 30), width=70, height=2)
    # 在窗体上放置Label控件
    date_label.pack(anchor='center')
    clock_label.pack(anchor='center')
    # 调用函数，显示新的时间
    show_time()
    win.mainloop()







