from functools import wraps
from flask import abort, request
from main_app import app, db
from .models import Service, MasterKey


def register_service(bp, description, name):
    current_service = Service.query.filter_by(base_url=bp.url_prefix).first()
    if not current_service:
        current_service = Service()
        db.session.add(current_service)
        current_service.base_url = bp.url_prefix
    current_service.name = name
    current_service.description = description
    db.session.commit()
    app.register_blueprint(bp)


def master_key_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.args.get('access_token')
        if MasterKey.query.filter_by(token=token).count() == 0:
            return abort(403)
        return f(*args, **kwargs)
    return decorated_function


def access_required(api_url):
    def actual_decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            current_service = Service.query.filter_by(base_url=api_url).first()
            token = request.args.get('access_token')
            print(current_service.users.filter_by(
                    access_token=token).all())
            if not current_service:
                abort(404)
            elif not token or current_service.users.filter_by(
                    access_token=token).count() == 0:
                abort(403)
            return func(*args, **kwargs)
        return wrapper
    return actual_decorator
