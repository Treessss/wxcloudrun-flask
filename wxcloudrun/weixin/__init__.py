from flask import Blueprint

wx = Blueprint('wx', __name__)

from . import views