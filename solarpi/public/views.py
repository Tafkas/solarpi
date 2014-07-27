# -*- coding: utf-8 -*-
'''Public section, including homepage and signup.'''
from datetime import datetime, timedelta
from flask import (Blueprint, request, render_template)
from solarpi.data.models import Data

from solarpi.public.forms import LoginForm

blueprint = Blueprint('public', __name__, static_folder="../static")


@blueprint.route("/")
def home():
    data = Data.query.filter(Data.created_at > (datetime.now() - timedelta(days=1)))
    actual_energy = data[-1].actual_energy
    daily_energy = data[-1].daily_energy
    total_energy = data[-1].total_energy
    return render_template("public/home.html", actual_energy=actual_energy, daily_energy=daily_energy,
                           total_energy=total_energy)


@blueprint.route("/about/")
def about():
    form = LoginForm(request.form)
    return render_template("public/about.html")