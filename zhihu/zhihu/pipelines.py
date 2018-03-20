# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


class PeoplePipeline(object):
    def process_item(self, item, spider):
        with open("my_meiju.txt", 'a') as fp:
            for single_item in item:
                fp.write(single_item + ":" + str(item[single_item])+"\t")
            fp.write("\r\n")


