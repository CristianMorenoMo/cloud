from flask_login import current_user
from flask import Blueprint, render_template, request, flash, redirect, url_for
import uuid
from datetime import datetime
from .models import Contest, Users

from werkzeug.utils import secure_filename

from . import db
import os

main = Blueprint('main', __name__)

@main.route('/home')
def home():
    folder_name=os.path.join('static','imagen1.jpeg')
    table=Contest.query.order_by(Contest.start_date).all()
    
    return render_template('home.html',imagen_muestra=folder_name,items=table)

@main.route('/')
def index():
    if current_user.is_authenticated is False:
        return render_template('home.html')
    else:
        query=Contest.query.filter_by(id_user=current_user.id).all()
        return render_template('home_login.html',query = query)

@main.route('/create_contest')
def create_contest():
    return render_template('create_contest.html')

@main.route('/create_contest', methods=['POST'])
def create_contest_post():
    contest_name = request.form.get('namecontest')
    start_date = request.form.get('datestart')
    end_date = request.form.get('dateend')
    award = request.form.get('award')
    dialog = request.form.get('dialog')
    description = request.form.get('description')
    banner = request.files['file']
    filename = str(uuid.uuid1()) + '.' + banner.filename.split('.')[-1]
    new_contest = Contest(id_user = current_user.id,
                            contest_name = contest_name,
                            banner_name=filename,
                            url_contest='192.168.0.1:8080/abcd',
                            start_date=datetime.strptime(str(start_date),"%Y-%m-%d"),
                            end_date=datetime.strptime(str(end_date),"%Y-%m-%d"),
                            award=float(award),
                            dialog=dialog,
                            desciption=description)
    db.session.add(new_contest)
    db.session.commit()
    banner.save( '/home/camilo/Documents/cloud/proyecto_01/uploads/images/' + filename)
    flash('evento cargado.')
    return redirect(url_for('main.index'))


@main.route('/apply/')
@main.route('/apply/<id>')
def apply(id):
    print(id)
    query = Contest.query.filter_by(id_contest=id).first()
    return render_template('apply.html',items=query)

@main.route('/applied/<id>', methods=['POST'])
def apply_post(id):
    contest_id=id
    apply_name = request.form.get('namecontest')
    apply_email = request.form.get('email')
    new_apply= Contest(id_user = current_user.id,
                            apply_name = apply_name,
                            apply_email= apply_email)
    db.session.add(new_apply)
    db.session.commit()
    banner.save( '/home/camilo/Documents/cloud/proyecto_01/uploads/images/' + filename)
    flash('evento cargado.')
    return redirect(url_for('main.home'))



@main.route('/view_contest')
def view_contest():
    return render_template('view_contest.html')

@main.route('/edit_contest')
def edit_contest():
    query= Contest.query.filter_by(id_contest=1).all()
    return render_template('edit_contest.html',query=query)

@main.route('/edit_contest',methods=['POST'])
def edit_contest_post():

    dict = request.form.to_dict()
    dict_filter ={k: v for k, v in dict.items() if len(v)!=0}

    #Contest.query.filter(id_contest == client_id_list).update(dict_filter)
    #db.session.commit()
    return redirect(url_for('main.index'))
@main.route('/delete/<id>')
def delete(id):
    'aa'
    #task = Contest.query.filter_by(id_contest=id).delete()
    #db.session.commit()
    #return redirect(url_for('main.index'))