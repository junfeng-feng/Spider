#encoding=utf-8
import copy
import re
from scrapy import Request

from scrapy.selector import Selector
from scrapy.spiders import Spider

from zscompany.items import ZscompanyItem
import logging
logging.basicConfig(level=logging.INFO,
                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                datefmt='%a, %d %b %Y %H:%M:%S',
                filename='zscompany.log',
                filemode='a')

class zscompanyspider(Spider):
    file("a.txt", "w").write("")
    name = 'zscompany'
    
    allowed_domain = ['to8to.com/']
    start_urls = [
                  ]
    '''
    start_id = 593266
    scope = 1000
    
    for id in xrange(start_id, scope+start_id):
        start_urls.append("http://bj.to8to.com/zs/company%d/"%(id))
    '''
    f = open("city.txt", "r")  
    for line in f:  
        start_urls.append(line.strip()+'company/list_1.html')    # do something here  
    f.close()  
    
    rule_getcompanyid = re.compile('[\d]+')
    #公司服务
    rule_companyinfo = re.compile(u'\u516c\u53f8\u670d\u52a1')
    #服务区域
    rule_servicezone = re.compile(u'\u670d\u52a1\u533a\u57df')
    #服务专长
    rule_decorationtype = re.compile(u'\u670d\u52a1\u4e13\u957f')
    #承接价位
    rule_price = re.compile(u'\u627f\u63a5\u4ef7\u4f4d')
    #专场风格
    rule_decorationstyle = re.compile(u'\u4e13\u957f\u98ce\u683c')
    #获得地址的链接
    url_address = 'http://bj.to8to.com/zs/%s/company-connect-1.html'
    #地址
    url_company_des= 'http://bj.to8to.com/zs/company%s/'
    
    def parse(self,response):
        url_patten = response.url[0:-11]+'list_%s.html'
        print "*********",url_patten
        sel = Selector(response)
        page_num = sel.xpath('//div[@class="pages"]/a/text()').extract()
        if page_num:
            max_num = page_num[-2]
            for id in xrange(1,int(max_num)+1):
                urltemp = url_patten%(id)
                request = Request(urltemp, callback=self.parse_nextt)
                yield request

#         request = Request(response.url, callback=self.parse_nextt)
#         yield request
    
    def parse_nextt(self,response):
        sel = Selector(response)
        urls = sel.xpath("//div[@class='zgscl_container']/a[1]/@href").extract()
        
        for url in urls:
            print url
            request = Request(url, callback=self.parse_zs_home)
            yield request
            
    def parse_zs_home(self,response):
        sel = Selector(response)
        item = self.init()
        con = sel.xpath("//meta[@name='keywords']/@content").extract()
        if con:
            item['company_shortname'] = con[0].split(',')[0]
        else:
            item['company_shortname'] = ''
            
        koubei = sel.xpath("//div[@class='zd_name']/p/a/text()").extract()
        if koubei:
            item['koubei'] = koubei[0]
        else:
            item['koubei'] = ''
        
        company_id = self.rule_getcompanyid.findall(response.url)[-1]
        url = self.url_company_des % company_id 
        item["company_id"] = company_id
        
        if len(sel.css("zgshb_menu")) == 0:
            file("a.txt", "a").write(company_id +"\n")
            yield item
        else:
            request = Request(url, callback=self.parse_des)
            request.meta["item"] = copy.deepcopy(item)
            yield request
        
    def parse_des(self,response):
        item = response.meta['item']
#         yield item
        if response.status != 200:
            pass
#             file("a.txt", "a").write(item["company_id"] +"\n")
#             yield item
        else:
            sel = Selector(response)
            company_id = self.rule_getcompanyid.findall(response.url)[-1]
            
            item['company_id'] = company_id
            company_name = sel.xpath("//div[@class='zd_name']/h1/text()").extract()
            item['company_name'] = company_name[0] if company_name else ''
    
            item['service_content'] = ''
            decoration_type = []
            divs = sel.css(".detail")
            if len( divs) == 0:
                file("a.txt", "a").write(company_id +"\n")
            else:
                for div in divs:
                    sign_title = div.xpath("./p/text()").extract()
                    if sign_title and self.rule_companyinfo.findall(sign_title[0]):
                            trs = div.xpath(".//tr")
                            for tr in trs:
                                thead = tr.xpath("./td[@class='thead']/text()").extract()
                                content = tr.xpath("./td[@class='content']/text()").extract()
                                if not thead:
                                    con = content[0] if content else ''
                                    item['decoration_type_gong'] = con
                                elif self.rule_servicezone.findall(thead[0]):
                                    item['service_zone'] = content[0] if content else ''
                                elif self.rule_price.findall(thead[0]):
                                    item['price'] = content[0] if content else ''
                                elif self.rule_decorationtype.findall(thead[0]):
                                    item['decoration_type_jia'] = content[0] if content else ''
                                elif self.rule_decorationstyle.findall(thead[0]):
                                    item['decoration_style'] = content[0] if content else ''
                                    
                des = sel.css(".describe").xpath("./p/text()").extract()
                logo = sel.css(".logo").xpath(".//img/@src").extract()
                item['company_des'] = des[0] if des else ''
                item['image_urls'] = logo
                connect_url = self.url_address % company_id
                request = Request(connect_url, callback=self.parse_next)
                request.meta["item"] = copy.deepcopy(item)
                
                yield request
        
    def init(self):
        item = ZscompanyItem()
        item["company_id"]=""
        item["company_name"]=""
        item["company_shortname"]=""
        item['koubei']=""
        item['service_zone']=""
        item["price"]=""
        item["service_content"]=""
        item["decoration_type_jia"]=""
        item['decoration_type_gong']=""
        item["decoration_style"]=""
        item['city']=""
        item['address']=""
        item['company_des']=""
        return item
    
    def parse_next(self,response):
        
        item = response.meta['item']
        sel = Selector(response)
        dds = sel.xpath("//div[@class='detail']/dl/dd/text()").extract()
        item['address']= dds[1]
        item['city'] = dds[0]
        yield item