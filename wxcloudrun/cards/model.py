from datetime import datetime

from wxcloudrun import db


class Category(db.Model):
    __tablename__ = 'categories'  # 表名
    id = db.Column(db.String(36), primary_key=True, unique=True, nullable=False)  # 分类的全局唯一标识符，UUID格式
    name = db.Column(db.String(255))  # 分类名称
    file_id = db.Column(db.String(255))  # 分类图片URL
    created_at = db.Column(db.Integer, nullable=False, default=int(datetime.now().timestamp()))  # 记录的创建时间（时间戳格式）
    updated_at = db.Column(db.Integer, nullable=False, default=int(datetime.now().timestamp()),
                           onupdate=int(datetime.now().timestamp()))  # 记录的更新时间（时间戳格式）


class Illustration(db.Model):
    __tablename__ = 'illustrations'  # 表名
    id = db.Column(db.String(36), primary_key=True, unique=True, nullable=False)  # 图鉴的全局唯一标识符，UUID格式
    name = db.Column(db.String(255))  # 图鉴名称
    category_id = db.Column(db.String(36), db.ForeignKey('categories.id'))  # 关联分类ID，外键
    activated_file_id = db.Column(db.String(255))  # 图鉴图片URL
    unactivated_file_id = db.Column(db.String(255))  # 图鉴图片URL
    music_file_id = db.Column(db.String(255))  # 激活音频URL
    created_at = db.Column(db.Integer, nullable=False, default=int(datetime.now().timestamp()))  # 记录的创建时间（时间戳格式）
    updated_at = db.Column(db.Integer, nullable=False, default=int(datetime.now().timestamp()),
                           onupdate=int(datetime.now().timestamp()))  # 记录的更新时间（时间戳格式）


class UserCollection(db.Model):
    __tablename__ = 'user_collections'  # 表名
    id = db.Column(db.String(36), primary_key=True, unique=True, nullable=False)  # 收藏记录的全局唯一标识符，UUID格式
    user_id = db.Column(db.String(255))  # 用户ID，外键
    card_id = db.Column(db.String(36))   # 卡片ID
    illustration_id = db.Column(db.String(36), db.ForeignKey('illustrations.id'))  # 图鉴ID，外键
    created_at = db.Column(db.Integer, nullable=False, default=int(datetime.now().timestamp()))  # 记录的创建时间（时间戳格式）
    updated_at = db.Column(db.Integer, nullable=False, default=int(datetime.now().timestamp()),
                           onupdate=int(datetime.now().timestamp()))  # 记录的更新时间（时间戳格式）


class Cards(db.Model):
    __tablename__ = 'cards'  # 表名
    id = db.Column(db.String(36), primary_key=True, unique=True, nullable=False)  # 收藏记录的全局唯一标识符，UUID格式
    illustration_id = db.Column(db.String(36), db.ForeignKey('illustrations.id'))  # 图鉴ID，外键
    created_at = db.Column(db.Integer, nullable=False, default=int(datetime.now().timestamp()))  # 记录的创建时间（时间戳格式）
    updated_at = db.Column(db.Integer, nullable=False, default=int(datetime.now().timestamp()),
                           onupdate=int(datetime.now().timestamp()))  # 记录的更新时间（时间戳格式）
