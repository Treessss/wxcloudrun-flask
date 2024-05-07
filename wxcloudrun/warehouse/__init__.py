from flask import Blueprint

warehouse = Blueprint('warehouse', __name__)

from . import views