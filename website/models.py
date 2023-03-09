from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class Note(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone = True), default = func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class Upload(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    date = db.Column(db.DateTime(timezone = True), default = func.now())
    participant_id = db.Column(db.String(5))
    task = db.Column(db.String(25))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    num_files = db.Column(db.Integer)
    comment = db.Column(db.String(1500))

    def __repr__(self):
        return f'The {self.task} audio files ({self.num_files}) for participant {self.participant_id} were uploaded on {self.date}'

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(50), unique = True)
    password = db.Column(db.String(50))
    name = db.Column(db.String(50))
    notes = db.relationship('Note')

# I ran the following code to generate a list of random participant ID's, then manually imported it into the database
# df = pd.DataFrame(data = {'id': range(1, 201), 'participant_id': random.sample(range(10000, 100000), k = 200)})
# df.to_csv('participant_id.csv', index = False)
class ParticipantId(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    participant_id = db.Column(db.String(5))
