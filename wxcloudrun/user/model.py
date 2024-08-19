from datetime import datetime

from wxcloudrun import db


class User(db.Model):
    __tablename__ = 'users'  # 表名
    id = db.Column(db.String(36), primary_key=True, unique=True, nullable=False)  # 用户的全局唯一标识符，UUID格式
    wx_uid = db.Column(db.String(255), unique=True)  # 微信用户ID，唯一
    tb_id = db.Column(db.String(255), unique=True)  # 淘宝ID
    dy_id = db.Column(db.String(255), unique=True)  # 抖音ID
    phone_number = db.Column(db.String(36), unique=True)  # 手机号
    created_at = db.Column(db.Integer, nullable=False, default=int(datetime.now().timestamp()))  # 记录的创建时间（时间戳格式）
    updated_at = db.Column(db.Integer, nullable=False, default=int(datetime.now().timestamp()),
                           onupdate=int(datetime.now().timestamp()))  # 记录的更新时间（时间戳格式）
