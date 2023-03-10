from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for, current_app
from flask_login import login_required, current_user
from .models import Note, Upload, ParticipantId
from .import db
import json
from werkzeug.utils import secure_filename
import os
from .forms import UploadForm, SearchForm

views = Blueprint('views', __name__)

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

@views.route('/upload', methods = ['GET', 'POST'])
@login_required
def upload_file():
    form = UploadForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            files = request.files.getlist('files')
            task = form.task.data.lower().replace(' ', '')
            comment = form.comment.data
            num_files = len(files)
            id = str(form.participant_id.data)
            if all(files) and all([allowed_file(file.filename) for file in files]):
                dir = os.path.join(current_app.config['UPLOAD_FOLDER'], id, task)
                if not os.path.exists(dir):
                    os.makedirs(dir, exist_ok = True)
                print(dir)
                for index, file in enumerate(files, start = 1):
                    ext = file.filename.rsplit('.', 1)[1].lower()
                    filename = '%s_%s_part%dof%d.%s' % (id, task, index, num_files, ext)
                    file.save(os.path.join(dir, filename))
                new_upload = Upload(participant_id = id, 
                                    task = task, 
                                    user_id = current_user.id,
                                    num_files = num_files, 
                                    comment = comment)
                db.session.add(new_upload)
                db.session.commit()
                flash('Upload successful!', category = 'success')
                return redirect(request.url)
        else:
            flash(list(form.errors.values())[0][0], category = 'error')
    # Add autocomplete feature when typing participant ID's

    return render_template('upload.html', user = current_user, form = form)

@views.route('/search', methods = ['GET', 'POST'])
@login_required
def search_upload():
    form = SearchForm()
    if request.method == 'POST': 
        if form.validate_on_submit():
            id = form.participant_id.data
            upload_query = db.session.query(Upload).filter_by(participant_id = id).order_by(Upload.task)
            results = upload_query if upload_query.first() else [f'It looks like no audio files have been uploaded for participant {id}.']
            return render_template('search.html', user = current_user, form = form, results = results)
        else:
            flash(list(form.errors.values())[0][0], category = 'error')
    return render_template('search.html', user = current_user, form = form)

@views.route('/autocomplete')
def autocomplete():
    query = request.args.get('query') # get the user input from the query string
    # use SQL query to retrieve suggestions from database based on the user input
    suggestions = db.session.query(ParticipantId.participant_id).filter(ParticipantId.participant_id.like(f'{query}%')).all()
    id_list = [id[0] for id in suggestions]
    return jsonify(id_list)


@views.route('/', methods = ['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        note = request.form.get('note')
        if len(note) < 1:
            flash('Note is too short!', category = 'error')
        else:
            new_note = Note(data = note, user_id = current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Note added!', category = 'success')
    return render_template('home.html', user = current_user)

@views.route('/delete-note', methods = ['POST'])
def delete_note():
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()
    return jsonify({})
