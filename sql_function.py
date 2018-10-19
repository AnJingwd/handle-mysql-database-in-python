#-*- coding: utf-8 -*-

import configparser,re,xlwt,xlrd,datetime,openpyxl,linecache
import mysql.connector
from mysql.connector import errorcode


def mysql_conf_parse(conf_file):
	cf = configparser.ConfigParser()
	cf.read(conf_file)
	conf_list = cf.items('baseconf')
	conf_dict ={}
	for (key,value) in conf_list:
		conf_dict[key] = cf.get('baseconf',key)
	return conf_dict

def mysql_connect(username,password,database,host,port):
	try:
		conn = mysql.connector.connect(user=username, \
									   password=password, \
									   database=database,\
									   host=host,port=port,\
									   use_unicode=True,buffered=True)
		print("Successed connecting to mysql database {Database} !".format(Database=database))
		return conn
	except mysql.connector.Error as err:
		if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
			print("Something is wrong with your user name or password")
		elif err.errno == errorcode.ER_BAD_DB_ERROR:
			print("Database does not exist")
		else:
			print(err)

def execute_sql(sql,cursor_obj,Return="no"):
	try:
		cursor_obj.execute(sql)
		if Return == "yes":
			result = cursor_obj.fetchall()
			return result
		else:
			pass
	except mysql.connector.errors.ProgrammingError as e:
		print(e)

def create_table_structure(file_name,table_name,cursor_obj,table_info,action="execute"):
	sql = 'create table '+"`"+table_name+"`"+' ('+'id int NOT NULL AUTO_INCREMENT PRIMARY KEY , '

	ret = 0
	'''open an excel file'''
	file_data = xlrd.open_workbook(table_info)
	'''get the first sheet'''
	sheet_data = file_data.sheet_by_index(0)
	'''get the number of rows and columns'''
	nrows_data = sheet_data.nrows
	ncols_data = sheet_data.ncols
	col_names_data = []

	file_info = xlrd.open_workbook(table_info)
	sheet_info = file_info.sheet_by_index(0)
	for i in range(0, ncols_data):
		title_data = sheet_data.cell(0, i).value
		title_data = title_data.strip()
		title_data = title_data.replace(' ','_')
		col_names_data.append(title_data)
	for i in range(0,ncols_data):
		sql = sql+"`"+col_names_data[i]+"`"+' '+sheet_info.cell(2, i).value
		if i != ncols_data-1:
			sql += ','
	sql = sql + ')'
	if action =="print":
		return sql
	else:
		try:
			execute_sql(sql, cursor_obj, Return="no")
			print("Successed creating table {TableName}".format(TableName=table_name))
		except mysql.connector.errors.ProgrammingError as err:
			print("Failed creating table {TableName}".format(TableName=table_name))

def get_line_context(file_path, row):
	line_content = linecache.getline(file_path, row).strip("\n")
	if line_content =="":
		pass
	else:
		value_list = line_content.split("\t")
		return value_list

def insert_data_from_txt(file_name,table_name,cursor_obj,action="execute"):
	ret = 0
	col_names_data = get_table_columns_name(table_name, cursor_obj, action="execute")
	ncols_data = len(col_names_data)
	nrows_data = len(open(file_name,'r').readlines())

	sql = 'INSERT INTO '+"`"+table_name+"`"+'('
	for i in range(1, ncols_data-1):
		sql = sql +"`"+col_names_data[i] +"`"+ ', '
	sql = sql +"`"+col_names_data[ncols_data-1]+"`"
	sql += ') VALUES ('
	sql = sql + '%s,'*(ncols_data-2)
	sql += '%s)'
	if action =="print":
		return sql
	else:
		parameter_list = []
		for row in range(2, nrows_data+1):
			for col in range(0, ncols_data-1):
				meta_data = str(get_line_context(file_name, row)[col])
				parameter_list.append(meta_data)
			try:
				cursor_obj.execute(sql, parameter_list)
				parameter_list = []
				ret += 1
			except mysql.connector.errors.ProgrammingError as err:
				 print(err)
	if ret == nrows_data-1:
		print("Successed inserting {Nrows} into table {TableName}!".format(Nrows=ret,TableName=table_name))

