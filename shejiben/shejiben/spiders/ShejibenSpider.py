# encoding=utf-8
import re
from scrapy.spiders import Spider
from scrapy.selector import Selector
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy import Request
import logging
import json
import copy
import time
import uuid
import sys
from Finder.Finder_items import item
from _cffi_backend import callback
reload(sys)
sys.setdefaultencoding('utf-8')

from shejiben.items import ShejibenItem

logging.basicConfig(level=logging.INFO,
                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                datefmt='%a, %d %b %Y %H:%M:%S',
                filename='dianping.log',
                filemode='a')

class SpiderTmallShop(Spider):
    name = 'shejiben'
    
    allowed_domain = ['shiejiben.com']
    start_urls = [
                "http://www.shejiben.com/sjs/116006/",
#                     "http://www.shejiben.com/sjs/1466490/",
                  ]
        
#     for id in file("shejiben/spiders/designerid.list"):
#         id = id.strip()
#         start_urls.append("http://www.shejiben.com/sjs/%s/" % (id))
        
    def __init__(self):
        self.idPatten = re.compile("[0-9]+")
        self.renqiPattern = re.compile("vnum:'([0-9]+?)'")
        self.renqiUrl = "http://www.shejiben.com/getuserdata.php?pos=homePage&uid=%s&s=0.8975054585491082"
        self.fw = file("pages.list", "a")
        pass
    
    def parse(self, response):
        select = Selector(response)
        
        item = self.initItem()
        allNo = self.idPatten.findall(response.url)
        designer_id = allNo[0]
        
        item["designer_id"] = designer_id
        
        item["designer_name"] = select.xpath(".//div[@class='about_he_con']/p/span/text()").extract()[0]
        
        try:
            item["signature"] = select.xpath(".//p[@class='company_name']/text()").extract()[0].strip()
        except Exception, e:
            print e
            
        # 默认，顺序是：设计经验->擅长空间->所在地
        allInfo = select.xpath(".//div[@class='about_he_con']/div[@class='a_info']/p[@class='a_info_txt no_con']")
        # 设计经验
        item["experience"] = allInfo[0].xpath("./text()").extract()[0]
        # 擅长空间
        item["style"] = ",".join(allInfo[1].xpath("./a/text()").extract())
        # 所在城市
        item["address"] = allInfo[2].xpath("./text()").extract()[0]
        # 简介
        item["introduction"] = select.xpath(".//p[@class='intro_award_con no_con']").extract()[0][34:-4]
  
        item["certification_rewords"] = select.xpath(".//div[@class='intro_award']/p[@class='intro_award_con']").extract()[0][27:-4]
  
        # 头像
        item["image_urls"] = select.xpath(".//p[@class='about_he_img']/img/@src").extract()
        
        item["fee"] = select.xpath(".//span[@class='price']/text()").extract()[0] + "元每平米"
        
        
        item["followers_number"] = select.xpath(".//span[@class='popularity_fans']/em/text()").extract()[0]
        item["follows"]= select.xpath(".//span[@class='attention']/em/text()").extract()[0]
        
        item["consulting_number"] = select.xpath(".//a[@id='sjsblog_yyzx']/em/text()").extract()[0]
        
        item["flag"] = "designer"
        request = Request(self.renqiUrl%(designer_id),callback=self.parseDesigner, priority=1234567)
        request.meta["item"] = item
        yield request
        
        item= self.initItem()
        item["flag"] = "rate"
        yield item
        
        item= self.initItem()
        item["flag"] = "blog"
        yield item
        
    def parseDesigner(self,response):
        item = response.meta["item"]
        try:
            item["renqi"] = re.compile("[^_]vnum:'([0-9]+?)'").findall(response.body)[0]
        except Exception,e:
            print e
        yield item
        pass
    
    def initItem(self):
        item = ShejibenItem()
        item["designer_id"] = ""
        item["designer_name"] = ""
        item["signature"] = ""
        item["consulting_number"] = ""
        item["view_number"] = ""
        item["designer_position"] = ""
        item["address"] = ""
        item["style"] = ""
        item["experience"] = ""
        item["fee"] = ""
        item["certification_rewords"] = ""
        item["introduction"] = ""
        item["head_photo"] = ""
        item["followers_number"] = ""
        item["renqi"] = ""
        item["follows"] = ""
        
        item["designer_id"] = ""
        item["rate_id"] = ""
        item["rate_content"] = ""
        item["rate_img"] = ""
        item["rate_addr"] = ""
        item["rate_datetime"] = ""
        
        item["designer_id"] = ""
        item["blog_id"] = ""
        item["blog_title"] = ""
        item["blog_datetime"] = ""
        item["view_number"] = ""
        item["blog_content"] = ""
        item["blog_img"] = ""
        item["blog_author"] = ""
        
        return item

