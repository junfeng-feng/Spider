# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import datetime
import os  
from os.path import join, getsize
import time
import uuid

import MySQLdb.cursors
from PIL import Image
from scrapy import log
import scrapy
from scrapy.pipelines.images import ImagesPipeline
from twisted.enterprise import adbapi

from fang import settings


class FangPipeline(object):
    def process_item(self, item, spider):
        return item
    
    
class FangImagesPipe(ImagesPipeline):
    def get_media_requests(self, item, info):
        yield scrapy.Request(item['origin_url'])
            
    def item_completed(self, results, item, info):
        image_paths = [x['path'] for ok, x in results if ok]
        item['new_url'] = settings.IMAGES_STORE + image_paths[0]
        mb = str(getsize(item['new_url']) /1024) + 'KB'
        item['mb'] = mb
        im = Image.open(item['new_url'])
        width = im.size[0]
        height = im.size[1]
        item['size'] = str(width) + 'x' + str(height)
        item['pixel'] = width * height
        
        return item
            
    def file_path(self, request, response=None, info=None):
        
        image_guid = request.url.split('/')[-1]
        hour = time.strftime("%H")
        suffix = image_guid.split('.')[-1]
        hour = time.strftime("%H")
        
        imagePath1 = str(time.time()).replace('.','1') + '.' + suffix
        return '%s/%s' % (hour,imagePath1)
        






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
        sql_insert = '''insert into fang(site,title,shortDescription,category,style,tag,origin_url,new_url,mb,pixel,size,format) 
        values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'''
        tx.execute(sql_insert,(
                               item['site'],item['title'],item['shortDescription'],
                                item['category'],item['style'],item['tag'],item['origin_url'],
                                item['new_url'],item['mb'],item['pixel'],item['size'],item['format']))
        
        
        
        