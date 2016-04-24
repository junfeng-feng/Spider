#encoding=utf-8
import scrapy
from scrapy.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import Selector
from scrapy.spiders import Spider
from scrapy.spiders.crawl import CrawlSpider, Rule

from fang.items import Fang_Item
import string 
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class Spider_Qijia(Spider):
    name = 'fang'
    
    allowed_domain = ['fang.com']
    start_urls = [
                  #'http://home.fang.com/album/lanmu/?sortid=11&a1=shufang&s2=dongnanya&a3=xiegui&page=1'       
                  ]
    params = []
    a1 = ['keting','chufang','woshi','weishengjian','xuanguan','canting','yangtai','ertongfang','yimaojian','shufang']
    a2 = ['xiandai','jianou','jianyue','zhongshi','oushi','tianyuan','dizhonghai','hunda','meishi','rihan','dongnanya','gudian']
    a3 = ['beijingqiang','chuanglian','zoulang','diaoding','louti','chugui','yigui','chuang','dianshigui',
          'shafa','chuanglian','geduan','zuhegui','chuwugui','shugui','batai','xiegui','chaji',
          'tatami','zhaopianqiang','bizhi','pingfeng','yingerchuang','dengju','canzhuo','yugang','chuangtougui',
          'jiugui','shuzhuangtai','shujia']
    for i in range(len(a1)):
        for j in range(len(a2)):
            for k in range(len(a3)):
                param = [a1[i],a2[j],a3[k]]
                params.append(param)
      
    for index in range(len(params)):
        url = 'http://home.fang.com/album/lanmu/?sortid=11&a1=%s&a2=%s&a3=%s&page=1'%(params[index][0],params[index][1],params[index][2])
        start_urls .append(url)
            
        
    def parse(self, response):
        arrays = response.url.split("&")[:-1]
        currentPage = string.atoi(response.url.split("&")[-1].split("=")[-1])
        prefix = '&'.join(arrays)
        
        preachs=Selector(response).xpath('//a[starts-with(@href, "http://home.fang.com/album/p")]').xpath('@href').extract();
        for item_url in preachs:
            yield scrapy.Request(item_url, self.parse_item)    
            
        list1 = Selector(response).xpath("//div[@class='pages']/ul/i[last()]/a/@href").extract()
    
        if list1 :
            pageNum = string.atoi(list1[0].split("=")[-1])#最后一页的编号
            if currentPage < pageNum:
                print "current pageNumber",(currentPage + 1)
                page = "&page=%d" % (currentPage + 1)
                print"currentPage < pageNum"+str(page)
                url_next = prefix + page
                print "new url is ",url_next
                yield scrapy.Request(url_next,self.parse) 
        #for index in range(1,page + 1):
        #    yield scrapy.Request(item_url, self.parse_item)  
        
    def parse_item(self,response):

        
        item = Fang_Item()
        
        item['site'] = response.url
        item['title'] = Selector(response).xpath("//div[@class='info']/h1/text()").extract()[0]
        item['shortDescription'] = ''
        item['shortDescription'] = "|".join(Selector(response).xpath("//div[@class='info']/p/text()").extract())
        item['category']=''
        item['style']=''
        
        category = Selector(response).xpath("//div[@class='info']/ul/li[1]/a/text()").extract()
        if category:
            item['category']=category[0]
            
        style = Selector(response).xpath("//div[@class='info']/ul/li[2]/a/text()").extract()
        if style:
            item['style']=style[0]
        
        tags =Selector(response).xpath("//div[@class='tag']/ul/a/text()").extract()
        tag = [];
        for n in tags:
            tag.append(n)
        item['tag'] = ','.join(tag);
        url = Selector(response).xpath("//img[@id='LeftImg']/@src").extract()[0]
        item['origin_url'] = url
        item['new_url']=''
        item['mb']=''
        widthPx = Selector(response).xpath("//img[@id='LeftImg']/@width").extract()
        heightPx = Selector(response).xpath("//img[@id='LeftImg']/@height").extract()
        item['pixel']=''
        item['format']=url.split("/")[-1].split('.')[-1]
        return item;
    pass   
        
        
        