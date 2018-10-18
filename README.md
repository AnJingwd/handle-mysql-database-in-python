
# 主要功能：
使用python的mysql.connector包实现在python中操作mysql数据库

# 主要脚本
- requirements.txt： 相关依赖的python包，使用python3.6 -m pip install -r requirements.txt进行安装
- get_table_info.py ： 获取xls或者txt表格的表头，每一列的数据类型，通过抽取一定行数的数据，确定每类的合适的数据长度，输出信息写入xls文件，作为创建mysql表结构的输入
- conf.py： 连接数据库相关参数，如用户名，密码等
- sql_function.py： 定义了一系列在python中操作mysql的函数
- import_datas.py： 批量从txt,xls,xlsx文件导入数据至mysql表中

# sql_function.py中相关函数简介

## 第一类：参数解析，数据库连接函数，执行sql语句函数

- mysql_conf_parse(conf_file)：   解析conf.py文件内的数据库连接参数
- mysql_connect(username,password,database,host,port)：  连接数据库函数
- execute_sql(sql,cursor_obj,Return="no")：   执行相应的sql查询语句，Return参数决定是否返回查询结果

## 第二类：数据库表格创建，导入数据，导出数据相关函数

- create_table(file_name,table_name,cursor_obj,table_info)：   创建mysql表结构，table_info参数为get_table_info.py脚本的输出
- insert_data_from_txt(file_name,table_name,cursor_obj,action="execute")： 从txt文件导入数据至mysql表格，action默认为直接执行，若action="print"则输出相应的mysql语句
- load_data_from_txt(file_name,table_name,cursor_obj,action="execute")：从txt文件导入数据至mysql表格，action默认为直接执行，若action="print"则输出相应的mysql语句，与上一函数实现方式不同，结果一致
- insert_data_from_xls(file_name,table_name,cursor_obj,action="execute")： 从xls文件导入数据至mysql表格，action默认为直接执行，若action="print"则输出相应的mysql语句
- insert_data_from_xlsx(file_name,table_name,cursor_obj,action="execute")： 从xlsx文件导入数据至mysql表格，action默认为直接执行，若action="print"则输出相应的mysql语句



## 第三类：sql_function.py模块内使用的函数

- get_line_context(file_path, row)：    获取txt文本指定行的内容


