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

from jiuzheng.items import JiuzhengItem

logging.basicConfig(level=logging.INFO,
                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                datefmt='%a, %d %b %Y %H:%M:%S',
                filename='tobato.log',
                filemode='a')

class SpiderTmallShop(Spider):
    name = 'jiuzheng'
    
    allowed_domain = ['jiuzheng.com']
    start_urls = [
                  "http://www.jiuzheng.com/ask-detail/id-48534.html",
                  "http://www.jiuzheng.com/ask-detail/id-37319.html",
                  ]

    for id in xrange(1, 1000):  # todo
        start_urls.append("http://www.jiuzheng.com/ask-detail/id-%s.html" % id)
        
    def __init__(self):
        self.questionIdPatten = re.compile("id-[0-9]+")
        pass

    def parse(self, response):
        select = Selector(response)
        item = JiuzhengItem()
        
        question_id = self.questionIdPatten.findall(response.url)[0]
        question_id = question_id[3:]
        item["question_id"] = question_id
        
        item["question_title"] = select.css(".ask-detail").xpath("./h3/text()").extract()[0]
        
        try:    
            # optinoal
            item["question_description"] = select.css(".ask-sub-info")[0].extract()[26:-6].strip()
            pass    
        except Exception, e:
            item["question_description"] = ""
            print e
        
        item["question_category"] = ""
        try:
            item["question_category"] = ">".join(select.css(".breadcrumb-arrow").xpath(".//li/a/text()")[2:].extract())
            pass
        except Exception, e:
            print e
            
        item["is_question"] = "yes"
        yield item
        
        item = copy.deepcopy(item)
        item["question_category"] = ""
        item["question_description"] = ""
        item["question_title"] = ""
        
        
        # best_answer
        bestFlag = False
        try:
            item["answer_id"] = str(uuid.uuid1())
            item["answer_content"] = select.css(".optimum-box").xpath(".//div/div[@class='detail-cont']").extract()[0][25:-6].strip()
            item["is_best"] = "yes"
            
            item["is_question"] = "no"
            bestFlag = True
            yield item
            item = copy.deepcopy(item)
        except Exception, e:
            print e            
         
        # other answers
        other_answers_list = select.css(".detail-cont")
        if bestFlag:
            other_answers_list = other_answers_list[1:]  # 如果有最佳答案，那么排除第一个最佳答案
        
        for other_answer in other_answers_list:
            item["answer_id"] = str(uuid.uuid1())
            item["answer_content"] = other_answer.extract()[25:-6].strip()
            item["is_best"] = "no"
            
            item["is_question"] = "no"
            yield item
            item = copy.deepcopy(item)
            pass
