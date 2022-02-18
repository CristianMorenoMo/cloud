from flask_login import current_user
from flask import Blueprint, render_template, request, flash, redirect, url_for
import uuid
from datetime import datetime
from .models import Contest, Proposal
import os
from . import db

main = Blueprint('main', __name__)
path_root = os.path.abspath(os.curdir)

@main.route('/home')
def home():
    table=Contest.query.order_by(Contest.start_date).all()
    return render_template('home.html', items=table)

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
    banner.save( path_root+ '/proyecto_01/static/uploads/images' + filename)
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
    flash('evento cargado.')
    return redirect(url_for('main.index'))

@main.route('/view_contest/<id>',methods=['GET', 'POST'])
def view_contest(id):
    query = Contest.query.filter_by(id_contest=id).all()
    query_speaker = Proposal.query.filter_by(id_contest=id).order_by(Proposal.create_date.desc()).all()
    return render_template('view_contest.html',query=query, speaker =query_speaker)

@main.route('/edit_contest/<id>', methods=['GET', 'POST'])
def edit_contest(id):
    dict = request.form.to_dict()
    if dict['start_date']!='':
        dict['start_date'] = datetime.strptime(dict['start_date'],"%Y-%m-%d")
    if dict['end_date'] !='':
        dict['end_date'] = datetime.strptime(dict['end_date'],"%Y-%m-%d")
    dict_filter = {k: v for k, v in dict.items() if len(str(v)) != 0}
    Contest.query.filter(Contest.id_contest == id).update(dict_filter,synchronize_session = False)
    db.session.commit()
    flash('evento editado.')
    return redirect(url_for('main.index'))

@main.route('/delete_contest/<id>', methods=['POST'])
def delete_contest(id):
    Contest.query.filter_by(id_contest=id).delete()
    db.session.commit()
    flash('Evento eliminado.')
    return redirect(url_for('main.index'))


@main.route('/apply/<id>')
def apply(id):
    query = Contest.query.filter_by(id_contest=id).first()
    query_speaker = Proposal.query.filter_by(id_contest=id).order_by(Proposal.create_date.desc()).all()
    return render_template('apply.html',items=query, speaker=query_speaker)

@main.route('/apply', methods=['GET','POST'])
def applied_post():
    id_contest = request.form.get('id_contest')
    email = request.form.get('email')
    query_user = Proposal.query.filter_by(id_contest=id_contest,email=email).first()
    if query_user is not None:
        flash('el usuario ya aplico a este evento')
        print('usuatrio error')
        return redirect(url_for('main.index'))
    song = request.files['file']
    if len(song.filename)==0:
        flash('el usuario debe adjuntar un audio')
        print('no audio')
        return redirect(url_for('main.index'))
    proposal_formato = song.filename.split('.')[-1]
    song_filename = str(uuid.uuid1()) + '.' + song.filename.split('.')[-1]
    if proposal_formato == 'mp3':
        song.save(path_root + '/proyecto_01/static/uploads/dialog_song_convert/' + song_filename)
        state_voice = 'convert'
        dialogo_sound_convert = song_filename
    else:
        song.save(path_root + '/proyecto_01/static/uploads/dialog_song/' + song_filename)
        state_voice = 'in process'
        dialogo_sound_convert = None
    new_proposal = Proposal(id_contest = int(id_contest),
                            create_date= datetime.now(),
                            full_name_speaker = request.form.get('nameproposal'),
                            email= email,
                            dialogo_sound= song_filename,
                            dialogo_sound_convert= dialogo_sound_convert,
                            formato=proposal_formato,
                            state_voice=state_voice,
                            observacion=request.form.get('observacion'))
    db.session.add(new_proposal)
    db.session.commit()
    flash('applied.')
    redirect(url_for('main.applied_post'))
    return redirect(url_for('main.home'))