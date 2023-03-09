from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for, current_app
from flask_login import login_required, current_user
from .models import Note, Upload
from .import db
import json
from werkzeug.utils import secure_filename
import os
from .forms import UploadForm

views = Blueprint('views', __name__)

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

@views.route('/upload', methods = ['GET', 'POST'])
@login_required
def upload_file():
    form = UploadForm()
    if request.method == 'POST':
        print(request.form)
        print(request.json)
        print(request.files.getlist('files'))
        files = request.files.getlist('files')
        task = request.form['task']
        comment = request.form.get('comment', '')
        num_files = len(files)
        id = request.form['participant_id']
        print(task)
        print(comment)
        print(num_files)
        print(id)
        upload_query = db.session.query(Upload).filter_by(participant_id = id, task = task)
        print(upload_query)
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
    '''
        # check if the post request has the file part
        upload_query = db.session.query(Upload).filter_by(Upload.participant_id == id, Upload.task == task)
        # check if a file has already been uploaded for this participant/task
        if upload_query:
            flash('Files have already been uploaded for this participant and task', category = 'error')
        if 'file' not in request.files:
            flash('No file part', category = 'error')
            return redirect(request.url)
        # check if ID is 5 digits
        if len(id) != 5 or not id.isdigit():
            flash('Please enter valid 5-digit ID.', category = 'error')
        # check if task is selected
        elif task == '':
            flash('Please select a task', category = 'error')
        # Check if the user does not select a file, the browser submits an
        # empty file without a filename.
        elif '' in [file.filename for file in files]:
            flash('Please make sure file names are not blank.', category = 'error')
            return redirect(request.url)
        # To add:
        # Update db
    '''

    # Add autocomplete feature when typing participant ID's

    return render_template('upload.html', user = current_user, form = form)

@views.route('/search', methods = ['GET', 'POST'])
@login_required
def search_upload():
    if request.method == 'POST':
        id = request.form['participant-id']
        upload_query = db.session.query(Upload).filter_by(participant_id = id).order_by(Upload.task)
        results = upload_query if upload_query.first() else [f'It looks like no audio files have been uploaded for participant {id}.']
        return render_template('search.html', user = current_user, results = results)
    return render_template('search.html', user = current_user)

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
