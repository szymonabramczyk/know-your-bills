from flask_login import UserMixin
from sqlalchemy.sql import func

from . import db


class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    amount = db.Column(db.Float)
    category = db.Column(db.String(150))
    payment_method = db.Column(db.String(30))
    vendor = db.Column(db.String(150))
    description = db.Column(db.String(1000))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    expenses = db.relationship('Expense')
