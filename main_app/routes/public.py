import json
import requests
from flask import Blueprint, render_template, request as rq
from main_app.models import Service, MasterKey

bp = Blueprint("public", __name__, url_prefix="/public")


@bp.route('/api_list')
def api_list():
    services = Service.query.all()
    return render_template("public/api_list.html", services=services)


@bp.route('/api_demo/<service_id>')
def api_demo(service_id=1):
    failed = False
    params = {}
    service = Service.query.filter_by(id=service_id).first()
    if service.internal:
        failed = True
    else:
        r = requests.get(service.get_params_url)
        if r.status_code != 200:
            failed = True
        else:
            params = json.loads(r.content.decode('utf-8-sig'))
    return render_template("public/api_demo.html", service=service, params=params, failed=failed)
