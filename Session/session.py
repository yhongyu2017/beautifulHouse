import hashlib
import time
from Session import session_config


class SessionHandler:
    def initialize(self):
        self.session_obj = SessionFacotory.get_session_obj(self)


class SessionFacotory:
    @staticmethod
    def get_session_obj(handler):
        if session_config.session_type == 'redis':
            return RedisSession(handler)
        elif session_config.session_type == 'memcache':
            return RedisSession(handler)
        else:
            return MemorySession(handler)


def md5():
    m = hashlib.md5()
    m.update(bytes(str(time.time()),encoding='utf-8'))
    return m.hexdigest()

class MemorySession:
    container = {

    }
    # self.r_str当前用户的随机字符串
    def __init__(self, handler):

        random_str = handler.get_cookie('___session_id___')
        if random_str:
            # 客户端有cookie
            # 合法cookie
            if random_str in MemorySession.container:
                self.r_str = random_str

            else:
                # 非法cookie
                random_str = md5()
                MemorySession.container[random_str] = {}
                self.r_str = random_str
        else:
            # 客户端无cookie，表示是新用户的到来
            random_str = md5()
            MemorySession.container[random_str] = {}
            self.r_str = random_str

        handler.set_cookie('___session_id___', random_str, expires=time.time() + 200)

    def __setitem__(self, key, value):
        MemorySession.container[self.r_str][key] = value

    def __getitem__(self, item):
        return MemorySession.container[self.r_str].get(item,None)

    def __delitem__(self, key):
        del MemorySession.container[self.r_str][key]


class RedisSession:
    def __init__(self):
        pass
    def __getitem__(self, item):
        pass

    def __setitem__(self, key, value):
        pass

    def __delitem__(self, key):
        pass