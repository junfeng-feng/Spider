# -*- coding: utf-8 -*-
import scrapy
import MySQLdb.cursors
from twisted.enterprise import adbapi
import os
import shutil
import logging

class DianpingPipeline(object):
    def __init__(self, dbargs):
        self.dbargs = dbargs
        
        self.insertQuestionSql = r"""INSERT INTO `dianping_shop` 
        (`shop_id`, `shop_name`, `shop_img`, `shop_area`, `shop_domain`, `shop_category`, `shop_cityname`, `shop_address`, 
        `shop_telphone`, `shop_open_time`, `shop_tag`, `shop_map_attitude`, `shop_contact_man`, 
         `shop_bus_line`, `shop_description`, `city_id`, `shop_template`) VALUES
(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
"""
        self.insertAnswerSql = r"""INSERT INTO `dianping_rate` 
        (`rate_id`, `user_photo`, `user_nickname`, `rate_content`, `rate_img`, `rate_datetime`, `shop_id`, `shop_template`) VALUES
(%s, %s, %s, %s, %s, %s, %s, %s);"""
    
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
        if item["shop_flag"] == "yes":
            try:
                if len(item["images"]) > 0:
                    # 创建shopid 目录
                    imgPath = "./shop/dp/" + item["shop_id"]
                    if not os.path.exists(imgPath):
                        os.makedirs(imgPath)
                    
                    # copy图片到新目录
                    for path in item["images"]:
                        oldPath = "./img/" + path["path"] 
                        shutil.copy(oldPath, imgPath + path["path"][4:])
                    
                    item["shop_img"] = ",".join(["shop/dp/" + item["shop_id"] + path["path"][4:] for path in item["images"]])
                else:
                    item["shop_img"] = ""
            except Exception, e:
                print e

            try:
                tx.execute(self.insertQuestionSql,
                       (item["shop_id"],
                        item["shop_name"],
                        item["shop_img"],
                        item["shop_area"],
                        item["shop_domain"],
                        item["shop_category"],
                        item["shop_cityname"],
                        item["shop_address"],
                        item["shop_telphone"],
                        item["shop_open_time"],
                        item["shop_tag"],
                        item["shop_map_attitude"],
                        item["shop_contact_man"],
                        item["shop_bus_line"],
                        item["shop_description"],
                        item["city_id"],
                        item['shop_template'],
                        ))
            except Exception, e:
                print e
        else:
            try:
                if len(item["images"]) > 0:
                    # 创建头像目录，使用头像ID的首字母作为目录，这样避免头像重复存储
                    userPhotoPath = "./shop/dpa/" + item["images"][0]["path"][4:][1]
                    if not os.path.exists(userPhotoPath):
                        os.makedirs(userPhotoPath)
                        
                    # 图片第一个为头像，移动
                    oldPath = "./img/" + item["images"][0]["path"] 
                    shutil.copy(oldPath, userPhotoPath + item["images"][0]["path"][4:])

                    item["user_photo"] = userPhotoPath + item["images"][0]["path"][4:] 

                    # 创建shopid 目录
                    imgPath = "./shop/dpc/" + item["shop_id"]
                    if not os.path.exists(imgPath):
                        os.makedirs(imgPath)

                    # 移动图片到新目录
                    for path in item["images"][1:]:
                        oldPath = "./img/" + path["path"] 
                        shutil.copy(oldPath, imgPath + path["path"][4:])
    
                    if len(item["images"]) > 1:
                        item["rate_img"] = ",".join([imgPath + path["path"][4:] 
                                                 for path in item["images"][1:]])
                else:
                    item["rate_img"] = ""
                    item["user_photo"] = ""
            except Exception, e:
                print e
                
            try:
                tx.execute(self.insertAnswerSql,
                       (
                        item["rate_id"],
                        item["user_photo"],
                        item["user_nickname"],
                        item["rate_content"],
                        item["rate_img"],
                        item["rate_datetime"],
                        item["shop_id"],
                        item["shop_template"],
                        ))
            except Exception, e:
                print e
            pass
