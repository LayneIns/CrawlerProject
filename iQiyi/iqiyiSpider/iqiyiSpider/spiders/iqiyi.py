# coding: utf-8

import scrapy
import chardet
from iqiyiSpider.items import IqiyispiderItem
import sys
import json, time
from scrapy.exceptions import CloseSpider
from scrapy.utils.response import open_in_browser

sys.path.append("../..")
from dataHelper import get_next_keyword

idx = int(open('idx.txt').read().strip())
keyword, video_type = get_next_keyword("../../dataHelper/new_iQiyi.xlsx", idx)
keyword, video_type = u'私人英雄 ', u'网络电影'

class iqiyiSpider(scrapy.Spider):
	name = "iqiyi_spider"
	custom_settings = {
		'FEED_URI': "../../data/" + keyword+'.csv',
		'FEED_FORMAT': 'csv'
	}
	total_comment_number = 0
	

	def start_requests(self):
		url = "http://search.video.iqiyi.com/o?if=html5&pageNum=1&pageSize=20&limit=20&timeLength=0&key=" + keyword
		print video_type.encode("gbk")
		print video_type == u'网络电影'
		print "============================"
		if video_type != u'网络电影':
			yield scrapy.Request(url, callback=self.parse)
		else:
			yield scrapy.Request(url, callback=self.parse3)

	def parse(self, response):
		text_content = response.body.decode("utf-8")
		
		content_dict = json.loads(text_content)
		try:
			play_count = content_dict[u'data'][u'docinfos'][0][u'albumDocInfo'][u'playCount']
		except:
			play_count = 0
		try:
			circle_id = content_dict[u'data'][u'docinfos'][0][u'albumDocInfo'][u'circle_summaries'][0][u'id']
		except:
			return
		
		now_time = int(time.time())
		for i in range(40):
			complete_url = "http://api-t.iqiyi.com/feed/get_feeds?agenttype=118&wallId=" + str(circle_id) + "&count=50&upOrDown=1&snsTime=" + str(now_time-i*30)

			yield scrapy.Request(url=complete_url, callback=self.parse2, meta={"playCount": play_count, "name":keyword, "circle_id":circle_id})

		
	def parse2(self, response):
		# open_in_browser(response)
		meta = response.meta
		item = IqiyispiderItem()
		text_content = response.body.decode("utf-8")
		content_dict = json.loads(text_content)
		comments = content_dict[u'data'][u'feeds']
		snsTime = 5
		for comment in comments:
			item["content"] = comment[u'description']
			item["name"] = meta[u'name']
			item["playCount"] = meta[u'playCount']

			snsTime = comment[u'snsTime']
			self.total_comment_number += 1
			yield item
		if snsTime != 0 and self.total_comment_number <= 6000:
			complete_url = "http://api-t.iqiyi.com/feed/get_feeds?agenttype=118&wallId=" + str(meta['circle_id']) + "&count=50&upOrDown=1&snsTime=" + str(snsTime)
			yield scrapy.Request(url=complete_url, callback=self.parse2, meta=meta)
	
	def parse3(self, response):
		text_content = response.body.decode("utf-8")
		
		content_dict = json.loads(text_content)
		try:
			play_count = content_dict[u'data'][u'docinfos'][0][u'albumDocInfo'][u'playCount']
		except:
			play_count = 0
		album_id = content_dict[u'data'][u'docinfos'][0][u'albumDocInfo'][u'albumId']

		complete_url = "http://mixer.video.iqiyi.com/jp/mixin/videos/" + str(album_id)
		print "=============="
		print album_id
		yield scrapy.Request(url=complete_url, callback=self.parse4, meta={"playCount": play_count, "name":keyword, "page": 1})
	
	def parse4(self, response):
		meta = response.meta
		text_content = response.body.decode("utf-8").strip(u'var tvInfoJs=')
		content_dict = json.loads(text_content)
		qitan_id = content_dict[u'qitanId']
		meta['qitan_id'] = qitan_id
		
		complete_url = "http://api-t.iqiyi.com/qx_api/comment/get_video_comments?page=" + str(meta['page']) + "&page_size=100&qitanid=" + str(qitan_id) + "&sort=add_time"
		yield scrapy.Request(url=complete_url, callback=self.parse5, meta=meta)
	
	def parse5(self, response):
		meta = response.meta
		item = IqiyispiderItem()
		text_content = response.body.decode("utf-8")
		content_dict = json.loads(text_content)
		
		try:
			comments = content_dict[u'data'][u'comments']
			for comment in comments:
				item["content"] = comment[u'content']
				item["name"] = meta[u'name']
				item["playCount"] = meta[u'playCount']
				yield item
		except:
			comments = [0]
			pass
			
		if self.total_comment_number <= 6000 and len(comments) != 0:
			page = int(meta['page']) + 1
			complete_url = "http://api-t.iqiyi.com/qx_api/comment/get_video_comments?page=" + str(page) + "&page_size=100&qitanid=" + str(meta['qitan_id']) + "&sort=add_time"
			meta['page'] = page
				
			yield scrapy.Request(url=complete_url, callback=self.parse5, meta=meta)
		

		
		

	def close(spider, reason):
		with open("idx.txt", "w") as f:
			print >> f, idx + 1
