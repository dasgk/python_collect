# -*- coding: utf-8 -*-
import scrapy
from scrapy_redis.spiders import RedisSpider
from lxml import etree
import re
from csdnblog.items import ArticleUrlItem
from csdnblog.items import UserUrlItem
from csdnblog.csdnblogredis import CsdnBlogRedis
from scrapy.http import Request
import redis
from scrapy.utils.project import get_project_settings

class BlogSpider(RedisSpider):
    # 根据用户url获得文章列表
    name = 'myspider'
    redis_key = 'user_list'
    allowed_domains = ['blog.csdn.net/dasgk']

    def get_next_page_url(self, url, ori_url):
        #page默认是2
        page = 2
        #获得用户名，获得ori_url的username参数
        username = re.findall(r"https://my.csdn.net/my/home/get_user_blog?username=(.+?)&page=", ori_url)
        if len(username) == 0:
            username = ''
        #如果获取失败，则获取最后一个my.csdn.net/后面的参数
        if username.strip() == '':
            username = re.findall(r"https://my.csdn.net/(.+)", ori_url)
        if (len(username) == 1):
            username = username[0]
        else:
            #没有找到用户名返回空
            return ''
        #获得页码page
        raw_page = re.split("/", str(url[0]))
        if len(raw_page) == 2:
            page = raw_page[1]
        #拼接参数https://my.csdn.net/my/home/get_user_blog?username=[用户名]&page=[页码]
        next_url = 'https://my.csdn.net/my/home/get_user_blog?username=' + username +"&page="+page
        #返回链接
        return next_url

    def parse(self, response):
        CsdnBlogRedis.redis_sadd('used_user_url', response.url)
        result = re.findall(r"username", response.url)
        if (len(result) == 1):
            #处理的是分页后的操作
            str_text = response.text
            str_text = str_text.replace('\n', '')
            str_text = str_text.replace("'""'", '"')
            if type(str_text) is bytes:
                str_text = str_text.decode('unicode_escape')
            else:
                if type(str_text) is str:
                    str_text = str_text.encode('utf8').decode('unicode_escape')
            str_text = str_text.replace('\\', '')
            e_tree = etree.HTML(str_text)
            li_list = e_tree.xpath('//*/li/a/@href')
            for li in li_list:
                CsdnBlogRedis.redis_sadd('article_list', li)
            #获得下一页
            next_page = e_tree.xpath('//*[@class="btn btn-xs btn-default btn-next"]/@href')
            page = 3
            if len(next_page) == 1:
                #说明有下一页
                raw_page = re.split("/", str(next_page[0]))
                if len(raw_page) == 2:
                    page = raw_page[1]
                url = response.url
                url_raw = re.split('page=',url)
                url_prefix = url_raw[0]
                url = url_prefix + "page=" + str(page)
                user_item = UserUrlItem()
                user_item['user_url'] = url
                yield user_item
            else:
                print('当前用户博客查找完毕')
        else:
            e_tree = etree.HTML(response.text)
            li_list = e_tree.xpath('//*[@id="divResources"]/div[1]/li/a/@href')
            for item in li_list:
                #根据正则表达式，匹配article/details/，匹配上了表示是文章详情，否则丢弃
                match = re.match(r'(\S)*/article/details(\S)*',item)
                if match:
                    #文章详情的URL
                    article = ArticleUrlItem()
                    article['article_url'] = item
                    yield article
                else:
                    print('没匹配到')
            #找到下一页的url
            next_page = e_tree.xpath('//*[@id="divResources"]/div[1]/div/a[last()]/@href')
            #加入user_list列表
            if(len(next_page) == 1):
                user_item = UserUrlItem()
                user_item['user_url'] = self.get_next_page_url(next_page, response.url)
                yield user_item
            #开始查找当前用户的关系网
            force_list = e_tree.xpath('//*[@class="focus"]/div/a/@href')
            for li in force_list:
                user_item = UserUrlItem()
                user_item['user_url'] = 'https://my.csdn.net/'+li
                yield user_item
            beforce_list = e_tree.xpath('//*[@class="focus beFocus"]/div/a/@href')
            for li in beforce_list:
                user_item = UserUrlItem()
                user_item['user_url'] = 'https://my.csdn.net/' + li
                yield user_item

