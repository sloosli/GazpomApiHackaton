from flask import Blueprint, jsonify
from main_app.utils import access_required, register_service, master_key_required

bp = Blueprint("exchange_rates", __name__, url_prefix="/api/exchange_rates")
description = "Возвращает JSON, содержащий информацию о крусах валют"
name = "Курс валют"


@bp.route('/')
@access_required(bp.url_prefix)
def main():
    return jsonify({
        "result": {
            "buy": {
                "usd": 80.9,
                "eur": 94.02,
            },
            "sold": {
                "usd": 77.86,
                "eur": 90.87,
            }
        }
    })


@bp.route('/params')
def get_params():
    return jsonify({})


@bp.route('/help')
def help():
    return "Помощь по api курс валют"


@bp.route('/demo')
@master_key_required
def demo():
    return jsonify({
        "result": {
            "buy": {
                "usd": 80,
                "eur": 94,
            },
            "sold": {
                "usd": 76,
                "eur": 90,
            }
        }
    })


register_service(bp, description, name)
