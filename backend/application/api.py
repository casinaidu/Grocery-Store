from flask_restful import Resource, fields, marshal_with, reqparse, marshal
from application.models import *
from flask_security import auth_required
from .database import db
import string, random


purchase_fields = {
    'id': fields.Integer,
    'user_id': fields.Integer,
    'product_id': fields.Integer,
    'quantity': fields.Integer,
    'purchased': fields.Boolean
}

purchase_parser = reqparse.RequestParser()
purchase_parser.add_argument('user_id')
purchase_parser.add_argument('product_id')
purchase_parser.add_argument('quantity')
purchase_parser.add_argument('purchased')

product_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'expiry': fields.DateTime,
    'price': fields.Float,
    'unit': fields.String,
    'quantity': fields.Integer,
    'category_id': fields.Integer,
    'purchases': fields.Nested(purchase_fields)
}

product_parser = reqparse.RequestParser()
product_parser.add_argument('name')
product_parser.add_argument('expiry')
product_parser.add_argument('price')
product_parser.add_argument('unit')
product_parser.add_argument('quantity')
product_parser.add_argument('category_id')

category_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'products': fields.Nested(product_fields)
}

category_parser = reqparse.RequestParser()
category_parser.add_argument('name')

user_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'email': fields.String,
    'role': fields.String,
    'purchases': fields.Nested(purchase_fields)
}

user_parser = reqparse.RequestParser()
user_parser.add_argument('email')
user_parser.add_argument('name')
user_parser.add_argument('password')
user_parser.add_argument('role')


class UserLoginAPI(Resource):
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
        active = 1
        fs_uniquifier = ''.join(random.choices(string.ascii_letters,k=10))
        if any(field is None for field in (email, name, password, role)):
            return {"message":"One or more fields are empty"}, 400
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
        if name is None:
            return {"message":"Name is required"}, 400
        category = Category.query.filter_by(name=name).first()
        if category:
            return {"message":"Category already exists"}, 400
        category = Category(name=name)
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
        if name is None:
            return {"message":"Name is required"}, 400
        category_exist = Category.query.filter_by(name=name).first()
        if category_exist and category_exist.id != category.id:
            return {"message":"Name already exists"}, 400
        category.name = name
        db.session.commit()
        return marshal(category, category_fields), 200
