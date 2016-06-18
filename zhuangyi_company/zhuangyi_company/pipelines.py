# -*- coding: utf-8 -*-
import scrapy
import MySQLdb.cursors
from twisted.enterprise import adbapi
import logging

class ZhuangyiCompanyPipeline(object):
    def __init__(self, dbargs):
        self.dbargs = dbargs
        self.insertDesignerSql = r"""INSERT INTO `zhuangyi_designer` (`designer_id`, `company_id`, `designer_name`, `position`, `good_at_filed`, `good_at_style`, `designer_introduction`, `head_img`) VALUES 
        (%s, %s, %s, %s, %s, %s, %s, %s);"""
        self.insertCompanySql = r"""INSERT INTO `zhuangyi_company` (`company_id`, `company_name`, `company_shortname`, `company_koubei`, `service_zone`, `price`, `service_content`, `decoration_type_jia`, `decoration_type_gong`, `decoration_style`, `city`, `address`, `company_des`, `logo`) VALUES
(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"""
    
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

        if item["is_designer"] == "yes":
            image_src = ""

            try:
                tx.execute(self.insertDesignerSql,
                       (
                        item["designer_id"],
                        item["company_id"],
                        item["designer_name"],
                        item["position"],
                        item["good_at_filed"],
                        item["good_at_style"],
                        item["designer_introduction"],
                        item["head_img"],
                        ))
            except Exception, e:
                print e
            pass
        else:
            image_src = ""
            
            try:
                tx.execute(self.insertCompanySql,
                       (
                        item["company_id"],
                        item["company_name"],
                        item["company_shortname"],
                        item["company_koubei"],
                        item["service_zone"],
                        item["price"],
                        item["service_content"],
                        item["decoration_type_jia"],
                        item["decoration_type_gong"],
                        item["decoration_style"],
                        item["city"],
                        item["address"],
                        item["company_des"],
                        item["logo"],
                        ))
            except Exception, e:
                print e
            pass
        



