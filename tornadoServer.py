import os

from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from tornado.web import url

from handlers.baseHandlers import BaseHandler
from myConfigs import myConfig
from app.myapp import MyApplication
from handlers.userHandlers import LoginHandler, UserHandler, UserHistoryHandler, \
    UserManageHandler, UserCommentHandler, UserReleaseHandler, AdviceHandler, RegHandler, UserPublishCommentHandler, \
    LogoutHandler
from handlers.indexHandlers import IndexHandler, AboutUsHandler, ThirdRentHandler, \
    RentHandler
from handlers.userGetInfoHandler import UserClickHandler, UserFindHandler, UserFindThirdHandler
from handlers.houseInfoHandler import HouseInfoHandler
from handlers.adminHandler import AdminLoginHandler, AdminLogoutHandler, AdminIndexHandler, \
    AdminUserHandler, AdminHouseListHandler, AdminHouseDeleteHandler, AdminHouseSearchHandler, \
    AdminHouseUpdateHandler, AdminListHandler, AdminAddHandler, AdminAdviceHandler, AdminIsBlockHandler, \
    AdminHouseEditHandler, AdminCommentHandler

current_path = os.path.dirname(__file__)
app = MyApplication(handlers=[
    url('/', IndexHandler, {}),  # 主页
    url('/index', IndexHandler, {}),  # 主页
    url('/login', LoginHandler, {}),  # 登陆页面
    url('/logout', LogoutHandler, {}),
    url('/reg', RegHandler, {}),  # 注册页面
    url('/about_us', AboutUsHandler, {}),  # 关于我们页面
    url('/third_rent', ThirdRentHandler, {}),  # 第三方租房页面
    url('/rent', RentHandler, {}),  # 租房页面
    url('/rent_info', HouseInfoHandler, {}),  # 租房详情页面
    url('/advice', AdviceHandler, {}),  # 投诉建议页面
    url(r'/user', UserHandler, {}),  # 用户首页
    url(r'/release', UserReleaseHandler, {}),  # 发布房源页面
    url(r'/user/history', UserHistoryHandler, {}),  # 用户历史记录页面
    url(r'/user/manage', UserManageHandler, {}),  # 个人管理页面
    url(r'/user/comment', UserCommentHandler, {}),  # 用户评论页面
    url(r'/comment', UserPublishCommentHandler, {}),  # 评论处理
    url(r'/get_info', UserClickHandler, {}),  # 主页用户点击搜索事件
    url(r'/find', UserFindHandler, {}),  # rent页面用户点击搜索
    url(r'/find_third', UserFindThirdHandler),  # 第三方页面用户点击搜索

# --------后台管理模块 start
    # 登陆后跳转到主页，对主页的处理
    url(r'/admin/index', AdminIndexHandler, {}),
    # 登陆处理
    url(r'/admin/login', AdminLoginHandler, {},),
    url(r'/admin', AdminLoginHandler, {}),
    url(r'/admin/', AdminLoginHandler, {}),
    # 退出登录处理
    url(r'/admin/logout', AdminLogoutHandler, {},),
    # 暂时没用到
    url(r'/admin/user', AdminUserHandler, {}),

    # 管理员管理处理，包括对管理员账号的添加，以及修改密码
    url(r'/admin/adminList', AdminListHandler, {}),
    # 超级管理员添加普通管理员信息
    url(r'/admin/adminAdd', AdminAddHandler, {}),
    # 超级管理员冻结普通管理员的账号
    url(r'/admin/adminIsBlock', AdminIsBlockHandler, {}),

    # 房源信息列表展示处理
    url(r'/admin/houseList', AdminHouseListHandler, {}),
    # 删除房源信息处理  其中主页中的不通过请求也是用的这个处理
    url(r'/admin/houseDelete', AdminHouseDeleteHandler),
    # 搜索房源信息  根据title模糊查询
    url(r'/admin/houseSearch', AdminHouseSearchHandler, {}),
    # 主页中通过请求的处理
    url(r'/admin/houseUpdate', AdminHouseUpdateHandler, {}),
    # 房源信息的编辑请求的处理
    url(r'/admin/houseEdit', AdminHouseEditHandler, {}),

    #---------------------杨宏宇
    # 建议请求的 处理
    url(r'/admin/adviceList', AdminAdviceHandler, {}),
    url(r'/admin/commentList', AdminCommentHandler, {}),

    # --------后台管理模块 end

    url(r'/.*', BaseHandler, {}),  # 未知url页面处理
    ],
    modules={},
    template_path=os.path.join(current_path, 'template'),
    static_path=os.path.join(current_path, 'static'),
    )
server = HTTPServer(app)
server.listen(myConfig.config['port'])
IOLoop.current().start()
