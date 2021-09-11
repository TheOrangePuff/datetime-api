from flask import Blueprint, request
from datetime import datetime, timedelta
from dateutil import parser
import math

bp = Blueprint("api", __name__)


@bp.route("/days")
def days():
    """Get the number of days between two datetime parameters"""
    start_date = request.args.get("start_date")
    end_date = request.args.get("end_date")
    unit = request.args.get("unit") or "days"

    date = parser.parse(start_date), parser.parse(end_date)
    difference = date[1] - date[0]
    difference = difference.days

    response = {
        "difference": difference,
        "unit": unit
    }

    return response


@bp.route("/weekdays")
def weekdays():
    """Get the number of weekdays between two datetime parameters"""
    start_date = request.args.get("start_date")
    end_date = request.args.get("end_date")
    unit = request.args.get("unit") or "days"

    date = parser.parse(start_date), parser.parse(end_date)
    difference = date[1] - date[0]
    difference = difference.days

    # Get the number of complete weeks
    weeks = math.floor(difference / 7)
    # Use that to calculate the number of weekdays
    weekdays = weeks * 5
    # Count the weekdays of the last incomplete week
    incomplete_week = date[0] + timedelta(weeks=weeks)
    while incomplete_week < date[1]:
        if incomplete_week.weekday() < 5:
            weekdays += 1
        incomplete_week += timedelta(days=1)

    response = {
        "difference": weekdays,
        "unit": unit
    }

    return response


@bp.route("/completeweeks")
def completeweeks():
    """Get the number of weekdays between two datetime parameters"""
    start_date = request.args.get("start_date")
    end_date = request.args.get("end_date")
    unit = request.args.get("unit") or "weeks"

    date = parser.parse(start_date), parser.parse(end_date)
    difference = date[1] - date[0]
    difference = difference.days

    # Get the number of complete weeks
    # if difference is negative don't floor the result
    if difference >= 0:
        weeks = math.floor(difference / 7)
    else:
        weeks = math.ceil(difference / 7)

    response = {
        "difference": weeks,
        "unit": unit
    }

    return response