def insert_data_from_xls(file_name,table_name,cursor_obj,action="execute"):
	ret = 0
	file_data = xlrd.open_workbook(file_name)
	sheet_data = file_data.sheet_by_index(0)
	nrows_data = sheet_data.nrows
	ncols_data = sheet_data.ncols
	'''get column names'''
	col_names_data = get_table_columns_name(table_name, cursor_obj, action="execute")

	'''insert data'''
	# construct sql statement
	sql = 'INSERT INTO ' + "`" + table_name + "`" + '('
	for i in range(1, ncols_data):
		sql = sql + "`" + col_names_data[i] + "`" + ', '
	sql = sql + "`" + col_names_data[ncols_data] + "`"
	sql += ') VALUES ('
	sql = sql + '%s,' * (ncols_data-1)
	sql += '%s)'

	if action == "print":
		print(sql)
	else:
		parameter_list = []
		for row in range(1, nrows_data):
			for col in range(0, ncols_data):
				cell_type = sheet_data.cell_type(row, col)
				cell_value = sheet_data.cell_value(row, col)
				if cell_type == xlrd.XL_CELL_DATE:
					dt_tuple = xlrd.xldate_as_tuple(cell_value, file_data.datemode)
					meta_data = str(datetime.datetime(*dt_tuple))
				else:
					meta_data = sheet_data.cell(row, col).value
				parameter_list.append(meta_data)
			try:
				cursor_obj.execute(sql, parameter_list)
				parameter_list = []
				ret += 1
			except mysql.connector.errors.ProgrammingError as err:
				print(err)
	if ret == nrows_data-1:
		print("Successed inserting {Nrows} records into table {TableName}!".format(Nrows=ret,TableName=table_name))

def insert_data_from_xlsx(file_name,table_name,cursor_obj,action="execute"):
	ret = 0
	file_data = openpyxl.load_workbook(file_name)
	sheet_data = file_data.active
	nrows_data = sheet_data.max_row
	ncols_data = sheet_data.max_column
	'''get column names'''
	col_names_data = get_table_columns_name(table_name, cursor_obj, action="execute")

	'''insert data'''
	# construct sql statement
	sql = 'INSERT INTO ' + "`" + table_name + "`" + '('
	for i in range(1, ncols_data):
		sql = sql + "`" + col_names_data[i] + "`" + ', '
	sql = sql + "`" + col_names_data[ncols_data] + "`"
	sql += ') VALUES ('
	sql = sql + '%s,' * (ncols_data-1)
	sql += '%s)'

	if action == "print":
		print(sql)
	else:
		parameter_list = []
		for i in range(2, nrows_data+1):
			for j in range(1, ncols_data+1):
				cell_value = sheet_data.cell(row=i,column=j).value
				parameter_list.append(cell_value)
			try:
				cursor_obj.execute(sql, parameter_list)
				parameter_list = []
				ret += 1
			except mysql.connector.errors.ProgrammingError as err:
				print(err)
	if ret == nrows_data-1:
		print("Successed inserting {Nrows} records into table {TableName}!".format(Nrows=ret,TableName=table_name))

def load_data_from_txt(file_name,table_name,cursor_obj,action="execute"):
	sql = "load data local infile '{FileName}' into table `{TableName}`".format(FileName=file_name,TableName=table_name)
	if action =="print":
		return sql
	else:
		try:
			execute_sql(sql, cursor_obj)
			print("Successed loading data into {TableName}".format(TableName=table_name))
		except  mysql.connector.Error as err:
			print("Failed loading data into {TableName}: {Error}".format(ableName=table_name,Error=err))


def insert_one_column(table_name,column_name,data_type,cursor_obj,position="first",action="execute"):
	sql = "ALTER TABLE {TableName} ADD COLUMN {ColumnName} {DataType} not null ".format(TableName=table_name,ColumnName=column_name,DataType=data_type)
	if position == "first":
		sql_alter = sql + " first"
	else:
		sql_alter = sql + "after {BeforeColumn}".format(BeforeColumn=position)
	if action =="print":
		return sql_alter
	else:
		try:
			execute_sql(sql_alter, cursor_obj)
			print("Successed inserting the {ColumnName} into {TableName}".format(ColumnName=column_name,TableName=table_name))
		except  mysql.connector.Error as err:
			print("Failed inserting the {ColumnName} into {TableName}: {Error}".format(ColumnName=column_name,TableName=table_name,Error=err))

