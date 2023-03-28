# -*- coding: utf-8 -*-
import calendar
from datetime import datetime, timedelta

from flask import Blueprint, render_template

from solarpi.charts.helper import get_timestamps, get_daily_pv_chart_data
from solarpi.electricity.helper import get_last_n_days_import, get_last_n_days_export
from solarpi.pvdata.helper import (
    get_sec,
    get_todays_date,
    get_daily_energy_series,
    get_7_day_max_energy_series,
    get_yearly_series,
    get_last_n_days,
    get_current_year_prediction,
)

blueprint = Blueprint("charts", __name__, url_prefix="/charts", static_folder="../static")


@blueprint.route("/daily")
@blueprint.route("/daily/<date>")
def daily(date=None):
    """Renders a page with charts for a given date
    :param date: a date in the format %Y-%m-%d
    :return: page with charts for a given date
    """
    error = None
    current_date = get_todays_date()
    try:
        if date:
            current_date = datetime.strptime(date, "%Y-%m-%d").date()
    except ValueError:
        error = "invalid date, displaying today's data instead"
        current_date = get_todays_date()
    yesterday = current_date - timedelta(days=1)
    tomorrow = current_date + timedelta(days=1)

    # get photovoltaic data for the day
    pv = get_daily_energy_series(current_date)

    daily_chart_data = get_daily_pv_chart_data(pv)

    timestamps_pv = get_timestamps(pv)
    # voltages
    input_voltage_1_chart_data = [list(x) for x in zip(timestamps_pv, [(int(d.dc_1_u or 0)) for d in pv])]
    input_voltage_2_chart_data = [list(x) for x in zip(timestamps_pv, [(int(d.dc_2_u or 0)) for d in pv])]
    output_voltage_1_chart_data = [list(x) for x in zip(timestamps_pv, [(int(d.ac_1_u or 0)) for d in pv])]
    output_voltage_2_chart_data = [list(x) for x in zip(timestamps_pv, [(int(d.ac_2_u or 0)) for d in pv])]
    output_voltage_3_chart_data = [list(x) for x in zip(timestamps_pv, [(int(d.ac_3_u or 0)) for d in pv])]

    # get maxium photovoltaic data for ± 3 days
    pv_max = get_7_day_max_energy_series(current_date)
    current_date_midnight = calendar.timegm(current_date.timetuple())
    timestamps_pv_max = [1000 * (get_sec(d.pvdata_created_at) + current_date_midnight) for d in pv_max]
    daily_chart_max_data = [list(x) for x in zip(timestamps_pv_max, [(int(d.pv_max or 0)) for d in pv_max])]

    # additional data
    daily_energy = 0.0
    if pv:
        daily_energy = pv[-1].daily_energy

    return render_template(
        "charts/daily.html",
        data=daily_chart_data,
        data2=daily_chart_max_data,
        yesterday=yesterday,
        today=current_date,
        tomorrow=tomorrow,
        daily_energy=daily_energy,
        all_data=pv,
        input_voltage_1_chart_data=input_voltage_1_chart_data,
        input_voltage_2_chart_data=input_voltage_2_chart_data,
        output_voltage_1_chart_data=output_voltage_1_chart_data,
        output_voltage_2_chart_data=output_voltage_2_chart_data,
        output_voltage_3_chart_data=output_voltage_3_chart_data,
        error=error,
    )


@blueprint.route("/weekly")
def weekly():
    """Renders a page with charts for the last seven days
    :return: a page with charts for the last seven days
    """
    return get_last_days_chart(number_of_days=7)


@blueprint.route("/monthly")
def monthly():
    """Renders a page with charts for the last 30 days
    :return: a page with charts for the last 30 days
    """
    return get_last_days_chart(number_of_days=30)


def get_last_days_chart(number_of_days=7):
    pv = get_last_n_days(number_of_days)
    timestamps = get_timestamps(pv)
    series = [(float(d.daily_energy or 0)) for d in pv]
    total_energy = sum(series)
    pv_chart_data = [list(x) for x in zip(timestamps, series)]

    electricity_import = [(float(d.daily_import or 0)) for d in get_last_n_days_import(number_of_days)]
    electricity_export = [(float(d.daily_export or 0)) for d in get_last_n_days_export(number_of_days)]
    import_chart_data = [list(x) for x in zip(timestamps, electricity_import)]
    export_chart_data = [list(x) for x in zip(timestamps, electricity_export)]
    return render_template(
        "charts/last_days.html",
        number_of_days=number_of_days,
        pvdata=pv_chart_data,
        importData=import_chart_data,
        exportData=export_chart_data,
        total_energy=total_energy,
    )


@blueprint.route("/yearly")
def yearly():
    """Renders a page with charts for the last years
    :return: a page with charts for the last years
    """
    data = list(get_yearly_series())
    total_energy = sum([x[1] for x in data])
    years = [int(x[0]) for x in data]
    data = [x[1] for x in data]
    yearly_data = len(data) * [5741.82]
    prediction = (len(data) - 1) * ["null"]
    prediction.extend([int(x[0]) for x in list(get_current_year_prediction())])

    return render_template(
        "charts/yearly.html",
        data=data,
        yearlyData=yearly_data,
        total_energy=total_energy,
        prediction=prediction,
        years=years,
    )
