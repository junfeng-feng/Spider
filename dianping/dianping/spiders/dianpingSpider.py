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
#                    "http://www.dianping.com/search/category/1/90/g90p50",
#                    "http://www.dianping.com/search/category/1/90/g90p31"
                  ]

#     for line in file("dianping/spiders/cityCode.list"):
#         line  = line.strip().split("\n")
#         cityCode = line[0]

    #1~2506都是cityCode        
    for id in xrange(1, 2510):
        start_urls.append("http://www.dianping.com/search/category/%s/90/g90p1" % id)
        
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
                
                #for test 测试数据，取前三页
                if nextPageNumber >= 3:
                    return
                
                url = self.pageUrl % (cityId, nextPageNumber)
                request = Request(url, callback=self.parse, priority=1234)
                yield request
                
            pass
        else:
            # 店铺页面
            item = response.meta["shopDetail"]
            
            # 店铺详情页div: main page-sa page-shop Fix
            main = select.xpath(".//div[@class='main page-sa page-shop Fix']")
            mainBody = select.xpath(".//div[@id='main-body']")
            breadcrumb_wrapper = select.xpath(".//div[@class='breadcrumb-wrapper']")
            body = select.xpath(".//div[@id='body']")
            
            
            print main
            print mainBody
            print body
            
            if len(main) > 0:
                yield self.parseMain(select, response, item)
                pass
            elif len(breadcrumb_wrapper)> 0: #优先级比manBody高
                yield self.parseBreadcrumb_wrapper(select, response, item)
                pass
            elif len(mainBody) > 0:
                yield self.parseMainBody(select, response, item)
                pass
            elif len(body) > 0 :
                yield self.parseBody(select, response, item)
                pass
            else:
                # 未识别的url
                self.fw.write(response.url + "\t unknown-------------\n")
                self.fw.flush()
            pass

    def parseMain(self, select, response, item):
        self.fw.write(response.url + "\tparseMain\n")

        print "parseMain"       
        item["shop_template"] = "Main"
        
        if response.body.find("地图坐标")!=-1:
            self.fw.write(response.url +" 地图坐标------------------------------")
            self.fw.flush()
        
        if response.body.find("门店介绍")!=-1:
            self.fw.write(response.url +" 门店介绍------------------------------")
            self.fw.flush()
        
        try:  
            breadcrumb = select.xpath(".//div[@class='breadcrumb']/b/a/span/text()").extract()
            item["shop_domain"] = breadcrumb[0]
            
            allBread = select.xpath(".//div[@class='breadcrumb']/b/a/@href").extract()[1:]#去掉第一个shop_domain
            
            shop_area_count = len([a for a in allBread if a.split("/")[-1].startswith("r")])
            shop_category_count = len([a for a in allBread if a.split("/")[-1].startswith("g")])
                        
            item["shop_area"] = ",".join(breadcrumb[1:1+shop_area_count])
            item["shop_category"] = ",".join(breadcrumb[1+shop_area_count: 1+shop_area_count + shop_category_count])
        except Exception, e:
            item["shop_domain"] = ""
            item["shop_area"] = ""
            item["shop_category"] = ""
            print e

        

        # shop info
        try:
            addressPrefix = select.xpath(".//span[@class='region']/text()").extract()[0]
            address = select.xpath(".//span[@itemprop='street-address']/text()").extract()[0]
            item["shop_address"] = addressPrefix + address
        except Exception, e:
            item["shop_address"] = ""
            print e
            
        try:
            item['shop_telphone'] = select.xpath(".//strong[@itemprop='tel']/text()").extract()[0]
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
        item = response.meta["item"]
        item["image_urls"] = []
        try:
            item["image_urls"] = select.xpath(".//a[@class='p-img']/img/@src").extract()
        except Exception, e:
            print e

        item["shop_flag"] = "yes"
        yield item
        pass
    
    #===========================================================================
    # parseMainBody
    #===========================================================================
    def parseMainBody(self, select, response, item):
        self.fw.write(response.url + "\tparseMainBody\n")
