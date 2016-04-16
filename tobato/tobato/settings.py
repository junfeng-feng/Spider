# -*- coding: utf-8 -*-

BOT_NAME = 'tobato'

SPIDER_MODULES = ['tobato.spiders']
NEWSPIDER_MODULE = 'tobato.spiders'


# Configure item pipelines
# See http://scrapy.readthedocs.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    'scrapy.pipelines.images.ImagesPipeline': 1,
    'tobato.pipelines.TobatoPipeline': 300,
}

# mysql config
MYSQL_HOST = '127.0.0.1'
MYSQL_DBNAME = 'spider_db'
MYSQL_USER = 'root'
MYSQL_PASSWD = 'root'
MYSQL_PORT = 3306

#delay
DOWNLOAD_DELAY = 0.05

#images
IMAGES_STORE = r'D:\ProgramingIDE\workspace\SuperSpider\tobato\img'
IMAGES_EXPIRES = 90