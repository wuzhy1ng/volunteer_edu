# 加上这两句，解决django自动使用mysqldb连接数据库的问题
import pymysql

pymysql.install_as_MySQLdb()
