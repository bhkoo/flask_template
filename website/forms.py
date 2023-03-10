from flask_wtf import FlaskForm
from flask_wtf.file import FileRequired, FileAllowed
from wtforms import (StringField, TextAreaField, IntegerField, SubmitField,
                     PasswordField, RadioField, MultipleFileField)
from wtforms.validators import InputRequired, Length, NumberRange, Email, DataRequired, EqualTo, ValidationError
from .models import User, Upload, ParticipantId

def validate_id(self, field):
    if not ParticipantId.query.filter_by(participant_id = field.data).first():
        raise ValidationError('The ID you entered is not in the list of valid participant IDs.')

def validate_email_registered(self, field):
    if not User.query.filter_by(email = field.data).first():
        raise ValidationError('Email address not registered.')

def validate_new_email(self, field):
    if User.query.filter_by(email = field.data).first():
        raise ValidationError('Email address already in use.')


class SignupForm(FlaskForm):
    name = StringField('Name', validators = [InputRequired(), Length(min = 2, max = 40)])
    email = StringField('Email', validators = [InputRequired(), Length(max = 50), 
                                               Email('Please enter a valid email address.'),
                                               validate_new_email])
    password = PasswordField('Password', validators = [DataRequired(),
                                                       EqualTo('confirm', message = 'Passwords must match')])
    confirm = PasswordField('Confirm Password')
    submit = SubmitField('Submit')

class LoginForm(FlaskForm):
    email = StringField('Email', validators = [InputRequired(), Length(max = 50), Email('Please enter a valid email address.'),
                                               validate_email_registered])
    password = PasswordField('Password', validators = [DataRequired()])
    submit = SubmitField('Submit')

class UploadForm(FlaskForm):
    def validate_upload(self, field):
        task = self.task.data.lower().replace(' ', '')
        if Upload.query.filter_by(participant_id = self.participant_id.data, task = task).first():
            raise ValidationError('This participant\'s audio files have already been uploaded for this task.')
    
    participant_id = IntegerField('Participant ID', validators = [InputRequired(message = 'Please enter a valid participant ID.'),
                                                                  NumberRange(min = 10000, max = 99999,
                                                                              message = 'Please enter a valid participant ID.'),
                                                                  validate_id,
                                                                  validate_upload])
    task = RadioField('Select a Task',
                      choices = ['Task 1', 'Task 2', 'Task 3'],
                      validators = [InputRequired(message = 'Please select a task.')])
    comment = TextAreaField('Comment', validators = [Length(max = 1500)])
    files = MultipleFileField('Upload mp3 file(s)', validators = [FileAllowed(['mp3'], '.mp3 only!')])
    submit = SubmitField('Submit')

class SearchForm(FlaskForm):
    participant_id = IntegerField('Participant ID', validators = [InputRequired(message = 'Please enter a valid participant ID.'),
                                                                  validate_id])
    submit = SubmitField('Submit')