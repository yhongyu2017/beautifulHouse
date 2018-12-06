from tornado.web import RequestHandler


# 未能被路由匹配的请求处理视图
class BaseHandler(RequestHandler):
    def get(self, *args, **kwargs):
        self.write_error(404)

    def write_error(self, status_code, **kwargs):
        if status_code == 404:
            ret = {'result': '404'}
            self.render(r'..\template\error_pages\404.html')
        elif status_code == 500:
            ret = {'result': '500'}
            self.render(r'..\template\error_pages\500.html')
        else:
            self.write(str(status_code))
