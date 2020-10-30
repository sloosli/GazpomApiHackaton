from flask import Blueprint, request, flash, url_for, render_template, redirect
from ProfilePageApp.main_app.models.models import User
from flask_login import login_user, logout_user
from werkzeug.urls import url_parse
from ProfilePageApp.main_app import db

bp = Blueprint('auth', __name__, url_prefix='auth')


@bp.route('login', methods=['POST'])
def login():
    data = request.form
    user = User.query.filter_by(username=data.get('username')).first
    if user is None or not user.check_password(data.get('password')):
        flash('Неправильное имя пользователя или пароль')
        return redirect(url_for('auth.login_get'))
    login_user(user)
    next_page = data.get('next_page')
    if not next_page or url_parse(next_page).netloc != '':
        next_page = url_for('community.index')
    return redirect(next_page)


@bp.route('login', methods=['GET'])
def login_get():
    return render_template('auth/login.html', title='Вход')


@bp.route('/logout', methods=['GET'])
def logout():
    logout_user()
    return redirect(url_for('auth.login_get'))


@bp.route('/register', methods=['POST'])
def register():
    data = dict(request.form)
    if User.validate(**data):
        user = User()
        user.from_dict(data)
        db.session.add(user)
        db.session.commit()
        login_user(user)
        return redirect(url_for('community.index'))
    return redirect(url_for('auth.register_get'))


@bp.route('/register', methods=['GET'])
def register_get():
    return render_template('auth/register.html', title='Регистрация')
