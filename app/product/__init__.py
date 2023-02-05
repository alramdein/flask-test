from flask import Blueprint

bp = Blueprint('product', __name__, url_prefix='/products')

from app.product import product_routes