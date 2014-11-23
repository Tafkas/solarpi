# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
from sqlalchemy import func
from solarpi.electricity.models import Electricity


def get_todays_electricity():
    return Electricity.query.with_entities(
        (func.max(Electricity.meter_280) - func.min(Electricity.meter_280)).label(
            'todays_export'), (func.max(Electricity.meter_180) - func.min(Electricity.meter_180)).label(
            'todays_import')).filter(
        func.strftime('%Y-%m-%d', Electricity.created_at) == datetime.now().strftime('%Y-%m-%d')).group_by(
        func.strftime('%Y-%m-%d', Electricity.created_at)).first()


def get_last_year_export():
    return Electricity.query.with_entities(Electricity.meter_280).filter(
        func.strftime('%Y', Electricity.created_at) == '2013').order_by(Electricity.id.desc()).first()
