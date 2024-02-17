import os
from flask_mail import Mail
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from isjcrm import config
from twilio.rest import Client
from flask_marshmallow import Marshmallow
from flask_cors import CORS
from twilio.rest import Client

db = SQLAlchemy()
migrate = Migrate()
mail = Mail()
ma = Marshmallow()
login_manager = LoginManager()

sid = config.TWILIO_ACCOUNT_SID
token=config.WILIO_AUTTH_TOKEN
phone=config.TWILIO_PHONE_NUMBER

# Download the helper library from https://www.twilio.com/docs/python/install


client = Client(sid, token)




# # Configurer les informations Twilio
# account_sid = config.TWILIO_ACCOUNT_SID
# auth_token = config.TWILIO_AUTH_TOKEN
# twilio_phone_number = config.TWILIO_PHONE_NUMBER

# # Initialiser le client Twilio
# client = Client(account_sid, auth_token)




def create_app():

    #creation de l'instance de l'application Flask
    from flask import Flask
    app = Flask(__name__, template_folder='templates', static_folder='static')
    CORS(app)
    # connexion local
    db_config = {
        'host': 'localhost',
        'user': 'postgres',
        'password': '10322',
        'database': 'isjcrm',
        'port': '5432'
    }

    # Connexion distante
    # db_config = {
    #     'host': 'dpg-cn102nug1b2c738bl5gg-a.frankfurt-postgres.render.com',
    #     'user': 'isjcrm_db_user',
    #     'password': 'WwL3uUBvojAp2THxDDfD0IVFvOla3tnK',
    #     'database': 'isjcrm_db',
    #     'port': '5432'
    # }
    
    app.config['SECRET_KEY'] = config.SECRET_KEY
    #Charger les configurations à partir de l'objet config
    app.config.from_object(config)
    #configuration de l'API GMAIL
    app.config['MAIL_SERVER'] = config.MAIL_SERVER
    app.config['MAIL_PORT'] = config.MAIL_PORT
    app.config['MAIL_USE_TLS'] = config.MAIL_USE_TLS
    app.config['MAIL_USERNAME'] = config.MAIL_USERNAME
    app.config['MAIL_PASSWORD'] = config.MAIL_PASSWORD
    app.config['MAIL_DEFAULT_SENDER'] = config.MAIL_DEFAULT_SENDER
    # Configuration pour MySQL avec XAMPP sans nom d'utilisateur ni mot de passe
    # app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{db_config['user']}:{db_config['password']}@{db_config['host']}/{db_config['database']}"
    app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql+psycopg2://{db_config['user']}:{db_config['password']}@{db_config['host']}:{db_config['port']}/{db_config['database']}"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


    mail.init_app(app=app)

    # Initialiser la base de données
    db.init_app(app)
    migrate.init_app(app, db)
    ma.init_app(app)

    #config de flask login
    @login_manager.user_loader
    def load_user(user_id):
        from isjcrm.users.models import User
        return User.query.get(user_id)
    login_manager.init_app(app)


    with app.app_context():

        from isjcrm.activities.routes import activities
        from isjcrm.candidat.routes import candidats
        from isjcrm.mailmodel.routes import mailmodel
        from isjcrm.notifications.routes import notifications
        from isjcrm.taches.routes import taches
        from isjcrm.users.routes import users
        from isjcrm.users.ui_routes import ui_users
        from isjcrm.candidat.ui_routes import ui_candidats
        from isjcrm.taches.ui_routes import ui_tasks
        from isjcrm.main.main import main

        # register routes with blueprint
        app.register_blueprint(main)
        app.register_blueprint(activities, url_prefix ='/activities')
        app.register_blueprint(users, url_prefix = '/users')
        app.register_blueprint(ui_users)
        app.register_blueprint(ui_candidats)
        app.register_blueprint(ui_tasks)
        app.register_blueprint(candidats, url_prefix = '/candidats')
        app.register_blueprint(mailmodel, url_prefix = '/mailmodels')
        app.register_blueprint(notifications, url_prefix = '/notifications')
        app.register_blueprint(taches, url_prefix = '/taches')


        db.create_all()

    return app 
