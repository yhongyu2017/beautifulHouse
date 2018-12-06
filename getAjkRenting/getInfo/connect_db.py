# 创建数据库连接的类
import pymysql


class ConnectDb(object):
    def __init__(self, host, port, user, password, database, charset):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.database = database
        self.charset = charset
        self.create_connect()

    def create_connect(self):
        self.db = pymysql.connect(host=self.host,
                                  port=self.port,
                                  user=self.user,
                                  password=self.password,
                                  database=self.database,
                                  charset=self.charset)
        self.cursor = self.db.cursor()

    def close_connect(self):
        self.cursor.close()
        self.db.close()

    def insert_into_db(self, sql, lst):
        try:
            self.cursor.execute(sql, lst)
            self.db.commit()
            print("yes")
        except:
            print("no")
            self.db.rollback()


# 测试连接
# conn = ConnectDb('127.0.0.1',
#                  3306,
#                  'root',
#                  '',
#                  'house',
#                  'utf8')
# sql = "insert into user_info(user_id, user_name) values('12a','Lee')"
# conn.insert_into_db(sql)
# conn.close_connect()
