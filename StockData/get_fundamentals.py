import time

from jqdatasdk import *
import pandas as pd

pd.set_option('display.max_rows', 100000)
pd.set_option('display.max_columns', 100)

auth('13551167709', '1355Jing.@')

# 获取多只股票在某一日期的市值, 利润
# df = get_fundamentals(query(
#         valuation, income
#     ).filter(
#         # 这里不能使用 in 操作, 要使用in_()函数
#         valuation.code.in_(['000001.XSHE', '600000.XSHG'])
#     ), date='2022-01-20')


df = get_fundamentals(query(indicator,), statDate='2022')
# df.to_csv('./finace2022.csv')

#基于盈利指标选股: eps,operating_profit, roe, inc_net_profit_year_on_year
df = df[(df['eps'] > 0) & (df['operating_profit'] > 3445088693) &(df['roe'] > 5) & (df['inc_net_profit_year_on_year'] > 0)]
print(df)