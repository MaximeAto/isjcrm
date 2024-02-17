from isjcrm import db


class Task(db.Model):
    
    __tablename__ = 'task'
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)

    titre = db.Column(db.Text, nullable=False)
    objective = db.Column(db.Text)
    deadline = db.Column(db.Date)
    priority = db.Column(db.Integer)
    status = db.Column(db.String(50), default="Not do")
    assigned = db.Column(db.String(50), nullable = False)

    id_user = db.Column(db.String(20), db.ForeignKey('user.username'), nullable=False)
    
    activities = db.relationship('Activity', backref='task') 