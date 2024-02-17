
from flask import Blueprint, jsonify, render_template, request
from flask_login import current_user, login_required
from isjcrm.candidat.mashmallow import Mashmallow
from isjcrm.users.mashmallow import Mashmallow as Mashmallow2

from isjcrm.candidat.models import Candidat
from sqlalchemy.exc import SQLAlchemyError
from isjcrm import db
from isjcrm.users.models import User

ui_candidats = Blueprint('ui_candidats', __name__)

@ui_candidats.route("/get_all_candidates", methods=['GET'])
@login_required
def get_all_candidates():
    username = current_user.username
    name = current_user.first_name + " " + current_user.last_name
    kanban = request.args.get('kanban', default= None)
    
    try:
        if Candidat.query.count() != 0:
            candidats = Candidat.query.filter(Candidat.id_user == username).all()
            users = User.query.filter(User.role != 'admin' )
            nb_etudiants = Candidat.query.filter_by(etatcandidature='ETUDIANT').count()
            nb_nouveaux = Candidat.query.filter(Candidat.id_user == username).count() - nb_etudiants

            # Créez un objet candidat_mashmallow en dehors de la boucle avec many=True
            candidat_mashmallow = Mashmallow(many=True)
            user_mashmallow = Mashmallow2(many=True)

            # Utilisez directement la méthode dump pour tout le lot
            candidats_data = candidat_mashmallow.dump(candidats)
            users_data = user_mashmallow.dump(users)
            
            if kanban:
                return render_template("candidates/candidates_list.html",
                        user_id = username,
                        kanban = kanban,
                        name = name,
                        candidates_data = candidats_data,
                        users_data = users_data,
                        candidates_active = "active"
                        )

            return render_template("candidates/candidates_list.html",
                    name = name,
                    candidates_data = candidats_data,
                    users_data = users_data,
                    nb_nouveaux = nb_nouveaux,
                    nb_etudiants = nb_etudiants,
                    candidates_active = "active"
                    )
        else:
            return render_template("candidates/candidates_list.html",
                    name = name,
                    candidates_active = "active"
                    )
    except SQLAlchemyError as e:
        return jsonify(message="Erreur lors du traitement de la requête")
    
@ui_candidats.route("/add_candidate", methods=['POST', 'GET'])
@login_required
def add_candidate():
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
    etat_candidature = request.form.get('etat_candidature')
    id_user= request.form.get('id_user')

    candidate_info = Candidat(
        nom= nom,
        prenom= prenom,
        email= email,
        telephone= telephone,
        telephone_parent= telephone_parent,
        classe= classe,
        choix= choix,
        etatcandidature= etat_candidature,
        pieces_jointes =  pieces_jointes ,
        id_user= id_user,
        sexe = sexe,
        etablissement = etablissement
    )

    db.session.add(candidate_info)
    db.session.commit() 

    return render_template("candidates/addcandidates.html")


@ui_candidats.route("/addpage", methods=['POST', 'GET'])
@login_required
def addpage():
    username = current_user.username
    name = current_user.first_name + " " + current_user.last_name
    return render_template("candidates/addcandidate.html",
                           name = name)
    