from isjcrm import db


class Activity(db.Model):

    __tablename__ = 'activity'

    id = db.Column(db.Integer, primary_key=True)
    activity_type = db.Column(db.String(50))
    deadline = db.Column(db.DateTime)
    priority = db.Column(db.Integer)
    status = db.Column(db.String(50))
    description = db.Column(db.String(255))

    id_task = db.Column(db.Integer, db.ForeignKey('task.id'), nullable=False)
    # task = db.relationship('Task', backref='activities') 