def update_one_column_value(table_name,column_name,column_value,cursor_obj,action="execute"):
	sql = "UPDATE `{TableName}` SET `{ColumnName}`=".format(TableName=table_name,ColumnName=column_name)
	sql_update = (sql + "{UpdateValue}").format(UpdateValue=column_value)
	if action =="print":
		return sql_update
	else:
		try:
			execute_sql(sql_update, cursor_obj)
			print("Successed updating the {ColumnName} column of {TableName}".format(ColumnName=column_name,TableName=table_name))
		except  mysql.connector.Error as err:
			print("Failed updating the {ColumnName} column of {TableName}: {Error}".format(ColumnName=column_name,TableName=table_name,Error=err))

def filter_columns(table_name,table_name_new,condition,cursor_obj,action="execute"):
	sql = "CREATE TABLE {NewTableName} SELECT * FROM {TableName} WHERE {Condition}"
	sql_filter = sql.format(NewTableName=table_name_new,TableName=table_name,Condition=condition)
	if action =="print":
		return sql_filter
	else:
		try:
			execute_sql(sql_filter, cursor_obj)
			print("Successed filtering {TableName}".format(TableName=table_name))
		except  mysql.connector.Error as err:
			print("Failed filtering {TableName}: {Error}".format(TableName=table_name,Error=err))


def export_table(table_name,output_file,cursor_obj,action="execute"):
	sql = "SELECT * FROM `{TableName}` INTO OUTFILE '{OutputFile}'"
	sql_export = sql.format(TableName=table_name,OutputFile=output_file)
	if action =="print":
		return sql_export
	else:
		try:
			execute_sql(sql_export, cursor_obj)
			print("Successed exporting {TableName}".format(TableName=table_name))
		except  mysql.connector.Error as err:
			print("Failed exporting {TableName}: {Error}".format(TableName=table_name,Error=err))

def drop_columns(table_name,columns_list,cursor_obj,action="execute"):
	if len(columns_list) == 1:
		columns_list_str = "DROP COLUMN "+columns_list[0]
	else:
		drop_str_list = add_prefix_str_list("DROP COLUMN ",columns_list,type="list")
		columns_list_str = ",".join(drop_str_list)
	sql = "ALTER TABLE {TableName} {ColumnsList}"
	sql_drop = sql.format(TableName=table_name,ColumnsList=columns_list_str)
	if action =="print":
		return sql_drop
	else:
		try:
			execute_sql(sql_drop, cursor_obj)
			print("Successed dropping columns")
		except  mysql.connector.Error as err:
			print("Failed dropping columns: {}".format(err))

def set_primary_key(table_name,keys_list,cursor_obj,action="execute"):
	if len(keys_list) == 1:
		keys_list_str = keys_list[0]
	else:
		keys_list_str = ",".join(keys_list)
	sql = "ALTER TABLE {TABLE_NAME} add primary key({COLUMNS_NAME})"
	sql_set = sql.format(TABLE_NAME=table_name,COLUMNS_NAME=keys_list_str)
	if action =="print":
		return sql_set
	else:
		try:
			execute_sql(sql_set, cursor_obj)
			print("Successed set primary key")
		except  mysql.connector.Error as err:
			print("Failed set primary key: {}".format(err))

def change_primary_key(table_name,new_keys_list,cursor_obj,action="execute"):
	origin_keys = get_table_primary_key(table_name, cursor_obj)
	sql_drop_primary_key = "ALTER TABLE {TABLE_NAME} drop primary key".format(TABLE_NAME=table_name)
	if action =="print":
		return sql_drop_primary_key
	else:
		try:
			if origin_keys != []:
				execute_sql(sql_drop_primary_key, cursor_obj)
			else:
				pass
			set_primary_key(table_name, new_keys_list, cursor_obj)
			print("Successed change primary key")
		except  mysql.connector.Error as err:
			print("Failed change primary key: {}".format(err))

