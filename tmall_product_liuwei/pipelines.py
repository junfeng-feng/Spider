# -*- coding: utf-8 -*-
import os
import shutil

import MySQLdb.cursors
import scrapy
from scrapy.contrib.pipeline.images import ImagesPipeline
from scrapy.exceptions import DropItem
from twisted.enterprise import adbapi


# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
class TmallPipeline(object):
    
    def process_item(self, item, spider):
        return item


#自定义图片下载管道
class Tmall_ProductImg_Pipeline(ImagesPipeline):
    
    def get_media_requests(self, item, info):
        
        if item['is_decoration'] == 'yes' :
            
            for image_url in item['image_urls']:
                
                yield scrapy.Request(image_url)
                

class modirfy_img_name(object):
    
    def __init__(self):
        
        self.path = 'D:/coding/workspace/Projects/tmall/product/'
    
    def process_item(self, item, spider):
        
        if spider.name in ['product']:
            
            if item['images']:
                
                src = 'D:/coding/workspace/Projects/tmall/product/full/'
                big_dst = 'D:/coding/workspace/Projects/tmall/product/tm/big/' + item['brand_id']
                small_dst = 'D:/coding/workspace/Projects/tmall/product/tm/small/' + item['brand_id']
                if not os.path.isdir(big_dst):
                    os.mkdir(big_dst)
                if not os.path.isdir(small_dst):
                    os.mkdir(small_dst)
                
                img0_name = item['images'][0]['path'].split('/')[-1]
                if not os.path.isfile(small_dst+'/'+ img0_name):
                    shutil.copy(src+img0_name,small_dst)
                    
                for info in item['images'][1:]:
                    
                    img_name = info['path'].split('/')[-1]
                    if not os.path.isfile(big_dst+'/'+img_name):
                        shutil.copy(src+img_name,big_dst)
                   
        return item
    
class Tmall_Product_Pipeline(object):
    
    def __init__(self,dbargs):
        
        self.dbargs = dbargs
    
    def process_item(self, item, spider):
        
        if spider.name in ['product']:
            
            self.dbpool.runInteraction(self.insertProduct,item)
            
        return item
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
    
    def open_spider(self,spider):
        
        self.dbpool = adbapi.ConnectionPool('MySQLdb', **(self.dbargs))
        
    def close_spider(self,spider):
        
        self.dbpool.close()
        
    def insertProduct(self,tx,item):
        sql = 'insert into tmall_product(product_id,product_name,shop_id,brand_id,brand_name,category_id,category_name,product_point,product_price,product_salepermonth,product_judgementnum,product_type,product_data,product_searchword,product_specialjudge,img_source,group_img_source,img,group_img,url) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
        product_data = ','.join(item['product_data'])
        search_word = ''
        if item['product_searchword']:
            for i in item['product_searchword']:
                search_word = search_word + i.split('|')[0] + ','
        img = ''
        group_img = ''
        img_source = ''
        group_img_source = ''
        
        if item['image_urls']:
            img_source = item['image_urls'][0]
            for r in item['image_urls'][1:]:
                group_img_source = group_img_source + r + ','
        
        if item['is_decoration']=='yes':
            if item['images']:
                img = 'product/tm/small/'+item['brand_id']+'/'+ item['images'][0]['path'].split('/')[-1]
                for r in item['images'][1:]:
                    t = 'product/tm/big/'+item['brand_id']+'/'+ r['path'].split('/')[-1]
                    group_img = group_img + t + ','
        
        tx.execute(sql,(item['product_id'],item['product_name'],item['shop_id'],item['brand_id'],item['brand_name'],item['category_id'],item['category_name'],item['product_point'],item['product_price'],item['product_salepermonth'],item['product_judgementnum'],item['product_type'],product_data,search_word,item['product_specialjudge'],img_source,group_img_source,img,group_img,item['url']))
        
        
class Tmall_ProductData_Pipeline(object):

    def __init__(self,dbargs):
        
        self.dbargs = dbargs
    
    def process_item(self, item, spider):
        
        if spider.name in ['product']:
            
            self.dbpool.runInteraction(self.insertProduct,item)
            
        return item
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
    
    def open_spider(self,spider):
        
        self.dbpool = adbapi.ConnectionPool('MySQLdb', **(self.dbargs))
        
    def close_spider(self,spider):
        
        self.dbpool.close()
        
    def insertProduct(self,tx,item):
        sql = 'insert into tmall_productdata(data_name,data_value,product_id,category_id) values(%s,%s,%s,%s)'
        if item['product_data']:
            for pd in item['product_data']:
                dataname,datavalue = pd.split(':')
                tx.execute(sql,(dataname,datavalue,item['product_id'],item['category_id']))
                
                
class Tmall_SearchWord_Pipeline(object):

    def __init__(self,dbargs):
        
        self.dbargs = dbargs
    
    def process_item(self, item, spider):
        
        if spider.name in ['product']:
            
            self.dbpool.runInteraction(self.insertSearchWord,item)
            
        return item
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
    
    def open_spider(self,spider):
        
        self.dbpool = adbapi.ConnectionPool('MySQLdb', **(self.dbargs))
        
    def close_spider(self,spider):
        
        self.dbpool.close()
        
    def insertSearchWord(self,tx,item):
        sql = 'insert into tmall_searchwords(product_id,searchword,category_id) values(%s,%s,%s)'
        if item['product_searchword']:
            for i in item['product_searchword']:
                searchword,category_id = i.split('|')
                tx.execute(sql,(item['product_id'],searchword,category_id))   