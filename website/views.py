from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for, current_app
from flask_login import login_required, current_user
from .models import Note
from .import db
import json
from werkzeug.utils import secure_filename
import os

views = Blueprint('views', __name__)

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

@views.route('/', methods = ['GET', 'POST'])
@login_required
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part', category = 'error')
            return redirect(request.url)
        files = request.files.getlist('file')
        task = request.form['task']
        id = request.form['participant-id']
        num_files = len(files)
        # check if ID is 5 digits
        if len(id) != 5 or not id.isdigit():
            flash('Please enter valid 5-digit ID.', category = 'error')
        # check if task is selected
        if task == '':
            flash('Please select a task', category = 'error')
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if '' in [file.filename for file in files]:
            flash('Please make sure file names are not blank.', category = 'error')
            return redirect(request.url)
        if all(files) and all([allowed_file(file.filename) for file in files]):
            dir = os.path.join(current_app.config['UPLOAD_FOLDER'], task, id)
            if not os.path.exists(dir):
                os.mkdir(dir)
            for index, file in enumerate(files, start = 1):
                ext = file.filename.rsplit('.', 1)[1].lower()
                filename = '%s_%s_part%dof%d.%s' % (id, task, index, num_files, ext)
                file.save(dir, filename)
            flash('Upload successful!', category = 'success')
            return redirect(request.url)
        
        # Other conditions:
        # File hasn't already been uploaded

        # To add:
        # Update db


    return render_template('home.html', user = current_user)

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
