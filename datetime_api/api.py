from flask import Blueprint, request, abort
from datetime import datetime, timedelta
from werkzeug.exceptions import BadRequest
from dateutil import parser
from dateutil.tz import UTC
import math

bp = Blueprint("api", __name__)


class DifferenceBetween:
    def __init__(self, start_date, end_date, unit):
        self.unit = unit

        self.validate_unit()
        self.validate_date(start_date)
        self.validate_date(end_date)

        self.start_date = parser.parse(start_date)
        self.end_date = parser.parse(end_date)

        # Add the UTC timezone if none if provided
        if not self.start_date.tzinfo:
            self.start_date = datetime(self.start_date.year, self.start_date.month,
                                       self.start_date.day, self.start_date.hour,
                                       self.start_date.minute, self.start_date.second,
                                       tzinfo=UTC)
        if not self.end_date.tzinfo:
            self.end_date = datetime(self.end_date.year, self.end_date.month,
                                     self.end_date.day, self.end_date.hour,
                                     self.end_date.minute, self.end_date.second,
                                     tzinfo=UTC)

        # Set difference to the correct unit
        if self.unit == "seconds":
            self.difference = self.secondsBetween()
        elif self.unit == "minutes":
            self.difference = self.minutesBetween()
        elif self.unit == "hours":
            self.difference = self.hoursBetween()
        elif self.unit == "days":
            self.difference = self.daysBetween()
        elif self.unit == "weeks":
            self.difference = self.weeksBetween()
        elif self.unit == "years":
            self.difference = self.yearsBetween()

    def validate_unit(self):
        valid_units = ["seconds", "minutes", "hours", "days", "weeks", "years"]

        if not self.unit in valid_units:
            abort(400, "Invalid unit provided. Must be seconds, minutes, hours, days, weeks or years.")

    def validate_date(self, date):
        if date is None:
            abort(400, "Must supply both a start and end date.")
        try:
            parser.parse(date)
        except ValueError:
            abort(400, "Invalid date format.")

    def getDifference(self):
        return self.difference

    def secondsBetween(self):
        """Get the number of seconds between the start and end date"""
        difference = self.end_date - self.start_date
        return int(difference.total_seconds())

    def minutesBetween(self):
        """Get the number of minutes between the start and end date"""
        return self.secondsBetween() / 60

    def hoursBetween(self):
        """Get the number of hours between the start and end date"""
        return self.minutesBetween() / 60

    def daysBetween(self):
        """Get the number of days between the start and end date"""
        difference = self.end_date - self.start_date
        return difference.days

    def weeksBetween(self):
        """Get the number of weeks between the start and end date"""
        return self.daysBetween() / 7

    def yearsBetween(self):
        """Get the number of years between the start and end date"""
        return self.daysBetween() / 365


class DifferenceBetweenWeekdays(DifferenceBetween):
    def daysBetween(self):
        """Get the number of days between the start and end date"""
        # Get the number of complete weeks
        difference = self.end_date - self.start_date
        weeks = math.floor(difference.days / 7)
        # Use that to calculate the number of weekdays
        weekdays = weeks * 5
        # Count the weekdays of the last incomplete week
        incomplete_week = self.start_date + timedelta(weeks=weeks)
        while incomplete_week < self.end_date:
            if incomplete_week.weekday() < 5:
                weekdays += 1
            incomplete_week += timedelta(days=1)

        return weekdays

    def secondsBetween(self):
        """Get the number of seconds between the start and end date"""
        return self.daysBetween() * 86400


class DifferenceBetweenCompleteWeeks(DifferenceBetween):
    def weeksBetween(self):
        """
        Get the number of complete weeks between the start and end date.
        A complete week is 7 consecutive days.
        """
        # Get the number of complete weeks
        # if difference is negative don't floor the result
        difference = (self.end_date - self.start_date).days
        if difference >= 0:
            weeks = math.floor(difference / 7)
        else:
            weeks = math.ceil(difference / 7)

        return weeks

    def daysBetween(self):
        """Get the number of days between the start and end date"""
        return self.weeksBetween() * 7

    def secondsBetween(self):
        """Get the number of seconds between the start and end date"""
        return self.daysBetween() * 86400


@bp.errorhandler(BadRequest)
def handle_bad_request(e):
    response = {
        "error": e.description
    }
    return response, 400


@bp.route("/days", methods=['GET', 'POST'])
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


@bp.route("/weekdays", methods=['GET', 'POST'])
def weekdays():
    """Get the number of weekdays between two datetime parameters"""
    start_date = request.args.get("start_date")
    end_date = request.args.get("end_date")
    unit = request.args.get("unit") or "days"

    weekdays = DifferenceBetweenWeekdays(start_date, end_date, unit).getDifference()

    response = {
        "difference": weekdays,
        "unit": unit
    }

    return response


@bp.route("/completeweeks", methods=['GET', 'POST'])
def completeweeks():
    """Get the number of weekdays between two datetime parameters"""
    start_date = request.args.get("start_date")
    end_date = request.args.get("end_date")
    unit = request.args.get("unit") or "weeks"

    weeks = DifferenceBetweenCompleteWeeks(start_date, end_date, unit).getDifference()

    response = {
        "difference": weeks,
        "unit": unit
    }

    return response
