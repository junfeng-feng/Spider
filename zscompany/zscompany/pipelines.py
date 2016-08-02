# -*- coding: utf-8 -*-
from twisted.enterprise import adbapi
import MySQLdb.cursors

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
class ZscompanyPipeline(object):
    def __init__(self, dbargs):
        self.dbargs = dbargs
        self.insertCompanySql = r"""INSERT INTO `zscompany`
(`company_id`, `company_name`, `company_shortname`, `company_koubei`,`service_zone`,`price`,`service_content`,`decoration_type_jia`,`decoration_type_gong`,`decoration_style`,`city`,`address`,`company_des`,`logo`) VALUES
(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s,%s,%s);"""
    
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
        if len(item['images']) >0:
            logo = item['images'][0]['path']
        else:
            logo = ""
        tx.execute(self.insertCompanySql,
               (
                item["company_id"],
                item["company_name"],
                item["company_shortname"],
                item['koubei'],
                item['service_zone'],
                item["price"],
                item["service_content"],
                item["decoration_type_jia"],
                item['decoration_type_gong'],
                item["decoration_style"],
                item['city'],
                item['address'],
                item['company_des'],
                logo
                ))
