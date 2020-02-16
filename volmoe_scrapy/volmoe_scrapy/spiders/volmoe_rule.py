# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
import re


class VolmoeRuleSpider(CrawlSpider):
    name = 'volmoe_rule'
    allowed_domains = ['volmoe.com']
    start_urls = ['http://volmoe.com/']
# 以crawl模板进行爬取,其逻辑和basic模板的有所不同,不再是先在标签中xpath找详情页网址,而是直接把网址全扒出来,再re找符合条件的详情页网址
# https://www.jianshu.com/p/2929d64503a3 crawl的初步解释
    rules = (
        # 扒详情页,具体详情页内的爬取内容去parse_item方法中callback,拿完就走,不需要重新执行rules,
        # re全数字\d+ 直译.就是\.
        Rule(LinkExtractor(allow=r'https://volmoe.com/comic/\d+\.htm'), callback='parse_item'),
        # 翻页,执行跳入下一页逻辑,没有新的方法,但是需要重新执行rules,这里,将\d+改成了 \d,就是只取1位数字,
        # 这里面的逻辑,是只取了第一页下面的跳转页数,还是进入第二页后依然有这一步,(就是到底是迭代了,还是只进行了一次)?????,迭代了,会扒出所有
        # Rule(LinkExtractor(allow=r'/list/all,all,all,sortpoint,all,all/\d\.htm'), follow=True)
    )

    def parse_item(self, response):
        # 爬取标题,下载链接
        # https://volmoe.com/down/10231/1001/0/2/1-0/ 
        # 这里是火凤燎原(10231),第一卷(1001,卷都是1打头,话是3打头,3521就是第521话),普通线路(0,2是vip线),epub格式下载(2,1是mobi格式)
        item = {}
        item['name'] = response.xpath('//head/title/text()').get()
        # item['desc1'] = re.findall('<div id="desc_text" style="word-wrap:break-word; word-break:break-all; ">(.*?)</div>',response.body.decode())
        # 除了用xpath,还可以用re,额,这里body的内容好像有些问题,尝试把那页下载到本地发现内容不太符合
        # item['down'] = re.findall("https://(volmoe.com/down/\d+/\d+/0/2/1-0)",response.body.decode())
        # 确实,用爬的获取的真实的网页都只是 javascript:display_codeinfo( 'e401', 0 )
        # response.xpath('//div[@id="div_mobi"]//tr[@class="listbg1"]//@href').extract()
        item["desc"] = response.xpath("//div[@class='book_desc']/div/text()[1]").extract_first()
        item["score"] = response.xpath("//div[@class='bookinfo']//td[@id='book_score']//tr[1]/td[1]/font[1]/text()").extract_first()
        item["filesize"] = response.xpath("//div[@class='bookinfo']//td[@id='book_score']//tr[1]/td[2]/font[2]/text()").extract_first()
        return item
