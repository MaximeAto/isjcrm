from flask_login import UserMixin
from isjcrm import db

class User(db.Model,UserMixin):
    
    __tablename__ = 'user'
    
    username = db.Column(db.String(20),  primary_key=True,unique=True, nullable=False)
    password = db.Column(db.String(100))
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    email = db.Column(db.String(50), unique=True, nullable=False)
    phone_number = db.Column(db.String(30), unique=True, nullable=False)
    role = db.Column(db.String(10))
    candidats = db.relationship('Candidat', backref='user') 
    model_emails = db.relationship('Modelemail', backref='user') 
    tasks = db.relationship('Task', backref='user') 
    notifications = db.relationship('Notification', backref='user') 


    def get_id(self):
        return str(self.username)

    def is_active(self):
        return True 