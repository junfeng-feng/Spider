#encoding=utf-8
import uuid

from scrapy.selector import Selector
from scrapy.spiders.crawl import CrawlSpider, Rule
from scrapy.linkextractors.sgml import SgmlLinkExtractor

from baike.items import Baike_Qijia_Item


class Spider_Yihaojiaju(CrawlSpider):
    name = 'baike_yihaojiaju_spider'
    
    allowed_domain = ['yihaojiaju.com/baike']
    
    start_urls = [
                  'http://www.yihaojiaju.com/baike/420.html'
                    #'http://www.jia.com/baike/bdetail-3083/'
                  ]
    
#    rules = [
#             Rule(
#                  SgmlLinkExtractor(allow=('//www.jia.com/baike/bdetail')),
#                  callback='parse_item',
#                  follow=True
#                  )
#            ]
            
    def parse(self,response):
        
        print '*****************************\n'+response.url+'****************************\n'
        
        global uuid
        #生成uuid的namespace，和当前链接相关
        namespace = uuid.uuid3(uuid.NAMESPACE_URL,response.url)
        sel = Selector(response)
        item = Baike_Qijia_Item()
        split1 = '>'
        split2 = ';'
        item['title_url'] = response.url
        item['title_introduction'] = sel.xpath("//div[@class='top-info']/p/text()").extract()
        #分类用>连接成为一个字符串
        category = sel.xpath("//div[@class='nav-top']/a/text()").extract()
        item['title_category'] = split1.join(category)
        #拿最后一个作为title_name
        item['title_name'] = category[-1:]
        contents = sel.xpath("//ul[@class='catalog-list']/li")
        index = 1
        content_uuid = []
        content_names = []
        content_texts = []
        image_urls = []
        for content in contents:
            content_name = content.xpath('.//a[1]/strong/text()').extract()
            content_text = content.xpath(".//div[@class='p']").extract()
            image_url = content.xpath('.//img/@src').extract()
            con_id = uuid.uuid3(namespace,('%d'%index))
            index = index + 1
            #因为分析出的数据是个元组，因此加上坐标0
            content_uuid.append(con_id.hex)
            content_names.append(content_name[0])
            content_texts.append(content_text[0])
            image_urls.append(image_url[0])
        #内容主键生成,标题表uuid_list生成
        item['content_uuid'] = content_uuid
        item['content_uuid_list'] = split2.join(content_uuid)
        #content_text得处理text里面的html标签
        item['content_text'] = content_texts
        item['content_name'] = content_names
        item['image_urls'] = image_urls
        
        return item
        