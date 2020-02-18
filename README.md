# volmoe_scrapy
先建空仓,后写代码的形式,同样是那个爬取volmoe网站的scrapy项目

0.5: 按一本为一个item逻辑去实现,并且带有详情页内容爬取,其中遇到的问题
(1)xpath的跳级模糊拿取时,是会有平行项出现的,尽量先用scrapy shell 进行尝试,其中还有extarct的疑问,什么时候是多个结果
(2)详情页跳转时,是用scrapy.Request(跳转页url,爬取逻辑,带的数据)
(3)如此跳转时,scrapy多线程会出现问题,此中原理还有疑问
(4)一般,spider中只写爬取的逻辑,爬取到的内容再进行修正或保存,在pipelines中进行,正则表达式的使用,和列表的批量操作的写法,用高阶函数?

待实现的:0.5
(1)爬取详情页中的下载地址,这又是一个循环,这里会有线程问题(应该)
>https://volmoe.com/down/10231/1001/0/2/1-0/ 这里是火凤燎原(10231),第一卷(1001,卷都是1打头,话是3打头,3521就是第521话),普通线路(0,2是vip线),epub格式下载(2,1是mobi格式)
(2)分页的实现,两种,一个是类似详情页跳转(直接用scrapy shell进行尝试即可),把下一页的url写入scrapy.Request进行callback=self.parse;另一个是用scrapy框架中的

待实现的:0.6
下载页的内容获取,如果直接用爬虫的话只会得到javascript:display_codeinfo( 'e401', 0 ),而不会获取真实的下载页
原因:只有以用户登录时才会得到下载页面的网址,即可以添加带有用户的cookies,或者发送post请求,但是如何在详情页里发送请求?

>http://rss.rrys.tv/rss/feed/26992 悠长假期的磁力链爬取
http://www.rrys2019.com/search/index?keyword=%E6%82%A0%E9%95%BF%E5%81%87%E6%9C%9F