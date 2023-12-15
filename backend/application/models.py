from .database import db
from flask_security import UserMixin, RoleMixin
from datetime import datetime

class Role(db.Model, RoleMixin):
    __tablename__ = 'role'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(80), unique=True)

class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String, unique=True)
    name = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)
    active = db.Column(db.Boolean, default=True)
    fs_uniquifier = db.Column(db.String, unique=True)
    role = db.Column(db.String, db.ForeignKey('role.name'))
    purchases = db.relationship('Purchase',backref='user',cascade='all,delete-orphan')
    carts = db.relationship('Cart',backref='user',cascade='all,delete-orphan')

user_roles = db.Table('user_roles',
    db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
    db.Column('role_id', db.Integer(), db.ForeignKey('role.id'))
)
    
class Category(db.Model):
    __tablename__ = 'category'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False, unique=True)
    active = db.Column(db.Boolean, nullable=False, default=False)
    products = db.relationship('Product', backref='category',cascade='all,delete-orphan')
    
class Product(db.Model):
    __tablename__ = 'product'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)
    expiry = db.Column(db.DateTime, nullable=False)
    price = db.Column(db.Float, nullable=False)
    unit = db.Column(db.String, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    active = db.Column(db.Boolean, nullable=False, default=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    purchases = db.relationship('Purchase',backref='product')
    carts = db.relationship('Cart',backref='product')

class Purchase(db.Model):
    __tablename__='purchase'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'))
    product_id = db.Column(db.Integer,db.ForeignKey('product.id'))
    quantity = db.Column(db.Integer, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.now())

class Cart(db.Model):
    __tablename__='cart'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'))
    product_id = db.Column(db.Integer,db.ForeignKey('product.id'))
    quantity = db.Column(db.Integer, nullable=False)

    
