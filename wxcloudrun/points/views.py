import uuid
from flask import request

from wxcloudrun import common
from wxcloudrun.points import dao
from wxcloudrun.points import model
from wxcloudrun.points import points
from wxcloudrun.response import make_succ_empty_response, make_succ_response, make_err_response


@points.route('/order', methods=['POST'])
def create_order_point():
    params = request.get_json()

    order_point = dao.get_order_point_by_order_id(params["order_id"])
    if order_point is None:
        new_order_point = model.OrderPoint()
        new_order_point.id = uuid.uuid4()
        new_order_point.order_id = params["order_id"]
        new_order_point.points = params["points"]

        try:
            dao.insert_order_point(new_order_point)
            return make_succ_response({"id": new_order_point.id})
        except Exception as e:
            return make_err_response({"error": str(e)})
    else:
        return make_err_response({"error": "该订单号已存在！"})


@points.route('/order/<id>', methods=['DELETE'])
def delete_order_point(id):
    try:
        dao.delete_order_point_by_id(id)
        return make_succ_response({"id": id})
    except Exception as e:
        return make_err_response({"error": str(e)})


@points.route('/order', methods=["GET"])
def list_order_point():
    order_points = dao.list_order_point_by_id()
    data = []
    if order_points is not None:
        for order_point in order_points:
            x = {
                "id": order_point.id,
                "order_id": order_point.order_id,
                "points": order_point.points,
                "is_used": order_point.is_used
            }
            data.append(x)

    return make_succ_response(data)


@points.route('/order/<id>', methods=["PUT"])
def update_order_point(id):
    params = request.get_json()

    order_point = dao.get_order_point_by_id(id)
    if order_point is None:
        return make_err_response({"error": "this order id is not exist"})
    order_point.points = params["points"]

    try:
        dao.update_order_point_by_id(order_point)
        return make_succ_response({"id": order_point.id})
    except Exception as e:
        return make_err_response({"error": str(e)})


@points.route('/user', methods=["POST"])
def create_user_point():
    """
    录入积分接口
    :return:
    """
    wx_uid = common.get_wx_uid(request)
    if wx_uid is None:
        return make_err_response({"error": "x-wx-openid is not exist"})

    params = request.get_json()

    # 检查order_id是否存在
    order = dao.get_order_point_by_order_id(params["order_id"])
    if order is None:
        return make_err_response({"error": "该订单号不存在！"})
    else:
        # 检查该order_id是否已经被使用
        if order.is_used == 1:
            return make_err_response({"error": "该订单号已使用！"})

    filters = {"user_id": wx_uid}
    user_points = dao.list_user_points_by_filters(filters)
    if user_points:
        # 走更新接口
        try:
            user_points = user_points[0]
            user_points.points = user_points.points + order.points
            dao.update_user_point_by_id(user_points)

            order.is_used = 1
            dao.update_order_point_by_id(order)
            return make_succ_response({"id": user_points.id})
        except Exception as e:
            return make_err_response({"error": "录入积分失败！"})
    else:
        new_user_point = model.UserPoint()
        new_user_point.id = uuid.uuid4()
        new_user_point.points = order.points
        new_user_point.order_id = params["order_id"]
        new_user_point.user_id = wx_uid

        try:
            dao.insert_user_point(new_user_point)
            order.is_used = 1
            dao.update_order_point_by_id(order)
            return make_succ_response({"id": new_user_point.id})
        except Exception as e:
            return make_err_response({"error": "录入积分失败！"})


@points.route('/user', methods=['GET'])
def get_user_points():
    wx_uid = common.get_wx_uid(request)
    if wx_uid is None:
        return make_err_response({"error": "未获取到openid！"})

    user_points = dao.get_user_point_by_openid(wx_uid)
    if user_points is None:
        return make_succ_response({"points": 0})
    else:
        return make_succ_response({"points": user_points.points})
