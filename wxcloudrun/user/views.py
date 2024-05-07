import uuid
from datetime import datetime
from flask import request
from wxcloudrun.user import user
from wxcloudrun import common
from wxcloudrun.user import dao
from wxcloudrun.user import model
from wxcloudrun.response import make_succ_empty_response, make_succ_response, make_err_response


@user.route('/', methods=['POST'])
def create_user():
    """
    获取请求头中的openid
    判断是否存在
    如果存在则返回用户UUID
    不存在则创建后返回用户UUID
    :return:
    """
    # 从请求头获取微信 OpenID
    wx_uid = common.get_wx_uid(request)
    if wx_uid is None:
        return make_err_response({"x-wx-openid is nil"})

    # 判断openid是否存在
    user = dao.query_user_by_id(wx_uid)
    print(user)
    if user is None:
        # 不存在则创建
        new_user = model.User()
        new_user.id = uuid.uuid4()
        new_user.wx_uid = wx_uid
        dao.insert_user(new_user)
        return make_succ_response({"id": new_user.id})
    else:
        return make_succ_response({"id": user.id})


@user.route('/', methods=['DELETE'])
def delete_user():
    """
    获取请求头中的openid
    判断是否存在
    如果存在则返回用户UUID
    不存在则创建后返回用户UUID
    :return:
    """
    # 从请求头获取微信 OpenID
    wx_uid = common.get_wx_uid(request)

    # 判断openid是否存在
    user = dao.query_user_by_id(wx_uid)
    if user is None:
        return make_succ_empty_response()
    else:
        dao.delete_user_by_id(wx_uid)
        return make_succ_empty_response()
