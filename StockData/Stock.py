import time

from jqdatasdk import *

auth('13551167709', '1355Jing.@')


#将所有股票列表转换成数组
stocks = list(get_all_securities(['stock']).index)
# print(stocks)
#

#获取平安银行按1分钟为周期以“2015-01-30 14:00:00”为基础前4个时间单位的数据
for st in stocks:
    df = get_price(st, end_date='2023-03-20 14:00:00', count=10, frequency='1d')
    print(df)
    time.sleep(3)

