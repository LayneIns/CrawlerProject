# coding: utf-8
import csv
import os

def getcontent(filename, outfilename):
	csvFile = open(filename, "r")
	reader = csv.reader(csvFile)
	result = {}
	outfile = open(outfilename, "w")
	playCount = 0
	for item in reader:
		if reader.line_num == 1:
			continue
		content = item[0]
		playCount = item[1]
		if content.strip().strip("。"):
			outfile.write(content + "\n")
	outfile.close()

	return playCount


def readcsv(absolute_path, infilelist):
	with open("index.txt", "w") as fout1:
		for i in range(len(infilelist)):
			filename = infilelist[i]
			print absolute_path + filename
			playCount = getcontent(absolute_path + filename, str(i) + ".txt")
			fout1.write(filename + ", " + str(i) + ", " + str(playCount) + "\n")

def getFileList(filepath):
	filelist = os.listdir(filepath)
	return filelist


if __name__ == "__main__":
	absolute_path = "../iQiyi/data/"
	filelist = getFileList(absolute_path)
	readcsv(absolute_path, filelist)

