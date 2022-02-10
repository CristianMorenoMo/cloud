from . import db
from flask_login import UserMixin

class Users(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(200),unique=True)
    first_name = db.Column(db.String(100))
    last_name =  db.Column(db.String(100))
    password = db.Column(db.String(8))
class Contest(db.Model):
    id_contest = db.Column(db.Integer, primary_key=True)
    id_user = db.Column(db.Integer)
    contest_name = db.Column(db.String(100))
    banner_name = db.Column(db.String(100))
    url_contest = db.Column(db.String(100))
    start_date = db.Column(db.DateTime)
    end_date = db.Column(db.DateTime)
    award = db.Numeric(10,2)
    dialog = db.Column(db.String(100))
    desciption = db.Column(db.String(100))
