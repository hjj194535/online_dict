'''
数据库处理
'''
import pymysql
import time

class ConnectDB:
    def __init__(self,host='127.0.0.1',port=3306,user='root',pwd='123456',database='dict',charset='utf8'):
        self.host = host
        self.port = port
        self.user = user
        self.pwd = pwd
        self.database = database
        self.charset = charset

    def do_connect(self):
        return pymysql.connect(host=self.host,port=self.port,
                               user=self.user,password=self.pwd,
                               database=self.database,charset=self.charset)
class User:
    def __init__(self):
        self.manager = ConnectDB()
        self.db = self.manager.do_connect()

    def do_register(self,name,pwd):
        cur = self.db.cursor()
        sql = 'select name from users where name = %s'
        cur.execute(sql,[name])
        data = cur.fetchone()
        if data:
            return False
        try:
            sql = 'insert into users(name,password) values(%s,%s)'
            cur.execute(sql,[name,pwd])
            self.db.commit()
            return True
        except Exception as e:
            print(e)
            self.db.rollback()
            return False
        finally:
            cur.close()
    def do_login(self,name,pwd):
        cur = self.db.cursor()
        sql = 'select name from users where name = %s and password=%s'
        cur.execute(sql,[name,pwd])
        data = cur.fetchone()
        if data:
            cur.close()
            return True
        cur.close()
        return False
    def insert_history(self,word,name):
        cur = self.db.cursor()
        try:
            sql = 'insert into history_record(username,word) values(%s,%s)'
            cur.execute(sql,[name,word])
            self.db.commit()
        except Exception as e:
            print(e)
            self.db.rollback()
        finally:
            cur.close()

    def do_query(self,word,name):
        self.insert_history(word,name)
        cur = self.db.cursor()
        sql = 'select mean from words where word=%s'
        cur.execute(sql,[word])
        data = cur.fetchone()
        if data:
            return data[0]
        return

    def get_history(self,name):
        cur = self.db.cursor()
        sql = 'select username,word,time from history_record where ' \
              'username=%s order by time desc limit 10'
        cur.execute(sql,[name])
        data = cur.fetchall()
        return data
    def db_close(self):
        self.db.close()


