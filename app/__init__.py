import os
from flask import Flask
from dotenv import load_dotenv
from . import db
from . import product

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    load_dotenv()

    app.config.from_mapping(
        SECRET_KEY='dev',
    )
    db.init_app(app)

    app.register_blueprint(product.bp)

    return app