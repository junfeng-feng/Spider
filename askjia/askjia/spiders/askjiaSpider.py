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

from askjia.items import AskjiaItem

logging.basicConfig(level=logging.INFO,
                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                datefmt='%a, %d %b %Y %H:%M:%S',
                filename='tobato.log',
                filemode='a')

class SpiderTmallShop(Spider):
    name = 'askjia'
    
    allowed_domain = ['jia.com']
    start_urls = [
                "http://ask.jia.com/a-812082.html",
                  "http://ask.jia.com/a-217678.html",
                  ]

    for id in xrange(1007, 100000):#todo
        start_urls.append("http://ask.jia.com/a-%s.html" % id)
        
    def __init__(self):
        self.questionIdPatten = re.compile("a-[0-9]+")
        
        self.pageUrl = "http://www.to8to.com/ask/k%s-%s.html"
        pass
    
    def parse(self, response):
        select = Selector(response)
        item = AskjiaItem()
        question_id = self.questionIdPatten.findall(response.url)[0]
        question_id = question_id[2:]
        item["question_id"] = question_id
        
        item["question_title"] = "".join(select.css(".timu_text").xpath(".//h1/text()").extract()).strip()
        
        
        try:    
            # optinoal
            item["question_description"] = "".join(select.css(".timu_buchong").xpath(".//text()").extract()[2:]).strip()
            pass    
        except Exception, e:
            item["question_description"] = ""
            print e
        
        item["image_urls"] = []
        try:    
            # optional
            question_img_url = select.css(".ducecon_img").xpath(".//img/@src").extract()[0]
            item["image_urls"].append(question_img_url)
            pass    
        except Exception, e:
            print e            
        pass
        item["question_category"] = ""
        try:
            item["question_category"] = ">".join(select.css(".ask6new_mbx").xpath(".//dt/a/text()").extract())
            pass
        except Exception, e:
            print e            
        item["is_question"] = "yes"
        yield item
        item = copy.deepcopy(item)
        item["question_category"] =""
        item["question_description"] = ""
        item["question_title"] = ""
        item["image_urls"] = []
        
        
        #best_answer
        try:
            item["answer_id"] = str(uuid.uuid1())
            item["answer_content"] =  select.css(".duce_con_ycn")[0].css(".con_text2")[0].extract()[30:-4]
            item["is_best"] = "yes"
            
            item["is_question"] = "no"
            item["image_urls"] = []
            yield item
            item = copy.deepcopy(item)
        except Exception, e:
            print e            
         
        #other answers
        other_answers_list = select.css(".duce_con")
        for other_answer in other_answers_list:
            item["answer_id"] = str(uuid.uuid1())
            item["answer_content"] = other_answer.css(".con_text2")[0].extract()[30:-4]
            item["is_best"] = "no"
            
            item["is_question"] = "no"
            item["image_urls"] = []
            yield item
            item = copy.deepcopy(item)
            pass
