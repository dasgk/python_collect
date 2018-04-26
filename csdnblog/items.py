# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class CsdnblogItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class ArticleUrlItem(scrapy.Item):
    article_url = scrapy.Field()


class UserUrlItem(scrapy.Item):
    user_url = scrapy.Field()

class ArticleDetailInfo(scrapy.Item):
    title = scrapy.Field()
    post_time = scrapy.Field()
    content = scrapy.Field()
    author = scrapy.Field()
    look_num = scrapy.Field()

