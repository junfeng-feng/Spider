#encoding=utf-8
import re

from scrapy.selector import Selector
from scrapy.spiders import Spider

from jcmd.items import shopItem


#from scrapy.linkextractors.sgml import SgmlLinkExtractor
#from scrapy.spiders.crawl import CrawlSpider, Rule
class shop_spider(Spider):
    name = 'shop'
    
    allowed_domain = ['china-10.com/']
    
    start_urls = [
                  ]
    
    begin = 200000
    scop = 100000
    i = 0
    while(i<=scop):
        url = 'http://www.china-10.com/shop/%d.html' % (begin+i)
        start_urls.append(url)
        i = i + 1
    
    
    #门店url
    rule_shopurl = re.compile(r'[\d]+.html$')
    #获取id规则
    rule_get_id = re.compile(r'[\d]+')
    #门店类型
    rule_get_shoptype = re.compile(u'\u5e97\u94fa\u7c7b\u578b')
    #联系电话
    rule_get_shopphone = re.compile(u'\u8054\u7cfb\u7535\u8bdd\uff1a')
    #所在地址
    rule_get_shopaddress = re.compile(u'\u6240\u5728\u5730\u5740\uff1a')
    #去除html规则
    rule_remove_html= re.compile(r'<[^>]+>',re.S)
    #空格分隔符
    split_blank = ' '
         
    def parse(self,response):
        
        sItem = shopItem()
        
        sel = Selector(response)
        #shop的url尾部
        tail= shop_spider.rule_shopurl.findall(response.url)[0]
        #得到shopid
        sItem['shop_id'] = shop_spider.rule_get_id.findall(tail)[0]
        #shop_name pipe中去除标签
        sItem['shop_name']= sel.xpath(".//div[@class='shoptitle']").extract()[0]
        #相关品牌信息
        brand_info = sel.xpath(".//div[@class='keywordlist']/div/a[@key='brandid']")
        sItem['brand_id'] = brand_info.xpath("@tid").extract()[0] if brand_info.xpath("@tid").extract() else ""
        sItem['brand_name'] = brand_info.xpath("@qname").extract()[0] if brand_info.xpath("@qname").extract() else ""
        #相关分类信息
        category_info = sel.xpath(".//div[@class='keywordlist']/div/a[@key='catid']")
        sItem['category_id'] = category_info.xpath("@tid").extract()[0] if category_info.xpath("@tid").extract() else ""
        sItem['category_name'] = category_info.xpath("@qname").extract()[0] if category_info.xpath("@qname").extract() else ""
        #门店介绍,pipe去除html
        shop_introduction = sel.xpath(".//div[@class='shopbox']/div").extract()
        sItem['shop_introduction'] = shop_introduction[0] if shop_introduction else ""
        
        #相关图片
        sItem['image_urls'] = sel.xpath(".//div[@class='shopbox shopinfo']/div/img/@src").extract()
        #其他详细信息
        sItem['url'] = response.url
        sItem['shop_type'] = ""
        sItem['shop_address'] = ""
        sItem['shop_phone'] = ""
        sItem['shop_site'] = ""
        #门店信息列表
        shop_infolist= sel.xpath(".//div[@class='shopbox shopinfo']/ul/li")
        
        
        for si in shop_infolist:
            
            title = si.xpath("./em[1]").extract()[0]
            #content = si.xpath("./span").extract()
            if shop_spider.rule_get_shoptype.findall(title):
                
                sItem['shop_type'] = "".join(si.xpath("./span").extract())
                
            elif shop_spider.rule_get_shopphone.findall(title):
                
                con_phone= si.xpath("./span/text()").extract()
                
                sItem['shop_phone'] = con_phone[0]
                
                if len(con_phone)>1:
                    
                    sItem['shop_person'] = con_phone[-1]
                else:
                    sItem['shop_person'] = ""
                
            elif shop_spider.rule_get_shopaddress.findall(title):
                
                con_address = (si.xpath("./span/@title").extract()[0]).split(self.split_blank)
                
                sItem['shop_address'] = con_address[-1]
                
                sItem['shop_site'] = self.split_blank.join(con_address[:-1])
            
        yield sItem
        
        
        
        
        
        
        