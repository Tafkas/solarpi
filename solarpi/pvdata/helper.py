# -*- coding: utf-8 -*-
import calendar
from datetime import datetime, timedelta

from sqlalchemy import func

from solarpi.extensions import db, cache
from solarpi.pvdata.models import PVData


@cache.cached(timeout=300, key_prefix="todays_max_power")
def get_todays_max_power():
    """
    :return: the maximum enegy yieled today
    """
    todays_max_power = (
        PVData.query.with_entities(func.max(PVData.current_power).label("todays_max_power"))
        .filter(PVData.created_at >= datetime.now())
        .first()
        .todays_max_power
    )

    if todays_max_power is None:
        todays_max_power = 0

    return todays_max_power


# @cache.memoize(timeout=300)
def get_daily_energy_series(current_date):
    """
    :param current_date: date of the energy series
    :return: energy series
    """
    query = """SELECT created_at,
                       current_power,
                       daily_energy,
                       dc_1_u,
                       dc_2_u,
                       ac_1_u,
                       ac_2_u,
                       ac_3_u
                FROM pvdata
                WHERE DATE(created_at) = ?
                  AND current_power > 0;
    """
    result = db.engine.execute(query, current_date)
    return list(result)


def get_7_day_max_energy_series(current_date):
    """
    :param current_date: pivot date of the energy series
    :return: theoretical maximum energy series ± 3 days around current date
    """
    return (
        PVData.query.with_entities(
            func.strftime("%H:%M:00", PVData.created_at).label("pvdata_created_at"),
            func.max(PVData.current_power).label("pv_max"),
        )
        .filter(PVData.created_at >= (current_date - timedelta(days=3)).strftime("%Y-%m-%d"))
        .filter(PVData.created_at <= (current_date + timedelta(days=3)).strftime("%Y-%m-%d"))
        .filter(PVData.current_power > 0)
        .group_by(func.strftime("%H:%M:00", PVData.created_at))
        .all()
    )


# @cache.memoize(timeout=300)
def get_last_n_days(n):
    """Returns a list of daily yields
    :param n: number of last days
    :return: list of daily yields
    """
    query = f"""SELECT strftime('%Y-%m-%dT00:00:00', created_at) AS created_at,
                       MAX(daily_energy) AS daily_energy
                FROM pvdata
                WHERE DATE(created_at) > DATE('now','-{n} day' )
                GROUP BY DATE(created_at);
    """
    result = db.engine.execute(query)
    return list(result)


@cache.cached(timeout=3600, key_prefix="yearly_series")
def get_yearly_series():
    """Returns a list of yearly generated energy for past years
    :return: list of yearly generated energy for past years
    """
    query = """SELECT strftime('%Y', created_at)            AS year,
                       MAX(total_energy) - MIN(total_energy) AS yearly_output
                FROM pvdata
                GROUP BY strftime('%Y', created_at);
    """
    result = db.engine.execute(query)
    return list(result)


@cache.cached(timeout=3600, key_prefix="max_daily_energy_last_seven_days")
def get_max_daily_energy_last_seven_days():
    """Returns the maximum daily yield within the last 7 days
    :return: returns the maximum energy yielded in the last 7 days
    """
    return (
        PVData.query.with_entities(func.max(PVData.daily_energy).label("max_daily_energy"))
        .filter(PVData.created_at >= (datetime.now() - timedelta(days=7)))
        .first()
        .max_daily_energy
    )


@cache.cached(timeout=3600, key_prefix="last_years_energy")
def get_last_years_energy():
    """Returns the total yielded energy for the previous year
    :return: total energy yielded in the previous year
    """
    current_year = datetime.now().year
    return (
        PVData.query.with_entities(PVData.total_energy)
        .filter(func.strftime("%Y", PVData.created_at) == str(current_year - 1))
        .order_by(PVData.id.desc())
        .first()
    )


def get_current_year_total_energy():
    query = """SELECT MAX(total_energy) - MIN(total_energy) as current_year_total_energy
               FROM pvdata
               WHERE strftime('%Y', created_at) = strftime('%Y', 'now')
               GROUP BY strftime('%Y', 'now');
    """
    result = db.engine.execute(query).first()[0]
    return result


