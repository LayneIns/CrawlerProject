# coding: utf-8

import xlrd, xlwt
import os, sys
import re
from score import senScore
import pickle

def getAllContent(filepath):
	all_comments = []
	filelist = os.listdir(filepath)
	for file in filelist:
		filename = filepath + file
		with open(filename) as fin:
			for line in fin:
				all_comments.append(line.decode("utf-8").strip())
	return all_comments

def getAllKeywords(filepath):
	all_keywords = []
	data = xlrd.open_workbook(filepath)
	table = data.sheet_by_name(u'Sheet1')
	nrows = table.nrows
	for i in range(nrows):
		keyword = table.cell(i, 0).value.strip()
		all_keywords.append(keyword)
	return all_keywords


def getContentKeywords(contents, keywords):
	keyword_index = {}
	for i in range(len(contents)):
		sys.stdout.flush()
		sys.stdout.write(" " * 20 + "\r")
		sys.stdout.flush()
		sys.stdout.write(str(i) + "/" + str(len(contents)) + "\r")
		for j in range(len(keywords)):
			if keywords[j] in contents[i]:
				if keyword_index.get(keywords[j], -1) == -1:
					keyword_index[keywords[j]] = []
				keyword_index[keywords[j]].append(contents[i])
	print "\n"
	return keyword_index


def writeComment(all_comments, filepath):
	with open(filepath, "w") as fout:
		for comment in all_comments:
			fout.write(comment.encode("utf-8") + "\n")

def getScore(keyword_index):
	new_file_list = {}
	for key, value in keyword_index.items():
		new_value = {}
		totalScore = 0.0
		writeComment(value, u"./微博/allComments/" + key + ".txt")
		for comment in value:
			one_score = senScore(comment)
			totalScore += one_score
		print "The score is", totalScore / len(value)
		new_value['aveScore'] = totalScore / len(value)
		new_value['sum'] = len(value)
		new_file_list[key] = new_value
		print "\n"

	return new_file_list

def write2file(file_list):
	data = xlwt.Workbook(encoding='gbk')
	table = data.add_sheet('Sheet1')
	table.write(0, 0, "name")
	table.write(0, 1, "source")
	table.write(0, 2, "score")
	table.write(0, 3, "comments_sum")

	line_cnt = 1
	for key, value in file_list.items():
		table.write(line_cnt, 0, key.encode('gbk'))
		table.write(line_cnt, 1, (u"微博").encode("gbk"))
		table.write(line_cnt, 2, value['aveScore'])
		table.write(line_cnt, 3, value['sum'])
		line_cnt += 1
	data.save(u"./微博/weibo.xls")

if __name__ == "__main__":
	absolute_path = u"./微博/"
	all_comments = getAllContent(absolute_path + "allweibos/")
	print "There are", len(all_comments), "comments"
	all_keywords = getAllKeywords(absolute_path + "program.xlsx")
	print "There are", len(all_keywords), "keywords"

	keyword_index = getContentKeywords(all_comments, all_keywords)
	print "There are", len(keyword_index), "keywords having related contents"

	out_file_1 = open(u"./微博/keyword_index.pkl", "w")
	pickle.dump(keyword_index, out_file_1)

	new_file_list = getScore(keyword_index)

	out_file = open(u"./微博/file_list.pkl", "w")
	pickle.dump(new_file_list, out_file)

	write2file(new_file_list)
