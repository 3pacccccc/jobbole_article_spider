# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import codecs
import json

import pymysql
from scrapy.exceptions import DropItem
from scrapy.exporters import JsonItemExporter
from scrapy.http import Request
import MySQLdb
from twisted.enterprise import adbapi



from scrapy.pipelines.images import ImagesPipeline

class JobboleArticleSpiderPipeline(object):
    def process_item(self, item, spider):
        return item



class jobbole_article_image_pipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        for image_url in item['image_urls']:
            yield Request(url=image_url, meta={'item': item})


    def item_completed(self, results, item, info):
        image_path = [x['path'] for ok, x in results if ok ]
        if not image_path:
            raise DropItem('item got no images')
        return item


    def file_path(self, request, response=None, info=None):
        item = request.meta['item']
        image_guid = request.url.split['/'][-1]
        filenames = 'full/%s/%s/' % (item['title'], image_guid)
        return filenames



class jsonwithencodingpipeline(object):
    #将爬取的数据以json的格式导出
    def __init__(self):
        self.file = codecs.open('/home/maruimin/Pictures/article.json', 'w', encoding= 'utf-8')

    def process_item(self, item, spider):
        lines = json.dumps(item['title'], ensure_ascii=False) + '\n' + '\n' + '\n' + '\n'
        self.file.write(lines)

    def spider_closed(self, spider):
        self.file.closed()


class jsonexporterpipeline(object):
    #将爬取的数据用JsonItemExporter以json的格式导出

    def __init__(self):
        self.file = open('article_exporter.json', 'wb')
        self.exporter = JsonItemExporter(self.file, encoding='utf-8', ensure_ascii=False)
        self.exporter.start_exporting()

    def close_spider(self, spider):
        self.exporter.finish_exporting()
        self.file.close()



    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item



# 配置pipeline将爬取得到数据导入到数据库当中
class mysqlpipeline(object):
    def __init__(self):
        self.conn = MySQLdb.connect('192.168.118.130', 'root', 'root', 'scrapy_spider', charset='utf8', use_unicode=True)
        self.cursor = self.conn.cursor()


    def process_item(self, item, spider):
        insert_sql = """
        insert into jobbole_article (tittle, create_date, url_object_id, comment_nums, fav_nums, praise_nums, tag)
        VALUES (%s, %s, %s, %s, %s, %s, %s)"""

        self.cursor.execute(insert_sql, (item['title'], item['date'], item['url_object_id'], item['comment_nums'], item['collect_nums'], item['praise_nums'], item['tags']))
        self.conn.commit()


# 使用Twisted异步插入链接数据库
class mysqltwistedpipeline(object):


    def __init__(self,dbpool):
        self.dbpool = dbpool



    @classmethod
    def from_settings(cls, settings):
        dbparams = dict(
            host=settings['MYSQL_HOST'],
            db=settings['MYSQL_DB'],
            user=settings['MYSQL_USER'],
            password=settings['MYSQL_PASSWORD'],
            charset='utf8',
            cursorclass=pymysql.cursors.DictCursor,
            use_unicode=True,
        )



        dbpool = adbapi.ConnectionPool('pymysql', **dbparams)

        return cls(dbpool)


    def process_item(self, item, spider):
        querry = self.dbpool.runInteraction(self.do_insert, item)
        querry.addErrback(self.handle_error)


    def handle_error(self,failure):
        print(failure)

    def do_insert(self, cursor, item):
        insert_sql = """
                insert into jobbole_article (tittle, create_date, url_object_id, comment_nums, fav_nums, praise_nums, tag)
                VALUES (%s, %s, %s, %s, %s, %s, %s)"""

        cursor.execute(insert_sql, (
        item['title'], item['date'], item['url_object_id'], item['comment_nums'], item['collect_nums'],
        item['praise_nums'], item['tags']))


