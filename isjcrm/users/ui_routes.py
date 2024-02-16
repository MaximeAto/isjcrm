from flask import Blueprint, flash, jsonify, redirect, render_template, request, url_for
from flask_login import login_required, login_user, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.exc import SQLAlchemyError
from isjcrm.candidat.models import Candidat
from isjcrm.roles.roles import Roles
from isjcrm.users.models import User
from isjcrm.candidat.mashmallow import Mashmallow
from isjcrm.users.mashmallow import Mashmallow as mashmallow2
from isjcrm import db

ui_users = Blueprint('ui_users', __name__)


@ui_users.route("/dashboard", methods=["GET", "POST"])
@login_required
def dashboard():
    name = current_user.first_name + " " + current_user.last_name
    try:
    
        candidats = Candidat.query.filter(Candidat.id_user == current_user.username).limit(10).all()
        nb_etudiants = Candidat.query.filter_by(etatcandidature='ETUDIANT').count()
        nb_nouveaux = Candidat.query.filter().count() - nb_etudiants


        # Créez un objet candidat_mashmallow en dehors de la boucle avec many=True
        candidat_mashmallow = Mashmallow(many=True)

        # Utilisez directement la méthode dump pour tout le lot
        candidates_data = candidat_mashmallow.dump(candidats)
        return render_template("index.html",
                                name = name,
                                candidates_data = candidates_data,
                                nb_nouveaux = nb_nouveaux,
                                nb_etudiants = nb_etudiants,
                                dashboard_active = "active"
                                )
    except SQLAlchemyError as e:
        return jsonify(message="Erreur lors du traitement de la requête")
    
@ui_users.route("/team", methods=["GET", "POST"])
@login_required
def team():
    name = current_user.first_name + " " + current_user.last_name
    try:
        members = User.query.filter(User.role == "tm").all()
        # Créez un objet candidat_mashmallow en dehors de la boucle avec many=True
        user_mashmallow = mashmallow2(many=True)

        # Utilisez directement la méthode dump pour tout le lot
        users_data = user_mashmallow.dump(members)
        return render_template("team/members_list.html", name = name, team_active = "active", members = users_data)
    except SQLAlchemyError as e:
        return jsonify(message="Erreur lors du traitement de la requête")

@ui_users.route("/member_details/<string:username>", methods=["GET", "POST"])
@login_required
def member_details(username):
    name = current_user.first_name + " " + current_user.last_name
    try:
        user_found = User.query.filter(User.username == username).first()
        candidats = Candidat.query.filter(Candidat.id_user == username).all()
        nb_etudiants = Candidat.query.filter_by(etatcandidature='ETUDIANT', id_user = username ).count()
        nb_nouveaux = len(candidats) - nb_etudiants

        # Créez un objet candidat_mashmallow en dehors de la boucle avec many=True
        candidat_mashmallow = Mashmallow(many=True)

        # Utilisez directement la méthode dump pour tout le lot
        candidates_data = candidat_mashmallow.dump(candidats)
        return render_template("team/members_details.html",
                                name = name,
                                user_name = user_found.first_name + " " + user_found.last_name,
                                candidates_data = candidates_data,
                                nb_nouveaux = nb_nouveaux,
                                nb_etudiants = nb_etudiants,
                                team_active = "active"
                                )
    except SQLAlchemyError as e:
        return jsonify(message="Erreur lors du traitement de la requête")
    

@ui_users.route("/login", methods=["GET", "POST"])
def login():
        try:
            data = request.form

            # verification de la conformité des informations
            if any(value == '' for value in data.values()):
                return jsonify({'error': 'Missing data'}), 400
            
            user_find = User.query.filter_by(username=data.get("user-name")).first()
            if user_find and check_password_hash(user_find.password, data.get("user-password")):
                login_user(user_find) 
                return jsonify(message= "/dashboard"),200
            else:
                return jsonify(message="Utilisateur introuvable"),404
        except SQLAlchemyError as e:
            return jsonify(message="Erreur lors de la connexion"),500
        
@ui_users.route("/signup", methods=["GET", "POST"])
def signup():
    try:
        data = request.form
        user_find = User.query.filter_by(username=data.get("username")).first()
        phone_number_find = User.query.filter_by(phone_number= data.get("phone_number")).first()
        email_find = User.query.filter_by(email= data.get("email")).first()

        # verification de la conformité des informations
        if any(value == '' for value in data.values()):
            return jsonify({'error': 'Missing data'}), 400

        if user_find:
            return jsonify(message='L\'utilisateur existe déjà'), 409
        
        if email_find:
            return jsonify(message='Ce mail est déjà utilisé'), 409
        
        if phone_number_find:
            return jsonify(message='Ce numéro est déjà utilisé'), 409
        
        # Sécurité du mot de passe
        hashed_password = generate_password_hash(data.get('password'), method='pbkdf2:sha256',  salt_length=8)

        admin = User(
            username= data.get("username"),
            password= hashed_password,
            first_name=data.get("first_name"),
            last_name=data.get("last_name"),
            email=data.get("email"),
            phone_number=data.get("phone_number"),
            role= Roles.ADMIN
        )
    
        db.session.add(admin)
        db.session.commit()
        login_user(admin) 
        return jsonify(message= "/dashboard"),200
    except SQLAlchemyError as e:
        print(e)
        return jsonify(message='Erreur lors de l\'inscription'), 500
    # return render_template("login/register.html")



@ui_users.route("/logout")
@login_required
def logout():
    logout_user()
    return render_template("login/login.html")