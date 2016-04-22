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
from ctypes.test.test_random_things import callback_func
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
                   "http://www.dianping.com/search/category/50/90/g90p3"
                  ]

#     for line in file("dianping/spiders/cityCode.list"):
#         line  = line.strip().split("\n")
#         cityCode = line[0]
        
#     for id in xrange(0, 2900):
#         start_urls.append("http://www.dianping.com/search/category/%s/90/g90p50" % id)
        
    def __init__(self):
        self.questionIdPatten = re.compile("[0-9]+")
        self.pageUrl = "http://www.dianping.com/search/category/%s/90/g90p%s"
        
        self.fw = file("pages.list", "a")
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
                item["shop_cityname"] = cityName  # 地区
                # domain，当做标签，非区域，抓取区域指地区
                item["shop_domain"] = ",".join(li.xpath(".//p[@class='area-key']/span[@class='area-list']/a/text()").extract())
                key_list = ",".join(li.xpath(".//p[@class='area-key']/span[@class='key-list']/a/text()").extract())
                
                item["shop_tag"] = ",".join([key_list, item["shop_domain"]])  # 标签包含区域
                
                # href = '/shop/123456'
                href = li.xpath(".//p[@class='title']/a[@class='shopname']/@href").extract()[0]
                item["shop_id"] = href.split("/")[-1]
                
                shopUrl = "http://www.dianping.com" + href
                request = Request(shopUrl, callback=self.parse, priority=12345)
                request.meta["shopDetail"] = copy.deepcopy(item)
                yield request
                
#                 yieldPageFlag = False
#                 break  # for test
                pass
            
            if yieldPageFlag:
                # 如果当前页有数据，则继续请求下一页
                # 翻页DONE
                nextPageNumber = int(pageNumber) + 1
                url = self.pageUrl % (cityId, nextPageNumber)
                request = Request(url, callback=self.parse, priority=1234)
                yield request
                
            pass
        else:
            # 店铺页面
            item = response.meta["shopDetail"]
            
            # 店铺详情页div: main page-sa page-shop Fix
            try:
                main = select.xpath(".//div[@class='main page-sa page-shop Fix']")
            except Exception, e:
                print e
            try:
                mainBody = select.xpath(".//div[@id='main-body']")
            except Exception, e:
                print e
            try:
                body = select.xpath(".//div[@id='body']")
            except Exception, e:
                print e
            
            print main
            print mainBody
            print body
            if len(main) > 0:
                yield self.parseMain(select, response, item)
            elif len(mainBody) > 0:
                yield self.parseMainBody(select, response, item)
            elif len(body) > 0 :
                yield self.parseBody(select, response, item)
            else:
                # 未识别的url
                self.fw.write(response.url + "\tunknown-------------\n")
                self.fw.flush()
            pass

    def parseMain(self, select, response, item):
        print "parseMain"       
        if response.body.find("地图坐标")!=-1:
            self.fw.write(response.url +" 地图坐标")
            self.fw.flush()
        
        if response.body.find("门店介绍")!=-1:
            self.fw.write(response.url +" 门店介绍")
            self.fw.flush()
        
        try:  
            breadcrumb = select.xpath(".//div[@class='breadcrumb']/b/a/span/text()").extract()
            item["shop_domain"] = breadcrumb[0]
            item["shop_area"] = ",".join(breadcrumb[1:3])
            item["shop_category"] = ",".join(breadcrumb[3:])
        except Exception, e:
            item["shop_domain"] = ""
            item["shop_area"] = ""
            item["shop_category"] = ""
            print e

        
#         self.fw.write(response.url + "\tparseMain\n")
#         self.fw.flush()
        # shop info
        try:
            addressPrefix = select.xpath(".//span[@class='region']/text()").extract()[0]
            address = select.xpath(".//span[@itemprop='street-address']/text()").extract()[0]
            item["shop_address"] = addressPrefix + address
        except Exception, e:
            item["shop_address"] = ""
            print e
            
        try:
            item['shop_telphone'] = select.xpath(".//strong [@itemprop='tel']/text()").extract()[0]
        except Exception, e:
            item['shop_telphone'] = ""
            print e
#              
#         # shop bus and other info
        
        item["shop_open_time"] = ""
        item["shop_bus_line"] = ""
        try:
            otherInfo = select.xpath(".//div[@class='block-inner desc-list']/dl")
            for li in otherInfo:
                html = li.extract()
                if html.find("营业") != -1:
                    item["shop_open_time"] = li.xpath(".//dd/span/text()").extract()[0]
                elif html.find("公交") != -1:
                    item["shop_bus_line"] = li.xpath(".//dd/span/text()").extract()[0]
                pass
        except Exception, e:
            print e
       
        item["shop_map_attitude"] = ""
        item["shop_contact_man"] = ""
        item["shop_description"] = ""
        photoUrl = response.url + "/photos"
        print photoUrl
        request = Request(photoUrl, callback=self.parseMainPhotos, priority=123)
        request.meta["item"] = copy.deepcopy(item)
        return request

    #===========================================================================
    # parseMainPhotos
    # return [item, request]
    #===========================================================================
    def parseMainPhotos(self, response):
        # 解析 http://www.dianping.com/shop/18097023/photos
        select = Selector(response)
        
        print "parseMainPhotos"
        
        item = response.meta["item"]
        item["image_urls"] = []
        
        
        try:
            pic_list = select.xpath(".//a[@class='p-img']/img/@src").extract()
            for pic in pic_list:
                # wrong toto
                item["image_urls"].append(pic)
        except Exception, e:
            print e
        item["shop_flag"] = "yes"
        yield item
        pass
    def parseMainBody(self, select, response, item):
        self.fw.write(response.url + "\tparseMainBody\n")
        self.fw.flush()
        pass
    def parseBody(self, select, response, item):
        self.fw.write(response.url + "\parseBody\n")
        self.fw.flush()
        pass
