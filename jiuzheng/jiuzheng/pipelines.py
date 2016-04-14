# -*- coding: utf-8 -*-
import scrapy
import MySQLdb.cursors
from twisted.enterprise import adbapi
import logging

class JiuzhengPipeline(object):
    def __init__(self, dbargs):
        self.dbargs = dbargs
        self.insertQuestionSql = r"""INSERT INTO `ask_askjia_question`  (`question_id`, `question_title`, `question_category`, `question_description`, `question_img`) VALUES
(%s, %s, %s, %s, %s);"""
        self.insertAnswerSql = r"""INSERT INTO `ask_askjia_answer` (`answer_id`, `question_id`, `answer_content`, `answer_img`, `is_best`) VALUES
(%s, %s, %s, %s, %s);"""
    
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
        if item["is_question"] == "yes":
            image_src = ""
            if len(item["images"]) > 0:
                image_src = "/ask/jia" + item["images"][0]["path"][4:]

            try:
                tx.execute(self.insertQuestionSql,
                       (item["question_id"],
                        item["question_title"],
                        item["question_category"],
                        item["question_description"],
                        image_src
                        ))
            except Exception, e:
                print e
            pass
        else:
            image_src = ""
            if len(item["images"]) > 0:
                image_src = "/ask/jia" + item["images"][0]["path"][4:]
            
            try:
                tx.execute(self.insertAnswerSql,
                       (item["answer_id"],
                        item["question_id"],
                        item["answer_content"].replace("\n",""),
                        image_src,
                        item["is_best"],
                        ))
            except Exception, e:
                print e
            pass