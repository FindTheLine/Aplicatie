from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_login import LoginManager
from flask_migrate import Migrate
from datetime import datetime
from flask_wtf.csrf import CSRFProtect
import os

# instantiate dependencies
app = Flask(__name__)
db = SQLAlchemy()
mail = Mail()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message = u"Vă rugăm să intrați în cont pentru a acces"
csrf = CSRFProtect()

DB_NAME = "projy"

def create_app(ENV="prod"):
    if ENV == "dev":
        app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:admin@localhost:5433/postgres'    
    if ENV == "prod":
        app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:admin@localhost:5433/postgres'

    # init db
    app.config['SECRET_KEY'] = 'testkey'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    # init mail
    mail_settings = {
        "MAIL_SERVER": 'smtp-mail.outlook.com',
        "MAIL_PORT": 587,
        "MAIL_USE_TLS": True,
        "MAIL_USERNAME": ''.format(os.environ.get("MAIL_USERNAME")),
        "MAIL_PASSWORD": ''.format(os.environ.get("MAIL_PASSWORD"))
    }

    app.config.update(mail_settings)
    mail.init_app(app)

    # init migrate
    migrate = Migrate(app,db)

    # create frontend filters
    @app.template_filter('sort_asc')
    def sort_asc(iterable):
        return sorted(iterable, key=lambda x:x.name)
    
    @app.template_filter('sort_desc')
    def sort_desc(iterable):
        return sorted(iterable, key=lambda x:x.name, reverse=True)
    
    @app.template_filter('clean_date')
    def clean_date(date):
        try:
            return datetime.strftime(date, '%d.%m.%Y')
        except:
            return datetime.strptime(date, '%d.%m.%Y').strftime('%d.%m.%Y')

    # register blueprints
    from .views import views
    from .auth import auth
    from .data import data

    app.register_blueprint(views, url_prefix='/')   
    app.register_blueprint(auth, url_prefix='/') 
    app.register_blueprint(data, url_prefix='/') 

    from .models import Usr, Role, Notification

    # init login manager
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return Usr.query.get(int(id))

    mail.init_app(app)

    with app.app_context():
        db.create_all()

    csrf.init_app(app)

    return app
