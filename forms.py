from flask_wtf import FlaskForm
from flask_wtf.file import FileRequired, FileAllowed
from wtforms import (StringField, TextAreaField, IntegerField, BooleanField,
                     RadioField, MultipleFileField)
from wtforms.validators import InputRequired, Length, NumberRange

class UploadForm(FlaskForm):
    participant_id = IntegerField('Participant ID', validators = [InputRequired(),
                                                                  NumberRange(min = 10000, max = 99999)])
    task = RadioField('Select a Task',
                      choices = ['Task 1', 'Task 2', 'Task 3'],
                      validators = [InputRequired()])
    comment = TextAreaField('Comment', validators = [Length(max = 1500)])
    files = MultipleFileField('Upload mp3 file(s)', validators = [FileRequired(), FileAllowed(['mp3'], '.mp3 only!')])