from datetime import datetime, timedelta

from solarpi.extensions import db

START_DATE = datetime.strptime("2013-01-31", "%Y-%m-%d")
LAT, LON = 52.518611111111, 13.408055555556


def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days)):
        yield start_date + timedelta(n)


def get_operating_hours():
    query = """WITH daily_seconds AS (SELECT DATE(created_at),
                              MAX(strftime('%s', created_at)) - MIN(strftime('%s', created_at)) total_seconds
                       FROM pvdata
                       GROUP BY DATE(created_at))
                SELECT SUM(total_seconds) / (60 * 60 * 24)
                FROM daily_seconds;
    """
    result = db.engine.execute(query).first()[0]
    return result


def get_operating_days():
    today = datetime.now()
    delta = today - START_DATE
    return delta.days
