import calendar
from datetime import datetime, timedelta

from flask import Blueprint, render_template

from solarpi.weather.models import Weather

blueprint = Blueprint("weather", __name__, url_prefix='/weather',
                      static_folder="../static")


@blueprint.route("/daily")
@blueprint.route("/daily/<date>")
def daily(date=datetime.now().strftime('%Y-%m-%d')):
    try:
        current_date = datetime.strptime(date, "%Y-%m-%d")
    except ValueError:
        current_date = datetime.strptime('2014-04-21', "%Y-%m-%d")
    yesterday = current_date - timedelta(days=1)
    tomorrow = current_date + timedelta(days=1)
    w = Weather.query.with_entities(Weather.created_at, Weather.temp).filter(
        Weather.created_at > current_date.strftime('%Y-%m-%d')).filter(
        Weather.created_at < tomorrow.strftime('%Y-%m-%d')).all()

    timestamps_w = [
        1000 * calendar.timegm(datetime.strptime(d.created_at.split(".")[0], "%Y-%m-%dT%H:%M:%S").timetuple())
        for d in w]
    series_w = [(int(d.temp or 0)) for d in w]
    daily_chart_data = [list(x) for x in zip(timestamps_w, series_w)]

    return render_template("weather/daily.html", data=daily_chart_data, yesterday=yesterday,
                           today=current_date, tomorrow=tomorrow, all_data=w)
