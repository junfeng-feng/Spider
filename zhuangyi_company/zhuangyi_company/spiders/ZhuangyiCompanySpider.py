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
import time
import sys
from scrapy.item import Item
reload(sys)
sys.setdefaultencoding('utf-8')

from zhuangyi_company.items import ZhuangyiCompanyItem

logging.basicConfig(level=logging.INFO,
                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                datefmt='%a, %d %b %Y %H:%M:%S',
                filename='zhuangyi.log',
                filemode='a')

class SpiderZhuangyiCompany(Spider):
    name = 'zhuangyi_company'
    
    allowed_domain = ['zhuangyi.com']
    start_urls = [
#                   "http://www.14994.zhuangyi.com/",
#                 "http://www.7054.zhuangyi.com/",
#                   "http://www.161207.zhuangyi.com"
                  ]

#     company_ids = [int(id.strip()) for id in  file("company_id.txt").readlines()]
#     print company_ids
#     time.sleep(6000)
    for id in xrange(79849, 90000):  # samples
        # 去掉已经爬取的
#         if not id in company_ids:
        start_urls.append("http://www.%s.zhuangyi.com/" % id)
        
    def __init__(self):
        self.digitalPattern = re.compile("[0-9]+")
        self.pageUrl = r"http://www.tobosu.com/ask/question/%s.html?p=%s&order=time"
        self.aPrefixPattern = re.compile("<a.*?>")
        self.aSuffixPattern = re.compile("< */a *>")
        self.fw = file("pages.list", "a")
        
        self.index = 1
        pass
    
    def parse(self, response):
        select = Selector(response)
        company_id = self.digitalPattern.findall(response.url)[0]
        self.index += 1
        
        if int(self.index) % 10 == 0:
#             time.sleep(10)
            pass
        
        item = self.initItem()
        item["company_id"] = company_id
        try:
            item["company_name"] = select.xpath(".//title/text()").extract()[0].strip().split("-")[0]
        except Exception, e:
            print e
        
        try:
            item["company_shortname"] = select.css(".s_tit").xpath(".//text()").extract()[0]
            
            space_index = item["company_shortname"].rfind(" ")
            item["city"] = item["company_shortname"][:space_index]
        except Exception, e:
            print e
            
        try:
            item["address"] = select.css(".s_add").xpath(".//span/text()").extract()[0].strip()
        except Exception, e:
            print e
        # logo
        logoUrl = select.css(".s_logo").xpath(".//img/@src").extract()[0]
        if not logoUrl.startswith("http") and logoUrl.find("googleapis.com") == -1:
            item["image_urls"] = ["http://www.zhuangyi.com" + logoUrl]
        else:
            item["image_urls"] = [logoUrl]
        
        item["service_zone"] = response.url
        item["is_designer"] = "no"        
            
        introduction_url = response.url + "/gsjj.aspx"
        request = Request(url=introduction_url, callback=self.parseCompanyIntroduction, priority=123456)
        request.meta["data"] = item
        yield request 
       
        designer_page = response.url + "/designer.aspx"
        request = Request(url=designer_page, callback=self.parseDesignerPage, priority=123456)
        request.meta["data"] = company_id
        request.meta["urlPrefix"] = response.url
        yield request 
        
    def parseDesignerPage(self, response):
        select = Selector(response)
        
        designerUrls = select.css(".designer_main").xpath(".//a/@href").extract()[::2]
        for url_d in designerUrls:
            if str(url_d).startswith("http"):
                request = Request(url=url_d, callback=self.parseDesigner, priority=1234567)
                request.meta["data"] = response.meta["data"]
                yield request 
            pass
        
        # 在第一页遍历其他所有页面遍历其他页面
        if not "page" in response.meta:
            designerPageUrls = set(select.css(".paginator").xpath(".//a/@href").extract())
            for url_d_page in designerPageUrls:
                url_d_page = response.meta["urlPrefix"] + url_d_page
                request = Request(url=url_d_page, callback=self.parseDesignerPage, priority=1234567)
                request.meta["data"] = response.meta["data"]
                request.meta["page"] = "1"
                yield request 
        pass
    
    def parseDesigner(self, response):
        select = Selector(response)
        company_id = response.meta["data"]
        item = self.initItem()
        item["company_id"] = company_id
        
        item["position"] = response.url
        item["designer_id"] = self.digitalPattern.findall(response.url)[0]
        item["designer_name"] = select.css(".s_tit").xpath(".//h1/a/text()").extract()[0]
        
        allInfo = select.css(".s_txtjbzl").xpath(".//span/text()").extract()
        item["position"] = response.url
        item["good_at_filed"] = ""
        try:
            item["good_at_style"] = allInfo[3].replace(" ", ",")
        except Exception, e:
            self.fw.write(str(item) + "\n")
            print e        
        
        item["image_urls"] = []
        image_urls = select.css(".s_logo").xpath(".//img/@src").extract()
        for url  in image_urls:
            if not url.startswith("http") and url.find("googleapis.com") == -1 and url.find("gstatic") == -1:
                item["image_urls"].append("http://www.zhuangyi.com" + url)
            else:
                item["image_urls"].append(url)   
            pass
        try:
            introduction_url = select.css(".smjj").xpath(".//a/@href").extract()[0]
        except Exception, e:
            self.fw.write(str(item) + "\n")
            print e
            
        request = Request(url=introduction_url, callback=self.parseDesignerIntroduction, priority=1234567)
        request.meta["data"] = item
        yield request 
        
    def parseDesignerIntroduction(self, response):
        select = Selector(response)
        item = response.meta["data"]    
        item["designer_introduction"] = select.css(".aboutme_main").extract()[0][26:-6].strip()  
        item["is_designer"] = "yes"
        yield item
        pass 
    
           
    def parseCompanyIntroduction(self, response):
        select = Selector(response)
        item = response.meta["data"]
        
        # 去掉a标签
        blog_content = select.css(".aboutme_main").extract()[0][26:-6].strip()
        blog_content, _ = self.aPrefixPattern.subn("", blog_content)
        blog_content, _ = self.aSuffixPattern.subn("", blog_content)  
        item["company_des"] = blog_content
        
        image_urls = select.css(".aboutme_main").xpath(".//img/@src").extract()
        for url  in image_urls:
            if not url.startswith("http"):
                item["image_urls"].append("http://www.zhuangyi.com" + url)
#             else:
#                 item["image_urls"].append(url)
            
        item["is_designer"] = "no"
        yield item
        pass
    
    
    def initItem(self):
        item = ZhuangyiCompanyItem()
        item["designer_id"] = ""
        item["company_id"] = ""
        item["designer_name"] = ""
        item["position"] = ""
        item["good_at_filed"] = ""
        item["good_at_style"] = ""
        item["designer_introduction"] = ""
        item["head_img"] = ""
        
        item["company_id"] = ""
        item["company_name"] = ""
        item["company_shortname"] = ""
        item["company_koubei"] = ""
        item["service_zone"] = ""
        item["price"] = ""
        item["service_content"] = ""
        item["decoration_type_jia"] = ""
        item["decoration_type_gong"] = ""
        item["decoration_style"] = ""
        item["city"] = ""
        item["address"] = ""
        item["company_des"] = ""
        item["logo"] = ""
        
        item["is_designer"] = "yes"
        return item
