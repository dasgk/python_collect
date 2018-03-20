# -*- coding: gbk -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


class PeoplePipeline(object):
    def process_item(self, item, spider):
        with open("my_meiju.txt", 'a') as fp:
            for single_item in item:
                gb18030TypeStr = single_item.encode("GBK", 'ignore')
                gb18030TypeStr = gb18030TypeStr.decode("GBK")
                value = str(item[single_item]).encode("GBK", 'ignore')
                value = value.decode("GBK")
                fp.write(str(gb18030TypeStr) + ":" + str(value)+"\t")
            fp.write("\r\n")


