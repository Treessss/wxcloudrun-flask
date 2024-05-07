from wxcloudrun.points import model
import logging
from sqlalchemy.exc import OperationalError
from wxcloudrun import db

# 初始化日志
logger = logging.getLogger('log')


def get_order_point_by_order_id(id):
    """
    根据ID查询order_point实体
    :param id: Counter的ID
    :return: Counter实体
    """
    try:
        return model.OrderPoint.query.filter(model.OrderPoint.order_id == id).first()
    except OperationalError as e:
        logger.info("query_counterbyid errorMsg= {} ".format(e))
        return None


def get_order_point_by_id(id):
    """
    根据ID查询order_point实体
    :param id: Counter的ID
    :return: Counter实体
    """
    try:
        return model.OrderPoint.query.filter(model.OrderPoint.id == id).first()
    except OperationalError as e:
        logger.info("query_counterbyid errorMsg= {} ".format(e))
        return None


def list_order_point_by_id():
    """
    根据ID查询order_point实体
    :param id: Counter的ID
    :return: Counter实体
    """
    try:
        return model.OrderPoint.query.filter().all()
    except OperationalError as e:
        logger.info("query_counterbyid errorMsg= {} ".format(e))
        return None


def insert_order_point(order_point):
    try:
        db.session.add(order_point)
        db.session.commit()
    except OperationalError as e:
        logger.info("insert_counter errorMsg= {} ".format(e))


def delete_order_point_by_id(id):
    try:
        order_point = model.OrderPoint.query.filter(model.OrderPoint.id == id).first()
        if order_point is None:
            return
        db.session.delete(order_point)
        db.session.commit()
    except OperationalError as e:
        logger.info("delete_counterbyid errorMsg= {} ".format(e))


def update_order_point_by_id(order_point):
    """
    :param warehouse:
    """
    try:
        old_warehouse = get_order_point_by_id(order_point.id)
        if old_warehouse is None:
            return
        db.session.flush()
        db.session.commit()
    except OperationalError as e:
        logger.info("update_counterbyid errorMsg= {} ".format(e))


def list_user_points_by_filters(filters):
    """
    根据给定的过滤条件查询仓库实体
    :param filters: 一个包含过滤条件的字典
    :return: 仓库实体的列表
    """
    try:
        # 构建基本查询
        query = model.UserPoint.query

        # 应用过滤条件
        for key, value in filters.items():
            query = query.filter(getattr(model.UserPoint, key) == value)

        # 执行查询并返回结果
        return query.all()
    except OperationalError as e:
        logger.info(f"query_user_points_by_filters errorMsg= {e}")
        return []


def insert_user_point(user_point):
    try:
        db.session.add(user_point)
        db.session.commit()
    except OperationalError as e:
        logger.info("insert_counter errorMsg= {} ".format(e))


def update_user_point_by_id(user_point):
    """
    :param warehouse:
    """
    try:
        db.session.flush()
        db.session.commit()
    except OperationalError as e:
        logger.info("update_counterbyid errorMsg= {} ".format(e))


def get_user_point_by_openid(openid):
    try:
        return model.UserPoint.query.filter(model.UserPoint.user_id == openid).first()
    except OperationalError as e:
        logger.info("query_counterbyid errorMsg= {} ".format(e))
        return None
