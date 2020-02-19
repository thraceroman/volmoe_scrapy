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
    