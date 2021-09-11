from flask import Blueprint, request
from datetime import datetime, timedelta
from dateutil import parser
import math

bp = Blueprint("api", __name__)


class DifferenceBetween:
    def __init__(self, start_date, end_date, unit):
        self.unit = unit

        self.start_date = parser.parse(start_date)
        self.end_date = parser.parse(end_date)

        if self.unit == "seconds":
            self.difference = self.secondsBetween()
        elif self.unit == "minutes":
            self.difference = self.minutesBetween()
        elif self.unit == "hours":
            self.difference = self.hoursBetween()
        elif self.unit == "days":
            self.difference = self.daysBetween()
        elif self.unit == "years":
            self.difference = self.yearsBetween()

    def getDifference(self):
        return self.difference

    def secondsBetween(self):
        return self.daysBetween() * 86400

    def minutesBetween(self):
        return self.daysBetween() * 1440

    def hoursBetween(self):
        return self.daysBetween() * 24

    def daysBetween(self):
        difference = self.end_date - self.start_date
        return difference.days

    def weekdaysBetween(self):
        # Get the number of complete weeks
        weeks = math.floor(self.daysBetween() / 7)
        # Use that to calculate the number of weekdays
        weekdays = weeks * 5
        # Count the weekdays of the last incomplete week
        incomplete_week = self.start_date + timedelta(weeks=weeks)
        while incomplete_week < self.end_date:
            if incomplete_week.weekday() < 5:
                weekdays += 1
            incomplete_week += timedelta(days=1)

        return weekdays

    def completeWeeksBetween(self):
        # Get the number of complete weeks
        # if difference is negative don't floor the result
        difference = self.daysBetween()
        if difference >= 0:
            weeks = math.floor(difference / 7)
        else:
            weeks = math.ceil(difference / 7)

        return weeks

    def yearsBetween(self):
        return self.daysBetween() / 365


@bp.route("/days")
def days():
    """Get the number of days between two datetime parameters"""
    start_date = request.args.get("start_date")
    end_date = request.args.get("end_date")
    unit = request.args.get("unit") or "days"

    difference = DifferenceBetween(start_date, end_date, unit).getDifference()

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

    weekdays = DifferenceBetween(start_date, end_date, unit).weekdaysBetween()

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

    weeks = DifferenceBetween(start_date, end_date, unit).completeWeeksBetween()

    response = {
        "difference": weeks,
        "unit": unit
    }

    return response
