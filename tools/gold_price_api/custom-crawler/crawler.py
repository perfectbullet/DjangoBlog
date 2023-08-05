import asyncio
import json
import os.path
import sched
import time
from datetime import datetime
import re
import random
import pyppeteer
import pytz
import requests
from loguru import logger
from requests_html import AsyncHTMLSession, HTMLSession

from data_utils import json_to_df, df_to_csv, save_json, get_csv_names, concat_csv

tz_info = pytz.timezone("America/New_York")

class Crawler:
    def __init__(self, name='', url=''):
        self.name = name
        self.url = url

    async def crawlerInit(self):
        print(f"Starting File... {self.name}")
        # Crawler
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        session = AsyncHTMLSession()
        browser = await pyppeteer.launch({
            'ignoreHTTPSErrors': True,
            'headless': True,
            'handleSIGINT': False,
            'handleSIGTERM': False,
            'handleSIGHUP': False
        })
        session._browser = browser
        r = await session.get(self.url)
        print("Starting session!")
        res = r.json()
        r.close()
        await session.close()
        with open('../data/{}.json'.format(self.name), 'w') as f:
            json.dump(res, f)
        print("File Success!")
        return 'ok'

    def get_history_date(self):
        """
        获取自 1970-01-01 至 今的数据
        按开始结束时间获取
        https://fsapi.gold.org/api/goldprice/v11/chart/price/usd/oz/31881600000,63417600000?cache
        @param start_date:
        @param end_date:
        @return:
        """
        year_1970 = 1970
        year_now = 2023
        # 美国东部时区的时间
        res = []
        for year in range(year_1970, year_now + 1):
            start_date = datetime(year, 1, 1, 0, 0, 0, tzinfo=tz_info).timestamp() * 1000
            end_date = datetime(year + 1, 1, 1, 0, 0, 0, tzinfo=tz_info).timestamp() * 1000
            csv_path = self.get_by_date(start_date, end_date)
            wait_seconds = random.randint(30, 90)
            logger.info('get data from {} to {} + 1, wait_seconds {}'.format(year, year, wait_seconds))
            res.append(csv_path)

            time.sleep(wait_seconds)
        return res

    def get_by_date(self, start_tmsp: float, end_tmsp: float):
        """
        按开始结束时间获取
        @param end_tmsp:
        @param start_tmsp:
        @return:
        """
        url_temp = "https://fsapi.gold.org/api/goldprice/v11/chart/price/usd/oz/{},{}?cache"
        ok_url = url_temp.format(int(start_tmsp), int(end_tmsp))
        return self.get_data_by_url(ok_url)

    def get_daily(self) -> str:
        """
        :return:
        """
        url_temp = "https://fsapi.gold.org/api/goldprice/v11/chart/price/usd/oz/{},{}?cache"
        # https://fsapi.gold.org/api/goldprice/v11/chart/price/usd/oz/1690719405089,1690805816601?cache

        # 美国东部时区的时间
        us_eastern_dt = datetime.now(tz=tz_info)
        end_date = us_eastern_dt.strftime('%Y%m%d%H%M%S')
        # datatime 模块的时间戳以秒计
        end_ts = us_eastern_dt.timestamp()

        start_ts = end_ts - 86402
        start_date = datetime.fromtimestamp(start_ts, tz=tz_info).strftime('%Y%m%d%H%M%S')

        # send requests， 请求中的时间戳以毫秒计
        ok_url = url_temp.format(start_ts * 1e3, end_ts * 1e3)
        return self.get_data_by_url(ok_url)

    def get_data_by_url(self, url) -> str:
        session = HTMLSession()
        resp: requests.Response = session.get(url)
        json_data = resp.json()

        df = json_to_df(json_data)
        parnt_str = r'https://fsapi.gold.org/api/goldprice/v11/chart/price/usd/oz/(\d*),(\d+)\?cache'
        mt = re.match(parnt_str, url)
        if mt.group(1):
            start_date = datetime.fromtimestamp(int(mt.group(1)) / 1000).strftime('%Y%m%d%H%M%S')
        else:
            start_date = '19700101000000'
        end_date = datetime.fromtimestamp(int(mt.group(2)) / 1000).strftime('%Y%m%d%H%M%S')
        csv_name = '{}_{}.csv'.format(start_date, end_date)
        csv_path = os.path.join('./data/', csv_name)
        save_json(json_data, csv_path.replace('.csv', '.json'))
        csv_path = df_to_csv(df, csv_path)
        return csv_path


def time_worker():
    crawler = Crawler('', '')
    csv_path = crawler.get_daily()

    csv_names = get_csv_names()
    new_csv = concat_csv(csv_names)

    logger.info(csv_path)
    # 这里要再次使用, 不然要退出
    loop_monitor()


def loop_monitor():
    s = sched.scheduler(time.time, time.sleep)  # 生成调度器
    logger.info('loop_monitor')
    # s.enter(3600 * 24, 1, time_worker, (crawler, ))
    s.enter(3600, 1, time_worker, ())
    s.run()
    logger.info('s.run')


if __name__ == '__main__':
    # https://www.gold.org/goldhub/data/gold-prices 为原始页面
    # url2 为表格接口的数据
    # url = "https://fsapi.gold.org/api/goldprice/v11/chart/main?cache&period=Max"

    # Gold prices
    # 2022-08-01_2023-07-28
    url2 = "https://fsapi.gold.org/api/goldprice/v11/chart/price/usd/oz/1682840342384,1690789144720?cache"
    url3 = "https://fsapi.gold.org/api/goldprice/v11/chart/price/usd/oz/1690709142748,1690795545188?cache"

    # Crawler
    # crawler = Crawler('2023-05-02_2023-07-28', url2)
    # url = 'https://fsapi.gold.org/api/goldprice/v11/chart/price/usd/oz/1690644325034,1691249127107?cache'
    # csv_path = crawler.get_data_by_url(url)
    # print(csv_path)

    # 获取历史数据
    crawler = Crawler()
    csv_paths = crawler.get_history_date()
    print(csv_paths)


    # loop = asyncio.new_event_loop()
    # print("Running...")
    # task = loop.create_task(crawler.crawlerInit())
    # loop.run_until_complete(task)
    # print("Finished!")
    # res = task.result()

    # crawler.get_daily()

    # loop_monitor()
