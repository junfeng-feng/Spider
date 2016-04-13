#encoding=utf-8
import re

from scrapy.selector import Selector
from scrapy.spiders import Spider

from jcmd.items import categoryItem


#from scrapy.linkextractors.sgml import SgmlLinkExtractor
#from scrapy.spiders.crawl import CrawlSpider, Rule
class category_spider(Spider):
    
    name = 'category'
    
    allowed_domain = ['china-10.com/']
    
    start_urls = [
                  'http://www.china-10.com/search/?catid=2202',
                  ]
    
    index = 2203
    
    while(index<=5000):
        url = 'http://www.china-10.com/search/?catid=%d' % index
        start_urls.append(url)
        index = index + 1
    
    #分类url规则
    rule_caturl = re.compile(r'catid=[\d]+$')
    #分类id规则
    rule_catid = re.compile(r'[\d]+')
    #子类判断
    rule_child = re.compile(u'\u4e0b\u7ea7\u884c\u4e1a')
    #同类判断
    rule_friend = re.compile(u'\u540c\u7ea7\u884c\u4e1a')
    #父类
    rule_father = re.compile(u'\u4e0a\u7ea7\u884c\u4e1a')
            
    def parse(self,response):
        
        sel = Selector(response)
        
        tail = category_spider.rule_caturl.findall(response.url)
        if tail:
            category_id = category_spider.rule_catid.findall(tail[0])[0]
            
        category_name = sel.xpath(".//div[@class='keywordlist']/div/a/@qname").extract()[0]
        
        if category_name == 'catid':
            
            return
    
        catlist = sel.xpath("//div[@class='menudiv']/ul[@class='navmenu']/li[2]/div[@class='otherblock']/ul[@class='nav-brandcatlist']")
        
        #category_father_id = []
        #category_child_id = []
        #category_father_name = []
        #category_child_name = []
        flag = False
        
        for cat in catlist:
            
            label = cat.xpath(".//li[1]/span/text()").extract()[0]
            
            if category_spider.rule_child.findall(label):
                flag = True
                links = cat.xpath(".//li/a")
                for link in links:
                    
                    child_url = link.xpath("@href").extract()[0]
                    child_name = link.xpath("text()").extract()[0]
                
                    tt = category_spider.rule_caturl.findall(child_url)
                    
                    if tt:
                        child_id = category_spider.rule_catid.findall(tt[0])[0]
                        #category_child_id.append(link_id)
                        #category_child_name.append(link_name)
                        ct = categoryItem()
                        ct['category_id'] = category_id
                        ct['category_name'] = category_name
                        ct['category_child_id'] = child_id
                        ct['category_child_name'] = child_name
                        ct['category_level'] = 'level2'
                        ct['url'] = response.url
                        yield ct
                        
                
            '''           
            elif category_spider1.rule_father.findall(label):
                
                links = cat.xpath(".//li/a")
                for link in links:
                    
                    link_url = link.xpath("@href").extract()[0]
                    link_name = link.xpath("text()").extract()[0]
                
                    tt = category_spider1.rule_caturl.findall(link_url)
                    
                    if tt:
                        link_id = category_spider1.rule_catid.findall(tt[0])[0]
                        category_father_id.append(link_id)
                        category_father_name.append(link_name)
            '''
        if not flag:
            ct = categoryItem()
            ct['category_id'] = category_id
            ct['category_name'] = category_name
            ct['category_child_id'] = ""
            ct['category_child_name'] = ""
            ct['category_level'] = 'level3'
            ct['url'] = response.url
            yield ct
            
        
        
        
             
        