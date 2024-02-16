from datetime import datetime
from isjcrm import db


class Notification(db.Model):
    
    __tablename__ = 'notification'
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    
    notification_type = db.Column(db.String(50))
    content = db.Column(db.String(255))
    recipient = db.Column(db.String(50))
    sender = db.Column(db.String(50))
    attachment = db.Column(db.String(255))
    timestamp = db.Column(db.DateTime, default=datetime.now)

    id_user = db.Column(db.String(20), db.ForeignKey('user.username'), nullable=True)

    id_candidat = db.Column(db.Integer, db.ForeignKey('candidat.id'), nullable=True)