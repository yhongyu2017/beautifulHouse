from tornado.escape import json_encode
from tornado.web import RequestHandler

from utils.dbutil import Db_Util
from Session import session


# 首页点击搜索处理视图
class UserClickHandler(session.SessionHandler, RequestHandler):
    def get(self, *args, **kwargs):
        region = self.get_argument('region')
        price = self.get_argument('price')
        door_model = self.get_argument('door_model')
        rent_type = self.get_argument('rent_type')
        self.render(r'..\template\rent.html', params=locals())


# 租房页面点击搜索处理视图
class UserFindHandler(session.SessionHandler, RequestHandler):
    def get(self, *args, **kwargs):
        region = self.get_argument('region')
        renting_price = self.get_argument('renting_price')
        door_model = self.get_argument('door_model')
        rent_type = self.get_argument('rent_type')
        params = {
            'region': region,
            'renting_price': renting_price,
            'door_model': door_model,
            'rent_type': rent_type
        }
        db_util = Db_Util()
        result = db_util.find_rent_info(**params)
        ret = {
            'info': result,
            'result': 'ok',
            'status': True,
            'code': 200
        }
        self.write(json_encode(ret))


# 第三方租房页面点搜索处理视图
class UserFindThirdHandler(RequestHandler):
    def get(self, *args, **kwargs):
        ajk_renting_region = self.get_argument('ajk_renting_region')
        ajk_renting_price = self.get_argument('ajk_renting_price')
        ajk_renting_door_model = self.get_argument('ajk_renting_door_model')
        ajk_renting_rent_type = self.get_argument('ajk_renting_rent_type')
        params = {
            'ajk_renting_region': ajk_renting_region,
            'ajk_renting_price': ajk_renting_price,
            'ajk_renting_door_model': ajk_renting_door_model,
            'ajk_renting_rent_type': ajk_renting_rent_type
        }
        db_util = Db_Util()
        result = db_util.find_third_rent_info(**params)
        ret = {
            'info': result,
            'result': 'ok',
            'status': True,
            'code': 200
        }
        self.write(json_encode(ret))
#=============================================================== gzw
