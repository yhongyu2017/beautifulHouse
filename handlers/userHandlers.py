import json
import os
import time

from tornado.escape import json_encode

from utils.encrypt import md5
from tornado.web import RequestHandler

from utils.dbutil import Db_Util

from Session import session


class LoginHandler(session.SessionHandler, RequestHandler):
    '''
    登录
    '''
    def get(self, *args, **kwargs):
        if self.session_obj['is_login']:      #如果结果为True则跳转到主页面
            self.render(r'..\template\index.html')
        else:
            self.render(r'..\template\login.html')  # 跳转页面

    def post(self, *args, **kwargs):
        user_name = self.get_body_argument('userName')        #彭修改过
        password = self.get_body_argument('userPwd')#彭修改过

        # 查询数据库
        database_util = Db_Util()
        params = {'user_name': user_name,'user_pwd':md5(password)}       #彭修改过，查询数据库用户信息
                    #key的值要和数据库中的字段一样
        result = database_util.find_user(**params)
        if result:         #如果为True执行以下代码
            self.session_obj['is_login'] = 1  # 1登录0未登录
            self.session_obj['user'] = user_name
            # -------------------------------------------------------------------------------------------
            ret = {"result": 'ok',
                   'user': self.session_obj['user'],
                   'status': True,
                   'code': 200
                   }
        else:
            ret = {
                 "result": 'fail',
                 'status': True,
                'code': 200
                 }

        self.write(json_encode(ret))
        database_util.close_conn()


# 用户handler
class UserHandler(session.SessionHandler, RequestHandler):
    def get(self, *args, **kwargs):
        if self.session_obj['is_login']:
            username = self.session_obj['user']
            database_util = Db_Util()  # 实例化对象，操作数库
            result_info = database_util.find_user_info(username)  # 操作数据库的方法，返回结果
            if result_info:
                self.render(r'..\template\user_info.html', result_info=result_info)
            else:
                self.render(r'..\template\user_info.html', result_info='0')
        else:
            self.render(r'..\template\login.html')

    def post(self, *args, **kwargs):
        filename = self.session_obj['user']
        if not filename:
            self.redirect('/?logout')

        ret = {'result': 'ok'}
        request_type = self.get_body_argument('request_type', None)

        if request_type == 'ajax':
            # ajax请求
            data_type = self.get_body_argument('data_type', None)
            if data_type == 'file':
                upload_path = os.path.join(os.path.dirname(__file__), 'files')
                file_metas = self.request.files.get('file', None)
                if not file_metas:
                    ret['result'] = 'invalid'  # 没有文件

                for meta in file_metas:

                    # filename = meta['filename']
                    # file_name_tags = filename.split('.')
                    # if file_name_tags[:0:-1] == 'txt' or file_name_tags[:0:-1] == 'doc':
                    filename = str(time.time()) + session['yhm']
                    file_path = os.path.join(upload_path, filename)
                    with open(file_path, 'wb') as up:
                        up.write(meta['body'])

            self.write(json.dumps(ret))
        else:
            # 非ajax请求
            self.render(r'..\template\user_info.html')


# 注册页面
class RegHandler(RequestHandler):
    def get(self, *args, **kwargs):
        self.render(r'..\template\login.html')

    def post(self, *args, **kwargs):
        user_name = self.get_body_argument('userName')
        user_pwd = self.get_body_argument('userPwd')
        email = self.get_body_argument('email')
        database_util = Db_Util()
        params = {'user_name': user_name}
        users = database_util.find_user(**params)       # 在数据库中查找存在的用户名
        if users:

            ret = {"result": 'exits',
                      'status': True,
                      'code': 200
                      }

        else:
            params = {
                'user_name': user_name,
                'user_pwd': user_pwd,
                'user_email': email,
            }
            result = database_util.save_user(**params)
            if result == 1:
                database_util.conn.commit()           #提交到数据库执行
                ret = {"result": 'ok',
                      'status': True,
                      'code': 200
                      }
                # self.redirect('/index')
            else:
                database_util.conn.rollback()
                ret = {"result": 'fail',
                      'status': True,
                      'code': 200
                      }  # 注册失败
                # self.redirect(r'/reg?fail')
        database_util.close_conn()
        self.write(json_encode(ret))  # 向前台返回ajax数据


class LogoutHandler(session.SessionHandler, RequestHandler):
    def get(self, *args, **kwargs):
        self.session_obj['user'] = None
        self.session_obj['is_login'] = 0
        self.redirect(r'/index')

    def post(self, *args, **kwargs):
        self.session_obj['user'] = None
        self.session_obj['is_login'] = 0
        self.redirect(r'/index')
# --------------------------------------------------peng10/25


