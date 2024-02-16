
from flask import Blueprint, jsonify, render_template, request
from flask_login import current_user, login_required
from isjcrm.candidat.mashmallow import Mashmallow
from isjcrm.users.mashmallow import Mashmallow as Mashmallow2

from isjcrm.candidat.models import Candidat
from sqlalchemy.exc import SQLAlchemyError

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
    
# @ui_candidats.route("/kanban", methods=['GET'])
# @login_required
# def kanban():
#     username = current_user.username
#     name = current_user.first_name + " " + current_user.last_name
#     kanban = request.args.get('kanban', default= None)
#     try:
#         if Candidat.query.count() != 0:
#             candidats = Candidat.query.filter(Candidat.id_user == username).all()
#             users = User.query.filter(User.role != 'admin' )

#             # Créez un objet candidat_mashmallow en dehors de la boucle avec many=True
#             candidat_mashmallow = Mashmallow(many=True)
#             user_mashmallow = Mashmallow2(many=True)

#             # Utilisez directement la méthode dump pour tout le lot
#             candidats_data = candidat_mashmallow.dump(candidats)
#             users_data = user_mashmallow.dump(users)
            


#             else:
                
#         else:
#             return jsonify(message='Aucun candidats existants')
#     except SQLAlchemyError as e:
#         return jsonify(message="Erreur lors du traitement de la requête")