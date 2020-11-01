from flask import Blueprint, jsonify, request
from main_app.models import DebetCardRequest
from main_app.utils import access_required, register_service, master_key_required

bp = Blueprint("debet_card_request", __name__, url_prefix="/api/debet_card_request")
description = "Заявка на оформление дебетовой карты газпромбанка, "
name = "Оформление дебетовой карты"


@bp.route('/')
@access_required(bp.url_prefix)
def main():
    flag, result = DebetCardRequest.register(request.args)
    return jsonify(result)


@bp.route('/params')
def get_params():
    return jsonify({
        'first_name': {'type': 'string', 'default': 'Иван'},
        'last_name': {'type': 'string', 'default': 'Иванов'},
        'email': {'type': 'string', 'default': 'ivanov@example.com'},
        'birthday': {'type': 'datetime', 'default': '01/02/1995', 'format': 'dd/mm/yyyy'},
    })


@bp.route('/help')
def help():
    return "Помощь по api курс валют"


@bp.route('/demo')
@master_key_required
def demo():
    flag, errors = DebetCardRequest.validate(request.args)
    if flag:
        return jsonify({'result': 'success', 'request_id': 'id'})
    return {'result': 'error', 'errors': errors}


register_service(bp, description, name)
