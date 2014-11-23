from datetime import timedelta, datetime
from itertools import chain
from flask import Blueprint, render_template
from sqlalchemy import func
from solarpi.pvdata.models import PVData
from solarpi.electricity.models import Electricity


blueprint = Blueprint("tables", __name__, url_prefix='/tables',
                      static_folder="../static")


@blueprint.route("/")
def tables():
    pvdata = PVData.query.with_entities(func.strftime('%Y-%m-%d', PVData.created_at).label('created_at'),
                                        func.max(PVData.daily_energy).label('daily_energy'),
                                        func.max(PVData.current_power).label('max_output'),
                                        func.max(PVData.total_energy).label('total_energy')).filter(
        PVData.created_at > datetime.now() - timedelta(days=30)).group_by(
        func.strftime('%Y-%m-%d', PVData.created_at)).all()

    data = reversed(pvdata)
    return render_template('tables/tables.html', data=data)