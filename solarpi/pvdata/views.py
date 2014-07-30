# -*- coding: utf-8 -*-
import calendar
from datetime import datetime, timedelta

from flask import Blueprint, render_template
from sqlalchemy import extract, func
from solarpi.pvdata.helper import get_sec

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
    pv = PVData.query.with_entities(PVData.created_at, PVData.current_power, PVData.daily_energy).filter(
        PVData.created_at > current_date.strftime('%Y-%m-%d')).filter(
        PVData.created_at < tomorrow.strftime('%Y-%m-%d')).filter(PVData.current_power > 0).all()

    pv_max = PVData.query.with_entities(func.strftime('%H:%M:00', PVData.created_at).label('pvdata_created_at'),
                                        func.max(PVData.current_power).label('pv_max')).filter(
        PVData.created_at >= (current_date - timedelta(days=3)).strftime('%Y-%m-%d')).filter(
        PVData.created_at <= (current_date + timedelta(days=3)).strftime('%Y-%m-%d')).filter(PVData.current_power > 0).group_by(
        func.strftime('%H:%M:00', PVData.created_at)).all()

    current_date_midnight = calendar.timegm(datetime.strptime(date, "%Y-%m-%d").timetuple())

    timestamps_pv_max = [1000 * (get_sec(d.pvdata_created_at) + current_date_midnight)
                         for d in pv_max]
    series_pv_max = [(int(d.pv_max or 0)) for d in pv_max]

    if len(pv) > 0:
        daily_energy = pv[-1].daily_energy
    else:
        daily_energy = 0

    timestamps_pv = [
        1000 * calendar.timegm(datetime.strptime(d.created_at.split(".")[0], "%Y-%m-%dT%H:%M:%S").timetuple())
        for d in pv]
    series_pv = [(int(d.current_power or 0)) for d in pv]
    daily_chart_data = [list(x) for x in zip(timestamps_pv, series_pv)]
    daily_chart_max_data = [list(x) for x in zip(timestamps_pv_max, series_pv_max)]

    return render_template("data/daily.html", data=daily_chart_data, data2=daily_chart_max_data, yesterday=yesterday,
                           today=current_date,
                           tomorrow=tomorrow,
                           daily_energy=daily_energy, all_data=pv)


@blueprint.route("/monthly")
def monthly(date=datetime.now().strftime('%Y-%m-%d')):
    try:
        current_date = datetime.strptime(date, "%Y-%m-%d")
    except ValueError, TypeError:
        current_date = datetime.strptime('2014-04-21', "%Y-%m-%d")
    #data = PVData.query.with_entities(func.strftime('%Y-%m-%d', PVData.created_at).label('pvdata_created_at')).join(PVData.query)

    #data = PVData.query.with_entities(func.strftime('%Y-%m-%d', PVData.created_at).label('created_at')).join()
    data = PVData.query.with_entities(func.max(PVData.id).label('max')).group_by(func.strftime('%Y-%m-%d', PVData.created_at))


    return render_template("data/monthly.html", data=data)