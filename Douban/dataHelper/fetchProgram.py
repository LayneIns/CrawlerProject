# coding: utf-8

import xlrd

def get_next_keyword(filepath, idx):
	data = xlrd.open_workbook(filepath)
	table = data.sheet_by_name('Sheet1')
	nrows = table.nrows
	ncols = table.ncols
	
	return table.cell(idx, 0).value

def get_all_keywords(filepath):
	data = xlrd.open_workbook(filepath)
	table = data.sheet_by_name('Sheet1')
	nrows = table.nrows
	ncols = table.ncols

	all_keywords = []
	for i in range(nrows):
		all_keywords.append(table.cell(i, 0).value)
	return all_keywords