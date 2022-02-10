from flask_login import current_user
from flask import Blueprint, render_template, request, flash, redirect, url_for
import uuid
from datetime import datetime
from .models import Contest, Users

from werkzeug.utils import secure_filename

from . import db

main = Blueprint('main', __name__)

@main.route('/')
def index():
    if current_user.is_authenticated is False:
        return render_template('home.html')
    else:
        return render_template('home_login.html')

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
    banner.save( '/home/camilo/Documents/cloud/proyecto_01/uploads/images/' + filename)
    new_contest = Contest(id_user = current_user.id,
                            contest_name = contest_name,
                            banner_name=filename,
                            url_contest='192.168.0.1:8080/abcd',
                            start_date=datetime.strptime(start_date,format='%Y-%m-%d'),
                            end_date=datetime.strptime(end_date,format='%Y-%m-%d'),
                            award=float(award),
                            dialog=dialog,
                            description=description)
    db.session.add(new_contest)
    db.session.commit()
    flash('evento cargado.')
    return redirect(url_for('main.index'))