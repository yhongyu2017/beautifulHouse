import uuid
import pymysql
import time
from utils.encrypt import md5

#数据库操作
class Db_Util(object):
    def __init__(self) -> None:
        # type: () -> None
        configs = {
            'host': 'localhost',
            'port': 3306,
            'user': 'root',
            'database': 'house',
            'charset': 'utf8'
        }
        host = configs.get('host')
        port = configs.get('port')
        user = configs.get('user')
        password = configs.get('password')
        database = configs.get('database')
        charset = configs.get('charset')

        config = dict(host=host, port=port, user=user, password=password,
                      database=database, charset=charset)
        self.conn = pymysql.connect(**config)

        self.cursor = self.conn.cursor()

    def close_conn(self):
        self.cursor.close()
        self.conn.close()

    def save_user(self, **kwargs):
        user_id = uuid.uuid1()
        name = kwargs.get('user_name')
        pwd = kwargs.get('user_pwd')
        email = kwargs.get('user_email')
        params = (str(user_id), name, md5(pwd), time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), email)
        print(params)
        sql_str = 'insert into ' \
                  'user_info(user_id,user_name,user_pwd,user_create_time,user_email) ' \
                  'VALUES (%s,%s,%s,%s,%s)'
        result = self.cursor.execute(sql_str, params)
        return result

    def find_user(self, **kwargs):
        '''

        :param kwargs:
        :return:
        :author:yuzl
        '''
        keys = []
        values = []
        for key in kwargs:
            keys.append(key)
            values.append(kwargs.get(key))

        sql_str = 'select * from user_info where'
        for key in kwargs:
            sql_str += ' ' + key + '=%s and'
        sql_str += ' 1=1'

        self.cursor.execute(sql_str, tuple(values))
        result = self.cursor.fetchall()
        return result

    def update_user_info(self, user, **kwargs):
        '''
        :param args:
        :param kwargs:
        :return:
        '''
        keys = []
        values = []
        douhao = [',', ',', ',', ',', ' ']
        for key in kwargs:
            keys.append(key)  # 键
            values.append(kwargs.get(key))  # 键的值
        sql_str = 'update user_info set'
        for key in kwargs:
            sql_str += ' ' + key + '= '
            #     peng 修改11.1日
            # sql_str += values[0]
            sql_str += "'{}'".format(values[0])
            values.remove(values[0])

            sql_str += douhao[0]
            douhao.remove(douhao[0])
        sql_str += ' where user_name= "{}"'.format(user)
        print(sql_str, __class__, '数据库89行')
        result = self.cursor.execute(sql_str)
        return result

    def find_user_manage(self, **kwargs):
        user_name = kwargs.get('user_name')
        sql_str = 'select * from user_info where user_name=%s'
        self.cursor.execute(sql_str, (user_name,))
        result = self.cursor.fetchall()
        print(result,__class__,'数据') #打印测试
        return result
#======================================================pyr

    def find_history_info(self, user):
        '''
        用户查询历史记录操作
        :param user: 用户名
        :return result: 查询结果（存放在元组）
        :author: gzw
        '''
        sql_str1 = "select ajk_renting_title,scan_time from ajk_renting_info,history_record where house_id=ajk_renting_id and user_id=(select user_id from user_info where user_name=%s)"
        self.cursor.execute(sql_str1, (user,))
        result1 = self.cursor.fetchall()
        sql_str2 = "select renting_title,scan_time from renting_house,history_record where house_id=renting_id and user_id=(select user_id from user_info where user_name=%s)"
        self.cursor.execute(sql_str2, (user,))
        result2 = self.cursor.fetchall()
        result = result1 + result2
        print(result)
        return result

    def delete_history_info(self, user):
        '''
        用户清空历史纪录操作
        :param user: 用户名
        :return result: 清空结果
        :author: gzw
        '''
        sql_str = "delete from history_record where user_id=(select user_id from user_info where user_name=%s)"
        self.cursor.execute(sql_str, (user,))
        result = self.conn.commit()
        return result

    def insert_history_info(self, user, house_id):
        history_id = uuid.uuid1()
        house_id = house_id
        scan_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        user_name = user
        sql_query = 'select user_id from user_info where user_name=%s'
        self.cursor.execute(sql_query, (user_name,))
        user_id = self.cursor.fetchone()[0]
        sql_str = "insert into history_record values(%s,%s,%s,%s)"
        result = self.cursor.execute(sql_str, (str(history_id),house_id,user_id,scan_time))
        print(result)
        return result
