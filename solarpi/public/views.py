# -*- coding: utf-8 -*-
'''Public section, including homepage and signup.'''
from datetime import datetime, timedelta
from flask import (Blueprint, render_template)
from solarpi.pvdata.models import PVData

blueprint = Blueprint('public', __name__, static_folder="../static")


@blueprint.route("/")
def home():
    data = PVData.query.filter(PVData.created_at > (datetime.now() - timedelta(days=1))).order_by(PVData.id.desc())
    current_power = data.first().current_power
    daily_energy = data.first().daily_energy
    total_energy = data.first().total_energy

    return render_template("public/home.html", current_power=current_power, daily_energy=daily_energy,
                           total_energy=total_energy, data=None)


@blueprint.route("/about/")
def about():
    return render_template("public/about.html")