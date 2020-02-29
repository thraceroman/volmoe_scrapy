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


class VodtagScrapyPipeline(object):
    def process_item(self, item, spider):
        # 数据处理
        # img_file = 'D:\\code\\photo\\' + item['title'][:10] +'.jpg'
        # img = requests.get(item['img'])
        # with open(img_file,'wb') as img_out:
        #     img_out.write(img.content)

        # 二次查找
        if item['title'].find('破解') != -1:
            print(item['title'])
            print(item['m3u8_li'])
            # 好像,,,ffmpeg可以直接解带密码的
            # 存成文件
            # dir_path = 'D:\\code\\photo\\'+ item['title'][:10]
            # os.mkdir(dir_path)
            # key_path = dir_path + '\\' +'key.m3u8'
            # text_path = dir_path + '\\' + 'index.m3u8'
            # if 'm3u8_key_text' in item.keys():
            #     with open(key_path,'w') as key_t:
            #         key_t.write(item['m3u8_key_text'])
            #     with open(text_path,'w') as text_t:
            #         # 两种情况,
            #         pass


            #  ffmpeg -i http://...m3u8 -c copy out.mkv
        # print(item['m3u8'])
        # print(item['title'][:15]+item['m3u8'])

        # https://play2.172cat.com/201910/31/ztqee2kf/index.m3u8
        # https://play2.172cat.com/201910/31/ztqee2kf/500kb/hls/index.m3u8
        return item