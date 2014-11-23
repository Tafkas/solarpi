from flask import Blueprint, render_template
from sqlalchemy import desc, func
from solarpi.pvdata.models import PVData

blueprint = Blueprint("statistics", __name__, url_prefix='/statistics',
                      static_folder="../static")


@blueprint.route("/")
def statistics():
    data = PVData.query.with_entities(func.strftime('%Y-%m', PVData.created_at).label('month'),
                                      func.avg(PVData.daily_energy).label('avg_daily_energy'),
                                      func.max(PVData.daily_energy).label('max_daily_energy')).filter(
        PVData.current_power > 0).group_by(func.strftime('%Y-%m', PVData.created_at)).order_by(
        desc(PVData.created_at)).limit(12).all()

    return render_template('statistics/statistics.html', data=data)