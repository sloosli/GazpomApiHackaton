from flask import Blueprint, render_template


bp = Blueprint("public", __name__, url_prefix="/public")

api_dict = [
    {
        "name": "Курс валют",
        "id": 1,
        "url_base": "/api/pass",
        "description": "Заглушка для апи курса валют"
    },
    {
        "name": "Заявка на кредит",
        "id": 2,
        "url_base": "/api/pass2",
        "description": "Заглушка для апи кредита"
    },
    {
        "name": "Заявка на дебетовую карту",
        "id": 3,
        "url_base": "/api/pass3",
        "description": "Заглушка для апи дебетовой карты"
    }
]


@bp.route('/api_list')
def api_list():
    services = api_dict
    return render_template("public/api_list", services=services)


@bp.route('/api_test')
def api_test():
    pass