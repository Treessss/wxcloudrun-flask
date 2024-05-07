from datetime import datetime

from wxcloudrun import db


class UserPoint(db.Model):
    __tablename__ = 'user_points'  # 表名
    id = db.Column(db.String(36), primary_key=True, unique=True, nullable=False)  # 积分记录的全局唯一标识符，UUID格式
    user_id = db.Column(db.String(255))  # 用户ID，外键
    points = db.Column(db.Integer)  # 积分数
    created_at = db.Column(db.Integer, nullable=False, default=int(datetime.now().timestamp()))  # 记录的创建时间（时间戳格式）
    updated_at = db.Column(db.Integer, nullable=False, default=int(datetime.now().timestamp()),
                           onupdate=int(datetime.now().timestamp()))  # 记录的更新时间（时间戳格式）


class OrderPoint(db.Model):
    __tablename__ = 'order_points'  # 表名
    id = db.Column(db.String(36), primary_key=True, unique=True, nullable=False)  # 订单积分记录的全局唯一标识符，UUID格式
    order_id = db.Column(db.String(255))  # 订单号
    points = db.Column(db.Integer)  # 积分数量
    is_used = db.Column(db.Integer, default=0)  # 是否使用 0：未使用  1：使用
    created_at = db.Column(db.Integer, nullable=False, default=int(datetime.now().timestamp()))  # 记录的创建时间（时间戳格式）
    updated_at = db.Column(db.Integer, nullable=False, default=int(datetime.now().timestamp()),
                           onupdate=int(datetime.now().timestamp()))  # 记录的更新时间（时间戳格式）
