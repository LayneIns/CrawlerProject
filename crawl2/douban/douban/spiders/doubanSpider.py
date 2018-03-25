# coding: utf-8
import scrapy
import chardet
from douban.items import DoubanItem
import sys
from scrapy.exceptions import CloseSpider
from scrapy.utils.response import open_in_browser

sys.path.append("../..")
from dataHelper import get_next_keyword


idx = int(open('../../dataHelper/idx.txt').read().strip())
keyword = get_next_keyword("../../dataHelper/program.xlsx", idx)


class doubanSpider(scrapy.Spider):
	name = "douban_spider"
	custom_settings = {
		'FEED_URI': keyword+'.csv',
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
		
		yield scrapy.Request(url=complete_url, callback=self.parse2, meta={"keyword": keyword, 'page_cnt':0, 'prefix':prefix, "suffix": suffix})

	def parse2(self, response):
		# open_in_browser(response)
		meta = response.meta
		item = DoubanItem()
		comments = response.xpath('//div[@class="comment"]')
		for comment in comments:
			item["keyword"] = meta["keyword"]
			item["content"] = comment.xpath('./p/text()').extract()[0].strip()
			item["time"] = comment.xpath('./descendant::span[@class="comment-time "][1]/text()').extract()[0].strip()
			# year_s, mon_s, day_s = item["time"].split('-')
			# year = int(year_s)
			# mon = int(mon_s)
			# day = int(day_s)
			# if year < 2018 or (year == 2018 and mon < 3):
			# 	raise CloseSpider(reason='Time = 2018.03.01')
			yield item
		yield scrapy.Request(meta['prefix'] + str(meta['page_cnt']+20) + meta['suffix'], callback=self.parse2, meta={"keyword": meta['keyword'], 'page_cnt':int(meta['page_cnt'])+20, 'prefix':meta['prefix'], "suffix": meta['suffix']})

	def close(spider, reason):
		with open("../../dataHelper/idx.txt", "w") as f:
			print >> f, idx + 1