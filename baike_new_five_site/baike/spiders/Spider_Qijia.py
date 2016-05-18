#encoding=utf-8
import uuid
from scrapy.spiders import Spider

from scrapy.selector import Selector
from scrapy.spiders.crawl import CrawlSpider, Rule
from scrapy.linkextractors.sgml import SgmlLinkExtractor

from baike.items import Baike_Qijia_Item


class Spider_Qijia(Spider):
    name = 'qijia'
    
    allowed_domain = ['jia.com/baike']
    start_urls = [
                    #'http://www.jia.com/baike/bdetail-3083/'
                  ]
    start_id = 1000
    scope = 10000
    
    for id in xrange(start_id, scope):
        start_urls.append("http://www.jia.com/baike/bdetail-%s"%(id))
        
    def parse(self,response):
        global uuid
        #生成uuid的namespace，和当前链接相关
        namespace = uuid.uuid3(uuid.NAMESPACE_URL,response.url)
        
        item = Baike_Qijia_Item()
        split1 = '>'
        split2 = ';'
        item['title_id'] = response.url.split("-")[1][:-1] #取url中的id
        
        item['title_url'] = response.url
        item['title_name'] = Selector(response).xpath("//div[@class='artical-des atical-des1 fl']/h1/text()").extract()
        item['title_introduction'] = Selector(response).xpath("//div[@class='artical-des atical-des1 fl']/div[1]/i/text()").extract()
        #分类用>连接成为一个字符串
        category = Selector(response).xpath("//div[@class='bk-nav clearfix']/a/text()").extract()
        item['title_category'] = split1.join(category)
        item['content_name'] = Selector(response).xpath("//div[@class='atical-floor']/div/h2/a/text()").extract()
        #内容主键生成,标题表uuid_list生成
        content_uuid = []
        index = 1
        while index <= len(item['content_name']):
            con_id = uuid.uuid3(namespace,'%d'%index)
            content_uuid.append(con_id.hex)
            index = index + 1
        item['content_uuid'] = content_uuid
        item['content_uuid_list'] = split2.join(content_uuid)
        #content_text得处理text里面的html标签
        item['content_text'] = Selector(response).xpath("//div[@class='atical-floor']/div/div/div/p").extract()
        
        item['image_urls'] = Selector(response).xpath("//div[@class='floor-content floor-content-ml clearfix']/div/img/@src").extract()
        
        return item
        