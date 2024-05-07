import logging

from sqlalchemy.exc import OperationalError

from wxcloudrun import db
from wxcloudrun.cards.model import Category, Illustration, UserCollection, Cards

# 初始化日志
logger = logging.getLogger('log')


def get_category_by_id(id):
    try:
        return Category.query.filter(Category.id == id).first()
    except OperationalError as e:
        logger.info("query_counterbyid errorMsg= {} ".format(e))
        return None


def get_card_by_id(id):
    try:
        return Cards.query.filter(Cards.id == id).first()
    except OperationalError as e:
        logger.info("query_counterbyid errorMsg= {} ".format(e))
        return None


def get_illustraion_by_id(id):
    try:
        return Illustration.query.filter(Illustration.id == id).first()
    except OperationalError as e:
        logger.info("query_counterbyid errorMsg= {} ".format(e))
        return None


def list_categories_by_filter(filters=None):
    if filters is None:
        filters = {}
    try:
        # 构建基本查询
        query = Category.query

        # 应用过滤条件
        for key, value in filters.items():
            query = query.filter(getattr(Category, key) == value)

        # 执行查询并返回结果
        return query.all()
    except OperationalError as e:
        logger.info(f"list_categories_by_filter errorMsg= {e}")
        return []


def list_illustrations_by_filter(filters=None):
    if filters is None:
        filters = {}
    try:
        # 构建基本查询
        query = Illustration.query

        # 应用过滤条件
        for key, value in filters.items():
            query = query.filter(getattr(Illustration, key) == value)

        # 执行查询并返回结果
        return query.all()
    except OperationalError as e:
        logger.info(f"list_categories_by_filter errorMsg= {e}")
        return []


def delete_category_by_id(id):
    try:
        category = Category.query.get(id)
        if category is None:
            return
        db.session.delete(category)
        db.session.commit()
    except OperationalError as e:
        logger.info("delete category errorMsg= {} ".format(e))


def delete_illustration_by_id(id):
    try:
        illustration = Illustration.query.get(id)
        if illustration is None:
            return
        db.session.delete(illustration)
        db.session.commit()
    except OperationalError as e:
        logger.info("delete category errorMsg= {} ".format(e))


def create_category(category):
    try:
        db.session.add(category)
        db.session.commit()
    except OperationalError as e:
        logger.error("insert_category errorMsg= {} ".format(e))


def batch_create_cards(cards):
    try:
        for card in cards:
            db.session.add(card)
        db.session.commit()
    except OperationalError as e:
        logger.error("insert_categories errorMsg= {} ".format(e))


def create_user_collection(user_collection):
    try:
        db.session.add(user_collection)
        db.session.commit()
    except OperationalError as e:
        logger.error("user_collection errorMsg= {} ".format(e))


def create_illustration(illustration):
    try:
        db.session.add(illustration)
        db.session.commit()
    except OperationalError as e:
        logger.error("insert_illustration errorMsg= {} ".format(e))


def update_illustration(illustration):
    try:
        db.session.flush()
        db.session.commit()
    except OperationalError as e:
        logger.info("update_counterbyid errorMsg= {} ".format(e))


def list_user_collections_by_filter(filters=None):
    if filters is None:
        filters = {}
    try:
        # 构建基本查询
        query = UserCollection.query

        # 应用过滤条件
        for key, value in filters.items():
            query = query.filter(getattr(UserCollection, key) == value)

        # 执行查询并返回结果
        return query.all()
    except OperationalError as e:
        logger.info(f"list_categories_by_filter errorMsg= {e}")
        return []
