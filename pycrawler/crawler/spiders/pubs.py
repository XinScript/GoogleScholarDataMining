from scrapy.spiders import Spider
from scrapy.selector import Selector
from scrapy.http import Request
from scrapy.conf import settings
from crawler.items import CrawlerItem
from datetime import datetime, timedelta
from bson import ObjectId
from fuzzywuzzy import fuzz
import string, random
import pymongo
import urllib, socket
import time
import re
import json

class Crawler(Spider):

	name = "pubs"

	allowed_domains = settings['ALLOWED_DOMAIN']

	def __init__(self):
		connection = pymongo.MongoClient(
            		settings['MONGODB_SERVER'],
            		settings['MONGODB_PORT']
        	)
		self.db = connection[settings['MONGODB_DB']]

		self.profile_table = self.db[settings['TABLE']]

		self.journals = set()

		self.start_urls = []

		cstart = 700

		records = self.profile_table.find({"pubs":{"$size":cstart}})

		ids = []

		links = []

		IDs = []

		self.id_mapper = {}


		for record in records:
			i = record['_id']
			l = record['url']
			k = record['ID']
			ids.append(i)
			links.append(l)
			IDs.append(k)

		length = len(links)

		for i in range(0, length):
			self.id_mapper[IDs[i]] = ids[i]
			self.start_urls.append(links[i] + '&cstart=%d&pagesize=100'%cstart)

		# records = self.profile_table.find("pubs.0":{"$exists":True});

		# for profile in records:
		# 	self.start_urls.append(profile['url']+'&cstart=0&pagesize=100')

	def parse(self, response):
		sel = Selector(response)
		url = response.url
		idx = url.find("user")
		ID = url[idx+5:idx+17]
		item = CrawlerItem()

		item['_id'] = self.id_mapper[ID]

		item['pubs'] = []

		n = len(sel.xpath('//tbody[@id="gsc_a_b"]/tr[@class="gsc_a_tr"]/td[@class="gsc_a_t"]/a/text()').extract())
		for i in range(1,n+1):

			pub = {}

			parent = sel.xpath('//tbody[@id="gsc_a_b"]/tr[@class="gsc_a_tr"][%d]'% i)

			pub['title'] = \
				parent.xpath('./td[@class="gsc_a_t"]/a/text()').extract()
			pub['url'] = \
				parent.xpath('./td[@class="gsc_a_t"]/a/@href').extract()
			pub['author'] = \
				parent.xpath('./td[@class="gsc_a_t"]/div[1]/text()').extract()
			pub['venue'] = \
				parent.xpath('./td[@class="gsc_a_t"]/div[2]/text()').extract()
			pub['citation'] = \
				parent.xpath('./td[@class="gsc_a_c"]/a/text()').extract()
			pub['year'] = \
				parent.xpath('./td[@class="gsc_a_y"]/span/text()').extract()

			fields = ['title','url','author','venue','citation','year']
			for field in fields:
				pub[field] = pub[field][0] if pub[field] else ''


			v = pub['venue']
			v = re.sub('[(!@#$"),./-]', '', v)
			v = re.sub("\d+", '', v)
			v = re.sub("\s\s+" , ' ', v)
			#Add item
			if not self.journals:
				self.journals.add(v)
			else:
				#Calculate and print all fuzzy scores
				for journal in self.journals.copy():
					a = fuzz.ratio(journal, v)
					b = fuzz.partial_ratio(journal, v)
					c = fuzz.token_sort_ratio(journal, v)
					d = fuzz.token_set_ratio(journal, v)
					maximum = max(a, b, c, d)

					if(len(journal) > 32 and len(v) > 32):
						if maximum > 90:
							pub['venue'] = journal
							break
					#Set threshold and replace if above
					else:
						if maximum > 70:
							pub['venue'] = journal
							break
					self.journals.add(v)
			item['pubs'].append(pub)

		yield item

		if n == 100:
			offset = 0; d = 0
			idx = url.find('cstart=')
			idx += 7
			while url[idx].isdigit():
				offset = offset*10 + int(url[idx])
				idx += 1
				d += 1
			yield Request(url[:idx-d] + str(offset+100) + '&pagesize=100', callback = self.parse)
