#encoding=utf-8
import uuid
import re
from scrapy.http.request import Request
from scrapy.selector import Selector
from scrapy.spiders import Spider

from jcmd.items import brandItem


#from scrapy.linkextractors.sgml import SgmlLinkExtractor
#from scrapy.spiders.crawl import CrawlSpider, Rule
class brand_spider(Spider):
    name = 'brand'
    
    allowed_domain = ['china-10.com/']
    
    start_urls = ['http://www.china-10.com/brand/1.html']
    
    index = 58227
    
    while(index<=100000):
        url = 'http://www.china-10.com/brand/%d.html' % index
        start_urls.append(url)
        index = index + 1
    
    #品牌url
    rule_brandurl = re.compile(r'[\d]+.html$')
    #获取id规则
    rule_get_id = re.compile(r'[\d]+')
        
    def parse(self,response):
        
        if response.status == 200:
            split = ","
            bItem = brandItem()
            sel = Selector(response)
            #brand的url尾部
            tail = brand_spider.rule_brandurl.findall(response.url)[0]
            #获取brand_id
            bItem['brand_id'] = brand_spider.rule_get_id.findall(tail)[0]
            
            bItem['brand_chname'] = sel.xpath("//div[@class='keywordlist']/div/span/text()").extract()[0]
            #category_url = sel.xpath("//div[@class='menu_xglist']/ul/li/a/@href").extract()
            #category_name = sel.xpath("//div[@class='menu_xglist']/ul/li/a/text()").extract()
            #category_uuid_list = []
            #for url in category_url:
                #category_uuid = uuid.uuid3(uuid.NAMESPACE_URL,str(url))
                #category_uuid_list.append(category_uuid.hex)
                
            #bItem['category_uuid'] = split.join(category_uuid_list)
            #bItem['category_name'] = split.join(category_name)
            bItem['category_id'] = ""
            bItem['category_name'] = ""
            
            bItem['brand_info'] = sel.xpath("//div[@class='brandinfo']/dl/dd/text()").extract()[0]
            bItem['brand_introduction'] = sel.xpath("//div[@class='moreinfo']").extract()[0]
            brand_detail = sel.xpath("//div[@class='brandinfo']/ul/li").extract()
            bItem['brand_leader'] = brand_detail[2]
            bItem['brand_address'] = sel.xpath("//div[@class='brandinfo']/ul/li[4]/em/text()").extract()[0]
            brand_word = sel.xpath("//div[@class='brandinfo']/ul/li[7]/em/text()").extract()
            if brand_word:
                bItem['brand_word'] = brand_word[0]
            else:
                bItem['brand_word'] = ""
            bItem['brand_website'] = sel.xpath("//div[@class='brandinfo']/ul/li[5]/a/@href").extract()[0]
            bItem['brand_phone'] = brand_detail[5]
            bItem['brand_year'] = []
            
            logo = sel.xpath("//div[@class='brandinfo']/dl/dt//img/@src").extract()[0]
            img = sel.xpath("//div[@class='bimage']/img/@src").extract()[0]
            bItem['image_urls'] = [logo,img]
            bItem['url'] = response.url
            
            yield bItem
        
            
            
        
            
   
        