# @cache.cached(timeout=3600, key_prefix="get_yearly_data")
def get_yearly_data(year):
    """Returns the yielded energy for the current year
    :param year: year of the data
    :return: returns an array of monthly energy for a given year
    """
    query = """
    SELECT MAX(total_energy) - MIN(total_energy) AS total_energy
    FROM pvdata
    WHERE strftime('%Y', created_at) = ?
    GROUP BY strftime('%Y-%m', created_at);
    """
    result = db.engine.execute(query, str(year))
    return result


def get_yearly_average_data():
    """Returns the monthly averages for the previous year
    :return: returns an array of monthly averages for previous years
    """
    current_year = str(datetime.now().year)
    query = """WITH monthly_yields AS (SELECT strftime('%m', created_at)            AS month,
                               max(total_energy) - min(total_energy)                AS monthly_yield
                        FROM pvdata
                        WHERE strftime('%Y', created_at) < ?
                        GROUP BY strftime('%Y-%m', created_at))

                SELECT ROUND(avg(monthly_yield), 2) AS avg_monthly_yield,
                       min(monthly_yield)           AS minimum_monthly_yield,
                       max(monthly_yield)           AS maximum_monthly_yield
                FROM monthly_yields
                WHERE monthly_yield > 0
                GROUP BY month;
"""
    result = db.engine.execute(query, current_year)
    return result


def get_current_month_prediction(current_month_energy, last_years_average):
    """

    :param current_month_energy: energy yieled so far this month
    :param last_years_average: daily average energy yield for the same month in the previous year
    :return: series with predicted energy yield for the current month
    """
    now = datetime.now()
    current_month_prediction = int(
        current_month_energy + last_years_average * (calendar.monthrange(now.year, now.month)[1] - now.day + 1)
    )

    current_month_prediction_series = [current_month_prediction if i == (now.month - 1) else "null" for i in range(12)]
    return current_month_prediction_series


def get_current_year_prediction():
    """Computes the prediction of kWh for the remaining days of the current year

    :return: the number of kWh for the remaining year
    """
    query = """WITH rest_of_year AS (SELECT min(total_energy) min_rest_year,
                             max(total_energy) max_rest_year
                      FROM pvdata
                      WHERE strftime('%j', created_at) > strftime('%j', 'now')
                        AND strftime('%Y', created_at) < strftime('%Y', 'now')
                      GROUP BY strftime('%Y', created_at)),

                     combo AS (SELECT max(total_energy) - min(total_energy) AS energy
                               FROM pvdata
                               WHERE strftime('%Y', created_at) = strftime('%Y', 'now')
                               UNION
                               SELECT AVG(max_rest_year - min_rest_year) AS energy
                               FROM rest_of_year)
                SELECT SUM(energy) AS prediction
                FROM combo;"""
    result = db.engine.execute(query)
    return result


def get_efficiency():
    """
    :return: efficiency of the inverter between 0 and 1
    """
    query = """WITH current_values AS (SELECT *
                        FROM pvdata
                        ORDER BY created_at DESC
                        LIMIT 1)

                SELECT ROUND((ac_1_p + ac_2_p + ac_3_p)
                                 / (dc_1_i * dc_1_u +
                                    dc_2_i * dc_2_u +
                                    dc_3_i * dc_3_u), 2) as current_efficiency
                FROM current_values;
    """
    result = db.engine.execute(query).first()[0]
    return result


def get_current_values():
    """
    :return: the current photovoltaic values from the system
    """
    return PVData.query.order_by(PVData.id.desc()).first()


def get_first_date():
    """
    :return: the date in the databse
    """
    return PVData.query.order_by(PVData.id.asc()).first().created_at


def get_sec(s):
    hours, minutes, seconds = map(int, s.split(":"))
    return hours * 3600 + minutes * 60 + seconds


def get_todays_date():
    return datetime.now().date()
