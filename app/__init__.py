from flask import Flask
from dotenv import load_dotenv
from flask_redis import FlaskRedis
from . import db
from . import product
from app.redis import check_redis_client

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    load_dotenv()
    check_redis_client()

    app.config.from_mapping(
        SECRET_KEY='dev',
    )
    db.init_app(app)

    app.register_blueprint(product.bp)

    return app