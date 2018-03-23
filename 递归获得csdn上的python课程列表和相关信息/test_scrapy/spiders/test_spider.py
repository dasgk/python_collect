# -*- coding: utf-8 -*-
import scrapy
import re
from bs4 import BeautifulSoup
from test_scrapy.items import TestScrapyItem

class TestSpiderSpider(scrapy.Spider):
    max_item_per_page = 20 #每一个页面最多有20个课程
    name = 'test_spider'
    current_page = 1
    allowed_domains = ['https://edu.csdn.net']
    start_urls = ['https://edu.csdn.net/courses/o280_s355_k%E7%BC%96%E7%A8%8B%E8%AF%AD%E8%A8%80_Python']

    def start_requests(self):
        yield scrapy.Request(self.start_urls[0], callback=self.parse)

    def parse_course(self,response):
        title = response.meta['title']
        author = response.meta['author']
        price = response.meta['price']
        soup = BeautifulSoup(response.text, 'lxml')
        for_who = soup.find('div',attrs={
            'class':'forwho'
        })
        for_people = for_who.find('span',attrs={
            'class':'for'
        })
        #适合人群
        for_people = for_people.text
        course_desc = soup.find('div', attrs={
            'class':'outline_discribe_box J_outline_discribe_box'
        })
        course_desc = course_desc.text
        item = TestScrapyItem()
        item['title'] = title
        item['author'] = author
        item['price'] = price
        item['for_people'] = for_people
        item['course_desc'] = course_desc
        yield item

    def parse(self, response):
        soup = BeautifulSoup(response.text,"lxml")
        course_list = soup.find_all('div', attrs={
            "class":"course_dl_list"
        })
        for course in course_list:
            author = course.p.text[len("讲师："):]
            href = course.a.get('href')
            title = course.div.span.text
            price_str = course.select(".clearfix")[0].i.text
            price = re.findall(r"￥(\d+)",price_str)
            if len(price) == 0:
                price = '免费'
            else:
                price = price[0]
            currnet_course_item = {
                "title": title,
                'author':author,
                'price':price,
                'href': href
            }
            #处理单个课程的信息
            yield scrapy.Request(href, callback=self.parse_course, meta=currnet_course_item,dont_filter=True)
        #获得下一页的地址，进行处理
        self.current_page = self.current_page + 1
        print(self.start_urls[0]+'/p'+str(self.current_page))
        if len(course_list) != 0:
            print("正在处理第"+str(self.current_page)+"页")
            yield scrapy.Request(self.start_urls[0]+'/p'+str(self.current_page), callback=self.parse,dont_filter=True)