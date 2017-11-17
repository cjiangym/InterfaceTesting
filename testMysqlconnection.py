#coding:utf-8
import pymysql

mysql_info = {
    "host" :"192.168.1.232",
    "port" :3306,
    "user" :"dba",
    "password" :"fvoz6oeC9Y9cMM0VmqlSYkno",
    "db": "appdb",
    "charset": "utf8"
}

class MysqlUtil():
    '''
       mysql数据库相关操作
       连接数据库信息：mysql_info
       创建游标：mysql_execute
       查询某个字段对应的字符串：mysql_getstring
         查询一组数据：mysql_getrows
       关闭mysql连接：mysql_close
    '''
    def __init__(self):
        u"连接池方式"
        self.db_info = mysql_info
        self.conn =MysqlUtil.get_connect(self.db_info)

    def get_connect(db_info):
        try:
            conn = pymysql.connect(host=db_info["host"],port = db_info["port"],user = db_info["user"],password = db_info["password"],db = db_info["db"],charset = db_info["charset"])
            return conn
        except Exception as a:
           print("数据库连接异常：%s" %a)

    def mysql_excute(self,sql):
        u"执行sql语句"
        cur = self.conn.cursor()
        try:
            cur.execute(sql)
        except Exception as a:
            self.conn.rollback()             #sql执行异常后回滚
            print("执行SQL语句出现异常：%s" % a)
        else:
            cur.close()
            self.conn.commit()               #sql执行无异常时提交
    def mysql_getrows(self,sql):
        #查询返回结果
        cur = self.conn.cursor()
        try:
            cur.execute(sql)
        except Exception as a:
            print ("执行SQL语句出现异常：%s" % a)
        else:
            rows = cur.fetchall()
            cur.close ()
            return rows
    def mysql_getstring(self,sql):
        #查询某个字段的对应值
        rows = self.mysql_getrows(sql)
        if rows!=None:
            for row in rows:
                for i in row:
                    return i

    def mysql_close(self):
        #关闭连接
        try:
            self.conn.close()
        except Exception as a:
            print("关闭数据库时连接异常%s"%a)

if __name__ == '__main__':
    mysql = MysqlUtil()
    sql = "select * from jmg_sys_user where id = 784"
    mysql.mysql_excute(sql)
    rows = mysql.mysql_getstring(sql)
    print(rows)


