# -*- coding: utf-8 -*-
import calendar
from datetime import datetime, timedelta
from sqlalchemy import func
from solarpi.pvdata.models import PVData


def get_todays_max_power():
    """
    :return: the maximum enegy yieled today
    """
    todays_max_power = PVData.query.with_entities(func.max(PVData.current_power).label('todays_max_power')).filter(
        PVData.created_at >= datetime.now()).first().todays_max_power

    if not todays_max_power:
        todays_max_power = 0

    return todays_max_power


def get_daily_energy_series(current_date):
    """
    :param current_date: date of the energy series
    :return: energy series
    """
    tomorrow = current_date + timedelta(days=1)
    return PVData.query.with_entities(PVData.created_at, PVData.current_power, PVData.daily_energy, PVData.dc_1_u,
                                      PVData.dc_2_u, PVData.ac_1_u, PVData.ac_2_u, PVData.ac_3_u).filter(
        PVData.created_at > current_date.strftime('%Y-%m-%d')).filter(
        PVData.created_at < tomorrow.strftime('%Y-%m-%d')).filter(PVData.current_power > 0).all()


def get_7_day_max_energy_series(current_date):
    """
    :param current_date: pivot date of the energy series
    :return: theoretical maximum energy series ± 3 days around current date
    """
    return PVData.query.with_entities(func.strftime('%H:%M:00', PVData.created_at).label('pvdata_created_at'),
                                      func.max(PVData.current_power).label('pv_max')).filter(
        PVData.created_at >= (current_date - timedelta(days=3)).strftime('%Y-%m-%d')).filter(
        PVData.created_at <= (current_date + timedelta(days=3)).strftime('%Y-%m-%d')).filter(
        PVData.current_power > 0).group_by(
        func.strftime('%H:%M:00', PVData.created_at)).all()


def get_weekly_series():
    return PVData.query.with_entities(
        func.strftime('%Y-%m-%dT00:00:00', PVData.created_at).label('created_at'),
        func.max(PVData.daily_energy).label('daily_energy')).filter(
        PVData.created_at > datetime.now() - timedelta(days=7)).group_by(func.strftime('%Y-%m-%d', PVData.created_at))


def get_monthly_series():
    return PVData.query.with_entities(
        func.strftime('%Y-%m-%dT00:00:00', PVData.created_at).label('created_at'),
        func.max(PVData.daily_energy).label('daily_energy')).filter(
        PVData.created_at > datetime.now() - timedelta(days=30)).group_by(func.strftime('%Y-%m-%d', PVData.created_at))


def get_yearly_series():
    return PVData.query.with_entities(
        func.max(PVData.total_energy.label('total_energy'))).group_by(
        func.strftime("%Y", PVData.created_at)).all()


def get_max_daily_energy_last_seven_days():
    """
    :return: returns the maximum energy yielded in the last 7 days
    """
    return PVData.query.with_entities(
        func.max(PVData.daily_energy).label('max_daily_energy')).filter(
        PVData.created_at >= (datetime.now() - timedelta(days=7))).first().max_daily_energy


def get_last_years_energy():
    """
    :return: total energy yielded in the previous year
    """
    return PVData.query.with_entities(PVData.total_energy).filter(
        func.strftime('%Y', PVData.created_at) == '2013').order_by(PVData.id.desc()).first()


def get_yearly_data(year):
    """
    :param year: year of the data
    :return: returns an array of monthly energy for a given year
    """
    return PVData.query.with_entities(func.strftime('%m', PVData.created_at).label('created_at'),
                                      (func.max(PVData.total_energy) - func.min(PVData.total_energy)).label(
                                          'total_energy')).filter(
        func.strftime('%Y', PVData.created_at) == str(year)).group_by(
        func.strftime('%Y-%m', PVData.created_at)).all()


def get_current_month_prediction(current_month_energy, last_years_average):
    """

    :param current_month_energy: energy yieled so far this month
    :param last_years_average: daily average energy yield for the same month in the previous year
    :return: predicted energy yield for the current month
    """
    now = datetime.now()
    if now.day > 1:
        current_month = int(
            current_month_energy + last_years_average * (
                calendar.monthrange(now.year, now.month)[1] - now.day + 1))
    else:
        current_month = 0
    current_month_series = ['null'] * 12
    current_month_series[now.month - 1] = current_month
    return current_month_series


def get_current_values():
    """
    :return: the current photovoltaic values from the system
    """
    return PVData.query.order_by(PVData.id.desc()).first()


def get_sec(s):
    l = map(int, s.split(':'))
    return sum(n * sec for n, sec in zip(l[::-1], (1, 60, 3600)))


def get_todays_date():
    return datetime.now().date()