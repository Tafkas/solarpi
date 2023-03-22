# -*- coding: utf-8 -*-
from datetime import datetime, timedelta

from sqlalchemy import func

from solarpi.electricity.models import Electricity
from solarpi.extensions import cache, db


@cache.cached(timeout=300, key_prefix="todays_electricity")
def get_todays_electricity():
    query = """SELECT
                    MAX(meter_280) - MIN(meter_280) AS todays_export,
                    MAX(meter_180) - MIN(meter_180) AS todays_import
                FROM electricity_data
                WHERE DATE(created_at) = DATE('now')
                GROUP BY DATE(created_at);"""
    result = db.engine.execute(query).first()
    print(result)
    return result


@cache.memoize(timeout=300)
def get_last_n_days_import(n):
    return (
        Electricity.query.with_entities(
            func.strftime("%Y-%m-%dT00:00:00", Electricity.created_at).label("created_at"),
            (func.max(Electricity.meter_180) - func.min(Electricity.meter_180)).label("electricity_import"),
        )
        .filter(Electricity.created_at > (datetime.now() - timedelta(days=n)))
        .group_by(func.strftime("%Y-%m-%d", Electricity.created_at))
        .all()
    )


@cache.memoize(timeout=300)
def get_last_n_days_export(n):
    return (
        Electricity.query.with_entities(
            func.strftime("%Y-%m-%dT00:00:00", Electricity.created_at).label("created_at"),
            (func.max(Electricity.meter_280) - func.min(Electricity.meter_280)).label("electricity_export"),
        )
        .filter(Electricity.created_at > (datetime.now() - timedelta(days=n)))
        .group_by(func.strftime("%Y-%m-%d", Electricity.created_at))
        .all()
    )


@cache.cached(timeout=3600, key_prefix="last_year_export")
def get_last_year_export():
    current_year = datetime.now().year
    return (
        Electricity.query.with_entities(Electricity.meter_280)
        .filter(func.strftime("%Y", Electricity.created_at) == str(current_year - 1))
        .order_by(Electricity.id.desc())
        .first()
    )


@cache.cached(timeout=3600, key_prefix="total_electricity")
def get_total_electricity():
    return Electricity.query.order_by(Electricity.id.desc()).first()


@cache.cached(timeout=3600, key_prefix="current_year_earnings")
def get_current_year_earnings():
    query = """WITH current_year_exports AS (SELECT max(meter_280) - min(meter_280) AS delta_280
                              FROM electricity_data
                              WHERE strftime('%Y', created_at) = strftime('%Y', 'now')
                              GROUP BY DATE(created_at))
                SELECT ROUND(SUM(delta_280) * 0.1702, 2) AS total_earnings -- EUR per kWh
                FROM current_year_exports;"""
    result = db.engine.execute(query).first()[0]
    return result


@cache.cached(timeout=3600, key_prefix="total_earnings")
def get_total_earnings():
    query = """WITH daily_exports AS (SELECT max(meter_280) - min(meter_280) AS delta_280
                       FROM electricity_data
                       GROUP BY DATE(created_at))
                SELECT ROUND(SUM(delta_280) * 0.1702, 2) AS total_earnings -- EUR per kWh
                FROM daily_exports;"""
    result = db.engine.execute(query).first()[0]
    return result
