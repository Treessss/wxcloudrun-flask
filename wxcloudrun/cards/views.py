import json
import uuid
from collections import defaultdict

from flask import request
from run import app
from wxcloudrun import common
from wxcloudrun.cards import dao
from wxcloudrun.cards import model
from wxcloudrun.cards import cards
from wxcloudrun.response import make_succ_empty_response, make_succ_response, make_err_response


@cards.route('/category', methods=["GET"])
def list_categories():
    """
    图鉴分类列表
    :return:
    """
    categories = dao.list_categories_by_filter()
    data = []
    for category in categories:
        x = {
            "id": category.id,
            "name": category.name,
            "file_id": category.file_id
        }
        data.append(x)
    return make_succ_response(data)


@cards.route('/category', methods=["POST"])
def create_category():
    """
    创建图鉴
    :return:
    """
    params = request.get_json()

    category = model.Category()
    category.id = uuid.uuid4()
    category.name = params["name"]
    category.file_id = params["file_id"]

    try:
        dao.create_category(category)
        return make_succ_response({"id": category.id})
    except Exception as e:
        return make_err_response({"error": "创建图鉴分类失败！"})


@cards.route('/category/<category_id>', methods=["DELETE"])
def delete_category(category_id):
    """
    删除图鉴
    :return:
    """
    try:
        dao.delete_category_by_id(category_id)
        return make_succ_empty_response()
    except Exception as e:
        return make_err_response({"error": "删除图鉴分类失败"})


@cards.route('/category/<category_id>', methods=["GET"])
def get_category(category_id):
    """
    获取图鉴详情
    :return:
    """
    category = dao.get_category_by_id(category_id)
    if category is None:
        return make_err_response({"error": "图鉴分类不存在"})
    else:
        data = {
            "id": category.id,
            "file_id": category.file_id,
            "name": category.name
        }
        return make_succ_response(data)


@cards.route('/illustration', methods=["GET"])
def list_illustration():
    """
    图鉴列表
    :return:
    """
    illustrations = dao.list_illustrations_by_filter()
    data = []
    for illustration in illustrations:
        if illustration.category_id not in ["9d8f656b-26f6-4b22-9cf9-eddd3e0614b1",
                                            "df292868-e236-456e-8119-9daa212a1d3c"]:
            continue
        x = {
            "id": illustration.id,
            "name": illustration.name,
            "category_id": illustration.category_id,
            "activated_file_id": illustration.activated_file_id,
            "unactivated_file_id": illustration.unactivated_file_id
        }
        data.append(x)
    return make_succ_response(data)


@cards.route('/illustration/<illustration_id>', methods=["GET"])
def get_illustration(illustration_id):
    """
    图鉴详情
    :param illustration_id:
    :return:
    """
    illustration = dao.get_illustraion_by_id(illustration_id)
    if illustration is None:
        return make_err_response({"error": "此图鉴不存在"})
    data = {
        "id": illustration.id,
        "name": illustration.name,
        "category_id": illustration.category_id,
        "activated_file_id": illustration.activated_file_id,
        "unactivated_file_id": illustration.unactivated_file_id,
        "created_at": illustration.created_at,
        "updated_at": illustration.updated_at
    }

    return make_succ_response(data)


@cards.route('/illustration', methods=["POST"])
def create_illustration():
    """
    创建图鉴
    :return:
    """
    params = request.get_json()

    # 判断图鉴分类是否存在
    category = dao.get_category_by_id(params["category_id"])
    if category is None:
        return make_err_response({"error": "所选图鉴分类不存在"})

    illustration = model.Illustration()
    illustration.id = uuid.uuid4()
    illustration.activated_file_id = params["activated_file_id"]
    illustration.unactivated_file_id = params["unactivated_file_id"]
    illustration.category_id = params["category_id"]
    illustration.name = params["name"]

    try:
        dao.create_illustration(illustration)
        return make_succ_response({"id": illustration.id})
    except Exception as e:
        return make_err_response({"error": "创建图鉴失败"})


@cards.route('/illustration/<illustration_id>', methods=["PUT"])
def update_illustration(illustration_id):
    """
    更新图鉴
    :param illustration_id:
    :return:
    """
    params = request.get_json()

    # 判断该图鉴是否存在
    illustration = dao.get_illustraion_by_id(illustration_id)
    if illustration is None:
        return make_err_response({"error": "该图鉴不存在"})

    illustration.name = params["name"]
    illustration.activated_file_id = params["activated_file_id"]
    illustration.unactivated_file_id = params["unactivated_file_id"]
    illustration.category_id = params["category_id"]

    try:
        dao.update_illustration(illustration)
        return make_succ_response({"id": illustration.id})
    except:
        return make_err_response({"error": "更新图鉴信息失败"})


@cards.route('/illustration/<illustration_id>', methods=["DELETE"])
def delete_illustration(illustration_id):
    """
    删除图鉴
    :param illustration_id:
    :return:
    """
    try:
        dao.delete_illustration_by_id(illustration_id)
        return make_succ_response({"id": illustration_id})
    except:
        return make_err_response({"error": "删除图鉴失败"})


