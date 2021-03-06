import re
from secrets import token_urlsafe
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from main_app import db, login

access_table = db.Table(
    'access_table',
    db.Column('access_token', db.String, db.ForeignKey('users.access_token')),
    db.Column('service_id', db.Integer, db.ForeignKey('services.id'))
)


class MasterKey(db.Model):
    __tablename__ = 'master_keys'
    token = db.Column(db.String(120), primary_key=True)


class Service(db.Model):
    __tablename__ = 'services'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), index=True, unique=True)
    base_url = db.Column(db.String(64), index=True, unique=True)
    description = db.Column(db.String(256))
    internal = db.Column(db.Boolean, default=True, nullable=False)

    @property
    def help_url(self):
        return self.base_url + "/help"

    @property
    def demo_url(self):
        return self.base_url + "/demo"

    @property
    def get_params_url(self):
        return self.base_url + "/params"


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    company = db.Column(db.String(64))
    email = db.Column(db.String(32))
    access_token = db.Column(db.String(128), index=True, unique=True)
    available_services = db.relationship('Service',
                                         secondary=access_table,
                                         lazy='dynamic',
                                         backref=db.backref('users', lazy='dynamic'))

    @property
    def other_services(self):
        ids = [item.id for item in self.available_services]
        return Service.query.filter(~Service.id.in_(ids))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @staticmethod
    def _validate(data):
        errors = []
        if ' ' in (data.get('username') or ' '):
            errors.append("Имя пользователя должно быть не пустым, и не должно содержать пробелы")
        if User.query.filter_by(username=data.get('username')).count() != 0:
            errors.append("К сожалению данный логин уже занят")
        if' ' in (data.get('password') or ' '):
            errors.append("Пароль не должен содержать пробелы")
        if len(data.get('company', '')) == 0:
            errors.append("Название компании не может быть пустым")
        if User.query.filter_by(email=data.get('email')).count() != 0:
            errors.append("Аккаунт с этой почтой уже зарегестрирован")
        return not bool(errors), errors

    def to_dict(self, full=False):
        data = {
            'username': self.username,
            'company': self.company,
            'email': self.email,
            'access_token': self.access_token
        }
        return data

    def _from_dict(self, data):
        for field in ['username', 'company', 'email']:
            if field in data:
                setattr(self, field, data[field])
        if 'password' in data:
            self.set_password(data['password'])

    @staticmethod
    def register(data):
        flag, errors = User._validate(data)
        if flag:
            new_user = User()
            new_user._from_dict(data)
            token = token_urlsafe(60)
            while User.query.filter_by(access_token=token).count() > 0:
                token = token_urlsafe(60)
            new_user.access_token = token
            db.session.add(new_user)
            db.session.commit()
            return new_user, None
        return None, errors


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class DebetCardRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(32))
    last_name = db.Column(db.String(32))
    email = db.Column(db.String(32))
    birthday = db.Column(db.DateTime)
    create_date = db.Column(db.DateTime, index=True, default=datetime.utcnow())
    status = db.Column(db.String(32), default='Подана')
    access_token = db.Column(db.String(128))

    @staticmethod
    def validate(data):
        errors = dict()
        if not data.get('first_name', ''):
            errors['firstname'] = 'Emtpty'
        if not data.get('first_name', ''):
            errors['firstname'] = 'Emtpty'
        if not data.get('email', ''):
            errors['email'] = 'Emtpty'
        if not data.get('birthday', ''):
            errors['birthday'] = 'Emtpty'
        return not bool(errors), errors

    @staticmethod
    def register(data):
        flag, errors = DebetCardRequest.validate(data)
        if flag:
            req = DebetCardRequest()
            req.first_name = data['first_name']
            req.last_name = data['last_name']
            req.email = data['email']
            req.birthday = data['birthday']
            req.access_token = data['access_token']
            db.session.add(req)
            db.session.commit()
            return True, {'result': 'success', 'request_id': req.id}
        return False, {'result': 'error', 'errors': errors}