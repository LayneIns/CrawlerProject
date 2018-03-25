# coding: utf-8
import xlrd
import os

def getallcomment(absolute_path, filelist):
	for file in filelist:
		data = xlrd.open_workbook(absolute_path + file)
		table = data.sheet_by_name('Sheet1')
		nrows = table.nrows
		ncols = table.ncols
		for i in range(nrows):
			

if __name__ == "__main__":
	absolute_path = "../allyoukus/"
	filelist = os.listdir(absolute_path)


