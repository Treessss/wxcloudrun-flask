from datetime import datetime
from wxcloudrun import db
import json


class Warehouse(db.Model):
    __tablename__ = 'warehouses'  # 表名
    id = db.Column(db.String(36), primary_key=True, unique=True, nullable=False)  # 仓库记录的全局唯一标识符，UUID格式
    user_id = db.Column(db.String(255))  # 用户ID
    name = db.Column(db.String(255))  # 商品名称
    description = db.Column(db.Text)  # 商品描述
    buy_time = db.Column(db.Integer)  # 购买时间（时间戳格式）
    buy_type = db.Column(db.Enum('partial', 'full'))  # 支付类型（定补或全款）
    created_at = db.Column(db.Integer, nullable=False, default=int(datetime.now().timestamp()))  # 记录的创建时间（时间戳格式）
    updated_at = db.Column(db.Integer, nullable=False, default=int(datetime.now().timestamp()),
                           onupdate=int(datetime.now().timestamp()))  # 记录的更新时间（时间戳格式）
    total_price = db.Column(db.Numeric(10, 2))  # 总价
    deposit = db.Column(db.Numeric(10, 2))  # 定金
    file_ids = db.Column(db.String(1024))  # 文件ID列表字符串

    def set_file_ids(self, file_ids):
        self.file_ids = json.dumps(file_ids)

    def get_file_ids(self):
        return json.loads(self.file_ids) if self.file_ids else []
