# coding: utf-8
import scrapy
import chardet
from doubanSpider.items import DoubanspiderItem
import sys
from scrapy.exceptions import CloseSpider
from scrapy.utils.response import open_in_browser

sys.path.append("../..")
from dataHelper import get_next_keyword


idx = int(open('idx.txt').read().strip())
keyword = get_next_keyword("../../dataHelper/program.xlsx", idx)


class doubanSpider(scrapy.Spider):
	name = "douban_spider"
	custom_settings = {
		'FEED_URI': "../../data/" + keyword+'.csv',
		'FEED_FORMAT': 'csv'
	}

	def start_requests(self):
		url = "https://m.douban.com/search/?query=" + keyword + "&type=movie"
		yield scrapy.Request(url)

	def parse(self, response):
		url = response.xpath('//ul[@class="search_results_subjects"]/li[1]/a/@href').extract()[0].strip("/movie")
		name = response.xpath('//ul[@class="search_results_subjects"]/li[1]/a/div/span[@class="subject-title"]/text()').extract()[0]
		prefix = "https://movie.douban.com/" + url + "/comments?start="
		suffix = "&limit=20&sort=new_score&status=P&percent_type="
		complete_url = prefix + "0" + suffix
		
		url_prefix = "https://movie.douban.com/" + url + "/comments"
		
		yield scrapy.Request(url=complete_url, callback=self.parse2, meta={"keyword": keyword, "prefix": url_prefix})
		
		complete_url_2 = "https://movie.douban.com/" + url + "/reviews?start=0"
		url_prefix_2 = "https://movie.douban.com/" + url + "/reviews"
		yield scrapy.Request(url = complete_url_2, callback=self.parse3, meta={"keyword": keyword, "prefix": url_prefix_2})
		
		
	def parse2(self, response):
		# open_in_browser(response)
		meta = response.meta
		item = DoubanspiderItem()
		comments = response.xpath('//div[@class="comment"]')
		if comments and len(comments) != 0:
			for comment in comments:
				item["name"] = meta["keyword"]
				item["content"] = comment.xpath('./p/text()').extract()[0].strip()
				# item["time"] = comment.xpath('./descendant::span[@class="comment-time "][1]/text()').extract()[0].strip()

				yield item
			
			next_page = response.xpath('//div[@id="paginator"]/a[last()]/@href').extract()
			if len(next_page) != 0:
				next_page = next_page[0]
			
				yield scrapy.Request(meta['prefix'] + next_page, callback=self.parse2, meta={"keyword": meta['keyword'], 'prefix':meta['prefix']})
			
	def parse3(self, response):
		meta = response.meta
		item = DoubanspiderItem()
		contents = response.xpath('//div[@class="short-content"]')
		if contents and len(contents) != 0:
			for content in contents:
				item['name'] = meta['keyword']
				item['content'] = content.xpath('./text()').extract()[0].strip()
				yield item
			
			next_page = response.xpath('//link[@rel="next"]/@href').extract()
			if len(next_page) != 0:
				next_page = next_page[0]
				
				yield scrapy.Request(url=meta['prefix']+next_page, callback=self.parse3, meta=meta)
		

	def close(spider, reason):
		with open("idx.txt", "w") as f:
			print >> f, idx + 1