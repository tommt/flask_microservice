from flask import Flask, jsonify, make_response, g
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import requests
from sqlalchemy import UniqueConstraint
from typing import List
from flask_restful import Api, Resource  # new


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:postgres@db/postgres"
CORS(app)

db = SQLAlchemy(app)
ma = Marshmallow(app)
api = Api(app)  # new


class Product(db.Model):
    id: int
    title: str
    image: str

    id = db.Column(db.Integer, primary_key=True, autoincrement=False)
    title = db.Column(db.String(255))
    image = db.Column(db.String(255))


class ProductSchema(ma.Schema):
    class Meta:
        fields = ("id", "title", "image")
        model: Product


product_schema = ProductSchema()
products_schema = ProductSchema(many=True)


class ProductUser(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    product_id = db.Column(db.Integer)

    UniqueConstraint('user_id', 'product_id', name='user_product_unique')


# @app.route('/api/products/')
# def index():
#     products = Product.query.all()
#     return jsonify(products)


class ProductListResource(Resource):
    def get(self):
        products = Product.query.all()
        return products_schema.dump(products)


class LikeView(Resource):
    def post(self, id):
        req = requests.get(
            'http://docker.for.linux.localhost:8000/api/v1/user')
        return jsonify(req.json())


api.add_resource(ProductListResource, '/api/products')
api.add_resource(LikeView, '/api/products/<int:id>/like')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
