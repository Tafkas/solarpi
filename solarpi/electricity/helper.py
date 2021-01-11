# -*- coding: utf-8 -*-
from datetime import datetime, timedelta

from sqlalchemy import func

from solarpi.electricity.models import Electricity
from solarpi.extensions import cache, db


@cache.cached(timeout=300, key_prefix='todays_electricity')
def get_todays_electricity():
    return (Electricity.query
            .with_entities((func.max(Electricity.meter_280) - func.min(Electricity.meter_280)).label('todays_export'),
                           (func.max(Electricity.meter_180) - func.min(Electricity.meter_180)).label('todays_import'))
            .filter(func.strftime('%Y-%m-%d', Electricity.created_at) == datetime.now().strftime('%Y-%m-%d'))
            .group_by(func.strftime('%Y-%m-%d', Electricity.created_at))
            .first())


@cache.memoize(timeout=300)
def get_last_n_days_import(n):
    return (Electricity.query.
            with_entities(func.strftime('%Y-%m-%dT00:00:00', Electricity.created_at).label('created_at'),
                          (func.max(Electricity.meter_180) - func.min(Electricity.meter_180))
                          .label('electricity_import'))
            .filter(Electricity.created_at > (datetime.now() - timedelta(days=n)))
            .group_by(func.strftime('%Y-%m-%d', Electricity.created_at))
            .all())


@cache.cached(timeout=3600, key_prefix='last_year_export')
def get_last_year_export():
    current_year = datetime.now().year
    return Electricity.query.with_entities(Electricity.meter_280).filter(
        func.strftime('%Y', Electricity.created_at) == str(current_year - 1)).order_by(Electricity.id.desc()).first()


@cache.cached(timeout=3600, key_prefix='total_electricity')
def get_total_electricity():
    return Electricity.query.order_by(Electricity.id.desc()).first()


@cache.cached(timeout=3600, key_prefix='current_year_earnings')
def get_current_year_earnings():
    query = """SELECT
                    sum( delta_280 ) * 0.1702 AS total_earnings -- EUR per kWh
                FROM
                    (
                    SELECT
                        max( meter_280 ) - min( meter_280 ) AS delta_280 
                    FROM
                        electricity_data 
                    WHERE
                        strftime( '%Y', created_at ) = strftime('%Y', 'now')
                    GROUP BY
                    strftime( '%Y-%m-%d', created_at ) 
                    ) q;"""
    result = db.engine.execute(query).first()[0]
    return result


@cache.cached(timeout=3600, key_prefix='total_earnings')
def get_total_earnings():
    query = """SELECT
                    sum( delta_280 ) * 0.1702 as total_earnings -- EUR per kWh
                FROM
                    (
                    SELECT
                        max( meter_280 ) - min( meter_280 ) AS delta_280 
                    FROM
                        electricity_data 
                    GROUP BY
                    strftime( '%Y-%m-%d', created_at ) 
                    ) q;"""
    result = db.engine.execute(query).first()[0]
    return result
