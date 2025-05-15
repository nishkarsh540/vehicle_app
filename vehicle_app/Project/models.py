from flask_login import UserMixin
from . import db
from flask import current_app

class User(db.Model,UserMixin):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(100),nullable=False)
    username = db.Column(db.String(100),nullable=False,unique=True)
    password = db.Column(db.String(100),nullable=False)
    role = db.Column(db.Numeric())

# admin role = 0 , customer = 1
    @staticmethod
    def create_dummy_admin():
        with current_app.app_context():
            if User.query.filter_by(username='admin').first() is None:
                admin_user = User(name='admin',username='admin',password='admin',role=0)

                db.session.add(admin_user)
                db.session.commit()

                print('Admin user created')

            else:
                print('Admin already exists')

class Category(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String,nullable=False)

    def can_be_deleted(self):
        return len(self.product) == 0

class Products(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String,nullable=False)
    category_id = db.Column(db.Integer,db.ForeignKey('category.id'))
    category = db.relationship('Category',backref=db.backref('product',lazy=True))