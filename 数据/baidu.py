# coding: utf-8

import xlrd, xlwt
import csv
import os, sys
import re
from score import senScore
import pickle

def getAllFile(filepath):
	file_list = os.listdir(filepath)
	return file_list

def getComments(file_list, filepath):
	file_index = {}
	for file in file_list:
		filename = filepath + file
		contents = []
		with open(filename) as fin:
			reader = csv.reader(fin)
			for item in reader:
				if reader.line_num == 1:
					continue
				content = item[0]
				if isinstance(content, float):
					content = str(content)
				content = content.decode("utf-8").strip().strip(u"。").strip(".")

				if len(content) > 15:
					contents.append(content)
		if len(contents) != 0:
			file_index[file.strip(".csv")] = contents

	return file_index

def writeComment(all_comments, filepath):
	with open(filepath, "w") as fout:
		for comment in all_comments:
			fout.write(comment.encode("utf-8") + "\n")


def getScore(keyword_index):
	new_file_list = {}
	cnt = 3
	for key, value in keyword_index.items():
		new_value = {}
		totalScore = 0.0
		writeComment(value, u"./百度贴吧/allComments/" + key + ".txt")
		for comment in value:
			one_score = senScore(comment)
			totalScore += one_score
		print key.encode("gbk"), "the score is", totalScore / len(value)
		new_value['aveScore'] = totalScore / len(value)
		new_value['sum'] = len(value)
		new_file_list[key] = new_value
		print "\n"
		cnt += 1
		if cnt == 3:
			break

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
		table.write(line_cnt, 1, (u"贴吧").encode("gbk"))
		table.write(line_cnt, 2, value['aveScore'])
		table.write(line_cnt, 3, value['sum'])
		line_cnt += 1
	data.save(u"./百度贴吧/tieba.xls")


if __name__ == "__main__":
	absolute_path = u"./百度贴吧/"
	file_list = getAllFile(absolute_path + u"data/")

	file_index = getComments(file_list, absolute_path + "data/")
	print "There are", len(file_index), "keywords having related contents"

	out_file_1 = open(u"./百度贴吧/file_index.pkl", "w")
	pickle.dump(file_index, out_file_1)

	new_file_list = getScore(file_index)

	out_file = open(u"./百度贴吧/file_list.pkl", "w")
	pickle.dump(new_file_list, out_file)

	write2file(new_file_list)