import json

import requests
from flask import Blueprint, render_template, request as rq

from main_app.models import Service, MasterKey

bp = Blueprint("public", __name__, url_prefix="/public")


@bp.route('/api_list')
def api_list():
    services = Service.query.all()
    return render_template("public/api_list.html", services=services)


'''
warning: the code bellow is guaranteed to make you cry =(
'''


@bp.route('/api_demo/<service_id>')
def api_demo(service_id=1):
    failed = False
    params = {}
    service = Service.query.filter_by(id=service_id).first()
    if service.internal:
        r = requests.get('http://' + rq.host + service.get_params_url)
    else:
        r = requests.get(service.get_params_url)
    if r.status_code != 200:
        failed = True
    else:
        params = json.loads(r.content.decode('utf-8-sig'))
    return render_template("public/api_demo.html", service=service,
                           params=params, failed=failed, result="")


@bp.route('api_demo/<service_id>', methods=['POST'])
def api_demo_post(service_id=1):
    failed = False
    result = ''
    token = MasterKey.query.first().token
    service = Service.query.filter_by(id=service_id).first()
    param_string = '&'.join("%s=%s" % (key, rq.form.get(key, ''))
                            for key in rq.form)
    html_params = {key: {"default": rq.form.get(key, '')}
                   for key in filter(lambda x: x != "result", rq.form)}
    if service.internal:
        url = "{}{}{}".format('http://', rq.host, service.demo_url)
    else:
        url = service.demo_url
    r = requests.get(url + "?" + param_string + "&access_token=" + token)
    if r.status_code != 200:
        failed = True
    else:
        result = json.loads(r.content.decode('utf-8-sig'))
        result = str(json.dumps(result, indent=4, sort_keys=True))
    return render_template("public/api_demo.html", service=service,
                           params=html_params, failed=failed, result=result)
