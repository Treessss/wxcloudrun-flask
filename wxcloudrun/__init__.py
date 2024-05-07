from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import pymysql
import config

# 因MySQLDB不支持Python3，使用pymysql扩展库代替MySQLDB库
pymysql.install_as_MySQLdb()

# 初始化web应用
app = Flask(__name__, instance_relative_config=True)
app.config['DEBUG'] = config.DEBUG

# 设定数据库链接
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://{}:{}@{}/huinantian'.format(config.username, config.password,
                                                                             config.db_address)

# 初始化DB操作对象
db = SQLAlchemy(app)

# 加载控制器
from .warehouse import warehouse as warehouse_blueprint
from .points import points as points_blueprint
from .cards import cards as cards_blueprint
from .user import user as user_blueprint

# 加载配置
app.config.from_object('config')
app.register_blueprint(cards_blueprint, url_prefix='/api/cards')
app.register_blueprint(warehouse_blueprint, url_prefix='/api/warehouse')
app.register_blueprint(points_blueprint, url_prefix='/api/points')
app.register_blueprint(user_blueprint, url_prefix='/api/user')
