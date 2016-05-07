# -*- coding: utf-8 -*-
import scrapy
import MySQLdb.cursors
from twisted.enterprise import adbapi
import os
import shutil
import logging

class ShejibenPipeline(object):
    def __init__(self, dbargs):
        self.dbargs = dbargs
        
        self.insertQuestionSql = r"""INSERT INTO `shijieben` (`designer_id`, `designer_name`, `designer_phone_no`, `designer_email`, `designer_sex`, `designer_position`, `apartment`, `style`, `program`, `average_price`, `work_years`, `introduction`, `head_photo`, `category_id`, `category_name`, `company_id`, `company_name`) VALUES
(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"""
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
        
        if len(item["images"]) > 0:
            item["head_photo"] = "shejiben" + item["images"][0]["path"][4:]
        else:
            item["head_photo"] = ""
            
        try:
            tx.execute(self.insertQuestionSql,
                   (
                    item["designer_id"],
                    item["designer_name"],
                    item["designer_phone_no"],
                    item["designer_email"],
                    item["designer_sex"],
                    item["designer_position"],
                    item["apartment"],
                    item["style"],
                    item["program"],
                    item["average_price"],
                    item["work_years"],
                    item["introduction"],
                    item["head_photo"],
                    item["category_id"],
                    item["category_name"],
                    item["company_id"],
                    item["company_name"],
                    ))
        except Exception, e:
            print e
