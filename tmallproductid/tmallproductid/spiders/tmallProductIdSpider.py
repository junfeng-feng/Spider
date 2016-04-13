# encoding=utf-8
import re
import uuid
import scrapy
from scrapy.spiders import CrawlSpider
from scrapy.spiders import Spider
from scrapy.selector import Selector
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy import Request
import logging
import json

from tmallproductid.items import TmallproductidItem

logging.basicConfig(level=logging.INFO,
                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                datefmt='%a, %d %b %Y %H:%M:%S',
                filename='tmallproductid.log',
                filemode='a')

#===============================================================================
# SpiderTmall
#  根据brandid  list 抓取，品牌的产品列表
#===============================================================================
class SpiderTmall(Spider):
    name = 'tmallproductid'
    
    allowed_domain = ['tmall.com']
    start_urls = [
                  ]
#     for brandId in xrange(202210022, 202210022 + 2):
#         start_urls.append("https://list.tmall.com//search_product.htm?brand=%s" % (brandId))
    
    for brandId in file("./tmallproductid/spiders/brandid.list"):
        brandId = brandId.strip()
        start_urls.append("https://list.tmall.com//search_product.htm?brand=%s" % (brandId))
            
    def __init__(self):
        self.brandIdPattern = re.compile(r"brand=[0-9]+")  # brandPattern re
        self.brandIdLength = len("brand=")
        
        self.productIdPattern = re.compile(r"\Wid=[0-9]+")  # product_id  \W匹配 “&”
        self.productIdLength = len("_id=")  # 截取的时候，去掉前四位
        self.pageUrl = "https://list.tmall.com//search_product.htm?brand=%s&s=%s"
        pass
    
    def parse(self, response):
        select = Selector(response)
        brandId = self.getBrandId(response.url)
#         itemListHtml = select.xpath("//div[@id='J_ItemList']").extract()[0]
#         productIdSet = set(self.productIdPattern.findall(itemListHtml))
#         for productIdStr in productIdSet:
#             productId = productIdStr[self.productIdLength:]
#             item = TmallproductidItem()
#             item["productId"] = productId
#             yield item

        itemList = select.css(".product")
        if len(itemList) > 1:#当前有产品，才需要处理
            for productItem in itemList:
                productId = self.productIdPattern.findall(productItem.extract())[0]  # 三个一样的id，取第一个
                product_id = productId[self.productIdLength:]
                try:
                    product_price = productItem.xpath("./div/p/em/@title").extract()[0]
                except Exception, e:
                    product_price = ""
                    print e
                
                item = TmallproductidItem()
                item["product_id"] = product_id
                item["brand_id"] = brandId
                item["product_price"] = product_price
                yield item
                pass
            
            pages = select.css(".ui-page-s-len").xpath("./text()").extract()[0]
            totalPage = int(pages.split("/")[1])
            if totalPage > 1:
                for pageNo in xrange(1, totalPage):
                    
                    #每页60个产品，参数s=60，表示请求第二页, s=120表示请求第三页
                    #self.pageUrl = "https://list.tmall.com//search_product.htm?brand=%s&s=%s"
                    requestUrl = self.pageUrl % (brandId, pageNo * 60)
                    yield Request(requestUrl, callback=self.parse, priority=123456)
                    pass
        pass
    
    def getProductId(self, url):
        match = self.productIdPattern.search(url)
        if match and match.group():
            itemId = match.group()[self.productIdLength:]
        else:
            return None
        return itemId
        pass
    
    def getBrandId(self, url):
        match = self.brandIdPattern.search(url)
        if match and match.group():
            id = match.group()[self.brandIdLength:]
        else:
            return None
        return id
        pass


