from flask import Blueprint, render_template
from main_app.models import Service

bp = Blueprint("public", __name__, url_prefix="/public")


@bp.route('/api_list')
def api_list():
    services = Service.query.all()
    return render_template("public/api_list.html", services=services)


@bp.route('/api_test')
def api_test():
    pass