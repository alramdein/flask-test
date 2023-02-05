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

@bp.route('/', methods=['GET'])
def get():
    sortBy = request.args.get("sortby")
    if sortBy is None or sortBy.upper() == "TERBARU":
        query = "SELECT * FROM products ORDER BY created_at DESC"
    elif sortBy.upper() == "TERMURAH":
        query = "SELECT * FROM products ORDER BY price ASC"
    elif sortBy.upper() == "TERMAHAL":
        query = "SELECT * FROM products ORDER BY price DESC"
    elif sortBy.upper() == "NAMEASC":
        query = "SELECT * FROM products ORDER BY name ASC"
    elif sortBy.upper() == "NAMEDESC":
        query = "SELECT * FROM products ORDER BY name DESC"

    db = get_db()
    try:
        cur = db.cursor()
        cur.execute(query)
        products = []
        for value in cur.fetchall():
            products.append({
                "name": value[1],
                "price": value[2],
                "description": value[3],
                "quantity": value[4],
                "created_at": str(value[5])
            })

        return Response(json.dumps(products), status=200, mimetype='application/json')
        
    except Exception as error:
        print(error)
        return Response(json.dumps({
                "message": "something went wrong",
            }), status=500, mimetype='application/json')