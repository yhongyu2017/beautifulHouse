from tornado.options import define, parse_config_file

define('port', type=int, default=8088, multiple=False, help='setting port')
define('db', type=str, default=[], multiple=True, help='database config')
define('files', type=str, default=r'/files', multiple=False, help='user files')
parse_config_file('config')

config = {
    'port': 9000
}