# -*- coding: utf-8 -*-
from scrapy import log
import scrapy
import MySQLdb.cursors
from twisted.enterprise import adbapi

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

class InsertTmallPipe(object):
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
        self.dbpool.runInteraction(self.updateTmallSql, item)
#         self.dbpool.runInteraction(self.insertTmallSql, item)
        return item
    
    #===========================================================================
    # 修改装修类的品牌和分类
    #===========================================================================
    def updateTmallSql(self, tx, item):
        updateCatSql = """update tmall_category set is_decoration='yes' where category_id=%s"""
        updateBrandSql="""update tmall_brand set is_decoration='yes' where brand_id=%s"""
        if item["flag"] == "category":
            try:
                print updateCatSql%(item["category_id"])
                tx.execute(updateCatSql,(item["category_id"]))
            except Exception,e:
                print e
        elif item["flag"] == "brand":
            brandList = item["category_pro"]["品牌"]
            for index, brandItem in zip(xrange(len(brandList)), brandList):
                try:
                    tx.execute(updateBrandSql, (brandItem["brand_id"]))
                except Exception,e:
                    print e
        pass
    def insertTmallSql(self, tx, item):
        insertProSql = """INSERT INTO `tmall_category_pro` 
            (`category_id`, `pro_id`, `pro_name`, `pro_value`) VALUES
                (%s, %s, %s, %s)"""
                        
        if item["flag"] == "category":
            insertCatSql = r"""INSERT INTO `tmall_category` (`category_id`, `category_name`, `category_level`, `category_level1`, `category_level2`, `category_level3`,`related_product_num`) VALUES
                (%s, %s, %s, %s, %s, %s, %s)"""
            
            try:
                tx.execute(insertCatSql, (item["category_id"], 
                                      item['category_name'].replace("'", ""),
                                      item["category_level"], 
                                      item["category_level1"].replace("'", ""), 
                                      item["category_level2"].replace("'", ""), 
                                      item["category_level3"].replace("'", ""),
                                      item["related_product_num"]
                                      ))
            except Exception,e:
                print e

            
            pro_id = 0
            for pro_name in item["category_pro"]:
                if pro_name=="品牌" or pro_name == "分类":
                    continue
                
                for pro_value in item["category_pro"][pro_name]:
                    pro_id = pro_id + 1
                    try:
                        tx.execute(insertProSql, (item["category_id"], 
                                              pro_id,
                                              pro_name,
                                              pro_value 
                                              ))
                    except Exception,e:
                        print e                        
                    pass
            pass
        elif item["flag"] == "brand":
            #===================================================================
            # TODO
            # 需要，将品牌信息和category关联起来
            #===================================================================
            brandList = item["category_pro"]["品牌"]
            insertBrandSql = r"""INSERT INTO `tmall_brand` (`brand_id`, `brand_en`, `brand_zh`, `brand_logo`) VALUES (%s, %s, %s, %s)"""
            for index, brandItem in zip(xrange(len(brandList)), brandList):
                brand_logo = item["images"][index]["path"] #uuid
                brand_logo = brand_logo.replace("full/", "brand/tm/")
                
                try:
                    tx.execute(insertBrandSql, (brandItem["brand_id"],
                                            brandItem["brand_en"],
                                            brandItem["brand_zh"], 
                                            brand_logo))
                except Exception,e:
                    print e   
                    
                try:
                    tx.execute(insertProSql, (item["category_id"], 
                                              brandItem["brand_id"],
                                              "品牌",
                                              brandItem["brand_zh"] 
                                              ))    
                except Exception,e:
                    print e
         
        pass
