# 创建应用实例
import sys

from wxcloudrun import app
from wxcloudrun import db

# 启动Flask Web服务
# 检查命令行参数
if len(sys.argv) > 1 and sys.argv[3] == 'init_db':
    with app.app_context():
        print("xxxxxxxxxxxxx")
        db.create_all()

if __name__ == '__main__':
    app.run(host=sys.argv[1], port=sys.argv[2])
