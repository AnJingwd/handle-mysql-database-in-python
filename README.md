
# 主要功能：
使用python的mysql.connector包实现在python中操作mysql数据库

# 主要脚本
- requirements.txt： 相关依赖的python包，使用python3.6 -m pip install -r requirements.txt进行安装
- get_table_info.py ： 获取xls或者txt表格的表头，每一列的数据类型，通过抽取一定行数的数据，确定每类的合适的数据长度，作为创建mysql表结构的输入
- conf.py： 连接数据库相关参数，如用户名，密码等
- sql_function.py： 定义了一系列在python中操作mysql的函数
- import_datas.py： 批量从txt,xls,xlsx文件导入数据至mysql表中

