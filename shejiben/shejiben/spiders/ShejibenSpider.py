
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
                "http://www.shejiben.com/sjs/5415229/",
#                     "http://www.shejiben.com/sjs/1466490/",
                  ]
        
    for id in file("shejiben/spiders/designerid.list"):
        id = id.strip()
        start_urls.append("http://www.shejiben.com/sjs/%s/" % (id))
        
    def __init__(self):
        self.idPatten = re.compile("[0-9]+")
        self.fw = file("pages.list", "a")
        pass
    
    def parse(self, response):
        #翻页请求，每10页，停30秒
        select = Selector(response)
        
        item = self.initItem()
        allNo = self.idPatten.findall(response.url)
        item["designer_id"] = allNo[0]
        
        item["designer_name"] = select.xpath(".//div[@class='about_he_con']/p/span/text()").extract()[0]
        
        #默认，顺序是：设计经验->擅长空间->所在地
        allInfo = select.xpath(".//div[@class='about_he_con']/div[@class='a_info']/p[@class='a_info_txt no_con']")
        #设计经验
        item["work_years"] = allInfo[0].xpath("./text()").extract()[0]
        #擅长空间
        item["style"] = ",".join(allInfo[1].xpath("./a/text()").extract())
        #所在城市
        item["apartment"] = allInfo[2].xpath("./text()").extract()[0]
        #简介
        item["introduction"] = select.xpath(".//p[@class='intro_award_con no_con']").extract()[0][34:-4]
  
        #头像
        item["image_urls"] = select.xpath(".//p[@class='about_he_img']/img/@src").extract()
        
        item["average_price"] = select.xpath(".//span[@class='price']/text()").extract()[0] + "元每平米"
        yield item
        
    def initItem(self):
        item =ShejibenItem()
        
        item["designer_id"]=""
        item["designer_name"]=""
        item["designer_phone_no"]=""
        item["designer_email"]=""
        item["designer_sex"]=""
        item["designer_position"]=""
        item["apartment"]=""
        item["style"]=""
        item["program"]=""
        item["average_price"]=""
        item["work_years"]=""
        item["introduction"]=""
        item["head_photo"]=""
        item["category_id"]=""
        item["category_name"]=""
        item["company_id"]=""
        item["company_name"]=""
        
        return item

