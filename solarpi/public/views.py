# -*- coding: utf-8 -*-
'''Public section, including homepage and signup.'''
from datetime import datetime, timedelta
from flask import (Blueprint, render_template)
from solarpi.data.models import Data

blueprint = Blueprint('public', __name__, static_folder="../static")


@blueprint.route("/")
def home():
    data = Data.query.filter(Data.created_at > (datetime.now() - timedelta(days=1)))
    current_power = data[-1].current_power
    daily_energy = data[-1].daily_energy
    total_energy = data[-1].total_energy
    return render_template("public/home.html", current_power=current_power, daily_energy=daily_energy,
                           total_energy=total_energy, data=None)


@blueprint.route("/about/")
def about():
    return render_template("public/about.html")