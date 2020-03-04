# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class VolmoeScrapyItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    author = scrapy.Field()
    num = scrapy.Field()
    url = scrapy.Field()
    desc = scrapy.Field()
    score = scrapy.Field()
    filesize = scrapy.Field()

class PhScrapyItem(scrapy.Item):
    # https://blog.csdn.net/sc_lilei/article/details/79587698?utm_source=distribute.pc_relevant.none-task
    # 参考
    # 使用图片的
    images = scrapy.Field() #必要
    image_name = scrapy.Field() #非必要,用来传递每个item的名称(按item命名文件夹)
    image_urls = scrapy.Field() #必要,
    image_results = scrapy.Field() #必要
    image_paths = scrapy.Field() #非必要,在pipeline中item_completed方法使用,暂时未知
    #自己定义的
    title = scrapy.Field()
    date = scrapy.Field()
    href = scrapy.Field()
class PhvScrapyItem(scrapy.Item):
    # https://blog.csdn.net/sc_lilei/article/details/79587698?utm_source=distribute.pc_relevant.none-task
    # 参考
    # 使用图片的
    images = scrapy.Field() #必要
    image_urls = scrapy.Field() #必要,就是img,这里是个坑,因为这里直接用的是s,
    # 就是scrapy框架里默认的写法是这urls是一个[]列表形式存储的,所以在spider中写获取的写成extract(),而不是first
    # 如果写成first,那在pipelines中就需要把for in去除,否则会报错
    image_results = scrapy.Field() #必要
    #自己定义的
    title = scrapy.Field()
    play = scrapy.Field()
    m3u8 = scrapy.Field()