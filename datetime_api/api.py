from flask import Blueprint, request
from datetime import datetime
from dateutil import parser

bp = Blueprint("api", __name__)


@bp.route("/days")
def days():
    """Get the number of days between two datetime parameters"""
    date1 = request.args.get("date1")
    date2 = request.args.get("date2")
    unit = request.args.get("unit") or "days"

    date = parser.parse(date1), parser.parse(date2)
    difference = date[1] - date[0]
    difference = difference.days

    response = {
        "difference": str(difference),
        "unit": unit
    }

    return response
