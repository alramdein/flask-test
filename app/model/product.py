from mimetypes import init
from app.db import get_db
from flask import g

class Product:
    def __init__(self, db) -> None:
        self.db = db
    
    def create(self, name, price, description, quantity):
        try:
            cur = self.db.cursor()
            cur.execute(
                "INSERT INTO products(name, price, description, quantity) VALUES (%s, %s, %s, %s)",
                (name, price, description, quantity),
            )
            cur.close()
            self.db.commit()
            self.db.close()
        except Exception as error:
            raise ValueError(error)
    
    def findAll(self, orderQuery):
        try:
            cur = self.db.cursor()
            cur.execute("SELECT * FROM products ORDER BY "+orderQuery)
            products = []
            for value in cur.fetchall():
                products.append({
                    "name": value[1],
                    "price": value[2],
                    "description": value[3],
                    "quantity": value[4],
                    "created_at": str(value[5])
                })
            return products
        except Exception as error:
            raise ValueError(error)
        
