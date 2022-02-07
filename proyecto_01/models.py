from . import db
from flask_login import UserMixin

class Users(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(200),unique=True)
    first_name = db.Column(db.String(100))
    last_name =  db.Column(db.String(100))
    password = db.Column(db.String(8))