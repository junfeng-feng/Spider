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
                   "http://www.dianping.com/search/category/1/90/g90p3720"
                  ]

#     for line in file("dianping/spiders/cityCode.list"):
#         line  = line.strip().split("\n")
#         cityCode = line[0]
        
#     for id in xrange(0, 2900):
#         start_urls.append("http://www.dianping.com/search/category/%s/90/g90p50" % id)
        
    def __init__(self):
        self.questionIdPatten = re.compile("[0-9]+")
        self.pageUrl = "http://www.dianping.com/search/category/%s/90/g90p%s"
        self.fw = file("pages.list", "w")
        pass
    
    def parse(self, response):
        select = Selector(response)
        if not "shopDetail" in response.meta:
            # 店铺列表页
            item = DianpingItem()
            allNo = self.questionIdPatten.findall(response.url)
            cityId = allNo[0]  # cityid
            pageNumber = allNo[-1]
            
            self.fw.write("%s cityId:%s, pageNumber：%s\n" % (response.url, cityId, pageNumber))
            
            item["city_id"] = cityId
            
            yieldPageFlag = False
            
            cityName = select.css(".city").xpath("./text()").extract()[0]
    #         self.fw.write("%s\t%s\n"%(cityId, cityName))
    #         self.fw.flush()
    #         
    #         if response.status == 403:
    #             sys.exit(0)
    #             return

            shop_list = select.xpath(".//div[@class='info']")
            for li in shop_list:
                yieldPageFlag = True
                
                item["shop_name"] = li.xpath(".//p[@class='title']/a/text()").extract()[0]
                item["shop_area"] = cityName  # 地区
                # domain，当做标签，非区域，抓取区域指地区
                item["shop_domain"] = ",".join(li.xpath(".//p[@class='area-key']/span[@class='area-list']/a/text()").extract())
                key_list = ",".join(li.xpath(".//p[@class='area-key']/span[@class='key-list']/a/text()").extract())
                
                item["shop_tag"] = ",".join([key_list, item["shop_domain"]])  # 标签包含区域
                
                # href = '/shop/123456'
                href = li.xpath(".//p[@class='title']/a[@class='shopname']/@href").extract()[0]
                item["shop_id"] = href.split("/")[-1]
                
                
                shopUrl = "http://www.dianping.com" + href
                
                request = Request(shopUrl, callback=self.parse, priority=12345678)
                request.meta["shopDetail"] = copy.deepcopy(item)
                yield request
                pass
            
            if yieldPageFlag:
                # 如果当前页有数据，则继续请求下一页
                #翻页DONE
                nextPageNumber = int(pageNumber) + 1
                url = self.pageUrl % (cityId, nextPageNumber)
                request = Request(url, callback=self.parse, priority=123456)
                yield request
                
            pass
        else:
            # 店铺页面
            item = response.meta["shopDetail"]
            # 店铺详情页div: main page-sa page-shop Fix
            main = select.xpath(".//div[@class='main page-sa page-shop Fix']")
            mainBody = select.xpath(".//div[@id='main-body']")
            body = select.xpath(".//div[@id='body']")
            
            if len(main) > 0:
                self.parseMain(select, response, item)
            elif len(mainBody) > 0:
                self.parseMainBody(select, response, item)
            elif len(body) > 0 :
                self.parseBody(select, response, item)
            else:
                # 未识别的url
                self.fw.write(response.url + "\tunknown-------------\n")
                self.fw.flush()
            pass

    def parseMain(self, select, response, item):
        self.fw.write(response.url + "\tparseMain\n")
        self.fw.flush()
        # shop info
#         item["shop_domain"] = select.xpath(".//span[@class='region']/text()").extract()[0]
#         address = select.xpath(".//span[@itemprop='street-address']/text()").extract()[0]
#         
#         item["shop_address"] = item["shop_domain"] + address
#         try:
#             item['shop_telphone'] = select.xpath(".//strong [@itemprop='tel']/text()").extract()[0]
#         except Exception, e:
#             print e
#             
#         # shop bus and other info
#         otherInfo = select.xpath(".//div[@class='block-inner desc-list']/dl")
#         item["shop_open_time"] = ""
#         item["shop_bus_line"] = ""
#         for li in otherInfo:
#             html = li.extract()
#             if html.find("营业") != -1:
#                 item["shop_open_time"] = li.xpath(".//dd/span/text()").extract()[0]
#             elif html.find("公交") != -1:
#                 item["shop_bus_line"] = li.xpath(".//dd/span/text()").extract()[0]
#             pass
        
    def parseMainBody(self, select, response, item):
        self.fw.write(response.url + "\tparseMainBody\n")
        self.fw.flush()
        pass
    def parseBody(self, select, response, item):
        self.fw.write(response.url + "\parseBody\n")
        self.fw.flush()
        pass
