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

from tobato.items import TobatoItem

logging.basicConfig(level=logging.INFO,
                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                datefmt='%a, %d %b %Y %H:%M:%S',
                filename='tobato.log',
                filemode='a')

class SpiderTmallShop(Spider):
    name = 'tobato'
    
    allowed_domain = ['to8to.com']
    start_urls = [
#                   "http://www.to8to.com/ask/k2003794.html",
#                   "http://www.to8to.com/ask/k42622.html",
#                 "http://www.to8to.com/ask/k2193132.html",
#                 "http://www.to8to.com/ask/k866853.html",
                  ]

    for id in xrange(0, 3000000):
        start_urls.append("http://www.to8to.com/ask/k%s.html" % id)
        
    def __init__(self):
        self.questionIdPatten = re.compile("k[0-9]+")
        self.pageUrl = "http://www.to8to.com/ask/k%s-%s.html"
        pass
    
    def parse(self, response):
        select = Selector(response)
        if "data" in response.meta:
            isNextPage = response.meta["data"]
        else:
            isNextPage = "firstPage"
        
        
        question_id = self.questionIdPatten.findall(response.url)[0]
        question_id = question_id[1:].replace("-", "")
        
        item = TobatoItem()
        item["question_id"] = question_id
        
        # pages 取第二页
        try:
            logging.info("# pages 取第二页")
            totoal_answers = select.css(".pages").xpath(".//em/b/text()").extract()[0]
            pages = int(totoal_answers) / 20 + 1  # page从2开始计算
            
            for page in xrange(2, pages + 1):  # xrange[)
                requestUrl = self.pageUrl % (question_id, page)
                logging.info(requestUrl + "---------------------------------------")
                request = Request(url=requestUrl, callback=self.parse, priority=123456)
                request.meta["data"] = "true"
                yield request
                pass
        except Exception, e:
            print e
        
        item["question_title"] = select.css(".ask_qustion").xpath(".//h1/text()").extract()[0]
        try:
            item["question_description"] = select.css(".ask_qustion").xpath("./p").extract()[0][21:-4]
        except Exception, e:
            item["question_description"] = ""
            print e
        
        item["imageStatus"] = {}
        item["image_urls"] = []
        try:
            question_image_url = select.css(".ask_qustion")[0].xpath(".//img/@src").extract()[0]
            item["image_urls"].append(question_image_url)
            
            item["imageStatus"] = {question_id:question_image_url}
        except Exception, e:
            print e
        
        
        try:
            big_category = select.css(".has_arrow")[2].xpath(".//a/text()").extract()[0]
        except Exception, e:
            big_category = ""
            print e
        try:
            small_category = select.css(".has_arrow")[3].xpath(".//a/text()").extract()[0]
        except Exception, e:
            small_category = ""
            print e
       
        item["question_category"] = big_category + "," + small_category
        item["is_question"] = "yes"
        yield item
        item = copy.deepcopy(item)
        
        item["question_title"] =""
        item["question_category"] = ""
        item["question_description"] = ""
        item["image_urls"] = []
        
        
        best_answer_flag = False
        try:        
            # 有的问题没有答案，所以使用try
            try:
                # best
                item["answer_id"] = str(uuid.uuid1())
                item["answer_content"] = select.css(".best_answer").xpath("./p").extract()[0][21:-4]
                item["is_best"] = "yes"
                # 如果最佳答案有图片
                try:
                    image_url = "http://www.to8to.com" + select.css(".best_answer").xpath(".//img/@src")[0].extract()
                    item["image_urls"].append(image_url)
                    
                    item["imageStatus"][item["answer_id"]] = image_url
                except Exception, e:
                    print e
                    
                best_answer_flag = True
                if not isNextPage == "true":#如果是翻页请求，则不保存最佳答案
                    #是第一页，则保存最佳答案
                    item["is_question"] = "no"
                    item["image_urls"] = []
                    yield item
                    item = copy.deepcopy(item)
            except Exception, e:
                print e
                           
            # other answer
            ask_answer_li_list = select.css(".ask_answer_li")
            if best_answer_flag:
                ask_answer_li_list = ask_answer_li_list[1:]  # 有最佳答案，就去掉最佳答案
                
            for li in ask_answer_li_list:
                item = copy.deepcopy(item)  # 还是需要复制一份，否则数据id是重复的
                item["answer_id"] = str(uuid.uuid1())
                
                item["answer_content"] = li.xpath(".//p").extract()[0][21:-4]
                item["is_best"] = "no"
                
                try:
                    image_url = "http://www.to8to.com" + li.xpath(".//img/@src")[0].extract()
                    item["image_urls"].append(image_url)
                    
                    item["imageStatus"][item["answer_id"]] = image_url
                except Exception, e:
                    print e
                
                item["is_question"] = "no"
                item["image_urls"] = []
                yield item
                item = copy.deepcopy(item)
                pass
        except Exception, e:
            print e
        pass