# =====================================================gzw

    def find_rent_house(self, house_id):
        '''
        获取租房的详细信息
        :param house_id:
        :return:
        '''
        sql_str = '''select renting_id, land_lord_id, city, region, renting_title,renting_pictrue, door_model, renting_area, renting_floor, renting_address,rent_type,renting_orientation,near_subway,has_elevator,renting_price,house_type,renting_fitment,release_time,renting_detail,is_check,user_name,user_phone from renting_house,user_info where renting_id=%s and renting_house.land_lord_id=user_info.user_id'''
        self.cursor.execute(sql_str, (house_id,))
        result = self.cursor.fetchall()
        print(result)
        return result

    def find_user_info(self, user):
        L = []
        data = ['user_name', 'user_email', 'user_create_time', 'user_gender', 'user_address', 'user_phone']
        sql_str = 'select user_name, user_email, user_create_time, user_gender, user_address, user_phone ' \
                  'from user_info where user_name=%s'
        self.cursor.execute(sql_str, (user,))
        result = self.cursor.fetchall()
        if result:
            for field in result:
                d = dict(zip(data, field))
                L.append(d)
        return L
#======================================================zjy

    def insert_advice(self, **kwargs):
        advice_id = str(uuid.uuid1())
        advice_type = kwargs.get('advice_type')
        advice_content = kwargs.get('advice_content')
        advice_time = str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        # sql_str = "insert into advice(advice_id,advice_content, advice_time) values (%s, %s, %s)".format(advice_id,advice_content,send_time)

        params = (advice_id, advice_type, advice_content, advice_time)
        print(params)
        sql_str = 'insert into ' \
                  'advice(advice_id,advice_type,advice_content, advice_time) ' \
                  'values (%s, %s, %s, %s)'
        print(sql_str)
        result = self.cursor.execute(sql_str, params)

        # self.cursor.execute(sql_str)
        print('插入显示：', result)
        return result
#======================================================zy

    def find_rent_info(self, **kwargs):
        keys = []
        values = []
        for key in kwargs:
            keys.append(key)
            if kwargs.get(key) == "1500以下":
                values.append("1500")
            elif kwargs.get(key) == "20000以上":
                values.append("20000")
            else:
                if key == "renting_price":
                    values += kwargs.get(key).split("-")
                else:
                    values.append(kwargs.get(key))
        print(keys, values)
        if len(values) == 4:
            if values[1] == "20000":
                sql_str = 'select * from renting_house where '+keys[0]+'=%s and '+keys[1]+'>=%s and '+keys[2]+' like %s and '+keys[3]+'=%s'
                self.cursor.execute(sql_str, (values[0],values[1],values[2][0]+'%',values[3]))
                result = self.cursor.fetchall()
                print(result)
            else:
                sql_str = 'select * from renting_house where '+keys[0]+'=%s and '+keys[1]+'<%s and '+keys[2]+' like %s and '+keys[3]+'=%s'
                self.cursor.execute(sql_str, (values[0],values[1],values[2][0]+'%',values[3]))
                result = self.cursor.fetchall()
                print(result)
        else:
            sql_str = 'select * from renting_house where '+keys[0]+'=%s and '+keys[1]+'>=%s and '+keys[1]+'<%s and '+keys[2]+' like %s and '+keys[3]+'=%s'
            self.cursor.execute(sql_str, (values[0],values[1],values[2],values[3][0]+'%',values[4]))
            result = self.cursor.fetchall()
            print(result)
        return result

    def find_third_rent_info(self, **kwargs):
        keys = []
        values = []
        for key in kwargs:
            keys.append(key)
            if kwargs.get(key) == "1500以下":
                values.append("1500")
            elif kwargs.get(key) == "20000以上":
                values.append("20000")
            else:
                if key == "ajk_renting_price":
                    values += kwargs.get(key).split("-")
                else:
                    values.append(kwargs.get(key))
        if len(values) == 4:
            if values[1] == "20000":
                sql_str = 'select * from ajk_renting_info where ' + keys[0] + '=%s and ' + keys[1] + '>=%s and ' + keys[
                    2] + ' like %s and ' + keys[3] + '=%s'
                self.cursor.execute(sql_str, (values[0], int(values[1]), values[2][0] + '%', values[3]))
                result = self.cursor.fetchall()
            else:
                sql_str = 'select * from ajk_renting_info where ' + keys[0] + '=%s and ' + keys[1] + '<%s and ' + keys[
                    2] + ' like %s and ' + keys[3] + '=%s'
                self.cursor.execute(sql_str, (values[0], int(values[1]), values[2][0] + '%', values[3]))
                result = self.cursor.fetchall()
        else:
            sql_str = 'select * from ajk_renting_info where ' + keys[0] + '=%s and ' + keys[1] + '>=%s and ' + keys[
                1] + '<%s and ' + keys[2] + ' like %s and ' + keys[3] + '=%s'
            self.cursor.execute(sql_str, (values[0], int(values[1]), int(values[2]), values[3][0] + '%', values[4]))
            result = self.cursor.fetchall()
        return result
