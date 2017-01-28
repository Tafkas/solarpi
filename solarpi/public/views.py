# -*- coding: utf-8 -*-
"""Public section, including homepage."""
import calendar
from datetime import datetime, timedelta

import dateutil.parser
from flask import (Blueprint, render_template, make_response, current_app, url_for, request)

from solarpi.electricity.helper import get_todays_electricity, get_last_year_export, get_total_electricity
from solarpi.electricity.models import Electricity
from solarpi.public.helper import get_operating_days
from solarpi.pvdata.helper import (get_todays_max_power, get_max_daily_energy_last_seven_days, get_current_values,
                                   get_last_years_energy, get_yearly_data, get_current_month_prediction, get_first_date,
                                   get_yearly_average_data, get_efficiency)
from solarpi.weather.helper import get_weather_icon, get_current_weather

blueprint = Blueprint('public', __name__, static_folder="../static")


@blueprint.route("/")
def home():
    """Renders the dashboard
    :return: the dashboard page
    """
    operating_days = get_operating_days()
    now = datetime.now()

    # weather
    current_temp, current_weather = None, None
    current_weather = get_current_weather()
    if current_weather:
        current_temp = current_weather.temp
        current_weather = get_weather_icon(current_weather.weather_id)

    # photovoltaic data
    pv = get_current_values()
    current_power = pv.current_power
    daily_energy = pv.daily_energy
    total_energy = pv.total_energy

    # efficiency
    efficiency = get_efficiency(pv)

    last_updated = dateutil.parser.parse(pv.created_at).strftime('%Y-%m-%d %H:%M')

    todays_max_power = get_todays_max_power()
    if not todays_max_power:
        todays_max_power = 0
        daily_energy = 0
        current_temp = None

    max_daily_energy_last_seven_days = get_max_daily_energy_last_seven_days()

    # electricity im- and export

    total_electricity = get_total_electricity()
    total_import = total_electricity.meter_180
    total_export = total_electricity.meter_280
    last_year_export = get_last_year_export()
    current_year_export = total_export - last_year_export.meter_280

    todays_import, todays_export = 0.0, 0.0
    todays_electricity = get_todays_electricity()
    if todays_electricity:
        todays_import = todays_electricity.todays_import
        todays_export = todays_electricity.todays_export

    last_year_energy = get_last_years_energy()
    current_year_energy = total_energy - last_year_energy.total_energy

    average_years_series = [int(x[0]) for x in get_yearly_average_data()]
    current_year_series = [int(x[0]) for x in get_yearly_data(datetime.now().year)]

    last_year_current_month_avg = average_years_series[now.month - 1] / calendar.monthrange(now.year, now.month)[1]
    current_month_prediction = get_current_month_prediction(current_year_series[-1], last_year_current_month_avg)

    return render_template("public/home.html",
                           current_power=current_power, daily_energy=daily_energy,
                           total_energy=total_energy, efficiency=efficiency,
                           current_temp=current_temp, current_weather=current_weather,
                           ac_1_p=pv.ac_1_p, ac_2_p=pv.ac_2_p, ac_3_p=pv.ac_3_p,
                           ac_1_u=pv.ac_1_u, ac_2_u=pv.ac_2_u, ac_3_u=pv.ac_3_u,
                           dc_1_u=pv.dc_1_u, dc_2_u=pv.dc_2_u, dc_3_u=pv.dc_3_u,
                           dc_1_i=pv.dc_1_i, dc_2_i=pv.dc_2_i, dc_3_i=pv.dc_3_i,
                           average_years_series=average_years_series, current_year_series=current_year_series,
                           current_month_pred=current_month_prediction,
                           current_year_energy=current_year_energy,
                           max_daily_energy_last_seven_days=max_daily_energy_last_seven_days,
                           todays_max_power=todays_max_power, last_updated=last_updated,
                           operating_days=operating_days, total_export=total_export,
                           total_import=total_import, todays_export=todays_export,
                           todays_import=todays_import, current_year_export=current_year_export)


@blueprint.route("/about/")
def about():
    """Renders the about page
    :return: the about page
    """
    return render_template("public/about.html")


@blueprint.route("/sitemap.xml")
def sitemap():
    """Renders a sitemap.xml for search engines
    :return: an xml sitemap
    """
    url_root = request.url_root[:-1]
    pages = []
    today = datetime.now()
    ten_days_ago = (today - timedelta(days=10)).date().isoformat()
    # static pages
    for rule in current_app.url_map.iter_rules():
        if "GET" in rule.methods and len(rule.arguments) == 0:
            url = url_root + '%s' % rule.rule
            pages.append([url, ten_days_ago])

    # daily charts
    start_date = dateutil.parser.parse(get_first_date())
    total_days = (today - start_date).days + 1

    for day_number in range(total_days):
        current_date = (start_date + timedelta(days=day_number)).date()
        url = url_root + url_for('charts.daily') + '/%s' % current_date
        pages.append([url, current_date])

    sitemap_xml = render_template("public/sitemap_template.xml", pages=pages)
    response = make_response(sitemap_xml)
    response.headers["Content-Type"] = "application/xml"

    return response
