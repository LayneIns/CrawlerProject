# coding: utf-8

import xlrd, xlwt
import os, sys
import re
from score import senScore
import pickle


def getAllProgram(filepath):
	file_index = {}
	data = xlrd.open_workbook(filepath)
	table = data.sheet_by_name(u'Sheet1')
	nrows = table.nrows
	for i in range(nrows):
		key = table.cell(i, 0).value
		value = {"playCount": 0, "score": 0.0, "comment_number": 0, "source":"", \
				"douban_score": 0.0, "douban_number":0, \
				"baidu_score": 0.0, "baidu_number": 0, \
				"weibo_score": 0.0, "weibo_number": 0}
		file_index[key] = value
	return file_index

def getMainContent(filepath, source):
	comment_list = {}
	data = xlrd.open_workbook(filepath)
	table = data.sheet_by_name(u'Sheet1')
	nrows = table.nrows
	for i in range(nrows):
		if i == 0:
			continue
		key = table.cell(i, 0).value
		value = {}
		value['playCount'] = table.cell(i, 1).value
		value['source'] = source
		value['score'] = table.cell(i, 3).value
		value['comment_number'] = table.cell(i, 4).value
		comment_list[key] = value
	return comment_list


def addContent(main_list, add_list):
	wrong_list = []
	for key, value in add_list.items():
		try:
			main_list[key]['playCount'] = value['playCount']
			main_list[key]['score'] = value['score']
			main_list[key]['comment_number'] = value['comment_number']
			main_list[key]['source'] = value['source']
		except:
			wrong_list.append(key)
	return main_list, wrong_list


def getDoubanContent(filepath):
	comment_list = {}
	data = xlrd.open_workbook(filepath)
	table = data.sheet_by_name(u'Sheet1')
	nrows = table.nrows
	for i in range(nrows):
		if i == 0:
			continue
		key = table.cell(i, 0).value
		value = {}
		value['score'] = table.cell(i, 2).value
		value['comment_number'] = table.cell(i, 1).value
		comment_list[key] = value

	return comment_list


def addDouban(main_list, add_list):
	wrong_list = []
	for key, value in add_list.items():
		try:
			main_list[key]['douban_score'] = value['score']
			main_list[key]['douban_number'] = value['comment_number']
		except:
			wrong_list.append(key)
	return main_list, wrong_list


def getWeiboContent(filepath):
	comment_list = {}
	data = xlrd.open_workbook(filepath)
	table = data.sheet_by_name(u'Sheet1')
	nrows = table.nrows
	for i in range(nrows):
		if i == 0:
			continue
		key = table.cell(i, 0).value
		value = {}
		value['score'] = table.cell(i, 2).value
		value['comment_number'] = table.cell(i, 3).value
		comment_list[key] = value
	return comment_list


def addWeibo(main_list, add_list):
	wrong_list = []
	for key, value in add_list.items():
		try:
			main_list[key]['weibo_score'] = value['score']
			main_list[key]['weibo_number'] = value['comment_number']
		except:
			wrong_list.append(key)
	return main_list, wrong_list


def getTiebaContent(filepath):
	comment_list = {}
	data = xlrd.open_workbook(filepath)
	table = data.sheet_by_name(u'Sheet1')
	nrows = table.nrows
	for i in range(nrows):
		if i == 0:
			continue
		key = table.cell(i, 0).value
		value = {}
		value['score'] = table.cell(i, 2).value
		value['comment_number'] = table.cell(i, 3).value
		comment_list[key] = value
	return comment_list


def addTieba(main_list, add_list):
	wrong_list = []
	for key, value in add_list.items():
		try:
			main_list[key]['baidu_score'] = value['score']
			main_list[key]['baidu_number'] = value['comment_number']
		except:
			wrong_list.append(key)
	return main_list, wrong_list


'''
{"playCount": 0, "score": 0.0, "comment_number": 0, "source":"", \
				"douban_score": 0.0, "douban_number":0, \
				"baidu_score": 0.0, "baidu_number": 0, 
				"weibo_score": 0.0, "weibo_number": 0}
'''
def write2file(file_list):
	data = xlwt.Workbook(encoding='gbk')
	table = data.add_sheet('Sheet1')
	table.write(0, 0, "name")
	table.write(0, 1, "playCount")
	table.write(0, 2, "score")
	table.write(0, 3, "comment_number")
	table.write(0, 4, "source")
	table.write(0, 5, "douban_score")
	table.write(0, 6, "douban_number")
	table.write(0, 7, "baidu_score")
	table.write(0, 8, "baidu_number")
	table.write(0, 9, "weibo_score")
	table.write(0, 10, "weibo_number")

	line_cnt = 1
	for key, value in file_list.items():
		table.write(line_cnt, 0, key)
		table.write(line_cnt, 1, value['playCount'])
		table.write(line_cnt, 2, value['score'])
		table.write(line_cnt, 3, value['comment_number'])
		table.write(line_cnt, 4, value['source'])
		table.write(line_cnt, 5, value['douban_score'])
		table.write(line_cnt, 6, value['douban_number'])
		table.write(line_cnt, 7, value['baidu_score'])
		table.write(line_cnt, 8, value['baidu_number'])
		table.write(line_cnt, 9, value['weibo_score'])
		table.write(line_cnt, 10, value['weibo_number'])
		line_cnt += 1
	data.save(u"result.xls")


if __name__ == "__main__":
	file_index = getAllProgram("program.xlsx")
	iqiyi_list = getMainContent(u"./爱奇艺/iqiyi.xls", u"爱奇艺")
	tencent_list = getMainContent(u"./腾讯/tencent.xls", u"腾讯")
	youku_list = getMainContent(u"./优酷/youku.xls", u"优酷")

	file_index, wrong_list_1 = addContent(file_index, iqiyi_list)
	file_index, wrong_list_2 = addContent(file_index, tencent_list)
	file_index, wrong_list_3 = addContent(file_index, youku_list)

	wrong_list = []
	wrong_list.extend(wrong_list_1)
	wrong_list.extend(wrong_list_2)
	wrong_list.extend(wrong_list_3)

	douban_list = getDoubanContent(u"./豆瓣/douban_result.xls")
	file_index, wrong_list_douban = addDouban(file_index, douban_list)

	weibo_list = getWeiboContent(u"./微博/weibo.xls")
	file_index, wrong_list_weibo = addWeibo(file_index, weibo_list)

	tieba_list = getTiebaContent(u"./百度贴吧/tieba.xls")
	file_index, wrong_list_tieba = addTieba(file_index, tieba_list)

	write2file(file_index)