@cards.route('/user', methods=["GET"])
def list_user_collection():
    """
    获取用户图鉴
    :return:{
        "category_id1":[
            {
                "id":"illustration_id",
                "file_id": "file_id",
                "name":"name"
            }
        ]
    }
    """
    wx_uid = common.get_wx_uid(request)
    if wx_uid is None:
        return make_err_response({"error": "用户不存在，请登录"})

    # 获取所有图鉴
    illustrations = dao.list_illustrations_by_filter()

    # 获取所有图鉴分类
    category_data = {}
    categories = dao.list_categories_by_filter()
    for category in categories:
        category_data[category.id] = category.name

    # 使用defaultdict来简化数据字典的创建，避免了显式检查和初始化的需要
    data = defaultdict(list)
    # 获取用户所激活的图鉴
    filters = {"user_id": wx_uid}
    user_collections = dao.list_user_collections_by_filter(filters)

    # 创建一个集合来存储用户激活的图鉴ID
    activated_illustrations = set(collection.illustration_id for collection in user_collections)

    for illustration in illustrations:
        data[illustration.category_id].append({
            "id": illustration.id,
            "name": illustration.name,
            "file_id": illustration.activated_file_id if illustration.id in activated_illustrations else illustration.unactivated_file_id
        })
    response = []
    for key, value in data.items():
        if len(value):
            while len(value) % 4 != 0 or len(value) == 4:
                value.append({
                    "id": str(uuid.uuid4()),
                    "name": "问号",
                    "file_id": "cloud://prod-3gg7rthva2e1757e.7072-prod-3gg7rthva2e1757e-1327531447/activate/kakuang.png"
                })
        response.append({
            "category_id": key,
            "category_name": category_data[key],
            "illustration": value
        })

    return make_succ_response(response)


@cards.route('/user', methods=["POST"])
def create_user_collection():
    """
    用户激活图鉴
    :return:
    """
    wx_uid = common.get_wx_uid(request)
    if wx_uid is None:
        return make_err_response({"error": "用户不存在，请登录"})

    params = request.get_json()

    card_id = params["id"]

    # TODO 临时放开两张卡片做激活测试使用
    if card_id in ["0434A5DAAA1C90", "043A47DAAA1C91"]:
        # 根据card_id去判断是否存在该卡片
        card = dao.get_card_by_id(card_id)
        if card is None:
            return make_err_response({"error": "卡片不存在，请确认后重试！"})

        illustrations = dao.list_illustrations_by_filter({"id": card.illustration_id})
        if len(illustrations) == 0:
            return make_err_response({"error": "卡片所属图鉴不存在，请确认后重试！"})

        categories = dao.list_categories_by_filter({"id": illustrations[0].category_id})
        if len(categories) == 0:
            return make_err_response(({"error": "卡片所属分类不存在，请确认后重试！"}))

        data = {
            "id": str(uuid.uuid4()),
            "category_id": categories[0].id,
            "category_name": categories[0].name,
            "illustration_id": illustrations[0].id,
            "illustration_name": illustrations[0].name,
            "illustration_file_id": illustrations[0].activated_file_id
        }
        return make_succ_response(data)

    # 根据card_id去判断是否存在该卡片
    card = dao.get_card_by_id(card_id)
    if card is None:
        return make_err_response({"error": "卡片不存在，请确认后重试！"})

    # 根据card_id去判断是否已经被激活
    filters = {"card_id": card_id}
    user_collection = dao.list_user_collections_by_filter(filters)
    if user_collection:
        return make_err_response({"error": "此卡片已被激活！"})

    illustrations = dao.list_illustrations_by_filter({"id": card.illustration_id})
    if len(illustrations) == 0:
        return make_err_response({"error": "卡片所属图鉴不存在，请确认后重试！"})

    categories = dao.list_categories_by_filter({"id": illustrations[0].category_id})
    if len(categories) == 0:
        return make_err_response(({"error": "卡片所属分类不存在，请确认后重试！"}))

    user_collection = model.UserCollection()
    user_collection.id = uuid.uuid4()
    user_collection.user_id = wx_uid
    user_collection.card_id = card.id
    user_collection.illustration_id = card.illustration_id

    try:
        dao.create_user_collection(user_collection)
        data = {
            "id": user_collection.id,
            "category_id": categories[0].id,
            "category_name": categories[0].name,
            "illustration_id": illustrations[0].id,
            "illustration_name": illustrations[0].name,
            "illustration_file_id": illustrations[0].activated_file_id
        }
        return make_succ_response(data)
    except Exception as e:
        return make_err_response({"error": "激活卡片失败，请稍后重试！"})


@cards.route("", methods=["POST"])
def create_cards():
    params = request.get_json()

    cards = params["cards"]

    batch_cards = []
    for card in cards:
        new_card = model.Cards()
        new_card.id = card["id"]
        new_card.illustration_id = card["illustration_id"]

        batch_cards.append(new_card)

    try:
        dao.batch_create_cards(batch_cards)
        return make_succ_empty_response()
    except Exception as e:
        return make_err_response({"error": "批量创建卡片失败"})


@cards.route('/user/count', methods=["GET"])
def get_user_collection_count():
    wx_uid = common.get_wx_uid(request)
    if wx_uid is None:
        return make_err_response({"error": "用户不存在，请重试！"})

    filters = {"user_id": wx_uid}
    user_collections = dao.list_user_collections_by_filter(filters)

    count = len(user_collections)

    return make_succ_response({"count": count})
