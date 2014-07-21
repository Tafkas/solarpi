# -*- coding: utf-8 -*-
import calendar
from datetime import datetime
from flask.ext.login import login_required
from flask import Blueprint, render_template
from solarpi.data.models import Data

blueprint = Blueprint("data", __name__, url_prefix='/data',
                      static_folder="../static")


@blueprint.route("/")
def index():
    data = Data.query.limit(500)
    categories = [1000 * calendar.timegm(datetime.strptime(d.created_at, "%Y-%m-%dT%H:%M:%S").timetuple()) for d in
                  data]
    series = [int(d.dc_1_i or 0) for d in data]
    data = [list(x) for x in zip(categories, series)]
    return render_template("data/index.html", data=data)