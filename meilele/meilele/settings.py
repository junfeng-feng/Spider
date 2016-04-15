# -*- coding: utf-8 -*-

# Scrapy settings for meilele project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#     http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#     http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'meilele'

SPIDER_MODULES = ['meilele.spiders']
NEWSPIDER_MODULE = 'meilele.spiders'

ITEM_PIPELINES = {
    'scrapy.pipelines.images.ImagesPipeline': 1,
    'meilele.pipelines.MeilelePipeline': 300,
}

# mysql config
MYSQL_HOST = '127.0.0.1'
MYSQL_DBNAME = 'spider_db'
MYSQL_USER = 'root'
MYSQL_PASSWD = 'root'
MYSQL_PORT = 3306

#delay
DOWNLOAD_DELAY = 0.1

#images
IMAGES_STORE = r'D:\ProgramingIDE\workspace\SuperSpider\tobato\img'
IMAGES_EXPIRES = 90