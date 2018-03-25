# coding: utf-8

import xlrd, xlwt
import os, sys
import re
from score import senScore
import pickle


def getFileList(filepath):
	file_list = os.listdir(filepath)
	return file_list

def getPlayCount(filepath):
	play_count_list = {}
	with open(filepath) as fin:
		for line in fin:
			line_decoded = line.decode("utf-8")
			line_cutted = re.split(ur"\s", line_decoded)
			play_count_list[line_cutted[0]] = line_cutted[2]

	return play_count_list

def readComments(filepath):
	comments = []
	data = xlrd.open_workbook(filepath)
	table = data.sheet_by_name(u'Sheet1')
	nrows = table.nrows
	for i in range(nrows):
		if i == 0:
			continue
		content = table.cell(i, 0).value
		if not isinstance(content, unicode):
			if isinstance(content, float):
				continue

		content = content.strip().strip(u'。').strip(".")
		if len(content) > 5:
			comments.append(content)
	return comments

def writeComment(all_comments, filepath):
	with open(filepath, "w") as fout:
		for comment in all_comments:
			fout.write(comment.encode("utf-8") + "\n")


def getScore(file_list, play_count_list, filepath):
	new_file_list = {}
	for one_file in file_list:
		file = one_file.strip(".xlsx")
		filename = filepath + file
		value = {}
		value['playCount'] = play_count_list[file]
		all_comments = readComments(filename + ".xlsx")
		log_info = "There are " + str(len(all_comments)) + " comments in " + file
		print log_info.encode("gbk")

		if len(all_comments) == 0:
			continue

		totalScore = 0.0
		writeComment(all_comments, u"./优酷/allComments/" + file + ".txt")
		for comment in all_comments:
			one_score = senScore(comment)
			totalScore += one_score
		print "The score is", totalScore / len(all_comments)
		value['aveScore'] = totalScore / len(all_comments)
		value['sum'] = len(all_comments)
		new_file_list[file] = value
		print "\n"


	return new_file_list


def write2file(file_list):
	data = xlwt.Workbook(encoding='gbk')
	table = data.add_sheet('Sheet1')
	table.write(0, 0, "name")
	table.write(0, 1, "playCount")
	table.write(0, 2, "source")
	table.write(0, 3, "score")
	table.write(0, 4, "comments_sum")

	line_cnt = 1
	for key, value in file_list.items():
		table.write(line_cnt, 0, key.encode('gbk'))
		table.write(line_cnt, 1, value['playCount'].encode("gbk"))
		table.write(line_cnt, 2, (u"优酷").encode("gbk"))
		table.write(line_cnt, 3, value['aveScore'])
		table.write(line_cnt, 4, value['sum'])
		line_cnt += 1
	data.save(u"./优酷/youku.xls")


if __name__ == "__main__":
	absolute_path = u"./优酷/"
	play_count_list = getPlayCount(absolute_path + u"优酷播放量统计.txt")
	
	file_list = getFileList(absolute_path + "allyoukus/")
	print "There are", len(file_list), "files."
	
	new_file_list = getScore(file_list, play_count_list, absolute_path+"allyoukus/")

	out_file = open(u"./优酷/file_list.pkl", "w")
	pickle.dump(new_file_list, out_file)
	
	write2file(new_file_list)
	
