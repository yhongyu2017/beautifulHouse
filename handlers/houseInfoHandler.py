from tornado.web import RequestHandler

from Session import session
from utils.dbutil import Db_Util


class HouseInfoHandler(session.SessionHandler,RequestHandler):
    def get(self, *args, **kwargs):
        house_id = self.get_argument('id', '')
        if house_id:
            database_util = Db_Util()
            result = database_util.find_rent_house(house_id)
            data = ['renting_id', 'land_lord_id', 'city', 'region',
                    'renting_title', 'renting_pictrue', 'door_model',
                    'renting_area', 'renting_floor','renting_address',
                    'rent_type','renting_orientation','near_subway',
                    'has_elevator','renting_price','house_type',
                    'renting_fitment','release_time','renting_detail',
                    'is_check','user_name','user_phone']

            dic = dict(zip(data, result[0]))
            if self.session_obj['is_login']:
                username = self.session_obj['user']
                database_util.insert_history_info(username, house_id)
                if result:
                    database_util.conn.commit()
                else:
                    database_util.conn.rollback()
            self.render('../template/rent_info.html', result=dic)
        else:
            self.render('../template/rent.html')
