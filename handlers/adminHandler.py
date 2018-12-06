#-*- coding:utf-8 -*-

import json

from utils.dbutil import Db_Util
from utils.session_manager import SessionClass
from tornado.web import RequestHandler
from tornado.escape import json_encode

from Session import session, session_config


class AdminIndexHandler(session.SessionHandler, RequestHandler):
    '''
    主页handler
    :param RequestHandler:
    :return:
    :author: Yanfuzi
    '''
    def get(self, *args, **kwargs):
        # 已经登陆的状态
        if self.session_obj['admin_is_login'] == 1:
            admin_name = self.session_obj['adminName']
            # self.redirect('/admin/user')
            # self.render('../template/admin_pages/index.html', adminName=admin_name)
            # 登录跳转的url
            database_util = Db_Util()
            # check = (0,)
            params = {'is_check': 0}
            result = database_util.find_house(**params)
            if result:
                # renting_id = result['renting_id']
                # user_name = result['user_name']
                # user_email = result['user_email']
                # release_time = result['release_time']
                # admin_name = self.session_obj['adminName']
                self.render(r'../template/admin_pages/index.html', resultViews=result)
            else:
                self.render(r'../template/admin_pages/index.html', resultViews='0')
        # 还没有登陆
        else:
            self.redirect(r'/admin/login')


    def post(self, *args, **kwargs):
        ret = {
            'admin_name': self.session_obj['admin_name'],
            'admin_is_login': self.session_obj['admin_is_login'],
            'result': 'ok',
            'status': True,
            'code': 200
        }
        self.write(json_encode(ret))

class AdminUserHandler(RequestHandler):
    '''
    处理主页管理
    :param RequestHandler:
    :return:
    :author: Yanfuzi
    '''
    def get(self, *args, **kwargs):
        session = SessionClass(self, 1)
        if session['zt']:
            self.render(r'../template/admin_pages/adviceList.html')
        else:
            self.render('../template/admin_pages/index.html')

    def post(self, *args, **kwargs):
        pass

class AdminLoginHandler(session.SessionHandler, RequestHandler):
    def get(self, *args, **kwargs):
        self.render(r'..\template\admin_pages\login.html')

    def post(self, *args, **kwargs):
        ret = {
            'result': 'ok',
            'status': True,
            'code': 200
        }
        # 获取ajax传递的数据
        admin_name = self.get_body_argument('adminName')
        admin_pwd = self.get_body_argument('adminPwd')
        # 判断是否是超级管理员，超级管理员的代号为 1 ，普通管理员的代号为 0
        if admin_name == 'admin':
            is_super_num = 1
        else:
            is_super_num = 0
        # 查询数据库
        database_util = Db_Util()
        params = {'admin_name': admin_name, 'admin_pwd': admin_pwd, 'is_super': is_super_num}
        result = database_util.find_admin(**params)
        # 处理结果
        if result:
            if result[0][-1] == 1:
                ret = {
                    'result': 'block',
                    'status': True,
                    'code': 200,
                }
            else:
                # print('登陆验证：',result)
                self.session_obj['admin_is_login'] = 1 # 1 表示已登录，其他表示未登录
                self.session_obj['admin_name'] = admin_name  # 记录登录的用户名
                ret = {
                    'result': 'ok',
                    'admin_name': self.session_obj['admin_name'],
                    'status': True,
                    'code': 200,
                    }
        else:
            ret = {
                'result': 'fail',
                'status': True,
                'code': 200
                }  # 登陆失败
            # self.redirect(r'/reg?fail')
        database_util.close_conn()
        self.write(json_encode(ret))  # 向前台返回ajax数据

class AdminLogoutHandler(session.SessionHandler, RequestHandler):
    '''
    退出登陆处理
    :param RequestHandler:
    :return:
    :author: Yanfuzi
    :notice:  暂时没用到
    '''
    def get(self, *args, **kwargs):
        self.session_obj['admin_name'] = None
        self.session_obj['admin_is_login'] = 0

        self.redirect(r'/admin/login')
        # self.render('../template/admin_pages/login.html')
        # self.redirect(r'/?logouted')

    def post(self, *args, **kwargs):
        self.session_obj['admin_name'] = None
        self.session_obj['admin_is_login'] = 0

        self.redirect(r'/admin/login')
        # self.render('../template/admin_pages/login.html')
        # self.redirect(/r'/?logouted')

