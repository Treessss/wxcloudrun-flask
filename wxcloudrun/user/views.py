import uuid
from datetime import datetime
from flask import request
from wxcloudrun.user import user
from wxcloudrun import common
from wxcloudrun.user import dao
from wxcloudrun.user import model
from wxcloudrun.response import make_succ_empty_response, make_succ_response, make_err_response


@user.route('', methods=['POST'])
def create_user():
    """
    获取请求头中的openid
    判断是否存在
    如果存在则返回用户UUID
    不存在则创建后返回用户UUID
    :return:
    """
    params = request.get_json()

    # 从请求头获取微信 OpenID
    wx_uid = common.get_wx_uid(request)
    if wx_uid is None:
        return make_err_response({"x-wx-openid is nil"})

    # 入参
    tb_id = params.get("tb_id")
    dy_id = params.get("dy_id")
    phone_number = params.get("phone_number")

    if tb_id is None or dy_id is None or phone_number is None:
        return make_err_response({"error": "手机号、淘宝ID与抖音ID不能为空"})

    # 判断wx_uid是否存在
    user = dao.query_user_by_id(wx_uid)
    if user is None:
        # 检查tb_id和dy_id是否已存在
        existing_user = model.User.query.filter(
            (model.User.tb_id == tb_id) | (model.User.dy_id == dy_id)
            | (model.User.phone_number == phone_number)
        ).first()

        if existing_user:
            return make_err_response({"error": "手机、淘宝ID与抖音ID已被绑定，请联系管理员！"})

        # 不存在则创建
        new_user = model.User()
        new_user.id = uuid.uuid4()
        new_user.wx_uid = wx_uid
        new_user.tb_id = tb_id
        new_user.dy_id = dy_id
        new_user.phone_number = phone_number
        dao.insert_user(new_user)
        return make_succ_response(
            {
                "wx_uid": new_user.wx_uid,
                "tb_id": new_user.tb_id,
                "dy_id": new_user.dy_id,
                "phone_number": new_user.phone_number
            }
        )
    else:
        return make_succ_response(
            {
                "wx_uid": user.wx_uid,
                "tb_id": user.tb_id,
                "dy_id": user.dy_id,
                "phone_number": user.phone_number
            }
        )


@user.route('', methods=['GET'])
def get_user():
    # 从请求头获取微信 OpenID
    wx_uid = common.get_wx_uid(request)
    if wx_uid is None:
        return make_err_response({"error": "x-wx-openid is nil"})

    # 判断wx_uid是否存在
    user = dao.query_user_by_id(wx_uid)
    if user is None:
        return make_succ_response({})
    else:
        return make_succ_response(
            {
                "wx_uid": user.wx_uid,
                "tb_id": user.tb_id,
                "dy_id": user.dy_id,
                "phone_number": user.phone_nember
            }
        )


@user.route('', methods=['DELETE'])
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
