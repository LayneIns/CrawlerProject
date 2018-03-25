# coding: utf-8
# 
import scrapy
import chardet
from doubanSpider.items import DoubanTotalspiderItem
import sys
from scrapy.exceptions import CloseSpider
from scrapy.utils.response import open_in_browser

sys.path.append("../..")
from dataHelper import get_all_keywords


idx = int(open('idx.txt').read().strip())
all_keywords = get_all_keywords("../../dataHelper/program.xlsx")


class doubanSpider(scrapy.Spider):
	name = "douban_total_spider"
	custom_settings = {
		'FEED_URI': "../../data/douban_total.csv",
		'FEED_FORMAT': 'csv'
	}

	def start_requests(self):
		for keyword in all_keywords:
			url = "https://m.douban.com/search/?query=" + keyword + "&type=movie"
			yield scrapy.Request(url, callback=self.parse, meta={"keyword":keyword})

	def parse(self, response):
		url = response.xpath('//ul[@class="search_results_subjects"]/li[1]/a/@href').extract()[0].strip("/movie")
		name = response.xpath('//ul[@class="search_results_subjects"]/li[1]/a/div/span[@class="subject-title"]/text()').extract()[0]
		
		complete_url = "https://movie.douban.com/" + url + "/"
		
		yield scrapy.Request(url=complete_url, callback=self.parse2, meta=response.meta)
		
		
	def parse2(self, response):
		# open_in_browser(response)
		meta = response.meta
		item = DoubanTotalspiderItem()
		number = response.xpath('//span[@property="v:votes"]/text()').extract()[0].strip()
		score = response.xpath('//strong[@class="ll rating_num"]/text()').extract()[0].strip()
		# five = response.xpath('//span[@class="stars5 starstop"]/text()').extract()[0].strip()
		# four = response.xpath('//span[@class="stars4 starstop"]/text()').extract()[0].strip()
		# three = response.xpath('//span[@class="stars3 starstop"]/text()').extract()[0].strip()
		# two = response.xpath('//span[@class="stars2 starstop"]/text()').extract()[0].strip()
		# one = response.xpath('//span[@class="stars1 starstop"]/text()').extract()[0].strip()
		rating_per = response.xpath('//span[@class="rating_per"]/text()').extract()
		
		item['name'] = meta['keyword']
		item['number'] = number
		item['score'] = score
		item['five'] = rating_per[0]
		item['four'] = rating_per[1]
		item['three'] = rating_per[2]
		item['two'] = rating_per[3]
		item['one'] = rating_per[4]

		yield item
			
		
	def close(spider, reason):
		with open("idx.txt", "w") as f:
			print >> f, idx + 1