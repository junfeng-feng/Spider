# -*- coding: utf-8 -*-
from scrapy import log
import scrapy
from scrapy.pipelines.images import ImagesPipeline
from twisted.enterprise import adbapi
import uuid
import re
import MySQLdb.cursors
from twisted.enterprise import adbapi

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
class BaikePipeline(object):
    
    def process_item(self, item, spider):
        return item

#图片下载管道
class BaikeImagesPipe(ImagesPipeline):
    def get_media_requests(self, item, info):
        for image_url in item['image_urls']:
            yield scrapy.Request(image_url)

#插入标题表格
class InsertTitlePipe(object):
    def __init__(self, dbargs):
        self.dbargs = dbargs
    
    def open_spider(self,spider):
        self.dbpool = adbapi.ConnectionPool('MySQLdb', **(self.dbargs))
        
    def close_spider(self,spider):
        self.dbpool.close()
        
    @classmethod
    def from_crawler(cls,crawler):
        settings = crawler.settings
        dbargs = dict(
                      host=settings['MYSQL_HOST'],
                      db=settings['MYSQL_DBNAME'],
                      user=settings['MYSQL_USER'],
                      passwd=settings['MYSQL_PASSWD'],
                      port=settings['MYSQL_PORT'],
                      charset='utf8',
                      cursorclass = MySQLdb.cursors.DictCursor,
                      use_unicode= True,
                      )
        return cls(dbargs)
        
    def process_item(self, item, spider):
        self.dbpool.runInteraction(self.insertTitleSql,item)
        return item
    
    def insertTitleSql(self, tx,item):
        sql_insert = 'insert into baike_title(title_id,title_name,title_introduction,title_category,content_uuid_list,title_url) values(%s,%s,%s,%s,%s,%s)'
        tx.execute(sql_insert,(item["title_id"], item['title_name'][0],item['title_introduction'][0],item['title_category'],item['content_uuid_list'],item['title_url']))
   
#插入内容表格      
class InsertContentPipe(object):
    def __init__(self, dbargs):
        self.dbargs = dbargs
        #去除html规则
        self.d_html_rule = re.compile(r'<[^>]+>', re.S)
    
    def open_spider(self,spider):
        self.dbpool = adbapi.ConnectionPool('MySQLdb', **(self.dbargs))
        
    def close_spider(self,spider):
        self.dbpool.close()
        
    @classmethod
    def from_crawler(cls,crawler):
        settings = crawler.settings
        dbargs = dict(
                      host=settings['MYSQL_HOST'],
                      db=settings['MYSQL_DBNAME'],
                      user=settings['MYSQL_USER'],
                      passwd=settings['MYSQL_PASSWD'],
                      port=settings['MYSQL_PORT'],
                      charset='utf8',
                      cursorclass = MySQLdb.cursors.DictCursor,
                      use_unicode= True,
                      )
        return cls(dbargs)
        
    def process_item(self, item, spider):
        self.dbpool.runInteraction(self.insertContent,item)
        return item
    
    def insertContent(self,tx,item):
        i = 0
        while(i<len(item['content_name'])):
            sql = 'insert into baike_content(content_uuid,content_name,content_text,img_address,title_id) values(%s,%s,%s,%s,%s)'
            content_text_i = self.d_html_rule.sub('', item['content_text'][i]).replace('\n',"")
            tx.execute(sql,(item['content_uuid'][i],item['content_name'][i], content_text_i, item['images'][i]['path'],item['title_id']))
            i=i+1
            
    def handle_error(self, e):
        log.err(e)