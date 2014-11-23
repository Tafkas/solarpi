# -*- coding: utf-8 -*-
'''Public section, including homepage and signup.'''
import calendar
import dateutil.parser
from cookielib import eff_request_host
from datetime import datetime, timedelta
from flask import (Blueprint, render_template)
from sqlalchemy import func
from solarpi.public.helper import get_operating_hours
from solarpi.pvdata.models import PVData
from solarpi.electricity.models import Electricity


blueprint = Blueprint('electricity', __name__, static_folder="../static")


@blueprint.route("/")
def home():
    render_template()