def set_index(table_name,columns_list,index_name,cursor_obj,action="execute"):
	columns_str = ",".join(columns_list)
	sql = ("ALTER TABLE {TableName} ADD INDEX {IndexName}({ColumnNames})")
	sql_set_index = sql.format(TableName=table_name,IndexName = index_name,ColumnNames = columns_str)
	if action =="print":
		return sql_set_index
	else:
		try:
			execute_sql(sql_set_index, cursor_obj)
			print("Successed setting index")
		except  mysql.connector.Error as err:
			print("Failed setting index: {}".format(err))

def get_tables_name_in_database(cursor_obj,pattern):
	tables = execute_sql("SHOW TABLES", cursor_obj, Return = "yes")
	tables_list = []
	for (table_name,) in tables:
		tables_list.append(table_name)
	sub_tables_list = []
	for each in tables_list:
		matchObj = re.search( r'{Pattern}'.format(Pattern=pattern), each)
		if matchObj:
			sub_tables_list.append(each)
	return sub_tables_list

def get_table_columns_name(table_name,cursor_obj,action="execute"):
	sql = "SHOW COLUMNS FROM {TABLE_NAME}".format(TABLE_NAME = table_name)
	columns_name_list = execute_sql(sql, cursor_obj,Return="yes")
	columns_names = []
	for i in range(len(columns_name_list)):
		columns_names.append(columns_name_list[i][0])
	if action =="print":
		return sql
	else:
		return columns_names

def get_table_primary_key(table_name,cursor_obj,action="execute"):
	sql = "SHOW COLUMNS FROM {TABLE_NAME}".format(TABLE_NAME = table_name)
	results_list = execute_sql(sql, cursor_obj,Return="yes")
	keys = []
	for i in range(len(results_list)):
		if results_list[i][3] == "PRI":
			keys.append(results_list[i][0])
	if action =="print":
		return sql
	else:
		return keys

def get_one_column_dataType(table_name,cursor_obj,column_name,action="execute"):
	sql = "SHOW COLUMNS FROM {TABLE_NAME}".format(TABLE_NAME = table_name)
	if action == "print":
		return sql
	else:
		columns_name_list = execute_sql(sql, cursor_obj,Return="yes")
		for i in range(len(columns_name_list)):
			if columns_name_list[i][0] == column_name:
				if columns_name_list[i][1]:
					return columns_name_list[i][1]
				else:
					return("just get None")

def union_tables(table_name_list,table_name,cursor_obj,type,action="execute"):
	sql_1 = "CREATE TABLE {} ".format(table_name)
	if type =="union_all":
		sql_2 = "(SELECT * FROM {}) UNION ALL "
	else:
		sql_2 = "(SELECT * FROM {}) UNION  "
	sql_3 = "(SELECT * FROM {})".format(table_name_list[-1])
	sql_combine = sql_1
	for i in range(len(table_name_list)-1):
		sql_combine = sql_combine + sql_2.format(table_name_list[i])
	sql_combine = sql_combine + sql_3
	if action =="print":
		return sql_combine
	else:
		try:
			execute_sql(sql_combine,cursor_obj)
			print("Successed combining tables")
		except	mysql.connector.Error as err:
			print("Failed combining tables: {}".format(err))

def remove_repetitive_rows(table_name,column_name,table_name_new,columns_list,cursor_obj,action="execute"):
	if columns_list =="*":
		columns_list_str = "*"
	else:
		columns_list_str = ""
		for i in range(len(columns_list)-1):
			columns_list_str = columns_list_str + columns_list[i] +","
		columns_list_str = columns_list_str + columns_list[-1]

	sql = ("CREATE TABLE {TableNameNew} "
		"SELECT {ColumnsList},count(DISTINCT {ColumnName}) "
		"FROM {TableName} "
		"GROUP BY {ColumnName}")
	sql_update =sql.format(TableNameNew=table_name_new, ColumnName=column_name, TableName=table_name,
						ColumnsList=columns_list_str)
	if action =="print":
		return sql_update
	else:
		try:
			execute_sql(sql_update, cursor_obj)
			print("Successed removing repetitive rows")
		except  mysql.connector.Error as err:
			print("Failed removing repetitive rows: {}".format(err))


def add_prefix_str_list(prefix, mylist,type="list"):
	newList = []
	for i in range(len(mylist)):
		newList.append(prefix + mylist[i])
	mystr = ",".join(newList)
	if type=="str":
		return mystr
	else:
		return newList

