from flask import Blueprint, render_template

from solarpi.extensions import db, cache

blueprint = Blueprint("statistics", __name__, url_prefix="/statistics", static_folder="../static")


@blueprint.route("/")
@cache.cached(timeout=3600, key_prefix="statistics")
def statistics():
    """Renders a page with statistics for the last 12 months
    :return: a page with statistics for the last 12 months
    """
    data = list(
        db.engine.execute(
            """SELECT
              Strftime('%Y-%m', created_at) AS month,
              Min(daily_yield) AS min_yield,
              Max(daily_yield) AS max_yield,
              Avg(daily_yield) AS avg_yield
            FROM (
              SELECT
                Strftime('%Y-%m-%d', created_at) AS created_at,
                Max(total_energy) - Min(total_energy) AS daily_yield
              FROM pvdata
              GROUP BY Strftime('%Y-%m-%d', created_at))
            GROUP BY Strftime('%Y-%m', created_at) ORDER BY month DESC LIMIT 12 """
        )
    )
    return render_template("statistics/statistics.html", data=data)
