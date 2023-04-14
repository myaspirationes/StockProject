import mpl_finance as mpf
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.ticker as ticker
import numpy as np
#创建绘图的基本参数
fig, axes = plt.subplots(2, 1, sharex=True, figsize=(15, 10))
ax1, ax2 = axes.flatten()



def date_to_num(dates):
    num_time = []
    for date in dates:
        date_time = datetime.strptime(date, '%Y-%m-%d')
        num_date = date2num(date_time)
        num_time.append(num_date)
    return num_time



#获取刚才的股票数据
df = pd.read_excel("牧原股份.xlsx")
print("df的数据类型：")
print(df.dtypes)
mpf.candlestick2_ochl(ax1, df["open"], df["close"], df["high"], df["low"], width=0.6, colorup='green',colordown='red',alpha=1.0)
df['trade_date'] = pd.to_datetime(df['trade_date'])
df['trade_date'] = df['trade_date'].apply(lambda x: x.strftime('%Y-%m-%d'))
def format_date(x, pos=None):
    if x < 0 or x > len(df['trade_date']) - 1:
        return ''
    return df['trade_date'][int(x)]





df["SMA5"] = df["close"].rolling(5).mean()
df["SMA10"] = df["close"].rolling(10).mean()
df["SMA30"] = df["close"].rolling(30).mean()
ax1.plot(np.arange(0, len(df)), df['SMA5'])  # 绘制5日均线
ax1.plot(np.arange(0, len(df)), df['SMA10'])  # 绘制10日均线
ax1.plot(np.arange(0, len(df)), df['SMA30'])  # 绘制30日均线
ax1.xaxis.set_major_formatter(ticker.FuncFormatter(format_date))
plt.setp(plt.gca().get_xticklabels(), rotation=45, horizontalalignment='right')

red_pred = np.where(df["close"] > df["open"], df["vol"], 0)
blue_pred = np.where(df["close"] < df["open"], df["vol"], 0)
ax2.bar(np.arange(0, len(df)), red_pred, facecolor="green")
ax2.bar(np.arange(0, len(df)), blue_pred, facecolor="red")



#显示出来
plt.show()
