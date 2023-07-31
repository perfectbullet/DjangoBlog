import asyncio
import json
import os.path
import time
from datetime import datetime
import requests
import pyppeteer
import pytz
from requests_html import AsyncHTMLSession, HTMLSession
from data_utils import json_to_df, df_to_csv, save_json
from loguru import logger


class Crawler:
    def __init__(self, name, url):
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

    def get_daily(self) -> str:
        """
        :return:
        """
        tz_info = pytz.timezone("America/New_York")
        url_temp = "https://fsapi.gold.org/api/goldprice/v11/chart/price/usd/oz/{},{}?cache"
        # https://fsapi.gold.org/api/goldprice/v11/chart/price/usd/oz/1690719405089,1690805816601?cache

        # 美国东部时区的时间
        us_eastern_dt = datetime.now(tz=tz_info)
        end_date = us_eastern_dt.strftime('%Y%m%d%H%M%S')
        # datatime 模块的时间戳以秒计
        end_ts = us_eastern_dt.timestamp()

        start_ts = end_ts - 86402
        start_date = datetime.fromtimestamp(start_ts).strftime('%Y%m%d%H%M%S')

        # send requests， 请求中的时间戳以毫秒计
        ok_url = url_temp.format(start_ts * 1e3, end_ts * 1e3)
        session = HTMLSession()
        resp: requests.Response = session.get(ok_url)
        json_data = resp.json()

        df = json_to_df(json_data)
        csv_name = '{}_{}.csv'.format(start_date, end_date)
        csv_path = os.path.join('../data/', csv_name)
        save_json(json_data, csv_path.replace('.csv', '.json'))
        csv_path = df_to_csv(df, csv_path)
        return csv_path


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

    # loop = asyncio.new_event_loop()
    # print("Running...")
    # task = loop.create_task(crawler.crawlerInit())
    # loop.run_until_complete(task)
    # print("Finished!")
    # res = task.result()

    crawler = Crawler('', '')
    crawler.get_daily()
