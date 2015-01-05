# -*- coding: utf-8 -*-
import calendar
from datetime import datetime, timedelta

from flask import Blueprint, render_template, flash
from solarpi.charts.helper import get_timestamps
from solarpi.electricity.helper import get_weekly_electricity_import, get_monthly_electricity_import
from solarpi.pvdata.helper import get_sec, get_todays_date, get_daily_energy_series, get_7_day_max_energy_series, \
    get_yearly_series, get_last_n_days

blueprint = Blueprint("charts", __name__, url_prefix='/charts',
                      static_folder="../static")


@blueprint.route("/daily")
@blueprint.route("/daily/<date>")
def daily(date=get_todays_date().strftime('%Y-%m-%d')):
    error = None
    try:
        current_date = datetime.strptime(date, "%Y-%m-%d")
    except ValueError, TypeError:
        error = "invalid date, displaying today's data instead"
        current_date = get_todays_date()
    yesterday = current_date - timedelta(days=1)
    tomorrow = current_date + timedelta(days=1)

    # get photovoltaic data for the day
    pv = get_daily_energy_series(current_date)

    timestamps_pv = get_timestamps(pv)
    daily_chart_data = [list(x) for x in zip(timestamps_pv, [(int(d.current_power or 0)) for d in pv])]

    # voltages
    input_voltage_1_chart_data = [list(x) for x in zip(timestamps_pv, [(int(d.dc_1_u or 0)) for d in pv])]
    input_voltage_2_chart_data = [list(x) for x in zip(timestamps_pv, [(int(d.dc_2_u or 0)) for d in pv])]
    output_voltage_1_chart_data = [list(x) for x in zip(timestamps_pv, [(int(d.ac_1_u or 0)) for d in pv])]
    output_voltage_2_chart_data = [list(x) for x in zip(timestamps_pv, [(int(d.ac_2_u or 0)) for d in pv])]
    output_voltage_3_chart_data = [list(x) for x in zip(timestamps_pv, [(int(d.ac_3_u or 0)) for d in pv])]

    # get maxium photovoltaic data for ± 3 days
    pv_max = get_7_day_max_energy_series(current_date)
    current_date_midnight = calendar.timegm(current_date.timetuple())
    timestamps_pv_max = [1000 * (get_sec(d.pvdata_created_at) + current_date_midnight)
                         for d in pv_max]
    daily_chart_max_data = [list(x) for x in zip(timestamps_pv_max, [(int(d.pv_max or 0)) for d in pv_max])]

    # additional data
    if len(pv) > 0:
        daily_energy = pv[-1].daily_energy
    else:
        daily_energy = 0.0

    return render_template("charts/daily.html", data=daily_chart_data, data2=daily_chart_max_data,
                           yesterday=yesterday, today=current_date,
                           tomorrow=tomorrow, daily_energy=daily_energy, all_data=pv,
                           input_voltage_1_chart_data=input_voltage_1_chart_data,
                           input_voltage_2_chart_data=input_voltage_2_chart_data,
                           output_voltage_1_chart_data=output_voltage_1_chart_data,
                           output_voltage_2_chart_data=output_voltage_2_chart_data,
                           output_voltage_3_chart_data=output_voltage_3_chart_data,
                           error=error)


@blueprint.route("/weekly")
def weekly():
    # solar data
    pv = list(get_last_n_days(7))
    timestamps = get_timestamps(pv)
    series = [(float(d.daily_energy or 0)) for d in pv]
    seven_days_energy = sum(series)
    weekly_pv_chart_data = [list(x) for x in zip(timestamps, series)]

    electricity_import = [(float(d.electricity_import or 0)) for d in get_weekly_electricity_import()]
    weekly_import_chart_data = [list(x) for x in zip(timestamps, electricity_import)]

    return render_template("charts/weekly.html", pvdata=weekly_pv_chart_data, importData=weekly_import_chart_data,
                           seven_days_energy=seven_days_energy)


@blueprint.route("/monthly")
def monthly():
    pv = list(get_last_n_days(30))
    timestamps = get_timestamps(pv)
    series = [(float(d.daily_energy or 0)) for d in pv]
    monthly_energy = sum(series)
    monthly_pv_chart_data = [list(x) for x in zip(timestamps, series)]

    electricity_import = [(float(d.electricity_import or 0)) for d in get_monthly_electricity_import()]
    monthly_import_chart_data = [list(x) for x in zip(timestamps, electricity_import)]

    return render_template("charts/monthly.html", pvdata=monthly_pv_chart_data,
                           importData=monthly_import_chart_data, monthly_energy=monthly_energy)


@blueprint.route("/yearly")
def yearly():
    data = list(get_yearly_series())
    total_energy = sum([x[1] for x in data])
    years = [int(x[0]) for x in data]
    data = [x[1] for x in data]
    yearly_data = [5741.82 for i in range(len(data))]

    return render_template("charts/yearly.html", data=data, yearlyData=yearly_data,
                           total_energy=total_energy, years=years)