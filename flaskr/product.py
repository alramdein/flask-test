from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from flaskr.db import get_db
from flask import Response, jsonify
import json


bp = Blueprint('product', __name__, url_prefix='/products')

@bp.route('/', methods=['POST'])
def add():
    name = request.form.get('name')
    price = request.form.get('price')
    description = request.form.get('description')
    quantity = request.form.get('quantity')
    db = get_db()
    error = None

    if not name:
        error = 'name is required.'
    elif not price:
        error = 'price is required.'
    elif not description:
        error = 'description is required.'
    elif not quantity:
        error = 'quantity is required.'

    if error is None:
        try:
            cur = db.cursor()
            cur.execute(
                "INSERT INTO products(name, price, description, quantity) VALUES (%s, %s, %s, %s)",
                (name, price, description, quantity),
            )
            cur.close()
            db.commit()
            db.close()
        except Exception as err:
            print(err)
            return Response(json.dumps({
                "message": "something went wrong. failed to add a product.",
            }), status=500, mimetype='application/json')
        else:
            return Response(json.dumps({
                "message": "successfully add a product"
            }), status=200, mimetype='application/json')

    return Response(json.dumps({
                "message": error,
            }), status=400, mimetype='application/json')