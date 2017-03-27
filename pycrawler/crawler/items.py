# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field

class CrawlerItem(Item):
	ID = Field()
	_id = Field()
	url = Field()
	name = Field()
	labels = Field()
	info = Field()
	index = Field()
	pubs = Field()
	portrait_url = Field()
