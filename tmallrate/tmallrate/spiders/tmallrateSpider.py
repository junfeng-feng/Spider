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

from tmallrate.items import TmallrateItem

logging.basicConfig(level=logging.INFO,
                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                datefmt='%a, %d %b %Y %H:%M:%S',
                filename='tmallrate.log',
                filemode='a')

class SpiderTmall(Spider):
    name = 'tmallrate'
    
    allowed_domain = ['tmall.com']
    start_urls = []

    #===========================================================================
    for productId in file("tmallrate/spiders/productid.list"):
        start_urls.append("https://detail.tmall.com/item.htm?id=%s" % (productId.strip()))
    
    def __init__(self):
        self.sellerIdPattern = re.compile(r"sellerId=[0-9]+")  # brandPattern re
        self.productIdPattern = re.compile(r"id=[0-9]+")  # product_id
        
        self.shopUrlPattern = re.compile(r'shopUrl:".*?"')
        self.shopUrlPrefixLength = len("shopUrl:'")
        pass
    
    def parse(self, response):
        jsonUrl = "https://rate.tmall.com/list_detail_rate.htm?itemId=%s&sellerId=%s&order=3&currentPage=%s"
        
        if "argsMap" in response.meta:
            argsMap = response.meta["argsMap"]
            shop_url = argsMap["shop_url"]
            
            # 表示是yield request的reponse，解析json
            prefix = '"rateDetail":"'
            body = response.body.strip()
            prefixLen = len(prefix)
            bodyJson = json.loads(body[prefixLen - 1:], encoding="gbk")
            
            paginator = bodyJson["paginator"]
            lastPage = int(paginator["lastPage"])
            currentPage = int(paginator["page"])
            if currentPage < lastPage and currentPage < 4:#只取前三页的评论数据
                itemId = argsMap["itemId"]
                sellerId = argsMap["sellerId"]                
                pageNo = currentPage + 1
                requestUrl = jsonUrl % (itemId, sellerId, pageNo)
                
                request = Request(requestUrl, callback=self.parse, priority=12345678)  # 优先级调高
                request.meta["argsMap"] = argsMap
                yield request
                pass

            rateList = bodyJson["rateList"]
            rateListLen = len(rateList)
            for index, rate in zip(xrange(rateListLen), rateList):
                item = TmallrateItem()
                
                nickName = rate["displayUserNick"]
                item["product_id"] = argsMap["itemId"]
                item["rate_id"] = "rateid-" + str(currentPage * 100 + index + 1)
                item["user_nickname"] = nickName
                if nickName.find("*") == -1:
                    item["user_name_star_flag"] = 1
                else:
                    item["user_name_star_flag"] = 0  # 有星号
                item["rate_content"] = rate["rateContent"]
                item["rate_content_time"] = rate["rateDate"]
                if rate["appendComment"] and len(rate["appendComment"]) > 0 :
                    item["rate_content_append"] = rate["appendComment"]["content"]
                    item["rate_append_time"] = rate["appendComment"]["commentTime"]
                else:
                    item["rate_content_append"] = ""
                    item["rate_append_time"] = ""
                
                item["shop_url"] = shop_url
                yield item
            pass
        else:
            # 解析html
            select = Selector(response)
            
            try:
                shop_url = self.shopUrlPattern.findall(response.body)[0]
                shop_url = "http:" + shop_url[self.shopUrlPrefixLength:-1]
            except Exception, e:
                shop_url = ""
                print e
            
            # 每页20个评论
            itemId = self.getProductId(response.url)
            sellerId = self.getSellerId(response.body)
            pageNo = "1"
            requestUrl = jsonUrl % (itemId, sellerId, pageNo)
            
            argsMap = {"itemId":itemId, "sellerId":sellerId, "shop_url":shop_url}
            request = Request(requestUrl, callback=self.parse, priority=123456)
            request.meta["argsMap"] = argsMap
            yield request
        pass
    
    def getProductId(self, url):
        match = self.productIdPattern.search(url)
        if match and match.group():
            itemId = match.group()[len("id="):]
        else:
            return None
        return itemId
        pass
    def getSellerId(self, html):
        match = self.sellerIdPattern.search(html)
        if match and match.group():
            sellerId = match.group()[len("sellerId="):]
        else:
            return None
        return sellerId
        pass


