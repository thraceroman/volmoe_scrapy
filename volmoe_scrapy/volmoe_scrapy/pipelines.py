# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import re
# 这里如果用image或file,那就要导入相应模块,并且重写get media requests和item completed方法
# image是基于pillow这个图片库的,需要先下载
# 如果想更改每张图的名字,重写file path方法
# 参考 https://blog.csdn.net/sc_lilei/article/details/79587698?utm_source=distribute.pc_relevant.none-task

from scrapy.pipelines.images import ImagesPipeline
from scrapy.http import Request
from scrapy.exceptions import DropItem
import requests
import os

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

# 传的是ImagesPipeline对象
class PhScrapyPipeline(ImagesPipeline):
    def get_media_requests(self,item,info):
        for image_url in item['image_urls']:
            # 这里用的scrapy.http的Request
            yield Request(
                image_url,
                meta={'item':item})

    def file_path(self,request,response=None,info=None):
        image_name = request.meta['item']['image_name']
        # 这里的意思?在哪里进行图片目录的存储呢,可以用相对的,也能是绝对路径,
        # 注意!!!!无论是绝对路径还是相对路径!都需要在settings中进行IMAGES_STORE设置
        # path = 'full/' +image_name+ '/' + request.url[-7:]
        path = 'D:\\code\\photo\\' +image_name+ '\\' + request.url[-7:]
        return path

    def item_completed(self,results,item,info):
        image_path = [x['path'] for ok,x in results if ok]
        if not image_path:
            raise DropItem('Item contains no images')
        item['image_paths'] = image_path
        # print(item)
        return item


# class VodtagScrapyPipeline(object):
#     def process_item(self, item, spider):
#         # 数据处理,原始形式,存的比较慢
#         img_file = 'D:\\code\\photo\\' + item['title'] +'.jpg'
#         img = requests.get(item['img'])
#         with open(img_file,'wb') as img_out:
#             img_out.write(img.content)
#         print(item['title'])
#         # https://play2.172cat.com/201910/31/ztqee2kf/index.m3u8
#         # https://play2.172cat.com/201910/31/ztqee2kf/500kb/hls/index.m3u8
#         return item
class VodtagScrapyPipeline(ImagesPipeline):
    # 以框架的形式,秒存,但是!item需要先写好
    def get_media_requests(self,item,info):
        yield Request(
            item['image_urls'],
            meta={'item':item})

    def file_path(self,request,response=None,info=None):
        image_name = request.meta['item']['title']
        # 这里的意思?在哪里进行图片目录的存储呢,可以用相对的,也能是绝对路径,
        # 注意!!!!无论是绝对路径还是相对路径!都需要在settings中进行IMAGES_STORE设置
        # path = 'full/' +image_name+ '/' + request.url[-7:]
        path = 'D:\\code\\photo\\' +image_name+ '.jpg'
        return path
   