# -*- coding: utf-8 -*-

import scrapy
from scrapy.http import Request
from dras.items import DrasItem


class SpiderZiroomSpider(scrapy.Spider):
    name = 'spider_ziroom'
    allowed_domains = ['ziroom.com']
    start_urls = [
        'http://www.ziroom.com/z/nl/z3.html',
        #'http://sh.ziroom.com/z/nl/z3.html',
        #'http://sz.ziroom.com/z/nl/z3.html',
        #'http://hz.ziroom.com/z/nl/z3.html',
    ]

    def parse(self, response):
        # 构造翻页url
        for i in range(50):
            purl = response.url + '?p=' + str(i+1)
            yield Request(url=purl, callback=self.next)

    def next(self, response):
        print response.url
        item = DrasItem()
        title = response.xpath('//div[@class="txt"]/h3/a/text()').extract()
        detail = response.xpath('//div[@class="txt"]/h3/a/@href').extract()
        #region = response.xpath('//div[@class="detail"]/p[2]/span/text()').extract()
        area = response.xpath('//div[@class="detail"]/p[1]/span[1]/text()').extract()
        #price = response.xpath()
        picture = response.xpath('//div[@class="img pr"]/a/img/@_src').extract()
        region = response.xpath('//div[@class="img pr"]/a/img/@alt').extract()
        #pubdate = response.xpath()

        for i in range(18):
            item['title'] = title[i]
            item['detail'] = detail[i]
            item['region'] = region[i]
            item['area'] = area[i]
            item['price'] = ''
            item['picture'] = picture[i]
            item['pubdate'] = ''
            item['source'] = '自如'
            item['collection'] = 'ziroom'

            print item['title']
            print item['detail']
            print item['region']
            print item['area']
            print item['picture']

            yield item


