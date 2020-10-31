import re
from secrets import token_urlsafe

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from main_app import db, login

access_table = db.Table(
    'access_table',
    db.Column('access_token', db.String, db.ForeignKey('users.access_token')),
    db.Column('service_id', db.Integer, db.ForeignKey('services.id'))
)


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

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @staticmethod
    def _validate(data):
        flag = True
        flag *= ' ' not in (data.get('username') or ' ')
        flag *= User.query.filter_by(username=data.get('username')).count() == 0
        flag *= ' ' not in (data.get('password') or ' ')
        flag *= len(data.get('company')) > 0
        flag *= len(re.findall(r'[\w.-]+@[\w.-]+\.?[\w]+?', data.get('email'))) > 0
        flag *= User.query.filter_by(email=data.get('email')).count() == 0
        return flag

    def _from_dict(self, data):
        for field in ['username', 'company', 'email']:
            if field in data:
                setattr(self, field, data[field])
        if 'password' in data:
            self.set_password(data['password'])

    @staticmethod
    def register(data):
        if User._validate(data):
            new_user = User()
            new_user._from_dict(data)
            token = token_urlsafe(60)
            while User.query.filter_by(access_token=token).count() > 0:
                token = token_urlsafe(60)
            new_user.access_token = token
            db.session.add(new_user)
            db.session.commit()
            return new_user
        return None


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class Service(db.Model):
    __tablename__ = 'services'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), index=True, unique=True)
    base_url = db.Column(db.String(64), index=True, unique=True)
    description = db.Column(db.String(256))

    @property
    def help_url(self):
        return self.base_url + "/help"

    @property
    def demo_url(self):
        return self.base_url + "/demo"
