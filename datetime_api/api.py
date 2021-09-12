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
        elif self.unit == "weeks":
            self.difference = self.weeksBetween()
        elif self.unit == "years":
            self.difference = self.yearsBetween()

    def getDifference(self):
        return self.difference

    def secondsBetween(self):
        """Get the number of seconds between the start and end date"""
        return self.daysBetween() * 86400

    def minutesBetween(self):
        """Get the number of minutes between the start and end date"""
        return self.daysBetween() * 1440

    def hoursBetween(self):
        """Get the number of hours between the start and end date"""
        return self.daysBetween() * 24

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
