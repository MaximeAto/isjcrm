from isjcrm import db

class Modelemail(db.Model):
    
    __tablename__ = 'modelemail'

    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    name = db.Column(db.String(50))
    subject = db.Column(db.String(255))
    body = db.Column(db.Text)
    attachments = db.Column(db.Text)  # En supposant que les pièces jointes soient stockées sous forme de chaîne sérialisée.
    creation_date = db.Column(db.DateTime)
    author = db.Column(db.String(50))
    language = db.Column(db.String(50))
    category = db.Column(db.String(50))

    id_user = db.Column(db.String(20), db.ForeignKey('user.username'), nullable=False)