class AdminHouseListHandler(session.SessionHandler, RequestHandler):
    '''
    房源信息管理 处理
    :param RequestHandler:
    :return:
    :author: Yanfuzi
    '''
    def get(self, *args, **kwargs):
        '''
        跳转到房源管理列表界面，显示的是已经发布的房源信息
        直接跳转页面属于默认的get请求方式，需要展示相关的信息，
            如：房源编号，房源标题，发布者信息，发布时间等，管理员可以对房源信息
            进行修改和删除，但是不可以更改关于发布人的信息及发布时间
        :param args:
        :param kwargs:
        :return:
        '''
        if self.session_obj['admin_is_login']:
            database_util = Db_Util()  # 实例化对象，操作数库
            params = {'is_check': 1}  # 已经发布的字段值为 1
            result = database_util.find_house(**params)  # 操作数据库的方法，返回结果
            if result:
                # 如果返回结果，则跳转到房源信息展示列表，并把返回结果传过去
                self.render(r'../template/admin_pages/houseList.html', result=result)
            else:
                self.render(r'../template/admin_pages/houseList.html', result='0')
        else:
            self.redirect(r'/admin/login')


class AdminHouseDeleteHandler(session.SessionHandler, RequestHandler):
    '''
    房源管理后台删除处理
    '''
    def get(self, *args, **kwargs):
        # get请求直接返回到houseList.html页面
        if self.session_obj['admin_is_login'] == 0:
            self.redirect(r'/admin/login')
        else:
            self.redirect(r'/admin/houseList')

    def post(self, *args, **kwargs):
        '''
        ajax请求，将要删除的id穿过来，进行处理，再返回给客户端json格式的数据
        :param args:
        :param kwargs:
        :return: json
        :author: Yanfuzi
        '''
        ret = {
            'result': 'ok',
            'status': True,
            'code': 200
        }
        # 接收的是一个列表
        renting_id = self.get_body_argument('renting_id')
        # print(renting_id)
        database_util = Db_Util()
        param = {'renting_id': renting_id}
        result = database_util.delete_house(**param)
        # 返回结果  1 （None） 或  0
        if result == 1:
            database_util.conn.commit()
            ret = {
                'result': 'ok',
                'status': True,
                'code': 200,
                'msg': '删除成功'
            }
        else:
            database_util.conn.rollback()
            ret = {
                'result': 'fail',
                'status': True,
                'code': 200,
                'msg': '删除失败'
            }
        database_util.close_conn()
        self.write(json_encode(ret))

class AdminHouseSearchHandler(session.SessionHandler, RequestHandler):
    '''
    处理后台房源列表中的搜索功能
    '''
    def get(self, *args, **kwargs):
        if self.session_obj['admin_is_login'] == 0:
            self.redirect(r'/admin/login')
        else:
            self.redirect(r'/admin/houseList')

    def post(self, *args, **kwargs):
        '''
        接收搜索内容，调用搜索函数，将函数返回的结果进行处理，返回json给前台页面
        :param args:
        :param kwargs:
        :return:
        :author: Yanfuzi
        '''
        ret = {
            'result': 'ok',
            'status': True,
            'code': 200
        }
        searchInput = self.get_body_argument('searchInput')
        database_util = Db_Util()
        param = {'searchInput': searchInput}
        searchResult = database_util.searchHouse(**param)
        if searchResult:
            ret = {
                'result': 'ok',
                'status': True,
                'code': 200,
                'searchResult': searchResult
            }
        else:
            ret = {
                'result': 'fail',
                'status': True,
                'code': 200
            }
        database_util.close_conn()
        self.write(json_encode(ret))

class AdminHouseUpdateHandler(session.SessionHandler, RequestHandler):
    '''
    后台管理系统主页的允许通过的处理
    '''
    def get(self):
        if self.session_obj['admin_is_login'] == 0:
            self.redirect(r'/admin/login')
        else:
            self.redirect(r'/admin/index')

    def post(self, *args, **kwargs):
        ret = {
            'result': 'ok',
            'status': True,
            'code': 200
        }
        renting_id = self.get_body_argument('renting_id')
        # print('ajsx传递过来的值', renting_id)

        # 要修改的字段，值
        param1 = {'is_check': '1'}

        # 作为条件的字段，值
        param2 = {'renting_id': renting_id}

        params = {'param1': param1, 'param2': param2}

        database_util = Db_Util()
        result = database_util.update_house(**params)
        # print('admin:', result)
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
        database_util.close_conn()
        self.write(json_encode(ret))

