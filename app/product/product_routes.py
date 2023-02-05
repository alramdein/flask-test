from flask import request
from flask import Response
import json
from app.db import get_db
from app.model.product import Product
from app.product import bp

@bp.route('/', methods=['POST'])
def add():
    name = request.form.get('name')
    price = request.form.get('price')
    description = request.form.get('description')
    quantity = request.form.get('quantity')
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
            p = Product(get_db())
            p.create(name, price, description, quantity)
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
    
    # default sortBy value
    orderByQuery = "created_at DESC"
    
    if sortBy is None or sortBy.upper() == "TERBARU":
        pass
    elif sortBy.upper() == "TERMURAH":
        orderByQuery = "price ASC"
    elif sortBy.upper() == "TERMAHAL":
        orderByQuery = "price DESC"
    elif sortBy.upper() == "NAMEASC":
        orderByQuery = "name ASC"
    elif sortBy.upper() == "NAMEDESC":
        orderByQuery = "name DESC"

    try:
        p = Product(get_db())
        products = p.findAll(orderByQuery)
        return Response(json.dumps(products), status=200, mimetype='application/json')
    except Exception as error:
        print(error)
        return Response(json.dumps({
                "message": "something went wrong",
            }), status=500, mimetype='application/json')