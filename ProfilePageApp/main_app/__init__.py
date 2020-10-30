from flask import Flask
from flask_bootstrap import Bootstrap

app = Flask(__name__)
bootstrap = Bootstrap(app)

from ProfilePageApp.main_app.routes.public import bp as public_bp
app.register_blueprint(public_bp)