def add_list_back_quote(mylist):
	newList = []
	for i in range(len(mylist)):
		newList.append("`" + mylist[i]+"`")
	return newList

def join_tables(join_type,table_name1,table_name2,table_name_new,column_name1,column_name2,columns1,columns2,cursor_obj,action="execute"):
	s1 = table_name1+"."
	columns1_str = add_prefix_str_list(s1,columns1,type="str")
	s2 = table_name2+"."
	columns2_str = add_prefix_str_list(s2,columns2,type="str")

	sql = ("create table {TABLE_NAME_NEW} "
		   "select {COLUMNS1_STR},{COLUMNS2_STR} "
		   "from {TABLE_NAME1} "
		   "{JoinType} join {TABLE_NAME2} "
		   "on ({TABLE_NAME1}.{COLUMN_NAME1} = {TABLE_NAME2}.{COLUMN_NAME2})")
	sql_left_join = sql.format(TABLE_NAME_NEW = table_name_new, \
					 TABLE_NAME1=table_name1, \
					 JoinType = join_type, \
					 TABLE_NAME2=table_name2, \
					 COLUMN_NAME1=column_name1, \
					COLUMN_NAME2=column_name2, \
					COLUMNS1_STR = columns1_str, \
					 COLUMNS2_STR = columns2_str)
	if action =="print":
		return sql_left_join
	else:
		try:
			execute_sql(sql_left_join, cursor_obj)
			print("Successed left join tables")
		except  mysql.connector.Error as err:
			print("Failed left join tables: {}".format(err))


def rename_columns(table_name,origin_name_list,new_name_list,cursor_obj,action="execute"):
	"""ALTER TABLE 表名字 CHANGE 列名称 新列名称 列数据类型"""
	table_all_names = get_table_columns_name(table_name,cursor_obj)
	if len(origin_name_list) != len(new_name_list):
		print("The length of origin_name_list and new_name_list should be equal")
	elif not set(origin_name_list).issubset(set(table_all_names)):
		print("Your origin_name_list has name that may be not correct!")
	else:
		for i in range(len(origin_name_list)):
			data_type = get_one_column_dataType(table_name,cursor_obj,origin_name_list[i])
			sql = ("ALTER TABLE {TableName} "
				   "CHANGE "
				   "{OriginName} {NewName} "
				   "{DataType}")
			sql_rename = sql.format(TableName=table_name, \
							 OriginName=origin_name_list[i],NewName=new_name_list[i], \
							 DataType = data_type)
			if action == "print":
				return sql_rename
			else:
				try:
					execute_sql(sql_rename, cursor_obj)
					comment = "Success rename column {ColumnName} of {TableName}"
					print(comment.format(ColumnName=origin_name_list[i],TableName = table_name))
				except  mysql.connector.Error as err:
					comment = "Failed rename column names of table {ColumnName} of {TableName}: {Error}"
					print(comment.format(ColumnName=origin_name_list[i],TableName = table_name,Error=err))


def truncate_tables(tables_list,cursor_obj,action='execute'):
	tables_list_new = add_list_back_quote(tables_list)
	tables_str = ",".join(tables_list_new)
	sql_truncate = "TRUNCATE TABLE {Tables_Str}".format(Tables_Str=tables_str)
	sql_drop = "DROP TABLE {Table_Str}".format(Table_Str=tables_str)
	if action =="print":
		return (sql_truncate,sql_drop)
	else:
		try:
			execute_sql(sql_truncate,cursor_obj)
			execute_sql(sql_drop,cursor_obj)
			print("Successed truncate tables")
		except	mysql.connector.Error as err:
			print("Failed truncate tables: {}".format(err))


def count_num(table_name,condition,cursor_obj,action='execute'):
	sql = "select count(*) from {TableName} {Condition}"
	sql = sql.format(TableName=table_name,Condition=condition)
	if action =="print":
		return sql
	else:
		try:
			num = execute_sql(sql,cursor_obj,Return="yes")
			return [table_name,num]
			print("Successed count rows")
		except	mysql.connector.Error as err:
			print("Failed count rows: {}".format(err))

