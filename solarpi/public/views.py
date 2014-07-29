# -*- coding: utf-8 -*-
'''Public section, including homepage and signup.'''
from datetime import datetime, timedelta
from flask import (Blueprint, render_template)
from solarpi.pvdata.models import PVData
from solarpi.weather.models import Weather

blueprint = Blueprint('public', __name__, static_folder="../static")


@blueprint.route("/")
def home():
    pv = PVData.query.filter(PVData.created_at >= (datetime.now())).order_by(
        PVData.id.desc()).first()
    current_power = pv.current_power
    daily_energy = pv.daily_energy
    total_energy = pv.total_energy
    efficiency = (pv.ac_1_p + pv.ac_2_p + pv.ac_3_p) / (
        pv.dc_1_u * pv.dc_1_i + pv.dc_2_u * pv.dc_2_i + pv.dc_3_u * pv.dc_3_i)

    w = Weather.query.filter(Weather.created_at >= (datetime.now())).order_by(
        Weather.id.desc()).first()
    current_temp = w.temp

    return render_template("public/home.html", current_power=current_power, daily_energy=daily_energy,
                           total_energy=total_energy, data=None, current_temp=current_temp, efficiency=efficiency)


@blueprint.route("/about/")
def about():
    return render_template("public/about.html")