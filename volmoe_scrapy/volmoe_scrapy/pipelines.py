# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import re

class VolmoeScrapyPipeline(object):
    def process_item(self, item, spider):
        # 数据处理
        item["desc"] = self.process_desc(item["desc"])
        item["filesize"] = self.process_desc(item["filesize"])
        #看
        print(item)
        return item

    def process_desc(self,content):
        content = re.sub(r"\xa0|\s|\n|\r","",content)
        return content
