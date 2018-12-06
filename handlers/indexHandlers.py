from tornado.escape import json_encode
from tornado.web import RequestHandler

from utils.dbutil import Db_Util
from Session import session


# 访问首页与点击登录注册处理视图
class IndexHandler(session.SessionHandler, RequestHandler):
    def get(self):
        if self.session_obj['is_login']:     #判断用户是否登录
            user_name = self.session_obj['user']
            self.render(r'..\template\index.html', userName=user_name)  # 跳转到主页
        else:
            self.render(r'..\template\index.html')  # 跳转到主页

    def post(self):
        ret = {
            'un': str(self.session_obj['user']),  # 用户名
            'is_login': self.session_obj['is_login'],   #判断是否登陆如果为True表示用户已经登陆否则失败
            'result': 'ok',
            'status': True,
            'code': 200
        }
        self.write(json_encode(ret))
#================================================================ pyr


# 访问关于我们页面处理视图
class AboutUsHandler(RequestHandler):
    def get(self):
        self.render(r'..\template\about_us.html')


# 访问第三方租房页面处理视图
class ThirdRentHandler(session.SessionHandler, RequestHandler):
    def get(self, *args, **kwargs):
        params = {
            'ajk_renting_region': '朝阳',
            'ajk_renting_price': '2000-3000',
            'ajk_renting_door_model': '3室1厅',
            'ajk_renting_rent_type': '合租'
        }
        db_util = Db_Util()
        result = db_util.find_third_rent_info(**params)
        self.render(r'..\template\third_rent.html', result=result)


# 访问租房页面处理视图
class RentHandler(session.SessionHandler, RequestHandler):
    def get(self, *args, **kwargs):
        params = {
            'region': '朝阳',
            'renting_price': '1500以下',
            'door_model': '1室1厅',
            'rent_type': '整租'
        }
        db_util = Db_Util()
        result = db_util.find_rent_info(**params)
        self.render(r'..\template\rent.html', result=result)
#================================================================ gzw
