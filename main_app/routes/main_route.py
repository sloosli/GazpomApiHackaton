import os
import importlib
from flask import redirect, url_for, render_template
from flask_login import current_user
from main_app import app
from .public import bp as public_bp
from .auth import bp as auth_bp
from .partner import bp as partner_bp

app.register_blueprint(public_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(partner_bp)

files = os.listdir(os.path.abspath(os.path.dirname(__file__)) + "/api")
modules = filter(lambda x: x.endswith('.py'), files)
for m in modules:
    importlib.import_module("main_app.routes.api." + m[0:-3])


@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('partner.api_list'))
    return redirect(url_for('public.api_list'))


@app.route('/test')
def test():
    return render_template("test.html")
