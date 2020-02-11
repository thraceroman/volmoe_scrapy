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
        # item = VolmoeScrapyItem() 
        # item["title"] = response.xpath("//tr[@class='listbg']//a/text()").extract()
        # # 这个text()的第零项,是空????从1开始的?
        # author = response.xpath("//tr[@class='listbg']/td/text()[5]").extract()
        # item["author"] = list(map(lambda str:str[2:-2],author))
        # item["author"] = [i[2:-2] for i in author]
        # item["num"] = response.xpath("//tr[@class='listbg']//font[@class='pagefoot']/text()").extract()
        # # print(item["title"])
        # # print(item["author"])
        # # print(item["num"])
        # yield item
# 结果是这样
# ...
# 其实两者是一样的
# 
        # item = VolmoeScrapyItem() #线程问题!!!!
        td_list = response.xpath("//tr[@class='listbg']//td")
        # item["title"] = response.xpath("//tr[@class='listbg']//a/text()").extract()
        # # 这个text()的第零项,是空????从1开始的?
        # author = response.xpath("//tr[@class='listbg']/td/text()[5]").extract()
        # item["author"] = list(map(lambda str:str[2:-2],author))
        # item["num"] = response.xpath("//tr[@class='listbg']//font[@class='pagefoot']/text()").extract()
        for td in td_list:
                item = VolmoeScrapyItem() 
                item["title"] = td.xpath(".//a/text()").extract_first()
                item["author"] = td.xpath("./text()[5]").extract_first()[2:-2]
                item["num"] = td.xpath(".//font[@class='pagefoot']/text()").extract_first()
                item["url"] = td.xpath("./a/@href").extract_first()
                # 传递详情页内容,需要进行跳转,此时就不是只传item了,而是
                yield scrapy.Request(
                        item["url"],
                        callback=self.parse_detail,
                        meta = {"item":item} #同时把item这个对象传了过去
                )


    def parse_detail(self,response): #处理详情页的
        item = response.meta["item"] #先把那个原始的item拿出来,因为还有些东西没加完全
        item["desc"] = response.xpath("//div[@class='book_desc']/div/text()[1]").extract_first()
        # 跳级时的模糊拿取,是会有层间的平行项出现的
        # https://www.jianshu.com/p/85a3004b5c06
        item["score"] = response.xpath("//div[@class='bookinfo']//td[@id='book_score']//tr[1]/td[1]/font[1]/text()").extract_first()
        item["filesize"] = response.xpath("//div[@class='bookinfo']//td[@id='book_score']//tr[1]/td[2]/font[2]/text()").extract_first()
        yield item



        
