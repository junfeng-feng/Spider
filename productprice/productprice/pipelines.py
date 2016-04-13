# -*- coding: utf-8 -*-
from scrapy import log
import scrapy
import MySQLdb.cursors
from twisted.enterprise import adbapi

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

# 插入标题表格
class InsertPricePipe(object):
    def __init__(self, dbargs):
        self.dbargs = dbargs
    
    def open_spider(self, spider):
        self.dbpool = adbapi.ConnectionPool('MySQLdb', **(self.dbargs))
        
    def close_spider(self, spider):
        self.dbpool.close()
        
    @classmethod
    def from_crawler(cls, crawler):
        settings = crawler.settings
        dbargs = dict(
                      host=settings['MYSQL_HOST'],
                      db=settings['MYSQL_DBNAME'],
                      user=settings['MYSQL_USER'],
                      passwd=settings['MYSQL_PASSWD'],
                      port=settings['MYSQL_PORT'],
                      charset='utf8',
                      cursorclass=MySQLdb.cursors.DictCursor,
                      use_unicode=True,
                      )
        return cls(dbargs)
        
    def process_item(self, item, spider):
        self.dbpool.runInteraction(self.insertTitleSql, item)
        return item
    
    def insertTitleSql(self, tx, item):
        if item['product_price']: #如果有价格则，记录
            sql_insert = 'insert into product_price(product_id,product_price) values(%s,%s)'
            tx.execute(sql_insert, (item["product_id"], item['product_price']))
