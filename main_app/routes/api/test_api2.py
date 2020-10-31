from flask import Blueprint, jsonify, request
from main_app.utils import access_required, register_service

bp = Blueprint("test_api_2", __name__, url_prefix="/api/test2")
description = "test api 2"
name = "Name2"


@bp.route('/')
@access_required(bp.url_prefix)
def main():
    return jsonify({'result': 'test2'})


@bp.route('/help')
def help():
    return "help test2"


@bp.route('/demo')
def demo():
    return jsonify({'result': 'test2_demo'})


register_service(bp, description, name)
