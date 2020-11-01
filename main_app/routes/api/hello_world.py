from flask import Blueprint, jsonify, request
from main_app.utils import access_required, register_service, master_key_required

bp = Blueprint("hello_world", __name__, url_prefix="/api/hello_world")
description = "Говорит привет, переданному имени(очередной тест)"
name = "Hello World"


@bp.route('/')
@access_required(bp.url_prefix)
def main():
    name = str(request.args.get('name'))
    return jsonify({"result": "Hello, %s!" % name.capitalize()})


@bp.route('/params')
def get_params():
    return jsonify({
        "name": {
            "type": "string",
            "default": "world"
        }
    })


@bp.route('/help')
def help():
    return "pass"


@bp.route('/demo')
@master_key_required
def demo():
    name = str(request.args.get('name', default="world"))
    return jsonify({"result": "Hello, %s!" % name.capitalize()})


register_service(bp, description, name)
