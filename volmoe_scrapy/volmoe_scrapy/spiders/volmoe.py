# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request

from volmoe_scrapy.items import VolmoeScrapyItem

class VolmoeSpider(scrapy.Spider):
    name = 'volmoe'
    allowed_domains = ['volmoe.com']
    start_urls = ['http://volmoe.com/']

    def parse(self, response):
        # 此处,是不同于第一版的在items类里写item对象,而是直接写了一个空字典,
        # item = {}
        # item["title"] = response.xpath("//tr[@class='listbg']//a/text()").extract()
        # author = response.xpath("//tr[@class='listbg']/td/text()[5]").extract()
        # item["author"] = list(map(lambda str:str[2:-2],author))
        # item["num"] = response.xpath("//tr[@class='listbg']//font[@class='pagefoot']/text()").extract()
        # yield item
        # 结果是这样
# {'title': ['排球少年!!', '火鳳燎原', '輝夜姬想讓人告白~天才們的戀愛頭腦戰~', '輕聲密語', 'given', '三十歲初戀', '月曜日のたわわ', '皇後娘娘的五毛特效', 'TIGER x DRAGON!', '她絕對喜
# 歡我', '因為女校所以safe', '咖啡遇上香草', '食色大陸', '邪氣凜然', '重生之都市修仙', '神醫
# 嫡女', '月光社亡靈奇談', '瑪雅小姐的熬夜生活'], 'author': ['古館春一', '陳某', '赤坂アカ', '池田學志', 'キヅナツキ,刺傷', '310(サトー)', '比村奇石', '萬畫筒漫畫', '竹宮悠由子,絕叫', 'ヨウハ', 'お一うち', '朱神寶', '刀瑞斯,爾東圖:爾東', '三福動漫', '大行道動漫', '三福互 
# 娛', '川端新', '保谷伸'], 'num': ['第 201-205 話', '第 66 卷', '第 156-160 話', '第 09 卷', '第 03 卷', '第 03 卷', '第 09 卷', '第 211-220 話', '第 091-095 話', '第 001-010 話', '第 001-006 話', '第 050-053 話', '第 341-354 話', '第 261-265 話', '第 336-337 話', '第 246-262 話', '第 008 話', '第 011-014 話']}
        item = VolmoeScrapyItem() 
        item["title"] = response.xpath("//tr[@class='listbg']//a/text()").extract()
        # 这个text()的第零项,是空????从1开始的?
        author = response.xpath("//tr[@class='listbg']/td/text()[5]").extract()
        item["author"] = list(map(lambda str:str[2:-2],author))
        item["num"] = response.xpath("//tr[@class='listbg']//font[@class='pagefoot']/text()").extract()
        # print(item["title"])
        # print(item["author"])
        # print(item["num"])
        yield item
# 结果是这样
# 其实两者是一样的
# {'author': ['古館春一',
#             '陳某',
#             '赤坂アカ',
#             '池田學志',
#             'キヅナツキ,刺傷',
#             '310(サトー)',
#             '比村奇石',
#             '萬畫筒漫畫',
#             '竹宮悠由子,絕叫',
#             'ヨウハ',
#             'お一うち',
#             '朱神寶',
#             '刀瑞斯,爾東圖:爾東',
#             '三福動漫',
#             '大行道動漫',
#             '三福互娛',
#             '川端新',
#             '保谷伸'],
#  'num': ['第 201-205 話',
#          '第 66 卷',
#          '第 156-160 話',
#          '第 09 卷',
#          '第 03 卷',
#          '第 03 卷',
#          '第 09 卷',
#          '第 211-220 話',
#          '第 091-095 話',
#          '第 001-010 話',
#          '第 001-006 話',
#          '第 050-053 話',
#          '第 341-354 話',
#          '第 261-265 話',
#          '第 336-337 話',
#          '第 246-262 話',
#          '第 008 話',
#          '第 011-014 話'],
#  'title': ['排球少年!!',
#            '火鳳燎原',
#            '輝夜姬想讓人告白~天才們的戀愛頭腦戰~',
#            '輕聲密語',
#            'given',
#            '三十歲初戀',
#            '月曜日のたわわ',
#            '皇後娘娘的五毛特效',
#            'TIGER x DRAGON!',
#            '她絕對喜歡我',
#            '因為女校所以safe',
#            '咖啡遇上香草',
#            '食色大陸',
#            '邪氣凜然',
#            '重生之都市修仙',
#            '神醫嫡女',
#            '月光社亡靈奇談',
#            '瑪雅小姐的熬夜生活']}
