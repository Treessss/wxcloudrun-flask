import logging

from sqlalchemy.exc import OperationalError

from wxcloudrun import db
from wxcloudrun.warehouse.model import Warehouse

# 初始化日志
logger = logging.getLogger('log')


def list_warehouse_by_wxuid(id):
    """
    根据ID查询user实体
    :param id: Counter的ID
    :return: Counter实体
    """
    try:
        return Warehouse.query.filter(Warehouse.user_id == id).all()
    except OperationalError as e:
        logger.info("query_counterbyid errorMsg= {} ".format(e))
        return None


def get_warehouse_by_id(id):
    """
    根据ID查询user实体
    :param id: Counter的ID
    :return: Counter实体
    """
    try:
        return Warehouse.query.filter(Warehouse.id == id).first()
    except OperationalError as e:
        logger.info("query_counterbyid errorMsg= {} ".format(e))
        return None


def delete_warehouse_by_wxuid(id):
    """
    根据ID删除Counter实体
    :param id: Counter的ID
    """
    try:
        warehouse = Warehouse.query.filter(Warehouse.user_id == id)
        if warehouse is None:
            return
        db.session.delete(warehouse)
        db.session.commit()
    except OperationalError as e:
        logger.info("delete_counterbyid errorMsg= {} ".format(e))


def delete_warehouse_by_id(id):
    """
    根据ID删除Counter实体
    :param id: Counter的ID
    """
    try:
        warehouse = Warehouse.query.filter(Warehouse.id == id).first()
        if warehouse is None:
            return
        db.session.delete(warehouse)
        db.session.commit()
    except OperationalError as e:
        logger.info("delete_counterbyid errorMsg= {} ".format(e))


def insert_warehouse(warehouse):
    """
    插入一个warehouse实体
    :param warehouse: warehouse实体
    """
    try:
        db.session.add(warehouse)
        db.session.commit()
    except OperationalError as e:
        logger.info("insert_counter errorMsg= {} ".format(e))


def update_warehouse_by_id(warehouse):
    """
    :param warehouse:
    """
    try:
        old_warehouse = get_warehouse_by_id(warehouse.id)
        if old_warehouse is None:
            return
        db.session.flush()
        db.session.commit()
    except OperationalError as e:
        logger.info("update_counterbyid errorMsg= {} ".format(e))


