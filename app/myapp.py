import os
from tornado.web import Application
from utils import dbutil


class MyApplication(Application):
    def __init__(self, handlers, modules, template_path, static_path):
        settings = {
            'cookie_secret': 'vd5vd94v4f9dfdf481v2s51v21ds51v215f1',
            # 'static_path': os.path.join(os.path.dirname(__file__), 'mystatics'),
            'login_url': '/',
            'static_path': static_path,
            'template_path': template_path,
            # 'static_url_prefix': '',
        }
        super().__init__(handlers=handlers, ui_modules=modules, **settings)
        self.db = dbutil.Db_Util()
