from flask import Blueprint

bp = Blueprint('product', __name__, url_prefix='/products')

from flaskr.product import product_routes