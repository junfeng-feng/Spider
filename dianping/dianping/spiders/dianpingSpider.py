# encoding=utf-8
import re
from scrapy.spiders import Spider
from scrapy.selector import Selector
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy import Request
import logging
import json
import copy
import uuid
import sys
from scrapy.item import Item
from __builtin__ import int
reload(sys)
sys.setdefaultencoding('utf-8')

from dianping.items import DianpingItem

logging.basicConfig(level=logging.INFO,
                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                datefmt='%a, %d %b %Y %H:%M:%S',
                filename='dianping.log',
                filemode='a')

class SpiderTmallShop(Spider):
    name = 'dianping'
    
    allowed_domain = ['dinaping.com']
    start_urls = [
                   "http://www.dianping.com/search/category/1/90/g90p50"
                  ]

#     for line in file("dianping/spiders/cityCode.list"):
#         line  = line.strip().split("\n")
#         cityCode = line[0]
        
    for id in xrange(0, 2900):
        start_urls.append("http://www.dianping.com/search/category/%s/90/g90p50" % id)
        
    def __init__(self):
        self.questionIdPatten = re.compile("[0-9]+")
        self.pageUrl = "http://www.dianping.com/search/category/%s/90/g90p%s"
        self.fw = file("cityCode.list", "w")
        pass
    
    def parse(self, response):
        select = Selector(response)
        if "shopDetail" in response.meta:
            #店铺详情页
            item = response.meta["shopDetail"]
            #shop info
            item["shop_domain"] = select.xpath(".//span[@class='region']/text()").extract()[0]
            address = select.xpath(".//span[@itemprop='street-address']/text()").extract()[0]
            
            item["shop_address"] = item["shop_domain"] + address
            item['shop_telphone'] = select.xpath(".//strong [@itemprop='tel']/text()").extract()[0]
            
            #shop bus and other info
            otherInfo = select.xpath(".//div[@class='block-inner desc-list']/dl")
            item["shop_open_time"] =  ""
            item["shop_bus_line"] = ""
            for li in otherInfo:
                html = li.extract()
                if html.find("营业") !=-1:
                    item["shop_open_time"] = li.xpath(".//dd/span/text()").extract()[0]
                elif html.find("公交")!= -1:
                    item["shop_bus_line"] = li.xpath(".//dd/span/text()").extract()[0]
                pass
            pass
        else:
            item = DianpingItem()
            
            allNo = self.questionIdPatten.findall(response.url)
            cityId = allNo[0]  # cityid
            pageNumber = allNo[-1]
            
            item["city_id"] = cityId
            
            yieldItemFlag = False
            
            cityName = select.css(".city").xpath("./text()").extract()[0]
    #         
    #         self.fw.write("%s\t%s\n"%(cityId, cityName))
    #         self.fw.flush()
    #         
    #         if response.status == 403:
    #             sys.exit(0)
    #             return
    
            priorityNo = 12345678
            shop_list =  select.xpath(".//div[@class='info']")
            for li in shop_list:
                priorityNo -= 10 #最先出现的店铺，优先采集
                yieldItemFlag = True
                
                item["shop_name"] = li.xpath(".//p[@class='title']/a/text()").extract()[0]
                item["shop_area"] = cityName #地区
                #domain，当做标签，非区域，抓取区域指地区
                item["shop_domain"] = ",".join(li.xpath(".//p[@class='area-key']/span[@class='area-list']/a/text()").extract())
                key_list = ",".join(li.xpath(".//p[@class='area-key']/span[@class='key-list']/a/text()").extract())
                
                item["shop_tag"] =",".join([key_list, item["shop_domain"]])#标签包含区域
                
                #href = '/shop/123456'
                href = li.xpath(".//p[@class='title']/a[@class='shopname']/@href").extract()[0]
                item["shop_id"] = href.split("/")[-1]
                
                
                shopUrl = "http://www.dianping.com" + href
                
                request = Request(shopUrl, callback=self.parse, priority=priorityNo)
                request.meta["shopDetail"] = copy.deepcopy(item)
                yield request
                pass
            
            if yieldItemFlag:
                # 如果当前页有数据，则继续请求下一页
                nextPageNumber = int(pageNumber) + 50
                url = self.pageUrl % (cityId, nextPageNumber)
                request = Request(url, callback=self.parse, priority=123456)
                yield request
            pass