class AdminListHandler(session.SessionHandler, RequestHandler):
    '''
    对管理员账号的管理
    '''
    def get(self, *args, **kwargs):
        '''
        显示管理员账号
        :param args:
        :param kwargs:
        :return:
        :author: Yanfuzi
        '''
        if self.session_obj['admin_name'] == 'admin':
            L = []
            database_util = Db_Util()
            params = {'is_super': 0}
            result = database_util.find_admin(**params)
            data = ['adminId', 'adminName', 'adminPwd', 'addTime', 'isSuper', 'isBlock']
            for tup in result:
                d = dict(zip(data, tup))
                L.append(d)
            # print(L)
            self.render(r'../template/admin_pages/adminList.html', result=L)
        else:
            self.render(r'../template/error_pages/404.html')
    def post(self, *args, **kwargs):
        '''
        对管理员账号的操作请求处理
        :param args:
        :param kwargs:
        :return: ret
        :author: Yanfuzi
        '''
        self.render(r'../template/admin_pages/adminList.html')

class AdminAddHandler(session.SessionHandler, RequestHandler):
    '''
    添加管理员handler
    '''
    def get(self, *args, **kwargs):
        if self.session_obj['admin_name'] == 'admin':
            self.render(r'../template/admin_pages/adminAdd.html')
        else:
            self.render(r'../template/error_pages/404.html')

    def post(self, *args, **kwargs):
        adminName = self.get_body_argument('adminName')
        adminPwd = self.get_body_argument('adminPwd')
        database_util = Db_Util()
        params = {'admin_name': adminName}
        result = database_util.find_admin(**params)
        # 如果查到说明已经存在，将不能添加管理员信息
        if result:
            ret = {
                'result': 'exist',
                'status': True,
                'code': 200
            }
        # 执行插入数据库
        else:
            params = {
                'adminName': adminName,
                'adminPwd': adminPwd
            }
            result = database_util.save_admin(**params)
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
        database_util.close_conn()
        self.write(json_encode(ret))


class AdminIsBlockHandler(session.SessionHandler, RequestHandler):
    '''
    账号冻结和解除冻结
    '''
    def get(self, *args, **kwargs):
        # 如果超级管理员已经登陆，返回到adminList.html页面
        if self.session_obj['admin_name'] != 'admin':
            self.render(r'../template/error_pages/404.html')
        # 没有登陆或不是超级管理员，返回404.html页面
        else:
            self.redirect(r'/admin/adminList')

    def post(self, *args, **kwargs):
        '''
        处理请求，如果获取的是 1 ，则修改数据库对应的字段为 0 ，否则改为 1
        :param args:
        :param kwargs: is_block, admin_id
        :return: json 数据
        :author: Yanfuzi
        '''
        ret = {
            'result': 'ok',
            'status': True,
            'code': 200
        }
        isBlock = self.get_body_argument('is_block')
        adminId = self.get_body_argument('admin_id')
        if isBlock == '0':
            isBlock = '1'
        else:
            isBlock = '0'
        database_util = Db_Util()
        result = database_util.update_admin_block(is_block=isBlock, admin_id=adminId)
        # result is 1, commit to db
        if result:
            database_util.conn.commit()
            ret = {
                'result': 'ok',
                'status': True,
                'code': 200
            }
        # result is 0(result not is 1) ,rollback
        else:
            database_util.conn.rollback()
            ret = {
                'result': 'fail',
                'status': True,
                'code': 200
            }

        database_util.conn.close()
        self.write(json_encode(ret))


class adminHouseCheck(session.SessionHandler, RequestHandler):
    def get(self, *args, **kwargs):
        if self.session_obj['admin_is_login'] == 1:
            renting_id = self.get_arguments('id')
            database_util = Db_Util()
            data = {'renting_id': renting_id}
            result = database_util.find_house(**data)
            # print('Manage:', result)  # 列表中嵌套着字典
            self.render(r'..\template\admin_pages\houseApplyCheck.html', houseManage = result[0])
        else:
            self.render(r'..\template\error_pages\404.html')

    def post(self, *args, **kwargs):
        pass


