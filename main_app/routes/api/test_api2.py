from flask import Blueprint, jsonify
from main_app.utils import access_required, register_service, master_key_required

bp = Blueprint("test_api_2", __name__, url_prefix="/api/test2")
description = "test api 2"
name = "Name2"


@bp.route('/')
@access_required(bp.url_prefix)
def main():
    return jsonify({'result': 'test2'})


@bp.route('/params')
def get_params():
    return jsonify({})


@bp.route('/help')
def help():
    return "help test2"


@bp.route('/demo')
@master_key_required
def demo():
    return jsonify({'result': 'test2_demo'})


register_service(bp, description, name)
