# coding=utf-8
"""定时任务"""

import requests
import logging
from apscheduler.schedulers.blocking import BlockingScheduler

logging.basicConfig()
logging.getLogger('apscheduler').setLevel(logging.DEBUG)


def tick(url):
    try:
        url_open = requests.get(f'http://127.0.0.1:32080/{url}', timeout=30)
        print(f'URL:{url} {url_open.text}')
    except Exception as e:
        print(f'URL:{url} Error:{e}')


if __name__ == '__main__':
    scheduler = BlockingScheduler()
    scheduler.add_executor('processpool')
    scheduler.add_job(tick, trigger='cron', args=('basisdata/', ), hour='16,20', name='基础')
    scheduler.add_job(tick, trigger='cron', args=('skoptional/slowcow/', ), hour='17,23', name='交易')

    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit) as e:
        print(f'Error:{e}')
