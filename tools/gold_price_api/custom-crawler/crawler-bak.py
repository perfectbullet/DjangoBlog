# Import Packages
import asyncio
import csv
from datetime import datetime

import pyppeteer
from requests_html import AsyncHTMLSession


class Crawler:
    def __init__(self, currency):
        self.currency = currency

    async def crawlerInit(self):
        print(f"Starting File... {self.currency}")

        # Timestamp
        now = datetime.now()
        print("Date success!")

        # Params
        url = f"https://www.gold.org/goldhub/data/gold-prices"
        url2 = "https://fsapi.gold.org/api/goldprice/v11/chart/main?cache&period=1y"
        print("Parameters success!")

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
        r = await session.get(url2)
        print("Starting session!")
        # script = """
        #     () => {
        #         if ( jQuery.isReady ) {
        #             $("[data-currency='%s']").click();
        #         }
        #     }
        # """ % (self.currency)

        #
        # script = """
        #             () => {
        #                 if( document.readyState === "complete") {
        #                     ("[data-currency="%s"]").click();
        #             }
        #             }
        #         """ % (self.currency)
        # print('script ', script)
        await r.html.arender(wait=4, sleep=4, timeout=200, keep_page=True)
        # await r.html.arender(script=script, wait=4, sleep=4, timeout=200, keep_page=True)

        print("Session started!")

        # Scraper
        print("Grabbing price!")
        xau = r.html.find('.text.value', first=True)
        print(f"{self.currency} {xau.text}")

        r.close()
        await session.close()

        # Result To CSV
        with open("../data/customprices.csv", "a+", newline="") as f:
            writer = csv.writer(f, delimiter=",")
            writer.writerow([now, self.currency, xau.text.replace(",", "")])

        print("File Success!")

        return {
            'currency': self.currency,
            'price': xau.text.replace(",", ""),
        }


if __name__ == '__main__':
    data = {'currency': 'USD'}

    # Crawler
    loop = asyncio.new_event_loop()
    print("Running...")
    crawler = Crawler(str(data['currency']))
    task = loop.create_task(crawler.crawlerInit())
    loop.run_until_complete(task)
    print("Finished!")

    res = task.result()
