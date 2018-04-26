# -*- coding: utf-8 -*-
import scrapy
from scrapy_redis.spiders import RedisSpider
from lxml import etree
from bs4 import BeautifulSoup
import re
from csdnblog.items import ArticleUrlItem
from csdnblog.items import UserUrlItem
from csdnblog.csdnblogredis import CsdnBlogRedis
import os
from csdnblog.items import ArticleDetailInfo

class ArticleSpider(RedisSpider):
    # 根据用户url获得文章列表
    name = 'myspider'
    redis_key = 'article_list'
    allowed_domains = ['blog.csdn.net/dasgk']
    def parse(self, response):
        soup = BeautifulSoup(response.text, 'lxml')
        title = soup.find(attrs={'class':'csdn_top'})
        time = soup.find(attrs={'class':'time'})
        content = soup.find(attrs={'id':'article_content'})
        author = soup.find(attrs={'id':'uid'})
        look_num = soup.find(attrs={'class':'btn-noborder'})
        article = ArticleDetailInfo()
        if title is None:
            title = soup.find(attrs={'class':'article_title'})
            if title is None:
                article['title'] = '未知'
            else:
                article['title'] = title.text
        else:
            article['title'] = title.text
        if look_num is None:
            look_num = soup.find(attrs={'class': 'link_view'})
            if look_num is None:
                article['look_num'] = 1
            else:
                article['look_num'] = look_num.text
        else:
            article['look_num'] = look_num.text
        if time is None:
            time = soup.find(attrs={'class': 'link_postdate'})
            if time is None:
                article['post_time'] = '未知'
            else:
                article['post_time'] = time.text
        else:
            article['post_time'] = time.text
        article['content'] = content.text
        if content is None:
            return
        article['content'] = article['content'].replace('"', '')
        article['content'] = article['content'].replace("'", "")
        article['author'] = author.text
        yield article
