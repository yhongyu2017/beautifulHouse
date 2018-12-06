import hashlib
import time
container = {}


class SessionClass:
    def __init__(self, handler, gqshijian):
        self.handler = handler
        self.random_str = None
        self.gqshijian = gqshijian

    def __genarate_random_str(self):
        obj = hashlib.md5()
        obj.update(bytes(str(time.time()), encoding='utf-8'))
        random_str = obj.hexdigest()
        self.random_str = random_str
        return random_str

    def __setitem__(self, key, value):
        if not self.random_str:
            random_str = self.handler.get_cookie('xr_cookie')
            if not random_str:
                self.__genarate_random_str()
                container[random_str] = {}
            else:
                if random_str in container.keys():
                    pass
                else:
                    random_str = self.__genarate_random_str()
                    self.random_str = random_str
                    container[self.random_str] = {}
                    container[self.random_str][key] = value
        self.handler.set_cookie('xr_cookie', self.random_str, expires_days=self.gqshijian)

    def __getitem__(self, key):
        random_str = self.handler.get_cookie('xr_cookie')
        if not random_str:
            return None
        user_info_dict = container.get(random_str, None)
        if not user_info_dict:
            return None
        value = user_info_dict.get(key, None)
        print(key, '999')
        return value
