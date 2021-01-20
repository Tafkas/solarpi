import time
from datetime import datetime, timedelta

from pysolar.util import get_sunrise_sunset

START_DATE = datetime.strptime("2013-01-31", "%Y-%m-%d")
LAT, LON = 52.518611111111, 13.408055555556


def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days)):
        yield start_date + timedelta(n)


def get_operating_hours():
    today = datetime.now()
    operating_hours = 0
    for single_date in daterange(START_DATE, today):
        day = datetime.fromtimestamp(time.mktime(single_date.timetuple()))
        sun_rise_set = get_sunrise_sunset(LAT, LON, day)
        daily_operating_hours = sun_rise_set[1] - sun_rise_set[0]
        operating_hours += divmod(daily_operating_hours.total_seconds(), 3600)[0]
    return 1.05 * operating_hours  # adding 5% overhead


def get_operating_days():
    today = datetime.now()
    delta = today - START_DATE
    return delta.days
