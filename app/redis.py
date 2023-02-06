import os
import redis
import json
from flask import g

redis_client = redis.Redis(host=os.getenv('REDIS_HOST'), port=os.getenv('REDIS_PORT'))

def check_redis_client():
    try:
        redis_client.ping()
        print(f"redis connected at {os.getenv('REDIS_HOST')}:{os.getenv('REDIS_PORT')}")
    except Exception as error:
        print(error)
        raise ValueError("redis is not connected properly")

def store_cache(key, data):
    try:
        return redis_client.set(key, str(data))
    except Exception as error:
        print(error)
        return None

def get_cache(key):
    try:
        data = redis_client.get(key)
        return json.loads(data)
    except Exception as error:
        print(error)
        return None

def flushdb_cache():
    try:
        return redis_client.flushdb()
    except Exception as error:
        print(error)
        return None
