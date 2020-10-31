import os
import importlib
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = 'auth.login'
login.login_message = 'Вам необходимо войти, что бы увидеть эту страницу'

from .routes.public import bp as public_bp
app.register_blueprint(public_bp)

from .routes.auth import bp as auth_bp
app.register_blueprint(auth_bp)

files = os.listdir(os.path.abspath(os.path.dirname(__file__)) + "/routes/api")
modules = filter(lambda x: x.endswith('.py'), files)
for m in modules:
    importlib.import_module("main_app.routes.api." + m[0:-3])

from . import models
