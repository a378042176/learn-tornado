import os
from datetime import timedelta, datetime

import tornado.web
from tornado.options import define, options, parse_command_line

# 定义默认启动的端口port为80
define('port', default=8080, type=int)


class MainHandler(tornado.web.RequestHandler):
    # 必须继承RequestHandler
    def get(self):
        # 接收参数
        name = self.get_argument('name', '空')
        age = self.get_query_argument('age', '空')
        # 渲染响应给浏览器的数据
        self.write('姓名:%s ,年龄:%s ' % (name, age))

    def post(self):
        name = self.get_argument('name')
        age = self.get_body_argument('age')
        self.write('姓名:%s ,年龄:%s ' % (name, age))


class ResHandler(tornado.web.RequestHandler):
    def get(self):
        self.write('<h2>今天天气真好</h2>')
        # 可手动设置响应状态码
        self.set_status(200)
        # 设置cookie
        self.set_cookie('token', '123456', expires_days=1)
        out_time = datetime.now() + timedelta(days=1)
        self.set_cookie('token', '123456', expires=out_time)

        # 删除cookie中的token
        self.clear_cookie('token')

        # 跳转
        self.redirect('/')

    def post(self):
        self.write('一般负责提交新数据')

    def put(self):
        self.write('负责更新全部数据')

    def patch(self):
        self.write('负责更新部分数据')

    def delete(self):
        self.write('负责删除数据')


class DaysHandler(tornado.web.RequestHandler):
    def get(self, year, month, day):
        self.write('%s年%s月%s日' % (year, month, day))


class Days2Handler(tornado.web.RequestHandler):
    def get(self, year, month, day):
        self.write('%s年%s月%s日' % (year, month, day))


class EntryHandler(tornado.web.RequestHandler):
    def initialize(self):
        print('initialize')

    def prepare(self):
        print('prepare')

    def get(self):
        self.write('get')
        print('get')

    def post(self):
        self.write('get')
        print('post')

    def on_finish(self):
        print('finish')


class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('index.html')


def make_app():
    # handlers参数中定义路由匹配地址
    return tornado.web.Application(handlers=[
        (r'/', MainHandler),
        (r'/res', ResHandler),
        (r'/days/(\d{4})/(\d+)/(\d{2})/', DaysHandler),  # 带参路由
        (r'/days/(?P<year>\d{4})/(?P<month>\d+)/(?P<day>\d{2})/', Days2Handler),  # 带参路由
        (r'/entry/', EntryHandler),  # 切入点函数
        (r'/index/', IndexHandler)
    ],
        # template_path=os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
        template_path='./templates')


if __name__ == '__main__':
    # 解析启动命令,python xxx.py --port=端口号
    parse_command_line()
    # 启动
    app = make_app()
    # 监听端口
    app.listen(options.port)
    # 监听启动的IO实例
    tornado.ioloop.IOLoop.current().start()
