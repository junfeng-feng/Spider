# -*- coding: utf-8 -*-
import logging
import scrapy
import MySQLdb.cursors
from twisted.enterprise import adbapi

class TmallratePipeline(object):
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
        self.dbpool.runInteraction(self.insertTmallrateSql, item)
        return item
    
    def insertTmallrateSql(self, tx, item):
        insertTmallrateSql = r"""INSERT INTO `tmall_rate` (`product_id`, `rate_id`, `user_nickname`, `user_name_star_flag`, `rate_content`,  `rate_content_time`,`rate_content_append`,`rate_append_time`, `shop_url`) VALUES
(%s, %s, %s, %s, %s,%s, %s, %s, %s)"""
        tx.execute(insertTmallrateSql, 
                   (item["product_id"],
                    item["rate_id"],
                    item["user_nickname"],
                    item["user_name_star_flag"],
                    item["rate_content"],
                    item["rate_content_time"],
                    item["rate_content_append"],
                    item["rate_append_time"],
                    item["shop_url"],))

