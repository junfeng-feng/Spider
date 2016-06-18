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
reload(sys)
sys.setdefaultencoding('utf-8')

from tobosu.items import ZhuangyiCompanyItem

logging.basicConfig(level=logging.INFO,
                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                datefmt='%a, %d %b %Y %H:%M:%S',
                filename='tobosu.log',
                filemode='a')

class SpiderZhuangyiCompany(Spider):
    name = 'zhuangyi_company'
    
    allowed_domain = ['zhuangyi.com']
    start_urls = [
#                 "http://www.tobosu.com/ask/question/3094.html", #描述
#                   "http://www.tobosu.com/ask/question/1427.html",  # 翻页
                  ]

#     for id in xrange(103750, 500000):  # samples
#         start_urls.append("http://www.tobosu.com/ask/question/%s.html" % id)
        
    def __init__(self):
        self.digitalPattern = re.compile("[0-9]+")
        self.pageUrl = r"http://www.tobosu.com/ask/question/%s.html?p=%s&order=time"
        pass
    
    def parse(self, response):
        if response.status == 404:
            # 如果返回404，可以直接返回，不需要处理
            logging.info("response.status:" + response.status)
            return
        
        select = Selector(response)
        if "data" in response.meta:
            isNextPage = response.meta["data"]
        else:
            isNextPage = "firstPage"
        
        question_id = self.digitalPattern.findall(response.url)[0]

        
        # 只在第一页取标题
        if isNextPage == "firstPage":
            item = TobosuItem()
            item["question_id"] = question_id
            item["question_title"] = select.css(".aqq-title").xpath(".//h1/text()").extract()[0]
            try:
                item["question_description"] = select.css(".des").extract()[0][15:-4].strip()
            except Exception, e:
                item["question_description"] = ""
                print e
        
            try:
                big_category = ",".join(select.css(".recom-lab").xpath(".//a/text()")[1:].extract())
            except Exception, e:
                big_category = ""
                print e
           
            item["question_category"] = big_category 
            item["is_question"] = "yes"
            yield item
        
            # pages 取后续页
            try:
                totoal_answers = select.css(".other-answer").xpath(".//span/text()").extract()[0]
                totoal_answers = self.digitalPattern.findall(totoal_answers)[0]
                pages = int(totoal_answers) / 5 + 1  # page从2开始计算
                
#                 print "00000000："+str(pages)
                for page in xrange(2, pages + 1):  # xrange[)
                    requestUrl = self.pageUrl % (question_id, page)
#                     logging.info("-------------requestUrl:" + requestUrl)
                    request = Request(url=requestUrl, callback=self.parse, priority=123456)
                    request.meta["data"] = "nextpage"
                    yield request
                    pass
            except Exception, e:
                print e
        try:        
            # 有的问题没有答案，所以使用try
            # other answer
            ask_answer_li_list = select.css(".des-info")
            for li in ask_answer_li_list:
                item = TobosuItem()
                item["question_id"] = question_id
                item["answer_id"] = str(uuid.uuid1())
                item["answer_content"] = li.extract()[20:-4]
                item["is_best"] = "no"
                 
                item["is_question"] = "no"
                yield item
                pass
        except Exception, e:
            print e
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
        pass