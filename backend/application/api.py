from flask_restful import Resource, fields, marshal_with, reqparse, marshal
from application.models import *
from flask_security import auth_required
from .database import db
import string, random
from datetime import datetime


purchase_fields = {
    'id': fields.Integer,
    'user_id': fields.Integer,
    'product_id': fields.Integer,
    'quantity': fields.Integer,
    'timestamp': fields.DateTime
}

purchase_parser = reqparse.RequestParser()
purchase_parser.add_argument('user_id')
purchase_parser.add_argument('product_id')
purchase_parser.add_argument('quantity')
purchase_parser.add_argument('timestamp')

product_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'expiry': fields.DateTime,
    'price': fields.Float,
    'unit': fields.String,
    'quantity': fields.Integer,
    'active': fields.Boolean,
    'category_id': fields.Integer,
    'purchases': fields.Nested(purchase_fields)
}

product_parser = reqparse.RequestParser()
product_parser.add_argument('name')
product_parser.add_argument('expiry')
product_parser.add_argument('price')
product_parser.add_argument('unit')
product_parser.add_argument('quantity')
product_parser.add_argument('active')
product_parser.add_argument('category_id')

category_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'active': fields.Boolean,
    'products': fields.Nested(product_fields)
}

category_parser = reqparse.RequestParser()
category_parser.add_argument('name')
category_parser.add_argument('active')

user_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'email': fields.String,
    'role': fields.String,
    'active': fields.Boolean,
    'purchases': fields.Nested(purchase_fields)
}

user_parser = reqparse.RequestParser()
user_parser.add_argument('email')
user_parser.add_argument('name')
user_parser.add_argument('password')
user_parser.add_argument('role')
user_parser.add_argument('active')


class UserAPI(Resource):
    def get(self,email):
        user = User.query.filter_by(email=email).first()
        if not user:
            return {"message":"Invalid email"}, 404
        return marshal(user, user_fields), 200
    
    def post(self):
        args = user_parser.parse_args()
        email = args.get('email',None)
        name = args.get('name',None)
        password = args.get('password',None)
        role = args.get('role',None)
        if role=='manager':
            active = 0
        else:
            active = 1
        fs_uniquifier = ''.join(random.choices(string.ascii_letters,k=10))
        if any(field is None for field in (email, name, password, role)):
            return {"message":"One or more fields are empty"}, 400
        user_exist = User.query.filter_by(email=email).first()
        if user_exist:
            return {"message":"Email already exists"},400
        user = User(email=email, name=name, password=password, active=active, fs_uniquifier=fs_uniquifier, role=role)
        db.session.add(user)
        db.session.commit()
        return marshal(user, user_fields), 201
    
class CategoryAPI(Resource):
    def get(self, id=None):
        if id is None:
            categories = Category.query.all()
            return marshal(categories, category_fields), 200
        category = Category.query.get(id)
        if category:
            return marshal(category, category_fields), 200
        else:
            return {"message":"Invalid ID"}, 404
        
    def post(self):
        args = category_parser.parse_args()
        name = args.get('name',None)
        active = args.get('active',None) == 'True'
        if name is None:
            return {"message":"Name is required"}, 400
        category_exist = Category.query.filter_by(name=name).first()
        if category_exist:
            return {"message":"Category already exists"}, 400
        category = Category(name=name, active=active)
        db.session.add(category)
        db.session.commit()
        return marshal(category, category_fields), 201
    
    def delete(self, id):
        category = Category.query.get(id)
        if not category:
            return {"message":"Invalid ID"}, 404
        db.session.delete(category)
        db.session.commit()
        return {"message":"Category deleted successfully"}, 200
    
    def put(self, id):
        category = Category.query.get(id)
        if not category:
            return {"message":"Invalid ID"}, 404
        args = category_parser.parse_args()
        name = args.get('name',None)
        active = args.get('active',None) == 'True'
        if name is None:
            return {"message":"Name is required"}, 400
        category_exist = Category.query.filter_by(name=name).first()
        if category_exist and category_exist.id != category.id:
            return {"message":"Category already exists"}, 400
        category.name = name
        category.active = active
        db.session.commit()
        return marshal(category, category_fields), 200

