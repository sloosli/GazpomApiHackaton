from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

app = Flask(__name__)
db = SQLAlchemy(app)
login = LoginManager(app)
bootstrap = Bootstrap(app)

from ProfilePageApp.main_app.routes.public import bp as public_bp
app.register_blueprint(public_bp)

from ProfilePageApp.main_app.routes.auth import bp as auth_bp
app.register_blueprint(auth_bp)

from ProfilePageApp.main_app import models
