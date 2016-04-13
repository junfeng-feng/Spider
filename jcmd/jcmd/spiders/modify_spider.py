# #encoding=utf-8
# import re
# from scrapy.selector import Selector
# from scrapy.spiders import Spider
# 
# from jcmd.items import brandItem
# 
# 
# #from scrapy.linkextractors.sgml import SgmlLinkExtractor
# #from scrapy.spiders.crawl import CrawlSpider, Rule
# class modify_spider(Spider):
#     
#     #补充品牌中文分类的spider
#     name = 'brand_modify'
#     
#     allowed_domain = ['china-10.com/']
#     
#     start_urls = ['http://www.china-10.com/brand/1.html']
#     
#     index = 1
#     
#     while(index<=100000):
#         
#         url = 'http://www.china-10.com/brand/%d.html' % index
#         start_urls.append(url)
#         index = index + 1
#     
#     #品牌url
#     rule_brandurl = re.compile(r'[\d]+.html$')
#     #获取id规则
#     rule_get_id = re.compile(r'[\d]+')
#     #匹配品牌行业
#     rule_brandcat = re.compile(u'\u54c1\u724c\u884c\u4e1a')
#     
#     def parse(self,response):
#         
#         bItem = brandItem()
#         sel= Selector(response)
#         #brand的url尾部
#         tail = modify_spider.rule_brandurl.findall(response.url)[0]
#         #获取brand_id
#         bItem['brand_id'] = modify_spider.rule_get_id.findall(tail)[0]
#         category_name = []
#         brandcatlist = sel.xpath(".//ul[@class='navmenu']/li[2]/div/ul[@class='nav-brandcatlist']")
#         for list in brandcatlist:
#             
#             title = list.xpath("./li[1]/span/text()").extract()[0]
#             if modify_spider.rule_brandcat.findall(title):
#                 category_name = list.xpath("./li/a/text()").extract()
#         bItem['category_name'] = ",".join(category_name)
#         
#         
#         yield bItem
#         
#             
#             
#         
#             
#    
#         