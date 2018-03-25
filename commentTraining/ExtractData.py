# coding: utf-8

import sys, os
import re
from lxml import etree
from snownlp import sentiment

def getSemEvalComments():
	filepath = "./SemEval/"
	fileList = os.listdir(filepath)

	postive_content = []
	negative_content = []

	for file in fileList:
		filename = filepath + file
		print "filename:", filename
		with open(filename) as fin:
			content = fin.read()
		
		tree = etree.HTML(content)
		# print tree
		sentences = tree.xpath('//sentence')
		#print sentences
		for sentence in sentences:
			text = sentence.xpath("./text/text()")[0]
			opinions = sentence.xpath("./opinions/opinion/@polarity")
			if opinions:
				opinion = opinions[0]
				if opinion == u"positive":
					postive_content.append(text.strip())
				elif opinion == u"negative":
					negative_content.append(text.strip())
	print len(postive_content)
	print len(negative_content)

	return postive_content, negative_content


def write2file(contents, filename):
	with open(filename, "w") as fout:
		for content in contents:
			fout.write(content.encode("utf-8") + "\n")


def getHotelComment(filepath):
	content_list = []
	files = os.listdir(filepath)
	for file in files:
		filename = filepath + file
		with open(filename) as fin:
			lines = fin.readlines()
		for line in lines:
			if line.strip():
				content_list.append(line.strip().decode("utf-8"))
	print len(content_list)
	return content_list


def TrainAndSave(negfile, posfile):
	sentiment.train(negfile, posfile)
	sentiment.save('sentiment.marshal')


if __name__ == "__main__":
	TrainAndSave("neg.txt", "pos.txt")
	'''
	pos_content, neg_content = getSemEvalComments()

	pos_content_1 = getHotelComment("./ChnSentiCorp/pos/")
	neg_content_1 = getHotelComment("./ChnSentiCorp/neg/")

	pos_content.extend(pos_content_1)
	print len(pos_content)
	neg_content.extend(neg_content_1)
	print len(neg_content)

	write2file(pos_content, "pos.txt")
	write2file(neg_content, "neg.txt")
	'''




	