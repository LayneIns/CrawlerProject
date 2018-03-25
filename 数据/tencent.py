# coding: utf-8

import xlrd, xlwt
import os, sys
from score import senScore
import pickle


def readFileList(filepath):
	file_list = {}
	with open(filepath) as fin:
		for line in fin:
			one_file = line.strip().decode("utf-8").split(", ")
			file_list[one_file[0].strip(".csv")] = {"playCount": one_file[2], "indexFile": one_file[1] + ".txt"}
	return file_list

def writeComment(all_comments, filepath):
	with open(filepath, "w") as fout:
		for comment in all_comments:
			fout.write(comment.encode("utf-8") + "\n")


def getScore(file_list, index_path):
	new_file_list = {}
	for key, value in file_list.items():
		all_comments = []
		with open(index_path + value["indexFile"]) as fin:
			for line in fin:
				line_decoded = line.decode("utf-8").strip().strip(u"。").strip(".")
				if len(line_decoded) > 5:
					all_comments.append(line_decoded)
		if len(all_comments) == 0:
			continue

		log_info = "There are " + str(len(all_comments)) + " comments in " +  key
		print log_info.encode("gbk")
		totalScore = 0.0
		writeComment(all_comments, u"./腾讯/allComments/" + key + ".txt")
		for comment in all_comments:
			one_score = senScore(comment)
			totalScore += one_score
		print "The score is", totalScore / len(all_comments)
		value['aveScore'] = totalScore / len(all_comments)
		value['sum'] = len(all_comments)
		new_file_list[key] = value
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
		table.write(line_cnt, 1, value['playCount'])
		table.write(line_cnt, 2, (u"腾讯").encode("gbk"))
		table.write(line_cnt, 3, value['aveScore'])
		table.write(line_cnt, 4, value['sum'])
		line_cnt += 1
	data.save(u"./腾讯/tencent.xls")


if __name__ == "__main__":
	index_path = u"./腾讯/new_data/"
	file_list = readFileList(index_path + "index.txt")
	print "There are", len(file_list), "files to score."
	new_file_list = getScore(file_list, index_path)
	
	out_file = open(u"./腾讯/file_list.pkl", "w")
	pickle.dump(new_file_list, out_file)
	
	write2file(new_file_list)


