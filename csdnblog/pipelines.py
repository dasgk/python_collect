# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from csdnblog.items import ArticleUrlItem
from csdnblog.items import UserUrlItem
from csdnblog.items import ArticleDetailInfo
from csdnblog.csdnblogredis import CsdnBlogRedis
import redis
import os
from csdnblog.csdnblogmysql import CsdnBlogMySql


class CsdnblogPipeline(object):
    def process_item(self, item, spider):
        if isinstance(item, ArticleUrlItem):
            #准备写入redis
            isset = CsdnBlogRedis.redis_sismember('used_article_list', item['article_url'])
            if isset == 0:
                CsdnBlogRedis.redis_sadd('article_list', item['article_url'])
        if isinstance(item, UserUrlItem):
            #处理用户url,如果不在used_user_list当中才会放在user_list里面
            isset = CsdnBlogRedis.redis_sismember('used_user_list', item['user_url'])
            if isset == 0:
                CsdnBlogRedis.redis_sadd('user_list', item['user_url'])
        if isinstance(item, ArticleDetailInfo):
            CsdnBlogMySql.mysql_insert(item['title'],item['author'],item['post_time'], item['content'],item['look_num'])
