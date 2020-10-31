from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user
from main_app.models import User, Service
from main_app import db

bp = Blueprint("partner", __name__, url_prefix="/partner")


@bp.route('/api_list')
@login_required
def api_list():
    available_services = current_user.available_services.all()
    other_services = current_user.other_services.all()
    return render_template("partner/api_list.html",
                           available_services=available_services,
                           other_services=other_services)


@bp.route('/stats')
@login_required
def stats():
    pass


@bp.route('/service_add/<service_id>')
@login_required
def service_add(service_id):
    if not current_user.available_services.filter_by(id=service_id).first():
        service = Service.query.filter_by(id=service_id).first_or_404()
        current_user.available_services.append(service)
        db.session.commit()
    return redirect(url_for('partner.api_list'))


@bp.route('/service_delete/<service_id>')
@login_required
def service_delete(service_id):
    if current_user.available_services.filter_by(id=service_id).first():
        service = Service.query.filter_by(id=service_id).first_or_404()
        current_user.available_services.remove(service)
        db.session.commit()
    return redirect(url_for('partner.api_list'))
