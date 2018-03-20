# -*- coding: utf-8 -*-
import scrapy
import json
from zhihu.items import PeopleItem

class ZhihuScrapySpider(scrapy.Spider):
    name = 'zhihu_scrapy'
    user_item_list = []
    allowed_domains = ['www.zhihu.com']
    start_urls = ['https://www.zhihu.com/api/v4/members/guan-jian-ming/followees?include=data%5B*%5D.answer_count%2Carticles_count%2Cgender%2Cfollower_count%2Cis_followed%2Cis_following%2Cbadge%5B%3F(type%3Dbest_answerer)%5D.topics&offset=0&limit=20']
    def parse(self, response):
        json_data = json.loads(response.text)
        user_list = json_data['data']
        for user in user_list:
            yield(self.parse_user(user))
    def parse_user(self,user):
        user_item = PeopleItem()
        for item in user_item.fields:
            user_item[item] = user[item]
        return user_item