class UserHistoryHandler(session.SessionHandler, RequestHandler):
    def get(self, *args, **kwargs):
        if self.session_obj['is_login']:
            user = self.session_obj['user']
            db_util = Db_Util()
            result = db_util.find_history_info(user)
            db_util.conn.close()
            self.render(r'..\template\user_history.html', result=result, user=user)
        else:
            self.render(r'..\template\login.html')

    def post(self, *args, **kwargs):
        if self.session_obj['is_login']:
            user = self.session_obj['user']
            db_util = Db_Util()
            result = db_util.delete_history_info(user)
            print('数据库返回的结果：', result)
            if not result:
                ret = {
                    'result': 'ok',
                    'status': True,
                    'code': 200,
                    'user': user
                }
            else:
                ret = {
                    'result': 'fail',
                    'status': True,
                    'code': 200,
                    'user': user
                }
            db_util.close_conn()
            self.write(json_encode(ret))
        else:
            self.render(r'..\template\login.html')
# ----------------------------------------------------gzw


#个人信息管理
class UserManageHandler(session.SessionHandler, RequestHandler):
    def get(self, *args, **kwargs):
        if self.session_obj['is_login'] != 1:
            self.redirect(r'/login')
        else:
            user_name = self.session_obj['user']
            print(user_name)
            database_util = Db_Util()
            data = {'user_name': user_name}
            result = database_util.find_user_manage(**data)
            print('result:', result)  # 调试用的
            # 优化把返回None的值替换
            Name = ['user_gender', 'user_address', 'user_phone', 'user_head_img', 'user_land_lord']
            Persion = []
            for i in result[0][5:]:
                if i ==None:
                    i = ' '
                    Persion.append(i)
                else:
                    Persion.append(i)
            data = dict(zip(Name, Persion))
            # print(Persion)      #调试
            # data = {
            #     'user_gender': result[0][5],
            #     'user_address':result[0][6],
            #     'user_phone':result[0][7],
            #     'user_head_img':result[0][8],
            #     'user_land_lord':result[0][9]
            # }
            self.render(r'..\template\user_manage.html', userManage=data)

    def post(self,*args,**kwargs):
        ret = {"result": 'ok',
               'status': True,
               'code': 200
               }
        # if self.session_obj['is_login']:      #判断用户是否登录
        if self.session_obj['is_login']:
            user = self.session_obj['user']
            print(user,__class__,'253hang ')
            gender =self.get_body_argument('gender')
            zhiye = self.get_body_argument('zhiye')
            phone = self.get_body_argument('phone')
            barthday =self.get_body_argument('birthday')
            Quyu =self.get_body_argument('Quyu')
        # print(gender,zhiye,phone,barthday,Quyu)
            databases_util = Db_Util()
            params = {   'user_gender':gender,
                      'user_address':zhiye,
                      'user_phone':phone,
                      'user_head_img':barthday,
                      'is_land_lord':Quyu
                      }
            print(params,__class__,'267行')
            # -------------------------------------------------------------
            result = databases_util.update_user_info(user,**params)
            print(result)
            if result == 1:
                databases_util.conn.commit()           #提交到数据库执行
                ret = {"result": 'ok',
                      'status': True,
                      'code': 200
                      }
            else:
                databases_util.conn.rollback()          #回滚
                ret = {"result":'no',
                      'status': True,
                      'code': 200}

            databases_util.close_conn()           #关闭数据库连接
            self.write(json_encode(ret))           # 向前台返回ajax数据
        else:
            self.render(r'..\template\login.html')    #如果用户没有登陆则跳转到登陆注册页面


class UserCommentHandler(session.SessionHandler, RequestHandler):
    def get(self, *args, **kwargs):
        if self.session_obj['is_login']:  # 判断是否登录
            user = self.session_obj['user']  # 用户名
            db_util = Db_Util()  # 数据库
            result = db_util.find_comments(user)
            print(result)
            self.render(r'..\template\user_comment.html', result=result, user=user)
        else:
            self.render(r'..\template\login.html')
            # self.render(r'..\template\rent_info.html')

    def post(self, *args, **kwargs):
        if self.session_obj['is_login']:
            user = self.session_obj['user']  # 用户名
            db_util = Db_Util()  # 数据库
            user_comment_id = self.get_body_arguments('user_comment_id')
            data = {'user_comment_id': user_comment_id}
            result = db_util.del_comments(**data)
            # print('result:', result)  #  1  0
            if result:
                db_util.conn.commit()
                ret = {
                    'result': 'ok',
                    'status': True,
                    'code': 200,
                    'user': user
                }
            else:
                db_util.conn.rollback()
                ret = {
                    'result': 'fail',
                    'status': True,
                    'code': 200,
                    'user': user
                }
            db_util.conn.close()
            self.write(json_encode(ret))
        else:
            self.render(r'..\template\login.html')
#================================================================hxx

