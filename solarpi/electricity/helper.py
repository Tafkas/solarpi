# -*- coding: utf-8 -*-
from datetime import datetime, timedelta

from sqlalchemy import func

from solarpi.electricity.models import Electricity
from solarpi.extensions import db, cache


@cache.cached(timeout=300, key_prefix='todays_electricity')
def get_todays_electricity():
    return (Electricity.query
            .with_entities((func.max(Electricity.meter_280) - func.min(Electricity.meter_280)).label('todays_export'),
                           (func.max(Electricity.meter_180) - func.min(Electricity.meter_180)).label('todays_import'))
            .filter(func.strftime('%Y-%m-%d', Electricity.created_at) == datetime.now().strftime('%Y-%m-%d'))
            .group_by(func.strftime('%Y-%m-%d', Electricity.created_at))
            .first())


def get_last_n_days_import(n):
    query = """SELECT
                  strftime('%Y-%m-%dT00:00:00', created_at) AS created_at,
                  max(meter_180) - min(meter_180) AS electricity_import
               FROM electricity_data
               WHERE created_at > ?
               GROUP BY strftime('%Y-%m-%d', created_at)"""
    return db.engine.execute(query, (datetime.now() - timedelta(days=n)))


@cache.cached(timeout=3600, key_prefix='last_year_export')
def get_last_year_export():
    current_year = datetime.now().year
    return Electricity.query.with_entities(Electricity.meter_280).filter(
        func.strftime('%Y', Electricity.created_at) == str(current_year - 1)).order_by(Electricity.id.desc()).first()


@cache.cached(timeout=3600, key_prefix='total_electricity')
def get_total_electricity():
    return Electricity.query.order_by(Electricity.id.desc()).first()
