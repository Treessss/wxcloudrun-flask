import logging

from sqlalchemy import desc
from sqlalchemy.exc import OperationalError

from wxcloudrun import db
from wxcloudrun.warehouse.model import Warehouse

# 初始化日志
logger = logging.getLogger('log')


from sqlalchemy.exc import OperationalError

def list_warehouse(id, search=None, buy_type=None):
    """
    根据ID查询user实体
    :param id: User ID (Counter's ID)
    :param search: String for searching warehouse names (optional)
    :param buy_type: String for filtering by buy_type (optional)
    :return: List of Warehouse entities matching the criteria
    """
    try:
        # Initialize the query with the user ID filter
        query = Warehouse.query.filter(Warehouse.user_id == id)

        # If a search string is provided, add the "ilike" filter to the query
        if search:
            search_pattern = f"%{search}%"
            query = query.filter(Warehouse.name.ilike(search_pattern))

        # If a buy_type is provided, add it as a filter
        if buy_type:
            query = query.filter(Warehouse.buy_type == buy_type)

        # Sort results in descending order by buy_time
        query = query.order_by(desc(Warehouse.created_at))

        return query.all()
    except OperationalError as e:
        logger.info(f"query_counterbyid errorMsg= {e}")
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


