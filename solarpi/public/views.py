# -*- coding: utf-8 -*-
'''Public section, including homepage and signup.'''
import calendar
from cookielib import eff_request_host
from datetime import datetime, timedelta
from flask import (Blueprint, render_template)
from sqlalchemy import func
from solarpi.pvdata.models import PVData
from solarpi.weather.models import Weather

blueprint = Blueprint('public', __name__, static_folder="../static")


@blueprint.route("/")
def home():
    pv = PVData.query.order_by(
        PVData.id.desc()).first()

    current_power = pv.current_power
    daily_energy = pv.daily_energy
    total_energy = pv.total_energy
    pac = pv.ac_1_p + pv.ac_2_p + pv.ac_3_p
    pdc = pv.dc_1_u * pv.dc_1_i + pv.dc_2_u * pv.dc_2_i + pv.dc_3_u * pv.dc_3_i
    if pdc > 0:
        efficiency = pac / pdc
    else:
        efficiency = 0

    w = Weather.query.with_entities(Weather.temp, Weather.weather_id).filter(
        Weather.created_at >= (datetime.now() - timedelta(days=2))).order_by(
        Weather.id.desc()).first()
    current_temp = w.temp
    current_weather = w.weather_id

    todays_max_power = PVData.query.with_entities(func.max(PVData.current_power).label('todays_max_power')).filter(
        PVData.created_at >= datetime.now() - timedelta(days=1)).first().todays_max_power

    max_daily_energy_last_seven_days = PVData.query.with_entities(
        func.max(PVData.daily_energy).label('max_daily_energy')).filter(
        PVData.created_at >= (datetime.now() - timedelta(days=7))).first().max_daily_energy

    last_year_energy = PVData.query.with_entities(PVData.total_energy).filter(
        func.strftime('%Y', PVData.created_at) == '2013').order_by(PVData.id.desc()).first()

    current_year_energy = total_energy - last_year_energy.total_energy

    data_2013 = PVData.query.with_entities(func.strftime('%m', PVData.created_at).label('created_at'),
                                           (func.max(PVData.total_energy) - func.min(PVData.total_energy)).label(
                                               'total_energy')).filter(
        func.strftime('%Y', PVData.created_at) == '2013').group_by(
        func.strftime('%Y-%m', PVData.created_at)).all()

    data_2014 = PVData.query.with_entities(func.strftime('%m', PVData.created_at).label('created_at'),
                                           (func.max(PVData.total_energy) - func.min(PVData.total_energy)).label(
                                               'total_energy')).filter(
        func.strftime('%Y', PVData.created_at) == '2014').group_by(
        func.strftime('%Y-%m', PVData.created_at)).all()

    t_2013 = [1000 * calendar.timegm(datetime.strptime(d.created_at, "%m").timetuple())
              for d in data_2013]

    t_2014 = [1000 * calendar.timegm(datetime.strptime(d.created_at, "%m").timetuple())
              for d in data_2014]

    series_2013 = [list(x) for x in zip(t_2013, [int(x[1]) for x in data_2013])]
    series_2014 = [list(x) for x in zip(t_2014, [int(x[1]) for x in data_2014])]

    return render_template("public/home.html",
                           current_power=current_power, daily_energy=daily_energy,
                           total_energy=total_energy, efficiency=efficiency,
                           current_temp=current_temp, current_weather=current_weather,
                           ac_1_p=pv.ac_1_p, ac_2_p=pv.ac_2_p, ac_3_p=pv.ac_3_p,
                           ac_1_u=pv.ac_1_u, ac_2_u=pv.ac_2_u, ac_3_u=pv.ac_3_u,
                           dc_1_u=pv.dc_1_u, dc_2_u=pv.dc_2_u, dc_3_u=pv.dc_3_u,
                           dc_1_i=pv.dc_1_i, dc_2_i=pv.dc_2_i, dc_3_i=pv.dc_3_i,
                           series_2013=series_2013, series_2014=series_2014,
                           current_year_energy=current_year_energy,
                           max_daily_energy_last_seven_days=max_daily_energy_last_seven_days,
                           todays_max_power=todays_max_power)


@blueprint.route("/about/")
def about():
    return render_template("public/about.html")