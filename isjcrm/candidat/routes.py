from datetime import datetime
from flask import Blueprint, current_app, jsonify, request
from flask_login import current_user
from isjcrm import db
from .mashmallow import Mashmallow
from sqlalchemy.exc import SQLAlchemyError
from isjcrm.candidat.models import Candidat
from flask_mail import Message

from faker import Faker



candidats = Blueprint('candidats', __name__)
fake = Faker()

# Fonction pour créer et ajouter un candidat à la base de données
#################################################################################################################################
def create_fake_candidat():
    current_date = datetime.now().date().strftime('%Y-%m-%d')
    candidat = Candidat(
        nom=fake.last_name(),
        prenom=fake.first_name(),
        email=fake.email(),
        telephone=fake.phone_number(),
        telephone_parent=fake.phone_number(),
        sexe=fake.random_element(elements=('M', 'F')),
        etablissement=fake.random_element(elements = ('LLG', 'H4', 'JdS', 'LLG', 'LF', 'LC', 'LM', 'LC', 'SL', 'LL')),
        etatcandidature= "NOUVEAU",
        classe=fake.random_element(elements=('Première', 'Terminale')),
        choix=fake.random_element(elements=('1', '2','3')),
        pieces_jointes=fake.file_name(),
        id_user=fake.random_element(elements=('maxato', 'jessicalawson','tammy74','kelly18')),
        date_ajout=current_date
    )
    db.session.add(candidat)
    db.session.commit()
    
# Créer 100 candidats
@candidats.route("/hundred_candidates", methods=['POST'])
def hundred_candidates():
    for _ in range(100):
        create_fake_candidat()
    return jsonify(message = "les 100 candidats ont été enregistré")
#################################################################################################################################



@candidats.route("/create_candidate", methods=['POST','GET'])
def create_candidate():
    nom = request.form.get('nom')
    prenom = request.form.get('prenom')
    email = request.form.get('email')
    telephone = request.form.get('telephone')
    telephone_parent = request.form.get('telephone_parent')
    sexe = request.form.get('sexe')
    choix = request.form.get('choix')
    classe = request.form.get('classe')
    etablissement = request.form.get('etablissement')
    pieces_jointes  = request.form.get('pieces')
    id_user= request.form.get('id_user')

    candidate_info = Candidat(
        nom= nom,
        prenom= prenom,
        email= email,
        telephone= telephone,
        telephone_parent= telephone_parent,
        classe= classe,
        choix= choix,
        etatcandidature= "NOUVEAU",
        pieces_jointes =  pieces_jointes ,
        id_user= current_user.username,
        sexe = sexe,
        etablissement = etablissement
    )

    db.session.add(candidate_info)
    db.session.commit() 

    return jsonify(message='Candidat enregistré'), 200
    

@candidats.route("/delete_candidate/<int:candidate_id>", methods=['DELETE'])
def delete_candidate(candidate_id):
    try:
        candidat = Candidat.query.get(candidate_id)
        if not candidat :
            return jsonify(message='candidat introuvable'), 404
        
        db.session.delete(candidat)
        db.session.commit()

        return jsonify(message='Suppression réussi'), 200
    except SQLAlchemyError as e :
        return jsonify(message='erreur lors de la suppression'), 500

@candidats.route("/update_candidate/<candidat_id>", methods=['PUT'])
def update_candidate_info(candidat_id):
    try:
        data = request.form

        candidat = Candidat.query.get(candidat_id)

        if not candidat:
            return jsonify(message='Candidat non trouvé'), 404


        if 'email' in data:
            email_find = Candidat.query.filter(Candidat.id != candidat_id, Candidat.email == data.get('email')).first()
            if email_find:
                return jsonify(message='Ce mail est déjà utilisé par un autre candidat'), 409
            candidat.email = data.get('email')

        if 'telephone' in data:
            telephone_find = Candidat.query.filter(Candidat.id != candidat_id, Candidat.telephone == data.get('telephone')).first()
            if telephone_find:
                return jsonify(message='Ce numéro est déjà utilisé'), 409
            candidat.telephone = data.get('telephone')

        candidat.nom = data.get('nom')
        candidat.prenom = data.get('prenom')
        candidat.adresse = data.get('adresse')
        candidat.datenaissance = data.get('date_naissance')
        candidat.sexe = data.get('sexe')
        candidat.etablissement = data.get('etablissement')
        candidat.lieunaissance = data.get('lieu_naissance')
        candidat.etatcandidature = data.get('etat_candidature')
    
        db.session.commit()
        return jsonify({'message': 'Le candidat a été mis à jour'}), 200

    except SQLAlchemyError as e:
        return jsonify(message='Erreur lors de la mise à jour du candidat'), 500

@candidats.route("/update_status/<int:candidat_id>/<string:etat>", methods=['PUT'])
def update_status(candidat_id, etat):
    try:
        candidat = Candidat.query.get(candidat_id)

        if candidat:
            candidat.etatcandidature = etat
            db.session.commit()
            return jsonify(message = "Mise à jour réussie de l'étatcandidature.")
        else:
            return jsonify(message = "Candidat non trouvé."), 404

    except Exception as e:
        return jsonify(message = f"Erreur lors de la mise à jour : {str(e)}"), 500

@candidats.route("/get_all_candidates/<user_id>", methods=['GET'])
def get_all_candidates(user_id):
    try:
        if Candidat.query.count() != 0:
            candidats = Candidat.query.filter(Candidat.id_user == user_id).all()

            # Créez un objet candidat_mashmallow en dehors de la boucle avec many=True
            candidat_mashmallow = Mashmallow(many=True)

            # Utilisez directement la méthode dump pour tout le lot
            candidats_data = candidat_mashmallow.dump(candidats)

            return jsonify(candidats_data)
        else:
            return jsonify(message='Aucun candidats existants')
    except SQLAlchemyError as e:
        return jsonify(message="Erreur lors du traitement de la requête")
    

@candidats.route("/get_candidate_by_id/<int:candidate_id>", methods=['GET'])
def get_candidate_by_id(candidate_id):
    try:
        candidat_find = Candidat.query.filter_by(id=candidate_id).first()
        if candidate_id:
            candidat = Mashmallow()
            candidat_data = candidat.dump(candidat_find)
            return jsonify(candidat_data)
        else:
            return jsonify(message = 'candidat introuvable')
    except SQLAlchemyError as e :
       return jsonify(message='erreur lors du traitement de votre requête')

@candidats.route("/move_candidate_to_stage/<newstage>/<int:candidate_id>", methods=['PUT'])
def move_candidate_to_stage(candidate_id, newstage):
    try:
        candidat = Candidat.query.get(candidate_id)

        if not candidat:
            return jsonify(message='Candidat non trouvé'), 404
        
        candidat.etatcandidature = newstage
        db.session.commit()
        return "good"
    except SQLAlchemyError as e:
        return jsonify(message='Erreur lors de la mise à jour du candidat'), 500

   

@candidats.route("/send_email_to_candidate/<int:candidate_id>", methods=['GET'])
def send_email_to_candidate(candidate_id):
    candidat = Candidat.query.filter_by(id=candidate_id).first()
    mail = current_app.extensions['mail']

    msg = Message('Mail de test', 
                  sender='melainenkeng@gmail.com',
                  recipients=[candidat.email])
    msg.body = 'Bonjour toi ! ici c\'est un mail de test'
    
    mail.send(msg)

    return "Message envoyé"

@candidats.route("/send_sms_to_candidate/<int:candidate_id>", methods=['GET'])
def send_sms_to_candidate(candidate_id):
    pass