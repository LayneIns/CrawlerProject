# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DoubanspiderItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    content = scrapy.Field()


class DoubanTotalspiderItem(scrapy.Item):
	name = scrapy.Field()
	number = scrapy.Field()
	score = scrapy.Field()
	five = scrapy.Field()
	four = scrapy.Field()
	three = scrapy.Field()
	two = scrapy.Field()
	one = scrapy.Field()
