# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
from bson import ObjectId
from scrapy.conf import settings

class CrawlerPipeline(object):
    def __init__(self):
        connection = pymongo.MongoClient(settings['MONGODB_SERVER'],settings['MONGODB_PORT'])
        self.db = connection[settings['MONGODB_DB']]
        self.profile = self.db[settings['TABLE']]

    def process_item(self, item, spider):
        if spider.name == "profile":
            post = {'ID':item['ID'], 'url':item['url'], 'name':item['name'],'labels':item['labels'], 'info':item['info'], 'index':item['index'], 'pubs':item['pubs'],'portrait_url':item['portrait_url']}
            self.profile.insert(post)
        elif spider.name == "pubs":
            self.profile.update({'_id':item["_id"]}, {"$push":{"pubs":{"$each":item['pubs']}}}, upsert=True)
            return item
