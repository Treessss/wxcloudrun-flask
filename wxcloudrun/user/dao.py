import logging

from sqlalchemy.exc import OperationalError

from wxcloudrun import db
from wxcloudrun.user.model import User

# 初始化日志
logger = logging.getLogger('log')


def query_user_by_id(id):
    """
    根据ID查询user实体
    :param id: Counter的ID
    :return: Counter实体
    """
    try:
        return User.query.filter(User.wx_uid == id).first()
    except OperationalError as e:
        logger.info("query_counterbyid errorMsg= {} ".format(e))
        return None


def delete_user_by_id(id):
    """
    根据ID删除Counter实体
    :param id: Counter的ID
    """
    try:
        user = User.query.filter(User.wx_uid == id)
        if user is None:
            return
        db.session.delete(user)
        db.session.commit()
    except OperationalError as e:
        logger.info("delete_counterbyid errorMsg= {} ".format(e))


def insert_user(user):
    """
    插入一个user实体
    :param counter: Counters实体
    """
    try:
        db.session.add(user)
        db.session.commit()
    except OperationalError as e:
        logger.info("insert_counter errorMsg= {} ".format(e))


def update_user_by_id(user):
    """
    :param counter实体
    """
    try:
        user = query_user_by_id(user.wx_uid)
        if user is None:
            return
        db.session.flush()
        db.session.commit()
    except OperationalError as e:
        logger.info("update_counterbyid errorMsg= {} ".format(e))
