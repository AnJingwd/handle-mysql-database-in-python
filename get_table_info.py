#-*- coding: utf-8 -*-
import os,argparse,random
import linecache
import xlrd,xlwt

'''import parameters'''
parser = argparse.ArgumentParser(description="get xls table file columns info for creating mysql tables")
parser.add_argument('--input_file',help="xls or txt file as input",required = True)
parser.add_argument('--output_file',help="xls file as output",required = True)
parser.add_argument('--n_rows',help="inter num for sample",required = True)
args = parser.parse_args()

'''creat output xls file '''
myWorkbook = xlwt.Workbook()
mySheet = myWorkbook.add_sheet('Sheet1',cell_overwrite_ok=True)


'''judue the type of value and calculate length'''
def judge(value):
	if isinstance(value, int):
		return(['int',0])
	elif isinstance(value,float):
		return(['float',0,])
	else:
		return (['str',len(value)])

def get_line_context(file_path, row):
	value_list = linecache.getline(file_path, row).strip("\n").split("\t")
	return value_list

file_name = os.path.basename(args.input_file)
input_file_type = file_name.split(".")[-1]


if input_file_type == "xls":
	'''open input xls file'''
	file = xlrd.open_workbook(args.input_file)
	sheet = file.sheet_by_index(0)
	nrows = sheet.nrows
	ncols = sheet.ncols

	'''random sample row nums of input file'''
	random.seed(1)
	rows_list = random.sample(range(1, nrows), int(args.n_rows))

	col_j_len_list = []
	for j in range(0, ncols):
		title = sheet.cell(0, j).value
		row_1 = sheet.cell(1, j).value
		mySheet.write(0, j, title)
		mySheet.write(1, j, judge(row_1)[0])
		for i in rows_list:
			row_i = sheet.cell(i, j).value
			col_j_len_list.append(judge(row_i)[1])
			if max(col_j_len_list) >= 200:
				mySheet.write(2, j, 'text')
			else:
				mySheet.write(2, j, 'varchar(255)')
			myWorkbook.save(args.output_file)

if input_file_type == "txt":
	file = open(args.input_file,'r').readlines()
	nrows = len(file)

	'''random sample row nums of input file'''
	random.seed(1)
	rows_list = random.sample(range(1, nrows), int(args.n_rows))

	file_path = args.input_file
	ncols = len(get_line_context(file_path, 1))

	col_j_len_list = []
	for j in range(0, ncols):
		title = get_line_context(file_path, 1)[j]
		row_1 = get_line_context(file_path, 2)[j]
		mySheet.write(0, j, title)
		mySheet.write(1, j, judge(row_1)[0])
		for i in rows_list:
			row_i = get_line_context(file_path, i)[j]
			col_j_len_list.append(judge(row_i)[1])
			if max(col_j_len_list) >= 200:
				mySheet.write(2, j, 'text')
			else:
				mySheet.write(2, j, 'varchar(255)')
			# myWorkbook.save(args.output_file)
			myWorkbook.save(args.output_file)