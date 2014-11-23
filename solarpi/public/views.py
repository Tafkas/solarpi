# -*- coding: utf-8 -*-
'''Public section, including homepage and signup.'''
import calendar
from time import strftime
import dateutil.parser
from cookielib import eff_request_host
from datetime import datetime, timedelta
from flask import (Blueprint, render_template)
from sqlalchemy import func
from solarpi.public.helper import get_operating_hours
from solarpi.pvdata.models import PVData
from solarpi.electricity.models import Electricity
from solarpi.weather.helper import get_weather_icon, get_current_weather

blueprint = Blueprint('public', __name__, static_folder="../static")


@blueprint.route("/")
def home():
    operating_hours = int(get_operating_hours())
    now = datetime.now()

    pv = PVData.query.order_by(
        PVData.id.desc()).first()

    last_updated = dateutil.parser.parse(pv.created_at).strftime('%Y-%m-%d %H:%M')

    total_electricity = Electricity.query.order_by(Electricity.id.desc()).first()
    total_import = total_electricity.meter_180
    total_export = total_electricity.meter_280

    todays_electricity = Electricity.query.with_entities(
        (func.max(Electricity.meter_280) - func.min(Electricity.meter_280)).label(
            'todays_export'), (func.max(Electricity.meter_180) - func.min(Electricity.meter_180)).label(
            'todays_import')).filter(
        func.strftime('%Y-%m-%d', Electricity.created_at) == datetime.now().strftime('%Y-%m-%d')).group_by(
        func.strftime('%Y-%m-%d', Electricity.created_at)).first()

    last_year_export = Electricity.query.with_entities(Electricity.meter_280).filter(
        func.strftime('%Y', Electricity.created_at) == '2013').order_by(Electricity.id.desc()).first()
    current_year_export = total_export - last_year_export.meter_280

    todays_import, todays_export = 0.0, 0.0
    if todays_electricity:
        todays_import = todays_electricity.todays_import
        todays_export = todays_electricity.todays_export

    current_power = pv.current_power
    daily_energy = pv.daily_energy
    total_energy = pv.total_energy
    pac = pv.ac_1_p + pv.ac_2_p + pv.ac_3_p
    pdc = pv.dc_1_u * pv.dc_1_i + pv.dc_2_u * pv.dc_2_i + pv.dc_3_u * pv.dc_3_i
    if pdc > 0:
        efficiency = pac / pdc
    else:
        efficiency = 0

    w = get_current_weather()
    current_temp = w.temp
    current_weather = get_weather_icon(w.weather_id)

    todays_max_power = PVData.query.with_entities(func.max(PVData.current_power).label('todays_max_power')).filter(
        PVData.created_at >= datetime.now()).first().todays_max_power

    if not todays_max_power:
        todays_max_power = 0
        daily_energy = 0
        current_temp = None

    max_daily_energy_last_seven_days = PVData.query.with_entities(
        func.max(PVData.daily_energy).label('max_daily_energy')).filter(
        PVData.created_at >= (datetime.now() - timedelta(days=7))).first().max_daily_energy

    last_year_energy = PVData.query.with_entities(PVData.total_energy).filter(
        func.strftime('%Y', PVData.created_at) == '2013').order_by(PVData.id.desc()).first()

    current_year_energy = total_energy - last_year_energy.total_energy

    last_year_data = PVData.query.with_entities(func.strftime('%m', PVData.created_at).label('created_at'),
                                                (func.max(PVData.total_energy) - func.min(PVData.total_energy)).label(
                                                    'total_energy')).filter(
        func.strftime('%Y', PVData.created_at) == str(datetime.now().year - 1)).group_by(
        func.strftime('%Y-%m', PVData.created_at)).all()

    current_year_data = PVData.query.with_entities(func.strftime('%m', PVData.created_at).label('created_at'),
                                                   (
                                                       func.max(PVData.total_energy) - func.min(
                                                           PVData.total_energy)).label(
                                                       'total_energy')).filter(
        func.strftime('%Y', PVData.created_at) == str(datetime.now().year)).group_by(
        func.strftime('%Y-%m', PVData.created_at)).all()

    last_year_series = [int(x[1]) for x in last_year_data]
    last_year_current_month_avg = last_year_series[now.month - 1] / calendar.monthrange(now.year, now.month)[1]
    current_year_series = [int(x[1]) for x in current_year_data]
    if now.day > 1:
        current_month = int(
            (current_year_series[-1]) + last_year_current_month_avg * (calendar.monthrange(now.year, now.month)[1] - now.day-1))
    else:
        current_month = 0
    current_month_series = ['null'] * 12
    current_month_series[now.month - 1] = current_month

    return render_template("public/home.html",
                           current_power=current_power, daily_energy=daily_energy,
                           total_energy=total_energy, efficiency=efficiency,
                           current_temp=current_temp, current_weather=current_weather,
                           ac_1_p=pv.ac_1_p, ac_2_p=pv.ac_2_p, ac_3_p=pv.ac_3_p,
                           ac_1_u=pv.ac_1_u, ac_2_u=pv.ac_2_u, ac_3_u=pv.ac_3_u,
                           dc_1_u=pv.dc_1_u, dc_2_u=pv.dc_2_u, dc_3_u=pv.dc_3_u,
                           dc_1_i=pv.dc_1_i, dc_2_i=pv.dc_2_i, dc_3_i=pv.dc_3_i,
                           series_2013=last_year_series, series_2014=current_year_series,
                           current_month_pred=current_month_series,
                           current_year_energy=current_year_energy,
                           max_daily_energy_last_seven_days=max_daily_energy_last_seven_days,
                           todays_max_power=todays_max_power, last_updated=last_updated,
                           operating_hours=operating_hours, total_export=total_export,
                           total_import=total_import, todays_export=todays_export,
                           todays_import=todays_import, current_year_export=current_year_export)


@blueprint.route("/about/")
def about():
    return render_template("public/about.html")