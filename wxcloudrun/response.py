import json

from flask import Response
from decimal import Decimal


def make_succ_empty_response():
    data = json.dumps({'code': 0, 'data': {}})
    return Response(data, mimetype='application/json')


def handle_decimal(obj):
    if isinstance(obj, Decimal):
        return str(obj)  # 或者使用 str(obj) 如果你想保持数字的精确性
    raise TypeError("Object of type Decimal is not JSON serializable")


def make_succ_response(data):
    data = json.dumps({'code': 0, 'data': data}, default=handle_decimal)
    return Response(data, mimetype='application/json')


def make_err_response(err_msg):
    data = json.dumps({'code': -1, 'errorMsg': err_msg})
    return Response(data, mimetype='application/json')
