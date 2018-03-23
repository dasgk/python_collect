# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from test_scrapy.items import  TestScrapyItem

class TestScrapyPipeline(object):
    def process_item(self, item, spider):
        with open("json.txt", 'a+') as handle:
            for single in item:
                handle.write(single+":"+item[single]+"\n")
            handle.write("\r\n")
        #return item
