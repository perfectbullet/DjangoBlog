import csv
import json
import os.path
import re
from datetime import datetime

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pytz
from pandas import DataFrame


class TimeUtils:
    # US Pacific Time
    us_eastern_dt = datetime.now(tz=pytz.timezone("America/New_York"))
    # China time
    china_time = datetime.now(pytz.timezone('Asia/Shanghai'))


def save_json(data: dict, json_path):
    with open(json_path, 'w') as f:
        json.dump(data, f)


def load_csv(csv_path: str):
    """
    csv_path
    :param csv_path:
    :return:
    """
    data = pd.read_csv(csv_path, index_col=False, sep=',')
    return data


def load_goldhub_data(json_path, chart_key='lbma_am_usd'):
    """
    读取 goldhub json格式数据
    :param json_path:
    :return:
    """
    with open(json_path) as f:
        data = json.load(f)
    return data['chartData'][chart_key]


def json_to_csv(json_path: str, chart_key='lbma_am_usd'):
    json_res = load_goldhub_data(json_path, chart_key=chart_key)
    new_path = json_path.replace('.json', '.csv')
    with open(new_path, "w", newline="") as f:
        writer = csv.writer(f, delimiter=",")
        for x_tmstp, y_value in json_res:
            x_date = datetime.fromtimestamp(float(x_tmstp) / 1000)
            writer.writerow([x_date, y_value])
    return new_path


def json_to_df(data: dict, chart_key='USD') -> pd.DataFrame:
    df = pd.DataFrame(data['chartData'][chart_key], columns=['date', 'price'])
    return df


def df_to_csv(df: pd.DataFrame, csv_path: str) -> str:
    df.to_csv(csv_path, index=False)
    return csv_path


def origin_data_deal(data):
    """
    读取json数据, 然后可视化
    :param data:
    :return:
    """
    # 时间
    npdata = np.array(data)
    # 获取的时间戳以毫秒为单位
    x = npdata[:, 0] / 1000
    x_date = [datetime.fromtimestamp(float(d)) for d in x]
    y = npdata[:, 1]
    fig, ax = plt.subplots()
    ax.plot(x_date, y)
    plt.ylabel('price')
    plt.xlabel('Interval 1 day')
    plt.title('gold price')
    plt.show()


def concat_csv(csv_names):
    """
    合并csv, 并排序, 然后保存， 返回csv路径
    :return:
    """
    tz_info = pytz.timezone("America/New_York")
    us_eastern_dt = datetime.now(tz=tz_info)
    date_str = us_eastern_dt.strftime('%Y%m%d%H%M%S')

    new_csv = '{}_before.csv'.format(date_str)
    new_df = DataFrame()
    for name in csv_names:
        # load data from csv
        df_data = load_csv(name)
        # csv 当前和新的数据合并
        new_df: DataFrame = pd.concat([new_df, df_data])
    new_df = new_df.sort_values(by='date')
    new_df['date'] = pd.to_datetime(new_df['date'], unit='ms')
    new_df.plot(x="date", y="price")
    new_df.to_csv(new_csv, index=False)
    plt.show()
    return new_csv


def get_csv_names(csv_dir='./data/'):
    '''
    csv_dir
    @return: csv_names
    '''

    csv_names = []
    for name in os.listdir(csv_dir):
        pattern = re.compile(r'\d{14}_\d{14}\.csv')
        mt = pattern.match(name)
        if mt is not None:
            csv_names.append(os.path.join(csv_dir, mt.group()))
    return csv_names


if __name__ == '__main__':
    json_path = '../data/2023-05-02_2023-07-28.json'
    # res = load_goldhub_data(json_path, chart_key='USD')

    # gold price json names
    # json_names = ['2023-05-02_2023-07-28', '2013-08-01_2023-07-28', '2020-08-03_2023-07-28', '2022-08-01_2023-07-28',
    #               '2023-02-01_2023-07-28', ]
    #
    # for name in json_names:
    #     csv_path = json_to_csv(os.path.join('../data/', name + '.json'), chart_key='USD')
    #     print('new csv path is ', csv_path)
    csv_names = get_csv_names()
    new_csv = concat_csv(csv_names)
    # print(new_csv)
