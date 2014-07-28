# -*- coding: utf-8 -*-
import calendar
from datetime import datetime, timedelta

from flask import Blueprint, render_template
from sqlalchemy import extract

from solarpi.pvdata.models import PVData

blueprint = Blueprint("data", __name__, url_prefix='/pvdata',
                      static_folder="../static")


@blueprint.route("/daily")
@blueprint.route("/daily/<date>")
def daily(date=datetime.now().strftime('%Y-%m-%d')):
    try:
        current_date = datetime.strptime(date, "%Y-%m-%d")
    except ValueError, TypeError:
        current_date = datetime.strptime('2014-04-21', "%Y-%m-%d")
    yesterday = current_date - timedelta(days=1)
    tomorrow = current_date + timedelta(days=1)
    data = PVData.query.filter(PVData.created_at > current_date.strftime('%Y-%m-%d')).filter(
        PVData.created_at < tomorrow.strftime('%Y-%m-%d')).filter(PVData.current_power > 0)

    try:
        daily_energy = data[-1].daily_energy
    except IndexError:
        daily_energy = 0

    categories = [1000 * calendar.timegm(datetime.strptime(d.created_at.split(".")[0], "%Y-%m-%dT%H:%M:%S").timetuple())
                  for d in data]

    series = [(int(d.current_power or 0)) for d in data]
    data = [list(x) for x in zip(categories, series)]

    return render_template("data/daily.html", data=data, yesterday=yesterday, today=current_date, tomorrow=tomorrow,
                           daily_energy=daily_energy)


@blueprint.route("/monthly")
def monthly(date=datetime.now().strftime('%Y-%m-%d')):
    try:
        current_date = datetime.strptime(date, "%Y-%m-%d")
    except ValueError, TypeError:
        current_date = datetime.strptime('2014-04-21', "%Y-%m-%d")
    data = PVData.query.filter(extract('year', PVData.created_at) == 2014).filter(
        extract('month', PVData.created_at) == 5)

    categories = [1000 * calendar.timegm(datetime.strptime(d.created_at, "%Y-%m-%dT%H:%M:%S").timetuple()) for d in
                  data]
    series = [(float(d.dc_1_p or 0) + float(d.dc_2_p or 0)) for d in data]
    data = [list(x) for x in zip(categories, series)]
    return render_template("data/monthly.html", data=data)