#======================================================gzw

    def find_admin(self, **kwargs):
        '''
        管理员登陆--数据库
        :param kwargs::
        :return:
        :author:Yanfuzi
        '''
        keys = []
        values = []
        for key in kwargs:
            keys.append(key)
            values.append(kwargs.get(key))
        sql_str = 'select * from admin_info where'
        for key in kwargs:
            sql_str += ' ' + key + '=%s and'
        sql_str += ' 1=1'
        self.cursor.execute(sql_str, tuple(values))
        result = self.cursor.fetchall()
        return result

    def save_admin(self, **kwargs):
        admin_id = uuid.uuid1()
        admin_name = kwargs.get('adminName')
        admin_pwd = kwargs.get('adminPwd')
        add_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        params = (str(admin_id), admin_name, admin_pwd, add_time)
        sql_str = "insert into admin_info(admin_id, admin_name, admin_pwd, add_time)" \
                  "values(%s,%s,%s,%s);"
        result = self.cursor.execute(sql_str, params)
        return result

    def find_house(self, **kwargs):
        '''
        查找已经发布的房源信息
        :param args:
        :return:
        :author:Yanfuzi
        '''
        # values = str(args[0])
        # is_check = str(kwargs.get('is_check', ''))
        # renting_id = str(kwargs.get('renting_id', ''))
        L = []
        keys = []
        values = []
        for key in kwargs:
            keys.append(key)
            values.append(kwargs.get(key))
        data = ['renting_id', 'renting_title', 'region', 'user_name', 'user_email', 'release_time', 'renting_detail']
        # sql_str = 'select renting_id, renting_title, region, user_name, user_email, release_time ' \
        #           'from renting_house ' \
        #           'join user_info ' \
        #           'on renting_house.land_lord_id=user_info.user_id ' \
        #           'where is_check=%s and user_info.is_land_lord=1;'

        sql_str = 'select renting_id, renting_title, region, user_name, user_email, release_time, renting_detail ' \
                  'from renting_house ' \
                  'join user_info ' \
                  'on renting_house.land_lord_id=user_info.user_id where'
        for key in kwargs:
            sql_str += ' ' + key + '=%s and'
        sql_str += ' 1=1 order by release_time desc'
        self.cursor.execute(sql_str, tuple(values))
        result = self.cursor.fetchall()
        if result:
            for field in result:
                d = dict(zip(data, field))
                L.append(d)
        # print('数据库内容：', L)
        return L

    def delete_house(self, **kwargs):
        '''
        删除房源   后台管理的处理
        :param args:
        :return:
        :author:Yanfuzi
        '''
        # print('kwargs:', kwargs)
        # values = []
        # for val in kwargs['renting_id']:
        #     values.append(val)
        # print('values', values)
        values = kwargs.get('renting_id')
        # print('要删除的获取的ajax传的值', values)
        sql_str = "delete from renting_house where renting_id=%s"
        result = self.cursor.execute(sql_str, [values])
        # print('result:', result)  1
        return result

    def searchHouse(self, **kwargs):
        searchInput = kwargs['searchInput']
        # print('要搜索的房源标题内容是：', searchInput)

        L = []
        data = ['renting_id', 'renting_title', 'region', 'user_name', 'user_email', 'release_time']
        sql_str = 'select renting_id, renting_title, region, user_name, user_email, release_time ' \
                  'from renting_house ' \
                  'join user_info ' \
                  'on renting_house.land_lord_id=user_info.user_id ' \
                  'where is_check=1 and user_info.is_land_lord=1 and renting_title like "%{}%"'.format(searchInput)
        self.cursor.execute(sql_str)
        result = self.cursor.fetchall()
        for field in result:
            d = dict(zip(data, field))
            L.append(d)
        # print(L)
        return L

    def update_house(self, **kwargs):

        print('kw:', kwargs)
        print("kw[]", kwargs['param1'])
        # 存放要修改的字段，值
        keys1 = []
        values1 = []
        # 存放条件字段，值
        key2 = []
        values2 = []

        for key in kwargs['param1']:
            keys1.append(key)
            values1.append(kwargs['param1'].get(key))
        for key in kwargs['param2']:
            key2.append(key)
            values2.append(kwargs['param2'].get(key))
        # print('kwargs:', kwargs)
        # print('keys:', keys1)
        # print('values:', values1)
        values = values1 + values2
        sql_str = 'update renting_house set '
        for key in kwargs['param1']:
            sql_str += key + '=%s ,'
        sql_str = sql_str[:-1]
        sql_str += ' where '
        for key in kwargs['param2']:
            sql_str += ' ' + key + '=%s and'
        sql_str += ' 1=1'
        # print(sql_str)

        result = self.cursor.execute(sql_str, tuple(values))
        # result = self.conn.commit()
        # print('数据库返回的结果：',result)  # 1
        return result

    def update_admin_block(self, is_block, admin_id):
        sql_str = 'update admin_info set is_block=%s where admin_id=%s'
        result = self.cursor.execute(sql_str, (is_block, admin_id))
        print('result:', result)
        # result is 1
        return result
