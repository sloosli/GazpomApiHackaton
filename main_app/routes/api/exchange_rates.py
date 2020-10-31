from flask import Blueprint, jsonify, request
from main_app.utils import access_required, register_service

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


@bp.route('/help')
def help():
    return "Помощь по api курс валют"


@bp.route('/demo')
def demo():
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

register_service(bp, description, name)