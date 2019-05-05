#!/usr/bin/env python
# -*- coding=utf-8 -*-

from scrapy import cmdline

import schedule
import threading
import multiprocessing


def run_thread(job_func):
    job_thread = threading.Thread(target=job_func)
    job_thread.start()


def run_process(job_func):
    job_process = multiprocessing.Process(target=job_func)
    #job_process.daemon = True
    job_process.start()


def job_lianjia():
    cmdline.execute('scrapy crawl spider_lianjia'.split())


def job_5i5j():
    cmdline.execute('scrapy crawl spider_5i5j'.split())


def run():
    schedule.every().day.at("00:01").do(run_process, job_lianjia)
    schedule.every().day.at("00:02").do(run_thread, job_5i5j)
    #schedule.every().minute.do(run_thread, job_lianjia)
    
    while True:
        schedule.run_pending()


if __name__ == '__main__':
    
    #run()
    run_process(job_lianjia)
    run_process(job_5i5j)
   

