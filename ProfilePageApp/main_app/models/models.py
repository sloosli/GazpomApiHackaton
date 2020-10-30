from flask_login import UserMixin
from ProfilePageApp.main_app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
import re


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    company = db.Column(db.String(64))
    email = db.Column(db.String(32))
    acces_key = db.Column(db.String(128))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @staticmethod
    def validate(**kwargs):
        flag = True
        flag *= not ' ' in (kwargs.get('username') or ' ')
        flag *= not ' ' in (kwargs.get('password') or ' ')
        flag *= len(kwargs.get('company')) > 0
        flag *= len(re.findall(r'[\w.-]+@[\w.-]+\.?[\w]+?', kwargs.get('email'))) > 0

    def from_dict(self, data):
        for field in ['username', 'company', 'email']:
            if field in data:
                setattr(self, field, data[field])
        if 'password' in data:
            self.set_password(data['password'])


@login.user_loader
def load_user(id):
    return User.query.get(int(id))
