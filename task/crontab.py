# coding=utf-8
"""定时任务"""

import requests
import logging
import asyncio
from apscheduler.schedulers.asyncio import AsyncIOScheduler


logging.basicConfig()
logging.getLogger('apscheduler').setLevel(logging.DEBUG)


def tick(url):
    try:
        url_open = requests.get(f'http://127.0.0.1:32080/{url}', timeout=30)
        logging.info(f'URL:{url} {url_open.text}')
    except Exception as e:
        logging.error(f'URL:{url} Error:{e}')


if __name__ == '__main__':
    scheduler = AsyncIOScheduler()
    scheduler.add_job(
        tick, trigger='cron', args=('basis/codeinfo/', ), hour='23, 5', name='基础'
    )
    scheduler.add_job(
        tick, trigger='cron', args=('basis/historydeals/', ), hour='16,19', name='历史交易'
    )
    scheduler.add_job(
        tick, trigger='cron', args=('basis/mainflowscurr/', ), hour='16,19', minute='30', name='当天交易量'
    )
    scheduler.add_job(
        tick, trigger='cron', args=('basis/mainflows/?code=1', ), hour='16,19', minute='50', name='资金流向当天'
    )
    scheduler.add_job(
        tick, trigger='cron', args=('basis/mainflows/', ), hour='3,6', name='资金流向历史'
    )
    scheduler.start()

    try:
        asyncio.get_event_loop().run_forever()
    except (KeyboardInterrupt, SystemExit) as e:
        logging.error(f'Error:{e}')
