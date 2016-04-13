# -*- coding: utf-8 -*-
import logging
import scrapy
import MySQLdb.cursors
from twisted.enterprise import adbapi

class TmallproductidPipeline(object):
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
        self.dbpool.runInteraction(self.insertTmallSql, item)
        return item
    
    def insertTmallSql(self, tx, item):
        insertProductIdSql = r"""INSERT INTO `tmall_product_id_list` (
`brand_id` ,
`product_id` ,
`product_price`
)
VALUES (
%s, %s, %s
);
"""
        try:
            tx.execute(insertProductIdSql, 
                                (item['brand_id'], #实际是brand_id
                                  item['product_id'],
                                  item["product_price"],
                                  ))
        except Exception, e:
            logging.error(str(e))
            print e
        pass

