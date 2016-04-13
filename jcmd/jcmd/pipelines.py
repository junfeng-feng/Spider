# -*- coding: utf-8 -*-
import uuid
import re
import MySQLdb.cursors
from twisted.enterprise import adbapi


# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
class JcmdPipeline(object):
    def process_item(self, item, spider):
        return item



class Jcmd_Category_Pipeline(object):
    
    def __init__(self,dbargs):
        
        self.dbargs = dbargs
    
    def process_item(self, item, spider):
        
        if spider.name in ['category1']:
            
            self.dbpool.runInteraction(self.insertCategory,item)
            
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
        
    def insertCategory(self,tx,item):
        
        sql = "insert into category(category_id,category_name,category_child_id,category_child_name,category_level,url) values(%s,%s,%s,%s,%s,%s)"
        tx.execute(sql,(item['category_id'],item['category_name'],item['category_child_id'],item['category_child_name'],item['category_level'],item['url']))
        
class Jcmd_Brand_Pipeline(object):
    
    def __init__(self,dbargs):
        
        self.dbargs = dbargs
    
    def process_item(self, item, spider):
        
        if spider.name in ['brand']:
            
            self.dbpool.runInteraction(self.insertBrand,item)
            
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
        
    def insertBrand(self,tx,item):
        
        sql = "insert into brand(brand_id,brand_chname,brand_enname,category_id,category_name,brand_info,brand_introduction,brand_word,brand_address,brand_leader,brand_phone,brand_website,brand_year,logo,img,url) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        tx.execute(sql,(item['brand_id'],item['brand_chname'],item['brand_enname'],item['category_id'],item['category_name'],item['brand_info'],item['brand_introduction'],item['brand_word'],item['brand_address'],item['brand_leader'],item['brand_phone'],item['brand_website'],item['brand_year'],item['images'][0]['path'],item['images'][1]['path'],item['url']))
        
        
class Jcmd_BrandItemAlter_Pipeline(object):
    
    def __init__(self):
        #初始化此处，提升运行效率
        #电话匹配规则
        self.phone_rule = re.compile(r'[0-9-]+')
        #年份匹配规则
        self.year_rule = re.compile(r'[\d]{4}')
        #去除html规则
        self.d_html_rule = re.compile(r'<[^>]+>',re.S)
        #匹配中文
        self.getchinese = re.compile(u'([\u4e00-\u9fa5]+)')
        #匹配英文
        self.getenglish = re.compile(r'[a-zA-Z0-9&-]+')
        #电话分隔符
        self.split = ','
    def process_item(self,item,spider):
            
        if spider.name in ['brand']:
            #----
            chname = self.getchinese.findall(item['brand_chname'])
            enname = self.getenglish.findall(item['brand_chname'])
            if chname :
                item['brand_chname'] = chname[0]
            else:
                item['brand_chname'] = ""
            if enname :
                item['brand_enname'] = enname[0]
            else:
                item['brand_enname'] = ""
            #----              
            item['brand_introduction'] = self.d_html_rule.sub('',item['brand_introduction']).replace('\n','')
            #----
            leader_year = self.d_html_rule.sub('',item['brand_leader']).split(' ')
            item['brand_leader'] = ("".join(leader_year[0:-1])).replace('\n', '')
            item['brand_year'] = self.year_rule.findall(leader_year[-1])[0]
            #----
            phone = self.phone_rule.findall(item['brand_phone'])
            item['brand_phone']=self.split.join(phone)
            
            if not item['brand_year']:
                item['brand_year'] = ""
        return item
    
class Jcmd_ShopItemAlter_Pipeline(object):
    
    def __init__(self):
        #去除html规则
        self.d_html_rule = re.compile(r'<[^>]+>',re.S)
        #去除联系人中括号
        self.rule_de_kuohao = re.compile(r'[()]')
        
    def process_item(self,item,spider):
        
        if spider.name in ['shop']:
            item['shop_name'] = self.d_html_rule.sub('',item['shop_name']).replace('\n',"")
            item['shop_type'] =  self.d_html_rule.sub('',item['shop_type'])
            #item['shop_phone'] = self.d_html_rule.sub('',item['shop_phone'])
            #item['shop_address'] = self.d_html_rule.sub('',item['shop_address'])
            item['shop_introduction'] = self.d_html_rule.sub('',item['shop_introduction']).replace('\n',"")
            item['shop_person'] = self.rule_de_kuohao.sub('',item['shop_person'])
        return item
        
class Jcmd_Shop_Pipeline(object):
    
    def __init__(self,dbargs):
        
        self.dbargs = dbargs
    
    def process_item(self, item, spider):
        
        if spider.name in ['shop']:
            
            self.dbpool.runInteraction(self.insertShop,item)
            
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
        
    def insertShop(self,tx,item):
        
        sql = "insert into shop(shop_id,shop_name,brand_id,brand_name,category_id,category_name,shop_type,shop_phone,shop_person,shop_site,shop_address,shop_introduction,img,url) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        tx.execute(sql,(item['shop_id'],item['shop_name'],item['brand_id'],item['brand_name'],item['category_id'],item['category_name'],item['shop_type'],item['shop_phone'],item['shop_person'],item['shop_site'],item['shop_address'],item['shop_introduction'],item['images'][0]['path'],item['url']))
        
                
            