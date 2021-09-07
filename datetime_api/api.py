from flask import Blueprint

bp = Blueprint("api", __name__)


@bp.route("/")
def index():
    return '<h1>Hello World</h1>'
