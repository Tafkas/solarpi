from datetime import timedelta, datetime
from itertools import chain
from flask import Blueprint, render_template
from sqlalchemy import func
from solarpi.extensions import db
from solarpi.pvdata.models import PVData
from solarpi.electricity.models import Electricity


blueprint = Blueprint("tables", __name__, url_prefix='/tables',
                      static_folder="../static")


@blueprint.route("/")
def tables():
    last_30_days = datetime.now() - timedelta(days=30)
    data = db.engine.execute(
        "SELECT "
            "p.*, e.daily_import, e.daily_export "
        "FROM ("
            "SELECT "
                "Strftime('%Y-%m-%d', created_at) AS created_at, "
                "Max(daily_energy) AS daily_energy, "
                "Max(current_power) AS max_output, "
                "Max(total_energy) AS total_energy "
            "FROM pvdata "
            "WHERE Strftime('%Y-%m-%d', created_at) > ? "
            "GROUP BY Strftime('%Y-%m-%d', created_at)) p "
        "JOIN ("
            "SELECT "
                "Strftime('%Y-%m-%d', created_at) AS created_at, "
                "Max(meter_180) - Min(meter_180) AS daily_import, "
                "Max(meter_280) - Min(meter_280) AS daily_export "
            "FROM electricity_data "
            "WHERE Strftime('%Y-%m-%d', created_at) > ? "
            "GROUP BY Strftime('%Y-%m-%d', created_at)"
        ") e ON p.created_at = e.created_at "
        "ORDER BY created_at DESC",
        (last_30_days, last_30_days))
    return render_template('tables/tables.html', data=list(data))