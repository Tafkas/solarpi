# -*- coding: utf-8 -*-
import calendar
from datetime import datetime, timedelta
from flask.ext.login import login_required
from flask import Blueprint, render_template
from solarpi.data.models import Data

blueprint = Blueprint("data", __name__, url_prefix='/data',
                      static_folder="../static")


@blueprint.route("/")
@blueprint.route("/<date>")
def index(date):
    try:
        current_date = datetime.strptime(date, "%Y-%m-%d")
    except ValueError:
        current_date = datetime.strptime('2014-04-21', "%Y-%m-%d")
    yesterday = current_date - timedelta(days=1)
    tomorrow = current_date + timedelta(days=1)
    data = Data.query.filter(Data.created_at > current_date.strftime('%Y-%m-%d')).filter(
        Data.created_at < tomorrow.strftime('%Y-%m-%d'))
    categories = [1000 * calendar.timegm(datetime.strptime(d.created_at, "%Y-%m-%dT%H:%M:%S").timetuple()) for d in
                  data]
    series = [(float(d.dc_1_p or 0) + float(d.dc_2_p or 0)) for d in data]
    data = [list(x) for x in zip(categories, series)]
    return render_template("data/index.html", data=data, yesterday=yesterday, today=current_date, tomorrow=tomorrow)