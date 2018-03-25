# coding: utf-8

import scrapy
import chardet
from tencentSpider.items import TencentspiderItem
import sys
import json, time
from scrapy.exceptions import CloseSpider
from scrapy.utils.response import open_in_browser
import re

sys.path.append("../..")
from dataHelper import get_next_keyword

idx = int(open('idx.txt').read().strip())
keyword, video_type = get_next_keyword("../../dataHelper/new_tencent.xlsx", idx)
keyword, video_type = u"有言在仙", u'网络电影'

max_comment_number = 6000


class tencentSpider(scrapy.Spider):
	name = "tencent_spider"
	custom_settings = {
		'FEED_URI': "../../data/" + keyword+'.csv',
		'FEED_FORMAT': 'csv'
	}
	total_comment_number = 0

	def start_requests(self):
		url = "http://m.v.qq.com/search.html?act=0&keyWord=" + keyword
		# complete_url = u"https://ncgi.video.qq.com/fcgi-bin/video_comment_id?op=3&cid=5ttxwmq791c3pa1"
		url = "https://video.coral.qq.com/varticle/2139603248/comment/v2?orinum=10&oriorder=o&pageflag=1&cursor=0&scorecursor=0&orirepnum=2&reporder=o&reppageflag=1&source=9&_=1521916977888"
		# yield scrapy.Request(url, callback=self.parse)
		yield scrapy.Request(url, callback=self.parse5, meta={'playCount':59178855, 'name':"有言在仙", "id": 2139603248})

	def parse(self, response):
		if video_type == u'网络综艺':
			# best_match_item = response.xpath('//p[@class="figure_play _figure_play"][1]/span/@data-href').extract()[0]
			best_match_item = response.xpath('//a[@class="figure _figure"]/@href').extract()[0]
			# query = re.compile(ur"\/[a-z]\/(.+)\.html")
			# program_id = re.findall(query, best_match_item)[0]
			# complete_url = "https://v.qq.com/x/cover/" + program_id + ".html"
			# print best_match_item
			# print "===================="
			index_id = best_match_item.split("=")[-1]
			complete_url = "https://data.video.qq.com/fcgi-bin/column/cover_list?column_id=" + str(index_id) + "&page_size=20&page_no=1&platform=1&version=1&cmd=list&subtype=1"
			yield scrapy.Request(url=complete_url, callback=self.parse6)
		else:
			best_match_item = response.xpath('//div[@class="search_item"][1]')
			if best_match_item:
				complete_url = best_match_item.xpath('./a/@href').extract()[0]
				# print complete_url
				yield scrapy.Request(url=complete_url, callback=self.parse2)


	def parse6(self, response):
		cids = response.xpath('//cid/text()').extract()
		total_view = response.xpath('//totalview/text()').extract()
		# for cid in cids:
		for i in range(len(cids)):
			complete_url = u'https://ncgi.video.qq.com/fcgi-bin/video_comment_id?op=3&cid=' + cids[i]
			if self.total_comment_number <= max_comment_number:
				yield scrapy.Request(url=complete_url, callback=self.parse4, meta={'name':keyword, "playCount":total_view[i], "id": cids[i]})
	

	def parse2(self, response):
		# open_in_browser(response)
		if video_type == u'网络综艺':
			lis = response.xpath('//ul[@data-tpl="variety"]/li')
			
			comment_id_list = []
			playCount = []
			for li in lis:
				one_id = li.xpath('./a[1]/@href').extract()[0].split("cover/")[-1]
				if one_id.endswith(".html"):
					one_id = one_id[:-5]
				#one_id = li.xpath('./a[1]/@href').extract()[0].split("cover/")[-1].strip(".html")
				comment_id_list.append(one_id)
				play_num = li.xpath('./descendant::span[@class="num"]/text()').extract()[1]
				playCount.append(play_num)
			
			for i in range(len(comment_id_list)):
				complete_url = u'https://ncgi.video.qq.com/fcgi-bin/video_comment_id?op=3&cid=' + comment_id_list[i]
				if self.total_comment_number <= max_comment_number:
					yield scrapy.Request(url=complete_url, callback=self.parse4, meta={'name':keyword, "playCount":playCount[i], "id": comment_id_list[i]})
		else:
			playCount = response.xpath('//span[@class="num _view_count"]/text()').extract()[0].replace(",","")
			title = response.xpath('//title/text()').extract()[0]
			print title
			print playCount
			body = response.body.decode('utf-8')
			query = re.compile(ur'targetid":([0-9]+),"title":"{0}'.format(title))
			res = re.findall(query, body)
			if len(res) == 0:
				query = re.compile(ur'targetid":([0-9]+),"title":"{0}'.format(keyword))
				res = re.findall(query, body)
			if res[0] == res[1]:
				res = res[1:]
			for one_id in res:
				complete_url = "https://coral.qq.com/article/" + one_id + "/firstpage/comment/timeline?callback=jsonp3&commentid=" + one_id
				if self.total_comment_number <= max_comment_number:
					yield scrapy.Request(url=complete_url, callback=self.parse3, meta={'playCount':playCount, 'name':title, "id": one_id})

	def parse4(self, response):
		meta = response.meta
		comment_id = response.xpath('//comment_id/text()').extract()[0]
		complete_url = "https://video.coral.qq.com/varticle/" + comment_id + "/comment/v2?orinum=30"
		meta['id'] = comment_id
		yield scrapy.Request(url=complete_url, callback=self.parse5, meta=meta)

	def parse5(self, response):
		item = TencentspiderItem()
		meta = response.meta
		text_content = response.body.decode("utf-8")
		content_dict = json.loads(text_content)
		oriCommList = content_dict[u'data'][u'oriCommList']
		cursor = content_dict[u'data'][u'last']
		for one_content in oriCommList:
			item['content'] = one_content[u'content']
			item['playCount'] = meta['playCount']
			item['name'] = meta['name']
			self.total_comment_number += 1
			yield item
			
		if cursor == "False" or cursor == False:
			cursor = "6270478955235058308"
		if self.total_comment_number <= max_comment_number:
			complete_url = "https://video.coral.qq.com/varticle/" + str(meta['id']) + "/comment/v2?orinum=30&oriorder=o&pageflag=1&cursor=" + str(cursor)
			yield scrapy.Request(url=complete_url, callback=self.parse5, meta=meta)

	def parse3(self, response):
		item = TencentspiderItem()
		meta = response.meta
		text_content = response.body.decode("utf-8").strip("\n").strip("jsonp3(").strip(")")
		content_dict = json.loads(text_content)
		hot_comment = content_dict[u'data'][u'hotcommentid']
		comments = content_dict[u'data'][u'commentid']
		parentinfo = content_dict[u'data'][u'parentinfo']
		cursor = content_dict[u'data'][u'last']
		
		for comment in hot_comment:
			item['content'] = comment[u'content']
			item['playCount'] = meta['playCount']
			item['name'] = meta['name']
			self.total_comment_number += 1
			yield item
		for comment in comments:
			item['content'] = comment[u'content']
			item['playCount'] = meta['playCount']
			item['name'] = meta['name']
			self.total_comment_number += 1
			yield item
		try:
			for key, comment in parentinfo.items():
				item['content'] = comment[u'content']
				item['playCount'] = meta['playCount']
				item['name'] = meta['name']
				self.total_comment_number += 1
				yield item
		except:
			pass
		
		if cursor == "False" or cursor == False:
			cursor = "6266224144146843373"
			print "======================"
		print cursor
		if self.total_comment_number <= max_comment_number:
			complete_url = "https://video.coral.qq.com/varticle/" + str(meta['id']) + "/comment/v2?orinum=30&oriorder=o&pageflag=1&cursor=" + str(cursor)
			yield scrapy.Request(url=complete_url, callback=self.parse5, meta=meta)


	def close(spider, reason):
		with open("idx.txt", "w") as f:
			print >> f, idx + 1