from scrapy.conf import settings
from scrapy.spiders import Spider
from scrapy.selector import Selector
from crawler.items import CrawlerItem
from scrapy.http import Request
from scrapy.exceptions import CloseSpider
from bson import ObjectId
from fuzzywuzzy import fuzz
import json
import string
import os
import re
import logging

class Crawler(Spider):

	name = "profile"

	allowed_domains = settings['ALLOWED_DOMAINS']

	def __init__(self):
		with open('history.json') as f:
			self.history = json.load(f)

		if self.history['NEXT_URL'] == settings['START_URL']:
			raise CloseSpider('THE NEXT_URL IS THE SAME AS START_URL!!')

		start_url = self.history['NEXT_URL'] if self.history['NEXT_URL'] else settings['START_URL']

		self.urlSet = set(self.history['VISTED'])

		self.count = settings['PROFILE_TO_GRAB']

		self.start_urls = []

		# self.start_urls = ['https://scholar.google.co.uk/citations?user=D7bpRJ8AAAAJ&hl=en']

		if start_url not in self.urlSet:
			self.start_urls.append(start_url)
			self.urlSet.add(start_url)



	def parse(self, response):
		sel = Selector(response)

		url = response.url
		idx = url.find("user")
		ID = url[idx+5:idx+17]
		item = CrawlerItem()

		item['ID'] = ID
		item['url'] = url
		item['name'] = sel.xpath('//div[@id="gsc_prf_in"]/text()').extract_first();
		item['labels'] = sel.xpath('//a[@class="gsc_prf_ila"]/text()').extract();
		item['info'] = sel.xpath('//div[@class="gsc_prf_il"][1]/a/text()').extract_first();
		item['portrait_url'] = sel.xpath('//img[@id="gsc_prf_pup"]/@src').extract_first();
		if item['portrait_url'] == '/citations/images/avatar_scholar_150.jpg':
			item['portrait_url'] = ''

		if not item['info']:
			item['info'] = sel.xpath('//div[@class="gsc_prf_il"][1]/text()').extract_first();

		item['index'] = sel.xpath('//table[@id="gsc_rsb_st"]/tr[3]/td[2]/text()').extract_first()

		item['pubs'] = []

		yield item

		urlList = sel.xpath('//a[@class="gsc_rsb_aa"]/@href').extract()
		for url in urlList:
			idx = url.find("user")
			_id = url[idx+5:idx+17]
			if _id in self.urlSet:
				continue
			else:
				self.count -= 1
				print(self.count)
				target_url = 'https://scholar.google.co.uk%s' % url
				if self.count > 0:
					self.urlSet.add(target_url)
					yield Request(target_url,callback=self.parse)
				else:
					self.history['NEXT_URL'] = target_url

	def closed(self,reason):
		self.history['VISTED']= list(self.urlSet)
		with open(file='history.json',mode='w') as f:
			json.dump(self.history,f,indent=4)
