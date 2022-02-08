from flask_login import current_user
from flask import Blueprint, render_template, request
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
    name_contest = request.form.get('namecontest')
    date_start = request.form.get('datestart')
    date_end = request.form.get('dateend')
    award = request.form.get('award')
    dialog = request.form.get('dialog')
    description = request.form.get('description')
    banner = request.files['file']
    banner.save('mio.png')
    #path_banner =  'path' + 'name'

    return 'ssas'