class UserReleaseHandler(session.SessionHandler, RequestHandler):
    def get(self, *args, **kwargs):
        if self.session_obj['user']:
            user_name = self.session_obj['user']
            database_util = Db_Util()
            params = {'user_name': user_name}

            data = database_util.find_user_manage(**params)
            user_manage = ['user_id', 'user_name', 'user_pwd', 'user_email', 'user_create_time',
                           'user_gender', 'user_address', 'user_phone', 'user_head_img', 'is_land_lord']
            userManage = dict(zip(user_manage, data[0]))
            self.render(r'..\template\release.html', userManage=userManage)
        else:
            self.redirect(r'/')

    def post(self, *args, **kwargs):
        ret = {
            "result": 'ok',
            'status': True,
            'code': 200
        }
        user_id = self.get_body_argument('user_id')
        user_name = self.get_body_argument('user_name')
        renting_title = self.get_body_argument('renting_title')
        region = self.get_body_argument('region')
        door_model = self.get_body_argument('door_model')
        renting_price = self.get_body_argument('renting_price')
        renting_area = self.get_body_argument('renting_area')

        city = self.get_body_argument('city')
        renting_floor = self.get_body_argument('renting_floor')
        renting_address = self.get_body_argument('renting_address')
        rent_type = self.get_body_argument('rent_type')
        renting_orientation = self.get_body_argument('renting_orientation')
        near_subway = self.get_body_argument('near_subway')
        house_type = self.get_body_argument('house_type')
        renting_fitment = self.get_body_argument('renting_fitment')
        renting_detail = self.get_body_argument('renting_detail')

        params = {
            'user_id': user_id,
            'user_name': user_name,
            'renting_title': renting_title,
            'region': region,
            'city': city,
            'renting_floor': renting_floor,
            'renting_address': renting_address,
            'rent_type': rent_type,
            'renting_orientation': renting_orientation,
            'near_subway': near_subway,
            'house_type': house_type,
            'renting_fitment': renting_fitment,
            'renting_detail': renting_detail,
            'door_model': door_model,
            'renting_price': renting_price,
            'renting_area': renting_area
        }

        database_util = Db_Util()
        result = database_util.insert_house(**params)
        print('返回的result', result)
        if result:
            database_util.conn.commit()
            ret = {
                "result": 'ok',
                'status': True,
                'code': 200
            }
        else:
            database_util.conn.rollback()
            ret = {
                "result": 'fail',
                'status': True,
                'code': 200
            }
        database_util.conn.close()
        self.write(json_encode(ret))

#====================================================================

class AdviceHandler(RequestHandler):
    def get(self, *args, **kwargs):
        self.render(r'..\template\advice.html')

    def post(self, *args, **kwargs):
        ret = {
            'result': 'ok',
            'status': True,
            'code': 200
        }
        advice_type = self.get_body_arguments('advice_type')
        advice_content = self.get_body_argument('advice_content')

        print('advice_type:', advice_type)
        print('advice_content:', advice_content)

        params = {'advice_type': advice_type, 'advice_content': advice_content}
        database_util = Db_Util()
        res = database_util.insert_advice(**params)
        # commit提交成功后返回的结果是None
        if res == 1:
            database_util.conn.commit()
            ret = {
                'result': 'ok',
                'status': True,
                'code': 200
            }
        else:
            database_util.conn.rollback()
            ret = {
                'result': 'fail',
                'status': True,
                'code': 200
            }
        database_util.conn.close()
        self.write(json_encode(ret))

#====================================================================zy
class UserPublishCommentHandler(session.SessionHandler, RequestHandler):
    # 点击发表留言，进入post请求，将用户id以字典的格式传到数据库处理函数
    def get(self, *args, **kwargs):
        pass

    def post(self, *args, **kwargs):
        ret = {
            'result': 'ok',
            'status': True,
            'code': 200
        }
        user = self.session_obj['user']
        database_util = Db_Util()
        param = {'user_name': user}
        user_id = database_util.find_user_id(**param)

        # 如果没有登录，返回nuid，前台提示‘请登录’，跳转到登录页面
        if user_id == 0:
            ret = {
                'result': 'nuid',
                'status': True,
                'code': 200
            }
        else:
            # 获取到house_id,user_comments
            house_id = self.get_body_argument('renting_id')
            user_comments = self.get_body_arguments('comment')

            params = {
                'user_id': user_id,
                'house_id': house_id,
                'user_comments': user_comments
            }
            result = database_util.insert_comment(**params)

            print('插入数据库返回的结果：', result)  # 0  1

            if result == 1:
                database_util.conn.commit()
                ret = {
                    'result': 'ok',
                    'status': True,
                    'code': 200
                }
            else:
                database_util.conn.rollback()
                ret = {
                    'result': 'fail',
                    'status': True,
                    'code': 200
                }
        database_util.conn.close()
        self.write(json_encode(ret))  # 展示到前台

# =============================================================hxx