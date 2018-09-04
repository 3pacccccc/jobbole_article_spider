# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import codecs
import json

from scrapy.exceptions import DropItem
from scrapy.http import Request


from scrapy.pipelines.images import ImagesPipeline

class JobboleArticleSpiderPipeline(object):
    def process_item(self, item, spider):
        return item



class jobbole_article_spider_pipeline(ImagesPipeline):
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
    def __init__(self):
        self.file = codecs.open('/home/maruimin/Pictures/article.json', 'w', encoding= 'utf-8')

    def process_item(self, item, spider):
        lines = json.dumps(dict(item), ensure_ascii=False) + '\n' + '\n' + '\n' + '\n'
        self.file.write(lines)

    def spider_closed(self,spider):
        self.file.closed()