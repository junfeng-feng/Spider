# encoding=utf-8
import re
from scrapy.spiders import Spider
from scrapy.selector import Selector
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy import Request
import logging
import json
import copy
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from tmallshop.items import TmallshopItem

logging.basicConfig(level=logging.INFO,
                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                datefmt='%a, %d %b %Y %H:%M:%S',
                filename='tmallshop.log',
                filemode='a')

class SpiderTmallShop(Spider):
    name = 'tmallshop'
    
    allowed_domain = ['tmall.com']
    start_urls = [
                  ]

    searchUrl = """https://list.tmall.com/search_product.htm?cat=%s&brand=%s&sort=s&style=w"""
    for line in file("tmallshop/spiders/categoryIdBrandId.list"):
        line = line.strip().split()
        start_urls.append(searchUrl % (line[0], line[1]))
        
    def __init__(self):
        self.useridPatten = re.compile("user_id=[0-9]+")
        self.useridPrefixLength = len("user_id=")
        
        self.catidPatten = re.compile("cat=[0-9]+")
        self.catidPrefixLength = len("cat=")
        self.brandidPatten = re.compile("brand=[0-9]+")
        self.brandidPrefixLength = len("brand=")
        
        self.userRateUrl = "https://list.tmall.com/ajax/user_rate.htm?user_id=%s"
        pass
    
    def parse(self, response):
        item = TmallshopItem()
        brandIdStr = self.brandidPatten.findall(response.url)[0]
        item["brand_id"] = brandIdStr[self.brandidPrefixLength:]
        catIdStr = self.catidPatten.findall(response.url)[0]
        item["category_id"] = catIdStr[self.catidPrefixLength:]
        
        item["company_name"] = ""
        
        
        select = Selector(response)
        shopHeaderList = select.css(".shopHeader")
        for shopHeader in shopHeaderList:
            
            item["image_urls"] = []
            imageurl = shopHeader.xpath(".//a/img/@data-ks-lazyload").extract()[0]
            item["image_urls"].append("http:" + imageurl)
        
            item["shop_name"] = shopHeader.css(".shopHeader-info")[0].xpath(".//a/text()")[0].extract()
            item["shop_type"] = shopHeader.css(".shopHeader-info")[0].xpath(".//b/text()")[0].extract()
            
            item["shop_area"] = shopHeader.css(".shopHeader-info")[0].xpath(".//p/text()")[1].extract()
            item["shop_area"] = item["shop_area"].split("：")[1]
            
            item["shop_commodity_num"] = shopHeader.css(".sHe-product").xpath(".//em/text()").extract()[0]
            
            
            userIdStr = shopHeader.css(".sHi-title").extract()[0]
            userIdStr = self.useridPatten.findall(userIdStr)[0]
            item["shop_id"] = userIdStr[self.useridPrefixLength:]
            
#             print item
            request =  Request(self.userRateUrl%(item["shop_id"]),
                          callback = self.parseRate, priority=123456
                          )
            request.meta["data"] = copy.deepcopy(item)
            yield request
            
    def parseRate(self, response):
        item = response.meta["data"]
        liResult = json.loads(response.body, encoding="GBK")
        liResult = liResult["shop1"]
        
        item["description_consist_score"] = liResult["ds"]["value"].strip()
        item["description_consist_cmp"] = self.pareeToText(liResult["ds"]["compare"].strip())
        item["service_attitude_score"] = liResult["sq"]["value"].strip()
        item["service_attitude_cmp"] = self.pareeToText(liResult["sq"]["compare"].strip())
        item["logistics_service_score"] = liResult["ss"]["value"].strip()
        item["logistics_service_cmp"] = self.pareeToText(liResult["ss"]["compare"].strip())
        
        yield item
        pass
    
    def pareeToText(self, score):
        if score == "0":
            return "持平 ---------"
        elif score.startswith("-"):
            return "低于 "+ score
        else:
            return "高于 "+ score
        pass