#         self.fw.flush()

        item["shop_template"] = "MainBody"
        print "parseMainBody"
        
        item["shop_domain"] = ""
        item["shop_area"] = ""
        item["shop_category"] = ""
        
        try:  
            breadcrumb = select.xpath(".//div[@class='breadcrumb']/b/a/span/text()").extract()
            item["shop_domain"] = breadcrumb[0]
            
            allBread = select.xpath(".//div[@class='breadcrumb']/b/a/@href").extract()[1:]#去掉第一个shop_domain
            
            shop_area_count = len([a for a in allBread if a.split("/")[-1].startswith("r")])
            shop_category_count = len([a for a in allBread if a.split("/")[-1].startswith("g")])
                        
            item["shop_area"] = ",".join(breadcrumb[1:1+shop_area_count])
            item["shop_category"] = ",".join(breadcrumb[1+shop_area_count: 1+shop_area_count + shop_category_count])
        except Exception, e:
            print e

        
#         self.fw.write(response.url + "\tparseMain\n")
#         self.fw.flush()
        # shop info
        item["shop_address"] = ""
        try:
            item["shop_address"] = select.xpath(".//div[@class='shop-addr']/span/text()").extract()[0]
        except Exception, e:
            print e
            
        item['shop_telphone'] = ""
        try:
            item['shop_telphone'] = select.xpath(".//div[@class='shopinfor']/p/span/text()").extract()[0]
        except Exception, e:
            print e
#              
#         # shop bus and other info
        
        item["shop_open_time"] = ""
        item["shop_description"] =""
        try:
            showWrap = select.xpath(".//div[@class='con J_showWarp']//tr")
            for li in showWrap:
                html = li.extract()
                if html.find("营业") != -1:
                    item["shop_open_time"] = li.xpath(".//div[@class='cont']/text()").extract()[0]
                elif html.find("商户介绍") != -1:
                    item["shop_description"] = li.xpath(".//div[@class='cont']/text()").extract()[0]
                pass
        except Exception, e: 
            print e
       
        
        item["image_urls"] = []
        try:
            item["image_urls"] = select.xpath(".//div[@class='slidephotos J_small']/img/@src").extract()
        except Exception, e:
            print e

        item["shop_bus_line"] = "" # TODO
        item["shop_map_attitude"] = ""
        item["shop_contact_man"] = ""

        item["shop_flag"] = "yes"
        return item
        pass
    
    def parseBody(self, select, response, item):
        self.fw.write(response.url + "\parseBody\n")
        self.fw.flush()
        
        item["shop_template"] = "Body"
        try:  
            breadcrumb = select.xpath(".//div[@class='breadcrumb']/a/text()").extract()
            breadcrumb = [a.strip() for a in breadcrumb]
            item["shop_domain"] = breadcrumb[0]
            
            allBread = select.xpath(".//div[@class='breadcrumb']/a/@href").extract()[1:]#去掉第一个shop_domain
            
            shop_area_count = len([a for a in allBread if a.split("/")[-1].startswith("r")])
            shop_category_count = len([a for a in allBread if a.split("/")[-1].startswith("g")])
                        
            item["shop_area"] = ",".join(breadcrumb[1:1+shop_area_count])
            item["shop_category"] = ",".join(breadcrumb[1+shop_area_count: 1+shop_area_count + shop_category_count])
        except Exception, e:
            item["shop_domain"] = ""
            item["shop_area"] = ""
            item["shop_category"] = ""
            print e

        
#         self.fw.write(response.url + "\tparseMain\n")
#         self.fw.flush()
        # shop info
        try:
            addressPrefix = select.xpath(".//span[@itemprop='locality region']/text()").extract()[0].strip()
            address = select.xpath(".//span[@itemprop='street-address']/text()").extract()[0].strip()
            item["shop_address"] = addressPrefix + address
        except Exception, e:
            item["shop_address"] = ""
            print e
            
        try:
            item['shop_telphone'] = select.xpath(".//span[@itemprop='tel']/text()").extract()[0]
        except Exception, e:
            item['shop_telphone'] = ""
            print e
#              
#         # shop bus and other info
        
        item["shop_open_time"] = ""
        item["shop_bus_line"] = ""
        item["shop_description"] = ""
        
        try:
            otherInfo = select.xpath(".//div[@class='other J-other Hide']/p[@class='info info-indent']")
            for li in otherInfo:
                html = li.extract()
                if html.find("营业") != -1:
                    item["shop_open_time"] = li.xpath(".//span/text()")[1].extract().strip()
                elif html.find("公交") != -1:
                    self.fw.write("body bus line info---------")
