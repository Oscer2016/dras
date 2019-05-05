# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DrasItem(scrapy.Item):

    title = scrapy.Field()
    detail = scrapy.Field()
    city = scrapy.Field()
    region = scrapy.Field()
    area = scrapy.Field()
    scale = scrapy.Field()
    floor = scrapy.Field()
    direction = scrapy.Field()
    price = scrapy.Field()
    picture = scrapy.Field()
    pubdate = scrapy.Field()
    source = scrapy.Field()
    collection = scrapy.Field()
    timestamp = scrapy.Field()

