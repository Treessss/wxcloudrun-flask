# 创建应用实例
import sys

from wxcloudrun import app
from wxcloudrun import db

# 启动Flask Web服务
# 检查命令行参数

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    # app.run(debug=True)
    app.run(host=sys.argv[1], port=sys.argv[2])
