# -*- coding: utf-8 -*-
import scrapy
import MySQLdb.cursors
from twisted.enterprise import adbapi
import  logging

class AzwPipeline(object):
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
        self.dbpool.runInteraction(self.insertTmallShopSql, item)
        return item
    
    def insertTmallShopSql(self, tx, item):
        insertTmallShopSql = r"""INSERT INTO `tmall_shop` (`shop_id`, `brand_id`, `shop_name`, `company_name`, `shop_area`, `shop_logo`, `description_consist_score`, `description_consist_cmp`, `service_attitude_score`, `service_attitude_cmp`, `logistics_service_score`, `logistics_service_cmp`, `shop_url`, `open_years`) VALUES
(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"""
        try:
#             print insertTmallShopSql %(item["shop_id"],
#                     item["brand_id"],
#                     item["shop_name"],
#                     item["company_name"],
#                     item["shop_area"],
#                     item["shop_logo"],
#                     item["description_consist_score"],
#                     item["description_consist_cmp"],
#                     item["service_attitude_score"],
#                     item["service_attitude_cmp"],
#                     item["logistics_service_score"],
#                     item["logistics_service_cmp"],
#                     item["shop_url"],
#                     item["open_years"])
            
            tx.execute(insertTmallShopSql, 
                   (item["shop_id"],
                    item["brand_id"],
                    item["shop_name"],
                    item["company_name"],
                    item["shop_area"],
                    item["shop_logo"],
                    item["description_consist_score"],
                    item["description_consist_cmp"],
                    item["service_attitude_score"],
                    item["service_attitude_cmp"],
                    item["logistics_service_score"],
                    item["logistics_service_cmp"],
                    item["shop_url"],
                    item["open_years"]
                    ))
        except Exception,e:
            print e
