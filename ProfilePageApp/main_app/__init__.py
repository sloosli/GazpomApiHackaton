from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from ProfilePageApp.config import Config

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
bootstrap = Bootstrap(app)
login = LoginManager(app)
login.login_view = 'auth.login'
login.login_message = 'Вам необходимо войти, что бы увидеть эту страницу'

from ProfilePageApp.main_app.routes.public import bp as public_bp
app.register_blueprint(public_bp)

from ProfilePageApp.main_app.routes.auth import bp as auth_bp
app.register_blueprint(auth_bp)

from ProfilePageApp.main_app import models
