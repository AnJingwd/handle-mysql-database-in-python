
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

- create_table_structure(file_name,table_name,cursor_obj,table_info)：   创建mysql表结构，table_info参数为get_table_info.py脚本的输出

- insert_data_from_txt(file_name,table_name,cursor_obj,action="execute")： 从txt文件导入数据至mysql表格，action默认为直接执行，若action="print"则输出相应的mysql语句

- load_data_from_txt(file_name,table_name,cursor_obj,action="execute")：从txt文件导入数据至mysql表格，action默认为直接执行，若action="print"则输出相应的mysql语句，与上一函数实现方式不同，结果一致

- insert_data_from_xls(file_name,table_name,cursor_obj,action="execute")： 从xls文件导入数据至mysql表格，action默认为直接执行，若action="print"则输出相应的mysql语句

- insert_data_from_xlsx(file_name,table_name,cursor_obj,action="execute")： 从xlsx文件导入数据至mysql表格，action默认为直接执行，若action="print"则输出相应的mysql语句

- export_table(table_name,output_file,cursor_obj,action="execute")： 导出mysql表至xls，txt等文件

## 第三类：mysql表的增删改查等基本操作

- insert_one_column(table_name,column_name,data_type,cursor_obj,position="first",action="execute")：   插入一列，默认位置为第一列，也可使用position指定相应的列名作为位置，则将在该列名之后插入一列

- update_one_column_value(table_name,column_name,column_value,cursor_obj,action="execute")： 更新一列的内容，常量使用字符串，变量需要在两端连接引号，例如"md5(Tag_cnv)"

- filter_columns(table_name,table_name_new,condition,cursor_obj,action="execute")： 对表table_name的某列根据condition进行过滤，过滤条件需要在两端连接引号，例如"`q0`<0.5"，返回过滤后的新表table_name_new

- drop_columns(table_name,columns_list,cursor_obj,action="execute")： 根据列名删除某列

- set_primary_key(table_name,keys_list,cursor_obj,action="execute")： 设置keys_list列表内的列为主键

- get_table_primary_key(table_name,cursor_obj,action="execute"）： 获取某个表的主键，返回列表

- change_primary_key(table_name,new_keys_list,cursor_obj,action="execute")： 丢弃原表格的主键，更新new_keys_list列表内的列为新的主键

- set_index(table_name,columns_list,index_name,cursor_obj,action="execute")： 设置columns_list列表内的列为索引

- get_tables_name_in_database(cursor_obj,pattern)： 根据正则表达式的pattern获取数据库内的表名，返回列表

- get_table_columns_name(table_name,cursor_obj,action="execute")： 获取某个表的列名，返回列表

- rename_columns(table_name,origin_name_list,new_name_list,cursor_obj,action="execute")： 更改某个表某些列名，需要更改的列名以origin_name_list列表指定，新的列名以new_name_list指定

- get_one_column_dataType(table_name,cursor_obj,column_name,action="execute")： 获取mysql表格某列的mysql数据类型

- remove_repetitive_rows(table_name,column_name,table_name_new,columns_list,cursor_obj,action="execute")： 根据某列column_name去除mysql表的重复数据行，columns_list指定输出的新表

- count_num(table_name,condition,cursor_obj,action='execute')： 根据条件查询某个域记录的数量

- truncate_tables(tables_list,cursor_obj,action='execute')： 删除tables_list指定的mysql表名的列表



# 第四类：多表的连接操作函数

- union_tables(table_name_list,table_name,cursor_obj,type,action="execute")： 对table_name_list内相同结构的表格，通过type指定连接类型，连接类型包括union all 或者union连接，返回新的表table_name

- join_tables(join_type,table_name1,table_name2,table_name_new,column_name1,column_name2,columns1,columns2,cursor_obj,action="execute")： 对表table_name1和table_name2根据join_type指定的连接类型进行连接，两表连接的条件列为column_name1和column_name2，参数columns1和columns2指定连接后分别保留原表的








## 第四类：sql_function.py模块内使用的函数

- get_line_context(file_path, row)：    获取txt文本指定行的内容

- add_prefix_str_list(prefix, mylist,type="list")： 在列表的每个元素前增加prefix前缀

- add_list_back_quote(mylist)： 在列表的每个元素两端增加``符号


