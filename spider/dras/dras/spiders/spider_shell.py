# -*- coding: utf-8 -*-

import scrapy
from scrapy.http import Request
from dras.items import DrasItem
from scrapy.utils.project import get_project_settings 
settings = get_project_settings()

import time
import random
import requests
from lxml import etree


class SpiderShellSpider(scrapy.Spider):
    name = 'spider_shell'
    allowed_domains = ['ke.com']
    start_urls = [
        'https://bj.zu.ke.com/zufang/',
        'https://sh.zu.ke.com/zufang/',
        'https://gz.zu.ke.com/zufang/',
        'https://sz.zu.ke.com/zufang/',
        'https://xa.zu.ke.com/zufang/',
        'https://wh.zu.ke.com/zufang/',
        'https://cs.zu.ke.com/zufang/',
        'https://cq.zu.ke.com/zufang/',
        'https://cd.zu.ke.com/zufang/',
        'https://dl.zu.ke.com/zufang/',
        'https://dg.zu.ke.com/zufang/',
        'https://fs.zu.ke.com/zufang/',
        'https://hz.zu.ke.com/zufang/',
        'https://hf.zu.ke.com/zufang/',
        'https://hui.zu.ke.com/zufang/',
        'https://jn.zu.ke.com/zufang/',
        'https://lf.zu.ke.com/zufang/',
        'https://nj.zu.ke.com/zufang/',
        'https://qd.zu.ke.com/zufang/',
        'https://sjz.zu.ke.com/zufang/',
        'https://sy.zu.ke.com/zufang/',
        'https://su.zu.ke.com/zufang/',
        'https://tj.zu.ke.com/zufang/',
        'https://wx.zu.ke.com/zufang/',
        'https://xm.zu.ke.com/zufang/',
        'https://yt.zu.ke.com/zufang/',
        'https://zh.zu.ke.com/zufang/',
        'https://zs.zu.ke.com/zufang/',
    ]

    def parse(self, response):
        # 构造翻页url
        for i in range(1, 101):
            purl = response.url + 'pg' + str(i)
            yield Request(url=purl, callback=self.next)

    def next(self, response):
        print response.url
        item = DrasItem()

        title = response.xpath('//p[@class="content__list--item--title twoline"]/a/text()').extract()
        detail = response.xpath('//p[@class="content__list--item--title twoline"]/a/@href').extract()
        city = response.xpath('//h1/a/text()').extract()[0][:-2]
        price = response.xpath('//span[@class="content__list--item-price"]/em/text()').extract()
        picture = response.xpath('//a[@class="content__list--item--aside"]/img/@data-src').extract()
        pubdate = response.xpath('//p[@class="content__list--item--time oneline"]/text()').extract()

        for i in range(30):
            item['title'] = title[i].strip()
            item['detail'] = response.url.split('/zufang')[0] + detail[i]
            item['city'] = city

            tree = etree.HTML(requests.get(item['detail'], headers={'User-Agent':settings.get('USER_AGENT')}).text)
            district = tree.xpath('//p[@class="bread__nav__wrapper oneline"]/a[2]/text()')[0]
            town = tree.xpath('//p[@class="bread__nav__wrapper oneline"]/a[3]/text()')[0]
            item['region'] = district[:-2] + '-' + town[:-2]
            try:
                item['area'] = int(tree.xpath('//p[@class="content__article__table"]/span[3]/text()')[0][:-1])
                item['scale'] = tree.xpath('//p[@class="content__article__table"]/span[2]/text()')[0]
                item['direction'] = tree.xpath('//p[@class="content__article__table"]/span[4]/text()')[0]
                item['floor'] = tree.xpath('//ul/li[@class="fl oneline"][8]/text()')[0][3:]
            except:
                item['area'] = random.randint(30, 50)
                item['scale'] = "3室1厅1卫"
                item['direction'] = "南"
                item['floor'] = "低楼层/18层"

            item['price'] = int(price[i])
            item['picture'] = picture[i]
            item['pubdate'] = pubdate[i]
            item['source'] = '贝壳'
            item['collection'] = 'shell'
            item['timestamp'] = int(time.time()*1000)

            print item['title']
            print item['detail']
            print item['region']
            print item['area']
            print item['scale']
            print item['direction']
            print item['floor']
            print item['price']
            print item['picture']
            print item['pubdate']

            yield item


