# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class BookItem(scrapy.Item):
    id = scrapy.Field()
    name = scrapy.Field()
    author = scrapy.Field()
    category = scrapy.Field()
    last_update = scrapy.Field()
    img_url = scrapy.Field()


class BookDetail(scrapy.Item):
    id = scrapy.Field()
    label = scrapy.Field()
    all_click = scrapy.Field()
    month_click = scrapy.Field()
    week_click = scrapy.Field()
    all_popular = scrapy.Field()
    month_popular = scrapy.Field()
    week_popular = scrapy.Field()
    all_commend = scrapy.Field()
    month_commend = scrapy.Field()
    week_commend = scrapy.Field()
    word_num = scrapy.Field()
    comment_num = scrapy.Field()
    status = scrapy.Field()
