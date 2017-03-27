# -*- coding: utf-8 -*-

# Scrapy settings for crawler project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'crawler'

SPIDER_MODULES = ['crawler.spiders']
NEWSPIDER_MODULE = 'crawler.spiders'
DOWNLOAD_DELAY = 3
DOWNLOAD_TIMEOUT = 300
# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'crawler hafsah'
#USER_AGENT = 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:47.0) Gecko/20100101 Firefox/47.0'

ITEM_PIPELINES = {
	'crawler.pipelines.CrawlerPipeline': 300
}

MONGODB_SERVER = "localhost"
MONGODB_PORT = 27018
MONGODB_DB = "googletest"

# Retry many times since proxies often fail
RETRY_TIMES = 3
# Retry on most error codes since proxies fail for different reasons
RETRY_HTTP_CODES = [500, 503, 504, 400, 403, 404, 408]

DOWNLOADER_MIDDLEWARES = {
    'scrapy.downloadermiddlewares.retry.RetryMiddleware': 300,
	'scrapy.downloadermiddlewares.httpcache.HttpCacheMiddleware':120
    # 'crawler.randomproxy.RandomProxy': 100,
    # 'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': 110,
}

# Proxy list containing entries like
# http://host1:port
# http://username:password@host2:port
# http://host3:port
# ...
PROXY_LIST = 'proxies.txt'
#USER_AGENT_LIST = "useragents.txt"

# TABLE = "googletest"
TABLE = "GoogleScholar"

ALLOWED_DOMAINS = ['scholar.google.co.uk']

LOG_LEVEL = 'INFO'

PROFILE_TO_GRAB = 500

PUBS_TO_GRAB = 100

CONCURRENT_REQUESTS=60

CONCURRENT_REQUESTS_PER_DOMAIN=60

DOWNLOAD_TIMEOUT=80

HTTPCACHE_POLICY = "scrapy.extensions.httpcache.RFC2616Policy"

COOKIES_ENABLED = False

HTTPCACHE_ENABLED = True

START_URL = "https://scholar.google.co.uk/citations?user=D7bpRJ8AAAAJ&hl=en"
# DEPTH_LIMIT = 1000

USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36"

#'scrapy.downloadermiddleware.useragent.UserAgentMiddleware': None,
#'crawler.random_useragent.RandomUserAgentMiddleware': 400
