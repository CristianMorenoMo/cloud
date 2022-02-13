from flask_login import current_user
from flask import Blueprint, render_template, request, flash, redirect, url_for
import uuid
from datetime import datetime
from .models import Contest, Users, Proposal


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
        return redirect(url_for('main.home'))
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
    banner.save( '/home/jaimeforero/cloud/proyecto_01/uploads/images' + filename)
    flash('evento cargado.')
    return redirect(url_for('main.index'))


@main.route('/apply/')
@main.route('/apply/<id>')
def apply(id):
    print(id)
    query = Contest.query.filter_by(id_contest=id).first()
    return render_template('apply.html',items=query)

@main.route('/applied', methods=['POST'])
def applied_post():
    contest_id = request.form.get('id_contest')
    proposal_name = request.form.get('nameproposal')
    proposal_email = request.form.get('email')
    date = request.form.get('datestart')
    observacion = request.form.get('observacion')
    song = request.files['file']
    proposal_formato = song.filename.split('.')[-1]
    song_filename = str(uuid.uuid1()) + '.' + song.filename.split('.')[-1]
    if proposal_formato=='mp3':
        song.save( '/home/jaimeforero/cloud/proyecto_01/uploads/dialog_song_convert/' + song_filename)
        state_voice='convert'
    else:
        song.save( '/home/camilo/Documents/cloud/proyecto_01/uploads/dialog_song/' + song_filename)
        state_voice='in process'
    new_proposal = Proposal(id_contest = contest_id,
                            full_name_speaker = proposal_name,
                            email= proposal_email,
                            dialogo_sound=song_filename,
                            create_date=datetime.strptime(str(date),"%Y-%m-%d"),
                            formato=proposal_formato,
                            state_voice=state_voice,
                            observacion=observacion)
    db.session.add(new_proposal)
    db.session.commit()
    
    flash('applied.')
    return redirect(url_for('main.home'))



@main.route('/view_contest/<id>',methods=['GET', 'POST'])
def view_contest(id):
    query = Contest.query.filter_by(id_contest=id).all()
    return render_template('view_contest.html',query=query)

@main.route('/edit_contest/<id>', methods=['GET','POST'])
def edit_contest(id):
    dict = request.form.to_dict()
    dict_filter ={k: v for k, v in dict.items() if len(v)!=0}
    Contest.query.filter(Contest.id_contest == id).update(dict_filter,synchronize_session = False)
    db.session.commit()
    flash('evento editado.')
    return redirect(url_for('main.index'))

@main.route('/delete_contest/<id>', methods=['GET','POST'])
def delete_contest(id):
    Contest.query.filter_by(id_contest=id).delete()
    db.session.commit()
    flash('Evento eliminado.')
    return redirect(url_for('main.index'))