#=====================================================yzz

    def find_advice(self):
        # alues = str(args[0])
        L = []
        data = ['advice_type', 'advice_id', 'advice_content', 'advice_time']
        sql_str = 'select advice_type, advice_id, advice_content, advice_time ' \
                  'from advice;'

        self.cursor.execute(sql_str)
        result = self.cursor.fetchall()
        if result:
            for field in result:
                d = dict(zip(data, field))
                L.append(d)
        # print('数据库内容：', L)
        return L

    def delete_advice(self, **kwargs):
        advice_id = kwargs.get('advice_id')
        # print("advice_id:"+advice_id)
        # print('要删除的获取的ajax传的值', advice_id)
        sql_str = "delete from advice where advice_id=%s"
        result = self.cursor.execute(sql_str, (advice_id,))
        # print('result:', result)  # 1
        if result:
            com_result = self.conn.commit()
            # print(com_result)  # None
        else:
            com_result = self.conn.rollback()
        return com_result

    def find_comment(self):
        '''
        显示评论
        :return:
        '''
        L = []
        data = ['user_comment_id', 'user_comments', 'user_comment_time', 'house_id', 'user_id']
        sql_str = 'select user_comment_id, user_comments, user_comment_time, house_id , user_id ' \
                  'from user_comment;'

        self.cursor.execute(sql_str)
        result = self.cursor.fetchall()
        if result:
            for field in result:
                d = dict(zip(data, field))
                L.append(d)
        return L

    def delete_comment(self, **kwargs):
        '''
        删除评论
        :param kwargs:
        :return:
        '''
        user_comment_id = kwargs.get('user_comment_id')
        sql_str = "delete from user_comment where user_comment_id=%s"
        result = self.cursor.execute(sql_str, (user_comment_id,))
        # print('result:', result)  # 1
        if result:
            com_result = self.conn.commit()
            # print(com_result)  # None
        else:
            com_result = self.conn.rollback()
        return com_result
