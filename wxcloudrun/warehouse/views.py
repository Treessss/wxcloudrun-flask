import json
from datetime import datetime
import uuid
from flask import request
from run import app
from wxcloudrun.warehouse import warehouse
from wxcloudrun.warehouse import dao
from wxcloudrun.warehouse import model
from wxcloudrun import common
from wxcloudrun.response import make_succ_empty_response, make_succ_response, make_err_response


@warehouse.route('', methods=['GET'])
def list_warehouse():
    wx_uid = common.get_wx_uid(request)
    if wx_uid is None:
        return make_err_response({"x-wx-openid is nil"})

    warehouses = dao.list_warehouse_by_wxuid(wx_uid)
    data = []
    if warehouses is not None:
        for warehouse in warehouses:
            x = {
                "id": warehouse.id,
                "file_ids": warehouse.get_file_ids(),
                "user_id": warehouse.user_id,
                "name": warehouse.name,
                "description": warehouse.description,
                "buy_time": warehouse.buy_time,
                "buy_type": warehouse.buy_type,
                "total_price": warehouse.total_price,
                "deposit": warehouse.deposit,
            }
            data.append(x)

    return make_succ_response(data)


@warehouse.route('/<warehouse_id>', methods=['GET'])
def get_warehouse(warehouse_id):
    wx_uid = common.get_wx_uid(request)
    if wx_uid is None:
        return make_err_response({"x-wx-openid is nil"})

    warehouse = dao.get_warehouse_by_id(warehouse_id)
    if warehouse is not None:
        if warehouse.user_id != wx_uid:
            return make_err_response({"no permission!"})
        else:
            data = {
                "id": warehouse.id,
                "user_id": warehouse.user_id,
                "name": warehouse.name,
                "description": warehouse.description,
                "buy_time": warehouse.buy_time,
                "buy_type": warehouse.buy_type,
                "created_at": warehouse.created_at,
                "updated_at": warehouse.updated_at,
                "total_price": warehouse.total_price,
                "deposit": warehouse.deposit,
                "file_ids": warehouse.get_file_ids(),
            }
    else:
        return make_err_response({"get warehouse failed"})

    return make_succ_response(data)


@warehouse.route('', methods=['POST'])
def create_warehouse():
    wx_uid = common.get_wx_uid(request)
    if wx_uid is None:
        return make_err_response({"x-wx-openid is nil"})
    warehouse = request.get_json()

    # 参数校验
    if not isinstance(warehouse, dict):
        return make_err_response({"error": "Invalid JSON data"})
    required_fields = ["name", "buy_time", "buy_type", "deposit", "total_price", "file_ids"]
    for field in required_fields:
        if field not in warehouse:
            return make_err_response({"error": f"Missing required field: {field}"})

    new_warehouse = model.Warehouse()
    new_warehouse.id = str(uuid.uuid4())  # 将 UUID 转换为字符串
    new_warehouse.user_id = wx_uid
    new_warehouse.name = warehouse["name"]
    new_warehouse.buy_time = warehouse["buy_time"]  # 转换为 datetime 对象
    new_warehouse.buy_type = warehouse["buy_type"]
    new_warehouse.deposit = warehouse["deposit"]
    new_warehouse.description = warehouse.get("description", "")
    new_warehouse.set_file_ids(warehouse["file_ids"])
    new_warehouse.total_price = warehouse["total_price"]

    try:
        dao.insert_warehouse(new_warehouse)
        return make_succ_response({"id": new_warehouse.id})
    except Exception as e:
        return make_err_response({"error": str(e)})


@warehouse.route('/<warehouse_id>', methods=['DELETE'])
def delete_warehouse(warehouse_id):
    wx_uid = common.get_wx_uid(request)
    if wx_uid is None:
        return make_err_response({"x-wx-openid is nil"})

    warehouse = dao.get_warehouse_by_id(warehouse_id)
    # 判断是否为该用户归属的warehouse
    if warehouse is not None and wx_uid != warehouse.user_id:
        return make_err_response({"delete warehouse err,no permission!"})

    try:
        dao.delete_warehouse_by_id(warehouse_id)
        return make_succ_empty_response()
    except Exception as e:
        return make_err_response({"error": str(e)})


@warehouse.route('/<warehouse_id>', methods=["PUT"])
def update_warehouse(warehouse_id):
    wx_uid = common.get_wx_uid(request)
    if wx_uid is None:
        return make_err_response({"x-wx-openid is nil"})
    params = request.get_json()

    warehouse = dao.get_warehouse_by_id(warehouse_id)
    if warehouse is not None and wx_uid != warehouse.user_id:
        return make_err_response({"error": "该仓库不存在，请重新创建！"})

    warehouse.id = warehouse_id
    warehouse.user_id = wx_uid
    warehouse.name = params.get("name", "")
    warehouse.description = params.get("description", "")
    warehouse.buy_time = params.get("buy_time", datetime.now().timestamp())
    warehouse.buy_type = params.get("buy_type", "full")
    warehouse.total_price = params.get("total_price", 0)
    warehouse.deposit = params.get("deposit", 0)
    warehouse.set_file_ids(params.get("file_ids", []))

    try:
        dao.update_warehouse_by_id(warehouse)
        return make_succ_response({"id": warehouse.id})
    except Exception as e:
        return make_err_response({"update warehouse by id err": str(e)})
