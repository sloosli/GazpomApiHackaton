from flask import Blueprint, request, flash, url_for, render_template, redirect
from main_app.models import User
from flask_login import login_user, logout_user
from werkzeug.urls import url_parse

bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/login', methods=['POST'])
def login():
    data = dict(request.form)
    user = User.query.filter_by(username=data.get('username')).first()
    if user is None or not user.check_password(data.get('password')):
        flash('Неправильное имя пользователя или пароль')
        return redirect(url_for('auth.login_get'))
    login_user(user)
    return redirect(url_for('partner.api_list'))


@bp.route('/login', methods=['GET'])
def login_get():
    return render_template('auth/login.html', title='Вход')


@bp.route('/logout', methods=['GET'])
def logout():
    logout_user()
    return redirect(url_for('auth.login_get'))


@bp.route('/register', methods=['POST'])
def register():
    data = dict(request.form)
    user, errors = User.register(data)
    if user:
        login_user(user)
        return redirect(url_for('community.index'))
    for error in errors:
        flash(error)
    return render_template('auth/register.html', title='Регистрация', params=request.form)


@bp.route('/register', methods=['GET'])
def register_get():
    return render_template('auth/register.html', title='Регистрация', params=dict())
