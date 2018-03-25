# coding: utf-8
import csv
import xlwt

def readcsv(filename):
	csvFile = open(filename, "r")
	reader = csv.reader(csvFile)
	result = []
	for item in reader:
		if reader.line_num == 1:
			continue
		one_line = []
		one_line.append(item[0].decode("utf-8"))
		one_line.append(item[1].decode("utf-8"))
		one_line.append(item[4].decode("utf-8"))
		one_line.append(item[2].decode("utf-8"))
		one_line.append(item[7].decode("utf-8"))
		one_line.append(item[6].decode("utf-8"))
		one_line.append(item[3].decode("utf-8"))
		one_line.append(item[5].decode("utf-8"))
		result.append(one_line)
	csvFile.close()
	return result

def write2xlsx(results):
	data = xlwt.Workbook(encoding="gbk")
	table = data.add_sheet('Sheet1')
	table.write(0, 0, "name")
	table.write(0, 1, "sum_of_people")
	table.write(0, 2, "score")
	table.write(0, 3, "one_star")
	table.write(0, 4, "two_star")
	table.write(0, 5, "three_star")
	table.write(0, 6, "four_star")
	table.write(0, 7, "five_star")

	for i in range(len(results)):
		for j in range(8):
			table.write(i + 1, j, results[i][j].encode("gbk"))
	data.save('douban_result.xls')

if __name__ == "__main__":
	write2xlsx(readcsv("douban_total.csv"))





