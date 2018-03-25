# coding: utf-8

import xlrd


def getProgramList(filepath):
	program_list = dict()
	program_list[u'网络剧'] = []
	program_list[u'网络电影'] = []
	program_list[u'网络综艺'] = []
	
	data = xlrd.open_workbook(filepath)
	
	table = data.sheet_by_name(u'网络剧')
	nrows = table.nrows
	ncols = table.ncols
	for i in range(2, nrows):
		one_program = dict()
		one_program[u'节目名称'] = table.cell(i, 1).value
		one_program[u'播出网站'] = table.cell(i, 3).value
		program_list[u'网络剧'].append(one_program)
	
	table = data.sheet_by_name(u'网络电影')
	nrows = table.nrows
	ncols = table.ncols
	for i in range(2, nrows):
		one_program = dict()
		one_program[u'节目名称'] = table.cell(i, 1).value
		one_program[u'播出网站'] = table.cell(i, 3).value
		program_list[u'网络电影'].append(one_program)
	
	table = data.sheet_by_name(u'网络综艺')
	nrows = table.nrows
	ncols = table.ncols
	for i in range(2, nrows):
		one_program = dict()
		one_program[u'节目名称'] = table.cell(i, 1).value
		one_program[u'播出网站'] = table.cell(i, 3).value
		program_list[u'网络综艺'].append(one_program)
	
	return program_list


def get_next_keyword(filepath, idx):
	data = xlrd.open_workbook(filepath)
	table = data.sheet_by_name('Sheet1')
	nrows = table.nrows
	ncols = table.ncols
	
	return table.cell(idx, 0).value
	
	
	
if __name__ == "__main__":
	program_list = getProgramList(u"征片情况汇总0213.xlsx")
	print(program_list)
	