#=====================================================yhy


    def find_user_id(self, **kwargs):
        user_name = kwargs.get('user_name')  # 获取当前用户名

        # 如果用户名没有登录，提示请登录
        if user_name == '' or user_name is None:
            return 0
        # 根据user_id查找user_name
        sql_str = 'select user_id from user_info where user_name=%s'
        self.cursor.execute(sql_str, (user_name,))
        result = self.cursor.fetchall()
        # 获取user_id,是一个大元祖中套无数个小元组
        user_id = result[0][0]
        return user_id

    def insert_comment(self, **kwargs):
        # 自动获取一个uuid,将几个自动添加到数据库表
        user_comment_id = uuid.uuid1()
        user_id = kwargs.get('user_id')
        house_id = kwargs.get('house_id')
        user_comments = kwargs.get('user_comments')
        user_comment_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

        params = (str(user_comment_id), user_id, house_id, user_comments, user_comment_time)

        sql_str = 'insert into ' \
                  'user_comment(user_comment_id,user_id,house_id,user_comments,' \
                  'user_comment_time) values(%s,%s,%s,%s,%s)'
        result = self.cursor.execute(sql_str, tuple(params))
        return result

    def find_comments(self, user):
        '''数据库查询用户评论'''
        sql_str = "select renting_title, user_comment_id, user_comments, user_comment_time " \
                  "from renting_house,user_comment " \
                  "where house_id=renting_id " \
                  "and user_id=(" \
                  "select user_id " \
                  "from user_info " \
                  "where user_name=%s)"
        self.cursor.execute(sql_str, (user,))
        result = self.cursor.fetchall()
        print(result)
        return result

    def del_comments(self, **kwargs):
        '''用户删除评论'''
        user_comment_id = kwargs.get('user_comment_id')
        # 用字典方式获取user_comment_id

        sql_str = 'delete from user_comment where user_comment_id=%s'
        result = self.cursor.execute(sql_str, (user_comment_id,))

        return result
#================================================================hxx

    def insert_house(self, **kwargs):
        '''
        房源发布插入操作
        :param kwargs:
        :return:
        '''
        renting_id = uuid.uuid1()
        release_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        user_name = kwargs.get('user_name')
        user_id = kwargs.get('user_id')
        renting_title = kwargs.get('renting_title')
        city = kwargs.get('city')
        region = kwargs.get('region')
        door_model = kwargs.get('door_model')
        renting_price = kwargs.get('renting_price')
        renting_area = kwargs.get('renting_area')

        renting_floor = kwargs.get('renting_floor')
        renting_address = kwargs.get('renting_address')
        rent_type = kwargs.get('rent_type')
        renting_orientation = kwargs.get('renting_orientation')
        near_subway = kwargs.get('near_subway')
        house_type = kwargs.get('house_type')
        renting_fitment = kwargs.get('renting_fitment')
        renting_detail = kwargs.get('renting_detail')


        params = (
        str(renting_id),release_time,user_id,renting_title,city,region,
        door_model,renting_price,renting_area,renting_floor,renting_address,
        rent_type,renting_orientation,near_subway,house_type,renting_fitment,renting_detail)

        sql_str = "insert into renting_house(renting_id,release_time,land_lord_id,renting_title,city,region,"\
        "door_model,renting_price,renting_area,renting_floor,renting_address,"\
        "rent_type,renting_orientation,near_subway,house_type,renting_fitment,renting_detail)" \
                  "values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        result = self.cursor.execute(sql_str, tuple(params))
        # print('result',result)
        return result