#                     item["shop_bus_line"] = li.xpath(".//dd/span/text()").extract()[0]
                elif html.find("商户简介") != -1:
                    item["shop_description"] = li.xpath(".//text()").extract()[2].strip()
                pass
        except Exception, e:
            print e
       
        item["shop_map_attitude"] = ""
        item["shop_contact_man"] = ""
        
        photoUrl = response.url + "/photos"
        request = Request(photoUrl, callback=self.parseMainBodyPhotos, priority=123)
        request.meta["item"] = copy.deepcopy(item)
        return request

    #===========================================================================
    # parseMainPhotos
    # return [item, request]
    #===========================================================================
    def parseMainBodyPhotos(self, response):
        # 解析 http://www.dianping.com/shop/18097023/photos
        select = Selector(response)
        item = response.meta["item"]
        item["image_urls"] = []
        try:
            item["image_urls"] = select.xpath(".//div[@class='picture-list']//img/@src").extract()
        except Exception, e:
            print e

        item["shop_flag"] = "yes"
        yield item
        pass
    
    def parseBreadcrumb_wrapper(self, select, response, item):
        item["shop_template"] = "MainBodyBreadcrumb-wrapper"
        print "parseBreadcrumb_wrapper"
        
        self.fw.write(response.url + " MainBodyBreadcrumb-wrapper\n")
#         self.fw.flush()
        
        item["shop_domain"] = ""
        item["shop_area"] = ""
        item["shop_category"] = ""
        
        try:  
            breadcrumb = select.xpath(".//div[@class='breadcrumb-wrapper']/ul/li/a/text()").extract()
            item["shop_domain"] = breadcrumb[0]
            
            allBread = select.xpath(".//div[@class='breadcrumb-wrapper']/ul/li/a/@href").extract()[1:]#去掉第一个shop_domain
            
            shop_area_count = len([a for a in allBread if a.split("/")[-1].startswith("r")])
            shop_category_count = len([a for a in allBread if a.split("/")[-1].startswith("g")])
                        
            item["shop_area"] = ",".join(breadcrumb[1:1+shop_area_count])
            item["shop_category"] = ",".join(breadcrumb[1+shop_area_count: 1+shop_area_count + shop_category_count])
        except Exception, e:
            print e

        
#         self.fw.write(response.url + "\tparseMain\n")
#         self.fw.flush()
        # shop info
        item["shop_address"] = ""
        try:
            address = "".join(select.xpath(".//p[@class='shop-contact address']/text()").extract()).strip()
            area = select.xpath(".//a[@class='region']/text()").extract()[0]
            item["shop_address"] = area + address 
        except Exception, e:
            print e
            
        item['shop_telphone'] = ""
        try:
            item['shop_telphone'] = select.xpath(".//div[@class='shop-contact telAndQQ']/span/strong/text()").extract()[0]
        except Exception, e:
            print e
#              
#         # shop bus and other info
        
        item["shop_open_time"] = ""
        
        try:
            item["shop_open_time"] =select.xpath(".//div[@class='business-card clearfix']//tr/td/text()").extract()[1]
        except Exception, e: 
            print e
        
        item["shop_description"] =""
        try:
            item["shop_description"] = "|".join([text.strip() for text in select.xpath(".//div[@class='business-card clearfix']/p//text()").extract()]).strip("|")
        except Exception, e: 
            print e
       
        
        item["image_urls"] = []
        try:
            item["image_urls"] = select.xpath(".//div[@class='slider-wrapper J_wrapPic']//img/@src").extract()
        except Exception, e:
            print e

        item["shop_bus_line"] = ""
        item["shop_map_attitude"] = ""
        item["shop_contact_man"] = ""
            
        item["shop_flag"] = "yes"
        
        return item
#         photoUrl = response.url + "/photos"
#         print photoUrl
#         request = Request(photoUrl, callback=self.parseMainPhotos, priority=123)
#         request.meta["item"] = copy.deepcopy(item)
#         return request
        pass    
