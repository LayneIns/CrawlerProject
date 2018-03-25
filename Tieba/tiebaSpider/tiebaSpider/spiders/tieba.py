# coding: utf-8

import scrapy
import chardet
from tiebaSpider.items import TiebaspiderItem
import sys
import json, time
from scrapy.exceptions import CloseSpider
from scrapy.utils.response import open_in_browser
import re

sys.path.append("../..")
from dataHelper import get_next_keyword

idx = int(open('idx.txt').read().strip())
keyword = get_next_keyword("../../dataHelper/newprogram.xlsx", idx)

# all_article_list = []


class tiebaSpider(scrapy.Spider):
	name = "tieba_spider"
	custom_settings = {
		'FEED_URI': "../../data/" + keyword+'.csv',
		# 'FEED_URI': "../../data/" + u'魔游纪4白骨之姬'+'.csv',
		'FEED_FORMAT': 'csv'
	}
	total_number_cnt = 0
	next_page_number = 0

	def start_requests(self):
		url = "https://tieba.baidu.com/f?ie=utf-8&kw=" + keyword
		yield scrapy.Request(url, callback=self.parse)

	def parse(self, response):
		item = TiebaspiderItem()
		text_content = response.body.decode('utf-8')

		query = re.compile(ur'<a rel="noreferrer"  href="(.+)" title="(.+)" target="_blank" class="j_th_tit ">')
		results = re.findall(query, text_content)

		next_page_query = re.compile(ur'<a href="(.+)" class="next pagination-item " >')
		next_page = re.findall(next_page_query, text_content)
		# all_article_list.extend(res)
		url_list = []
		for res in results:
			if len(set(keyword)&set(res[1])) == len(keyword):
				item[u'name'] = keyword
				item[u'content'] = res[1]
				url_list.append(res[0])
				yield item
				
		for url in url_list:
			complete_url = "https://tieba.baidu.com" + url
			yield scrapy.Request(url=complete_url, callback=self.parse2, meta={'name':keyword})

		if next_page:
			if self.total_number_cnt <= 2000 and self.next_page_number <= 15:
				self.next_page_number += 1
				if next_page[0].startswith("https:"):
					yield scrapy.Request(url=next_page[0], callback=self.parse)
				else:
					yield scrapy.Request(url="https:"+next_page[0], callback=self.parse)

	def parse2(self, response):
		item = TiebaspiderItem()
		meta = response.meta
		content = response.xpath('//div[@class="d_post_content j_d_post_content "]/text()').extract()
		times = response.xpath('//div[@class="post-tail-wrap"]/span[@class="tail-info"][last()]/text()').extract()
		page_content = response.body.decode("utf-8")
		query = re.compile(ur'<a href="(.+)">下一页</a>')
		# next_url = re.findall(query, page_content)
		# print len(content)
		# print len(times)
		# print times
		# print "================="
		for i in range(len(content)):
			one_content = content[i].strip()
			try:
				one_time = times[i].strip()
			except:
				continue
			formatted_time = time.strptime(one_time, "%Y-%m-%d %H:%M")
			if formatted_time.tm_year == 2018 or (formatted_time.tm_year==2017 and formatted_time.tm_mon>=3):
				if len(one_content) >= 8:
					item[u'name'] = meta['name']
					item[u'content'] = one_content
					yield item

		# if len(next_url) != 0 and self.total_number_cnt <= 2000 and meta['next_page'] <= 10:
		# 	meta['next_page'] = int(meta['next_page']) + 1
		# 	next_url = "https://tieba.baidu.com" + next_url[0]
		# 	yield scrapy.Request(url=next_url, callback=self.parse2, meta=meta)


	def close(spider, reason):
		with open("idx.txt", "w") as f:
			print >> f, idx + 1