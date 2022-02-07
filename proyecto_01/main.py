from flask_login import current_user
from flask import Blueprint, render_template
from . import db

main = Blueprint('main', __name__)

@main.route('/')
def index():
    if current_user.is_authenticated is False :
        return render_template('home.html')
    else:
        return render_template('home_login.html')

@main.route('/profile')
def profile():
    return 'Profile'