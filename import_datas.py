#-*- coding: utf-8 -*-
import os,sys,argparse
'''import customized module'''
current_path = os.path.split(os.path.realpath(__file__))[0]
sys.path.append(current_path)
import sql_function as myfunction


'''import parameters'''
parser = argparse.ArgumentParser(description="Read xls files in datapath and creat mysql tables automaticly")
parser.add_argument('--table_info',help="the header,data type and length info",required = True)
parser.add_argument('--data_path',help="the absolute path or relative path of data folder",required = True)
args= parser.parse_args()


conf_file = os.path.join(current_path,"conf.py")
conf_dict = myfunction.mysql_conf_parse(conf_file)
conn = myfunction.mysql_connect(conf_dict['user'],conf_dict['password'],\
								conf_dict['db_name'],conf_dict['host'],conf_dict['port'])
cursor = conn.cursor()


table_info = args.table_info
for root, subfolders, filenames in os.walk(args.data_path):
	num = len(filenames)
	for filename in filenames:
		file_path = os.path.join(root,filename)
		table_name = filename.split(".")[0].replace("-","_")
		myfunction.create_table_structure(file_path,table_name,cursor,table_info)
		conn.commit()
		file_type = filename.split(".")[-1]
		if file_type =="txt":
			myfunction.insert_data_from_txt(file_path, table_name, cursor)
		elif file_type =="xls":
			myfunction.insert_data_from_xls(file_path, table_name, cursor)
		else:
			myfunction.insert_data_from_xlsx(file_path, table_name, cursor)
		conn.commit()
	print("Successed creating  and instering data into {Num} tables !".format(Num=num))