class AdminHouseEditHandler(session.SessionHandler, RequestHandler):
    '''
    在房源管理列表中，点击编辑，对编辑的处理，首先跳转到编辑的页面，点击保存，更新数据库
    '''
    def get(self, *args, **kwargs):
        '''
        跳转到编辑的页面的处理
        :param args:
        :param kwargs:  房源id
        :return: 该id对应的房源信息
        :author: Yanfuzi
        '''
        # 如果没有登陆
        if self.session_obj['admin_is_login'] == 0:
            self.redirect(r'/admin/login')
        else:
            # 如果想要直接跳转到编辑界面，返回到houseList.html
            # if kwargs == {}:
            #     self.redirect(r'/admin/houseEdit')
            # else:

            # 获取要编辑的房源id
            id = self.get_argument('id')
            # 根据id获取数据库的内容，将对应的房源信息发送给前台
            database_util = Db_Util()
            params = {'renting_id': id}
            result = database_util.find_house(**params)
            if result:
                renting_id = result[0]['renting_id']
                renting_title = result[0]['renting_title']
                region = result[0]['region']
                user_name = result[0]['user_name']
                user_email = result[0]['user_email']
                release_time = result[0]['release_time']
                renting_detail = result[0]['renting_detail']

                self.render(r'../template/admin_pages/houseEdit.html', result = locals())
            else:
                print('没有查到任何信息 ')
    def post(self, *args, **kwargs):
        '''
        点击保存后的处理
        :param args: none
        :param kwargs: 传过来的data字典
        :return:json格式的数据
        :author: Yanfuzi
        '''
        ret = {
            'result': 'ok',
            'status': True,
            'code': 200
        }

        renting_id = self.get_body_argument('renting_id')
        renting_title = self.get_body_argument('renting_title')
        region = self.get_argument('region')
        print('region', region)
        renting_detail = self.get_body_argument('renting_detail')

        # 要修改的字段，值
        param1 = {
             'renting_title': renting_title,
             'region': region,
             'renting_detail': renting_detail
        }
        # 当作条件
        param2 = {'renting_id': renting_id}


        params = {'param1': param1, 'param2': param2}

        database_util = Db_Util()
        result = database_util.update_house(**params)
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
        self.write(json_encode(ret))


class AdminAdviceHandler(RequestHandler):
    def get(self, *args, **kwargs):
        database_util = Db_Util()  # 实例化对象，操作数库
        result_advice = database_util.find_advice()  # 操作数据库的方法，返回结果
        # print("result_advice:"+result_advice)
        if result_advice:
            # 如果返回结果，则跳转到房源信息展示列表，并把返回结果传过去
            self.render(r'../template/admin_pages/adviceList.html', result_advice=result_advice)
        else:
            # 还没写完
            self.render(r'../template/admin_pages/adviceList.html', result_advice='0')

    def post(self, *args, **kwargs):
        ret = {
            'result': 'ok',
            'status': True,
            'code': 200
        }
        # 接收的是一个列表
        advice_id = self.get_body_argument('advice_id')
        print("advice_id:"+advice_id)
        database_util = Db_Util()
        param = {'advice_id': advice_id}
        result = database_util.delete_advice(**param)
        # 删除成功返回None
        if result != 0:
            ret = {
                'result': 'ok',
                'status': True,
                'code': 200,
                'msg': '删除成功'
            }
        else:
            ret = {
                'result': 'fail',
                'status': True,
                'code': 200,
                'msg': '删除失败'
            }
        database_util.close_conn()
        self.write(json_encode(ret))


# yhy修改过
class AdminCommentHandler(RequestHandler):
    def get(self, *args, **kwargs):
        database_util = Db_Util()  # 实例化对象，操作数库
        result_comment = database_util.find_comment()  # 操作数据库的方法，返回结果
        if result_comment:
            # 如果返回结果，则跳转到房源信息展示列表，并把返回结果传过去
            self.render(r'../template/admin_pages/commentList.html', result_comment=result_comment)
        else:
            # 还没写完
            self.render(r'../template/admin_pages/commentList.html', result_comment='0')

    def post(self, *args, **kwargs):
        ret = {
            'result': 'ok',
            'status': True,
            'code': 200
        }
        # 接收的是一个列表
        user_comment_id = self.get_body_argument('user_comment_id')
        database_util = Db_Util()
        param = {'user_comment_id': user_comment_id}
        result = database_util.delete_comment(**param)
        # 删除成功返回None
        if result != 0:
            ret = {
                'result': 'ok',
                'status': True,
                'code': 200,
                'msg': '删除成功'
            }
        else:
            ret = {
                'result': 'fail',
                'status': True,
                'code': 200,
                'msg': '删除失败'
            }
        database_util.close_conn()
        self.write(json_encode(ret))