class ProductAPI(Resource):
    def get(self, id=None):
        if id is None:
            products = Product.query.all()
            return marshal(products, product_fields), 200
        product = Product.query.get(id)
        if product:
            return marshal(product, product_fields), 200
        else:
            return {"message":"Invalid ID"}, 404
        
    def post(self):
        args = product_parser.parse_args()
        name = args.get('name',None)
        expiry = datetime.strptime(args.get('expiry',None),'%d/%m/%Y')
        price = args.get('price',None)
        unit = args.get('unit',None)
        quantity = args.get('quantity',None)
        active = args.get('active',None) == 'True'
        category_id = args.get('category_id',None)
        if any(field is None for field in (name, expiry, price, unit, quantity, category_id)):
            return {"message":"One or more fields are empty"}, 400
        category = Category.query.get(category_id)
        if not category:
            return {"message":"Category not exists"}, 400
        product_exist = Product.query.filter_by(name=name, category_id=category_id).first()
        if product_exist:
            return {"message":"Product already exists in this category"}, 400
        product = Product(name=name, expiry=expiry, price=price, unit=unit, quantity=quantity, active=active, category_id=category_id)
        db.session.add(product)
        db.session.commit()
        return marshal(product, product_fields), 201
    
    def delete(self, id):
        product = Product.query.get(id)
        if not product:
            return {"message":"Invalid ID"}, 404
        db.session.delete(product)
        db.session.commit()
        return {"message":"Product deleted successfully"}, 200
    
    def put(self, id):
        product = Product.query.get(id)
        if not product:
            return {"message":"Invalid ID"}, 404
        args = product_parser.parse_args()
        name = args.get('name',None)
        expiry = datetime.strptime(args.get('expiry',None),'%d/%m/%Y')
        price = args.get('price',None)
        unit = args.get('unit',None)
        quantity = args.get('quantity',None)
        active = args.get('active',None) == 'True'
        category_id = args.get('category_id',None)
        if any(field is None for field in (name, expiry, price, unit, quantity, category_id)):
            return {"message":"One or more fields are empty"}, 400
        category = Category.query.get(category_id)
        if not category:
            return {"message":"Category not exists"}, 400
        product_exist = Product.query.filter_by(name=name, category_id=category_id).first()
        if product_exist and product_exist.id != product.id:
            return {"message":"Product already exists in this category"}, 400
        product.name = name
        product.expiry = expiry
        product.price = price
        product.unit = unit
        product.quantity = quantity
        product.active = active
        product.category_id = category_id
        db.session.commit()
        return marshal(product, product_fields), 200
        

class PurchaseAPI(Resource):
    def get(self, id=None):
        if id is None:
            purchases = Purchase.query.all()
            return marshal(purchases, purchase_fields), 200
        purchase = Purchase.query.get(id)
        if purchase:
            return marshal(purchase, purchase_fields), 200
        else:
            return {"message":"Invalid ID"}, 404
        
    def post(self):
        args = purchase_parser.parse_args()
        user_id = args.get('user_id',None)
        product_id = args.get('product_id',None)
        quantity = args.get('quantity',None)
        if any(field is None for field in (user_id, product_id, quantity)):
            return {"message":"One or more fields are empty"}, 400
        user = User.query.get(user_id)
        product = Product.query.get(product_id)
        if not user or not product:
            return {"message":"User or Product not exists"}, 400
        if product.quantity < int(quantity):
            return {"message":"The selected quantity is more than the available stock"}, 400
        purchase = Purchase(user_id=user_id, product_id=product_id, quantity=quantity)
        db.session.add(purchase)
        db.session.commit()
        return marshal(purchase, purchase_fields), 201
    
    def delete(self, id):
        purchase = Purchase.query.get(id)
        if not purchase:
            return {"message":"Invalid ID"}, 404
        db.session.delete(purchase)
        db.session.commit()
        return {"message":"Purchase deleted successfully"}, 200
    
    def put(self, id):
        purchase = Purchase.query.get(id)
        if not purchase:
            return {"message":"Invalid ID"}, 404
        args = purchase_parser.parse_args()
        user_id = args.get('user_id',None)
        product_id = args.get('product_id',None)
        quantity = args.get('quantity',None)
        if any(field is None for field in (user_id, product_id, quantity)):
            return {"message":"One or more fields are empty"}, 400
        user = User.query.get(user_id)
        product = Product.query.get(product_id)
        if not user or not product:
            return {"message":"User or Product not exists"}, 400
        purchase.user_id = user_id
        purchase.product_id = product_id
        purchase.quantity = quantity
        db.session.commit()
        return marshal(purchase, purchase_fields), 200    