from flask import Blueprint, jsonify, request
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.exc import SQLAlchemyError
from flask_login import logout_user
from isjcrm.roles.roles import Roles
from isjcrm.users.models import User
from isjcrm import db, mail
from .mashmallow import Mashmallow
from flask_mail import Message
from faker import Faker
import secrets
import string

users = Blueprint('users', __name__)
fake = Faker()
##############################################################################################################################

def create_fake_user():
    hashed_password = generate_password_hash("10322Isjcrm#", method='pbkdf2:sha256',  salt_length=8)
    user = User(
        username=fake.user_name(),
        password= hashed_password,
        first_name=fake.first_name(),
        last_name=fake.last_name(),
        email=fake.email(),
        phone_number=fake.phone_number(),
        role= "tm",  # Remplacez cela par vos rôles spécifiques
    )
    db.session.add(user)
    db.session.commit()

@users.route("/ten_users",methods=["POST"])
def ten_users():
    for _ in range(3):
        create_fake_user()
    return jsonify(message = "les 3 users ont été enregistré")

##############################################################################################################################
@users.route("/logout")
def logout():
    return jsonify({'message': 'Logout successful'})

@users.route("/login", methods=["GET"])
def user_login():
    try:
        data = request.form

        # verification de la conformité des informations
        if any(value == '' for value in data.values()):
            return jsonify({'error': 'Missing data'}), 400
        
        user_find = User.query.filter_by(username=data.get("username")).first()
        if user_find and check_password_hash(user_find.password, data.get("password")):
            return jsonify(message='ok')
        else:
            return jsonify(message='utilisateur introuvable')
    except SQLAlchemyError as e:
        return jsonify(message='Erreur lors de connexion'), 500
        
@users.route("/register", methods=["POST","GET"])
def register_user():   
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
        return jsonify({'message': 'utilisateur enregistré'}), 200
    except SQLAlchemyError as e:
        return jsonify(message='Erreur lors de l\'inscription'), 500
    
@users.route("/get_user_by_id/<user_id>", methods=["GET"])
def get_user_by_id(user_id):
    try:
        user_find = User.query.filter_by(username=user_id).first()
        if user_find:
            user = Mashmallow()
            user_data = user.dump(user_find)
            return jsonify(user_data)
        else:
            return jsonify(message = 'utilisateur introuvable')
    except SQLAlchemyError as e :
       return jsonify(message='erreur lors du traitement de votre requête')

@users.route("/update_user/<username>", methods=["PUT"])
def update_user(username):

    try:
        data = request.form

        user = User.query.get(username)

        if not user:
            return jsonify(message='Utilisateur introuvable'), 404

        if 'username' in data:
            username_find = User.query.filter(User.username == data.get('username')).first()
            if username_find:
                user.username = data.get('username')

        if 'email' in data:
            email_find = User.query.filter(User.username != data.get('username'), User.email == data.get('email')).first()
            if email_find:
                return jsonify(message='Ce mail est déjà utilisé par un autre utilisateur'), 409
            user.email = data.get('email')

        if 'phone_number' in data:
            phone_number_find = User.query.filter(User.username != data.get('username'), User.phone_number == data.get('phone_number')).first()
            if phone_number_find:
                return jsonify(message='Ce numéro est déjà utilisé par un autre utilisateur'), 409
            user.phone_number = data.get('phone_number')

        db.session.commit()
        return jsonify({'message': 'Utilisateur mis à jour'}), 200

    except SQLAlchemyError as e:
        return jsonify(message='Erreur lors de la mise à jour de l\'utilisateur'), 500

@users.route("/delete_user/<user_id>", methods = ["DELETE"])
def delete_user(user_id):
    try:
        user = User.query.get(user_id)
        if not user :
            return jsonify(message='utilisateur introuvable'), 404
        
        db.session.delete(user)
        db.session.commit()

        return jsonify(message='Suppression réussi'), 200
    except SQLAlchemyError as e :
        return jsonify(message='erreur lors de la suppression'), 500
    
@users.route("/get_all_users")
def get_all_users():
    try:
        if User.query.count() != 0:
            users = User.query.all()
            for user in users :
                user_mashmallow = Mashmallow()
                user_data = user_mashmallow.dump(user)
                users[users.index(user)] = user_data
            return jsonify(users)
        else:
            return jsonify(message='Aucun utilidateurs existants')
    except SQLAlchemyError as e:
        return jsonify(message ="Erreur lors du traitement de la requête")

@users.route("/create_account_team_member", methods=["POST","GET"])
def crate_account_team_member():
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

        team_member = User(
            username= data.get("username"),
            password= hashed_password,
            first_name=data.get("first_name"),
            last_name=data.get("last_name"),
            email=data.get("email"),
            phone_number=data.get("phone_number"),
            role= Roles.TEAM_MEMBER
        )

        db.session.add(team_member)
        db.session.commit()
        return jsonify({'message': 'compte enregistré'}), 200
    except SQLAlchemyError as e:
        return jsonify(message='Erreur lors de l\'enregistrement'), 500
    
@users.route("/get_all_user_team", methods=["GET"])
def get_all_user_team():
    try:
        users_team = User.query.filter_by(role="team_member").all()
        # for user in users_team :
        user_mashmallow = Mashmallow()
        user_data = user_mashmallow.dump(users_team)
        # users_team[users_team.index(user)] = user_data
        return jsonify(user_data)
    except SQLAlchemyError as e:
        return jsonify(message ='Erreur lors du traitement de la requête')

@users.route("/reset_password", methods=["POST"])
def reset_password():
    m = mail
    address = request.form.get("email")
    ### il va falloir vérifier si l'adresse est dans la bd
    password = generate_password()
    msg = Message('Mail de test', 
                  sender='melainenkeng@gmail.com',
                  recipients=[address])
    msg.body = 'Votre mot de passe de rénitialisation est : ' + password
    
    m.send(msg)

    ## il va falloir écire le code pour

    return "Message envoyé"

def generate_password(length=8):
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(secrets.choice(characters) for _ in range(length))
    return password