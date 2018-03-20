# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
import json
from zhihu.items import PeopleItem

class ZhihuScrapySpider(scrapy.Spider):
    name = 'zhihu_scrapy'
    user_item_list = []
    allowed_domains = ['www.zhihu.com']
    #开始运行的用户名
    user_name = "guan-jian-ming"
    include = "data%5B*%5D.answer_count%2Carticles_count%2Cgender%2Cfollower_count%2Cis_followed%2Cis_following%2Cbadge%5B%3F(type%3Dbest_answerer)%5D.topics&offset=0&limit=20"
    follows_url = "https://www.zhihu.com/api/v4/members/{user}/followees?include={include}&offset={offset}&limit={limit}"
    follows_query = "data%5B*%5D.answer_count%2Carticles_count%2Cgender%2Cfollower_count%2Cis_followed%2Cis_following%2Cbadge%5B%3F(type%3Dbest_answerer)%5D.topics"
    user_url = 'https://www.zhihu.com/api/v4/members/{user}/followees?include={include}'
    # followers_url是获取粉丝列表信息的url地址，followers_query存储的为查询参数。
    followers_url = "https://www.zhihu.com/api/v4/members/{user}/followers?include={include}&offset={offset}&limit={limit}"
    followers_query = "data%5B*%5D.answer_count%2Carticles_count%2Cgender%2Cfollower_count%2Cis_followed%2Cis_following%2Cbadge%5B%3F(type%3Dbest_answerer)%5D.topics"
    user_query = "locations,employments,gender,educations,business,voteup_count,thanked_Count,follower_count,following_count,cover_url,following_topic_count,following_question_count,following_favlists_count,following_columns_count,avatar_hue,answer_count,articles_count,pins_count,question_count,columns_count,commercial_question_count,favorite_count,favorited_count,logs_count,marked_answers_count,marked_answers_text,message_thread_token,account_status,is_active,is_bind_phone,is_force_renamed,is_bind_sina,is_privacy_protected,sina_weibo_url,sina_weibo_name,show_sina_weibo,is_blocking,is_blocked,is_following,is_followed,mutual_followees_count,vote_to_count,vote_from_count,thank_to_count,thank_from_count,thanked_count,description,hosted_live_count,participated_live_count,allow_message,industry_category,org_name,org_homepage,badge[?(type=best_answerer)].topics"
    start_urls = []

    def start_requests(self):
        yield Request(self.user_url.format(user=self.user_name, include=self.include), callback=self.parse_user)
        yield Request(self.follows_url.format(user=self.user_name, include=self.follows_query, offset=0, limit=20),
                      callback=self.parse_follows)
        yield Request(self.followers_url.format(user=self.user_name, include=self.followers_query, offset=0, limit=20),
                  callback=self.parse_followers)

    def parse_user(self, response):
        json_data = json.loads(response.text)
        user_list = json_data['data']
        for user in user_list:
            yield(self.do_parse_user(user))

    def do_parse_user(self,user):
        user_item = PeopleItem()
        for item in user_item.fields:
            user_item[item] = user[item]
        return user_item

    def parse_follows(self, response):
        results = json.loads(response.text)
        if 'data' in results.keys():
            for result in results.get('data'):
                yield Request(self.user_url.format(user=result.get("url_token"), include=self.user_query),
                              callback=self.parse_user)

        # 这里判断page是否存在并且判断page里的参数is_end判断是否为False，如果为False表示不是最后一页，否则则是最后一页
        if 'page' in results.keys() and results.get('is_end') == False:
            next_page = results.get('paging').get("next")
            # 获取下一页的地址然后通过yield继续返回Request请求，继续请求自己再次获取下页中的信息
            yield Request(next_page, self.parse_follows)

    def parse_followers(self, response):
        '''
        这里其实和关乎列表的处理方法是一样的
        用户粉丝列表的解析，这里返回的也是json数据 这里有两个字段data和page，其中page是分页信息
        :param response:
        :return:
        '''
        results = json.loads(response.text)

        if 'data' in results.keys():
            for result in results.get('data'):
                yield Request(self.user_url.format(user=result.get("url_token"), include=self.user_query),
                              callback=self.parse_user)

        # 这里判断page是否存在并且判断page里的参数is_end判断是否为False，如果为False表示不是最后一页，否则则是最后一页
        if 'page' in results.keys() and results.get('is_end') == False:
            next_page = results.get('paging').get("next")
            # 获取下一页的地址然后通过yield继续返回Request请求，继续请求自己再次获取下页中的信息
            yield Request(next_page, self.parse_followers)
