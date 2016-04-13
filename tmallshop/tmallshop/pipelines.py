# -*- coding: utf-8 -*-
import scrapy
import MySQLdb.cursors
from twisted.enterprise import adbapi
import  logging

class TmallshopPipeline(object):
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
        insertTmallShopSql = r"""INSERT INTO `tmall_shop`
 (`shop_id`, `brand_id`,`category_id`, 
 `shop_type`, `shop_name`, `company_name`, `shop_area`, 
 `shop_logo`,`shop_commodity_num`, 
 `description_consist_score`, `description_consist_cmp`, `service_attitude_score`, `service_attitude_cmp`, `logistics_service_score`, `logistics_service_cmp`) VALUES
(%s, %s, %s, 
%s, %s, %s, %s,
 %s, %s,
  %s, %s, %s, %s, %s, %s);"""

        item["shop_logo"] = "logo/tm" + item["images"][0]["path"][4:]

        try:
            tx.execute(insertTmallShopSql, 
                   (item["shop_id"],
                    item["brand_id"],
                    item["category_id"],
                    
                    item["shop_type"],
                    item["shop_name"],
                    item["company_name"],
                    item["shop_area"],
                    item["shop_logo"],
                    
                    item["shop_commodity_num"],
                    item["description_consist_score"],
                    item["description_consist_cmp"],
                    item["service_attitude_score"],
                    item["service_attitude_cmp"],
                    item["logistics_service_score"],
                    item["logistics_service_cmp"],
                    ))
        except Exception,e:
            print e
