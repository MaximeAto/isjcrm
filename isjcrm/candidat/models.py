from datetime import datetime
from isjcrm import db


class Candidat(db.Model):
    
    __tablename__ = 'candidat'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nom = db.Column(db.String(50))
    prenom = db.Column(db.String(50))
    email = db.Column(db.String(50), unique=True, nullable=False)
    telephone = db.Column(db.String(30), unique=True, nullable=False)
    telephone_parent = db.Column(db.String(30), nullable=False)
    sexe = db.Column(db.String(10))
    etablissement = db.Column(db.String(50))
    etatcandidature = db.Column(db.String(12))
    classe = db.Column(db.String(50))
    choix = db.Column(db.String(2))
    date_ajout = db.Column(db.DateTime, default=datetime.now)
    pieces_jointes = db.Column(db.String(100))
    id_user = db.Column(db.String(20), db.ForeignKey('user.username'), nullable=False) 
    notifications = db.relationship('Notification', backref='candidat') 


    def to_dict(self):
        return {
            'id': self.id,
            'nom': self.nom,
            'prenom': self.prenom,
            'email': self.email,
            'telephone': self.telephone,
            'classe': self.classe,
            'telephone_parent': self.telephone_parent,
            'sexe': self.sexe,
            'choix': self.choix,
            'etablissement': self.etablissement,
            'etat_candidature': self.etatcandidature,
            'pieces_jointes': self.pieces_jointes,
            'id_user': self.id_user,
            'notifications': [notif.to_dict() for notif in self.notifications],
        }
