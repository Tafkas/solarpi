# -*- coding: utf-8 -*-
'''Public section, including homepage and signup.'''
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

    w = Weather.query.with_entities(Weather.temp).filter(
        Weather.created_at >= (datetime.now() - timedelta(days=2))).order_by(
        Weather.id.desc()).first()
    current_temp = w.temp

    monthly_data = PVData.query.with_entities(func.strftime('%Y-%m', PVData.created_at).label('pvdata_created_at'),
                                              (func.max(PVData.total_energy) - func.min(PVData.total_energy)).label(
                                                  'total_energy')).group_by(
        func.strftime('%Y-%m', PVData.created_at)).all()
    categories = [x[0] for x in monthly_data]
    series = [int(x[1]) for x in monthly_data]

    return render_template("public/home.html",
                           current_power=current_power, daily_energy=daily_energy,
                           total_energy=total_energy, current_temp=current_temp,
                           efficiency=efficiency,
                           ac_1_p=pv.ac_1_p, ac_2_p=pv.ac_2_p, ac_3_p=pv.ac_3_p,
                           ac_1_u=pv.ac_1_u, ac_2_u=pv.ac_2_u, ac_3_u=pv.ac_3_u,
                           dc_1_u=pv.dc_1_u, dc_2_u=pv.dc_2_u, dc_3_u=pv.dc_3_u,
                           dc_1_i=pv.dc_1_i, dc_2_i=pv.dc_2_i, dc_3_i=pv.dc_3_i,
                           categories=categories, series=series)


@blueprint.route("/about/")
def about():
    return render_template("public/about.html")