from flask import Blueprint, render_template, request, url_for, redirect, flash
from .models import Users
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user,logout_user
from . import db


auth = Blueprint('auth', __name__)

@auth.route('/login')
def login():
    return render_template('login.html')

@auth.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False
    user = Users.query.filter_by(email=email).first()
    if not user or not check_password_hash(user.password, password):
        flash('Please check your login details and try again.')
        return redirect(url_for('auth.login'))
    login_user(user, remember=remember)
    return redirect(url_for('main.index'))


@auth.route('/signup')
def signup():
    return render_template('signup.html')

@auth.route('/signup', methods=['POST'])
def signup_post():
    email = request.form.get('email')
    password = request.form.get('password')
    confirm_password = request.form.get('conpassword')
    query = Users.query.filter_by(email=email).first()
    if query is not None:
        flash('Email address already exists')
        return redirect(url_for('auth.signup'))
    if password != confirm_password:
        flash('password mal')
        return redirect(url_for('auth.signup'))

    new_user = Users(email = email,
                     first_name = request.form.get('firstname'),
                     last_name = request.form.get('lastname'),
                     password = generate_password_hash(password, method='sha256')
                )
    db.session.add(new_user)
    db.session.commit()
    return redirect(url_for('auth.login'))

@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))
