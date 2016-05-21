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
        
        self.insertDesignerSql = r"""INSERT INTO `shejiben_designer` 
        (`designer_id`, `designer_name`, `signature`, `consulting_number`, `view_number`, `designer_position`, `address`, `style`, `experience`, `fee`, `certification_rewords`, `introduction`, `head_photo`, `followers_number`, `renqi`, `follows`) 
        VALUES 
        (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"""
        self.insertDesignerRateSql = r"""INSERT INTO `shejiben_designer_rate` 
        (`designer_id`, `rate_id`, `rate_content`, `rate_img`, `rate_addr`, `rate_datetime`) 
        VALUES 
        (%s, %s, %s, %s, %s, %s);"""
        self.insertDesignerBlogSql = r"""INSERT INTO `shejiben_designer_blog`
        (`designer_id`, `blog_id`, `blog_title`, `blog_datetime`, `view_number`, `blog_content`, `blog_img`, `blog_author`) 
        VALUES
         (%s, %s, %s, %s, %s, %s, %s, %s);"""
        # 博客评论不抓
#         self.insertDesignerBlogRateSql = r""""""
        # 成交记录不需要抓取
#         self.insertDesignerProgramSql = r"""INSERT INTO `shejiben_designer_program` 
#         (`designer_id`, `program_id`, `program_name`, `deal_time`, `status`) 
#         VALUES 
#         (%s, %s, %s, %s, %s);"""
        
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
        
        if item["flag"] == "designer":
            try:
                if len(item["images"]) > 0:
                    item["head_photo"] = "shejiben" + item["images"][0]["path"][4:]
                else:
                    item["head_photo"] = ""
                tx.execute(self.insertDesignerSql,
                       (
                        item["designer_id"],
                        item["designer_name"],
                        item["signature"],
                        item["consulting_number"],
                        item["view_number"],
                        item["designer_position"],
                        item["address"],
                        item["style"],
                        item["experience"],
                        item["fee"],
                        item["certification_rewords"],
                        item["introduction"],
                        item["head_photo"],
                        item["followers_number"],
                        item["renqi"],
                        item["follows"],
                        ))
            except Exception, e:
                print e
        elif item["flag"] == "rate":
            try:
                tx.execute(self.insertDesignerRateSql,
                       (
                        item["designer_id"],
                        item["rate_id"],
                        item["rate_content"],
                        item["rate_img"],
                        item["rate_addr"],
                        item["rate_datetime"],
                        ))
            except Exception, e:
                print e
        else:
            try:
                tx.execute(self.insertDesignerBlogSql,
                       (
                        item["designer_id"],
                        item["rate_id"],
                        item["rate_content"],
                        item["rate_img"],
                        item["rate_addr"],
                        item["rate_datetime"],
                        ))
            except Exception, e:
                print e
