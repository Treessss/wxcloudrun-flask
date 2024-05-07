import os

# 是否开启debug模式
DEBUG = True

# 读取数据库环境变量
username = os.environ.get("MYSQL_USERNAME", 'huinantian')
password = os.environ.get("MYSQL_PASSWORD", 'A2y8Drap5tEzPYAF')
db_address = os.environ.get("MYSQL_ADDRESS", '47.107.62.163:3306')
