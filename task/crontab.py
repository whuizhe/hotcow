# coding=utf-8
"""定时任务"""

import requests
import logging
import asyncio
from apscheduler.schedulers.asyncio import AsyncIOScheduler


logging.basicConfig()
logging.getLogger('apscheduler').setLevel(logging.DEBUG)


def tick(url):
    for i in url:
        try:
            url_open = requests.get(f'http://127.0.0.1:32080/{i}', timeout=30)
            logging.info(f'URL:{i} {url_open.text}')
        except Exception as e:
            logging.error(f'URL:{i} Error:{e}')


if __name__ == '__main__':
    scheduler = AsyncIOScheduler()
    scheduler.add_job(
        tick, trigger='cron', args=([
                                        'basis/concept/',   # 拉取概念域名
                                        'basis/codeinfo/',  # 拉取基础数据
                                        'basis/mainflows/'  # 资金流向历史
                                    ], ), hour='20, 7', name='基础'
    )
    scheduler.add_job(
        tick, trigger='cron', args=(['basis/historydeals/'], ), hour='16,19', name='历史交易'
    )
    scheduler.add_job(
        tick, trigger='cron', args=([
                                        'basis/mainflowscurr/',  # 当天交易量
                                        'basis/mainflows/?code=1'  # 资金流向当天
                                    ], ), hour='16,19', minute='30', name='当天数据'
    )
    scheduler.add_job(
        tick, trigger='cron', args=(['intraday/turnover/'], ), hour='9-15', second='*/30', name='历史交易'
    )

    scheduler.start()

    try:
        asyncio.get_event_loop().run_forever()
    except (KeyboardInterrupt, SystemExit) as e:
        logging.error(f'Error:{e}')
