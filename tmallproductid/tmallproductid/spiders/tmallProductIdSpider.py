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
class SpiderTmallFromCatAndbrand(Spider):
    name = 'tmallproductid_from_cat_brand'
    
    allowed_domain = ['tmall.com']
    start_urls = []
    
    for line in file("./tmallproductid/spiders/catBrandId.list"):
        line = line.strip().split()
        catId = line[0]
        brandId = line[1]
        
        start_urls.append("https://list.tmall.com//search_product.htm?cat=%s&brand=%s&style=l" % 
                          (catId, brandId))
#         if catId=="50024922":
#             break
            
    def __init__(self):
        self.brandIdPattern = re.compile(r"brand=[0-9]+")  # brandPattern re
        self.brandIdLength = len("brand=")
        
        self.catPattern = re.compile(r"cat=[0-9]+")  # cat re
        self.catPrefixLen = len("cat=")
        
        self.productIdPattern = re.compile(r"\Wid=[0-9]+")  # product_id  \W匹配 “&”
        self.productIdLength = len("_id=")  # 截取的时候，去掉前四位
        
        self.pageUrl = "https://list.tmall.com//search_product.htm?cat=%s&brand=%s&s=%s&style=l"
        self.fw = file("pageList.list", "a")
        pass
    
    def parse(self, response):
        select = Selector(response)
        catId = self.getCatId(response.url)
        brandId = self.getBrandId(response.url)
        
        nrt =  select.xpath(".//div[@class='nrt']")
        if len(nrt) > 0:
            #===================================================================
            #喵~没有找到指定条件下相关的商品哦。
            #下面是我们去掉一些条件找到的结果：
            #===================================================================
            return

        itemList = select.css(".product")
        if len(itemList) > 0:  # 当前有产品，才需要处理
            for productItem in itemList:
                productId = self.productIdPattern.findall(productItem.extract())[0]  # 三个一样的id，取第一个
                product_id = productId[self.productIdLength:]
                
                item = TmallproductidItem()
                item["product_id"] = product_id
                item["brand_id"] = brandId
                item["category_id"] = catId
                
                yield item
                pass
            
            try:
                pages = select.css(".ui-page-s-len").xpath("./text()").extract()[0]
                totalPage = int(pages.split("/")[1])
                if totalPage > 1:
                    for pageNo in xrange(1, totalPage):
                        # 每页60个产品，参数s=60，表示请求第二页, s=120表示请求第三页
                        #style = l 小图模式，每页84个
                        # self.pageUrl = "https://list.tmall.com//search_product.htm?brand=%s&s=%s"
                        requestUrl = self.pageUrl % (catId, brandId, pageNo * 84)
                        self.fw.write(requestUrl+'\n')
                        self.fw.flush()
                        
                        yield Request(requestUrl, callback=self.parse, priority=123456)
                        pass
            except Exception,e:
                print e
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
    
    def getCatId(self, url):
        match = self.catPattern.search(url)
        id = ""
        if match and match.group():
            id = match.group()[self.catPrefixLen:]
        else:
            return None
        return id
        pass


class SpiderTmallFromCat(Spider):
    name = 'tmallproductid_from_cat'
    
    allowed_domain = ['tmall.com']
    start_urls = [
#                   "https://list.tmall.com//search_product.htm?cat=50024921&style=l",
                  ]
    
    for line in file("./tmallproductid/spiders/catId.list"):
        line = line.strip()
        catId = line
         
        start_urls.append("https://list.tmall.com//search_product.htm?cat=%s&style=l" % 
                          (catId))
            
    def __init__(self):
        self.brandIdPattern = re.compile(r"brand=[0-9]+")  # brandPattern re
        self.brandIdLength = len("brand=")
        
        self.catPattern = re.compile(r"cat=[0-9]+")  # cat re
        self.catPrefixLen = len("cat=")
        
        self.productIdPattern = re.compile(r"\Wid=[0-9]+")  # product_id  \W匹配 “&”
        self.productIdLength = len("_id=")  # 截取的时候，去掉前四位
        
        self.pageUrl = "https://list.tmall.com//search_product.htm?cat=%s&s=%s&style=l"
        self.fw = file("pageListCat.list", "a")
        pass
    
    def parse(self, response):
        select = Selector(response)
        catId = self.getCatId(response.url)
        brandId = ""
        
        nrt =  select.xpath(".//div[@class='nrt']")
        if len(nrt) > 0:
            #===================================================================
            #喵~没有找到指定条件下相关的商品哦。
            #下面是我们去掉一些条件找到的结果：
            #===================================================================
            return

        itemList = select.css(".product")
        if len(itemList) > 0:  # 当前有产品，才需要处理
            for productItem in itemList:
                productId = self.productIdPattern.findall(productItem.extract())[0]  # 三个一样的id，取第一个
                product_id = productId[self.productIdLength:]
                
                item = TmallproductidItem()
                item["product_id"] = product_id
                item["brand_id"] = brandId
                item["category_id"] = catId
                
                yield item
                pass
            
            try:
                pages = select.css(".ui-page-s-len").xpath("./text()").extract()[0]
                totalPage = int(pages.split("/")[1])
                if totalPage > 1:
                    for pageNo in xrange(1, totalPage):
                        # 每页60个产品，参数s=60，表示请求第二页, s=120表示请求第三页
                        # self.pageUrl = "https://list.tmall.com//search_product.htm?brand=%s&s=%s"
                        requestUrl = self.pageUrl % (catId, pageNo * 84)
                        self.fw.write(requestUrl+'\n')
                        self.fw.flush()
                        
                        yield Request(requestUrl, callback=self.parse, priority=123456)
                        pass
            except Exception,e:
                print e
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
    
    def getCatId(self, url):
        match = self.catPattern.search(url)
        id = ""
        if match and match.group():
            id = match.group()[self.catPrefixLen:]
        else:
            return None
        return id
        pass


