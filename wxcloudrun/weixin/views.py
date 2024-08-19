import uuid
from datetime import datetime
from flask import request
from wxcloudrun.weixin import wx
from wxcloudrun import common
from wxcloudrun.weixin import dao
from wxcloudrun.user import model
from wxcloudrun.response import make_succ_empty_response, make_succ_response, make_err_response

APP_ID = "wx3e9f36f57582edac"
APP_SECRET = "0878dd0cfe8082aff37f9a335234ddc7"


@wx.route('/phonenumber', methods=['POST'])
def get_weixin_phone_number():
    code = request.json.get('code')
    if not code:
        return make_err_response({"error": "Missing 'code' parameter"})

    token_info = dao.get_wechat_access_token(APP_ID, APP_SECRET)

    # 检查是否成功获取 access_token
    if 'access_token' in token_info:
        access_token = token_info['access_token']
        # 在这里处理使用 access_token 的逻辑
        phone_info = dao.get_weixin_phone_number(access_token, code)
        return make_succ_response(phone_info)
    else:
        # 如果未获取到 access_token，返回错误信息
        return make_err_response({"error": token_info})
