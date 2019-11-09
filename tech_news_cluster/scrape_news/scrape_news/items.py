# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class ScrapeNewsItem(scrapy.Item):
    title = scrapy.Field()
    date = scrapy.Field()
    summary = scrapy.Field()
    publication = scrapy.Field()
    author = scrapy.Field()
    date = scrapy.Field()
    url = scrapy.Field()
    content = scrapy.Field()
    pass
