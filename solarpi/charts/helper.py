import calendar
from datetime import datetime


def get_timestamps(series):
    return [
        1000 * calendar.timegm(
            datetime.strptime(d.created_at.split(".")[0], "%Y-%m-%dT%H:%M:%S")
            .replace(second=0).timetuple()) for d in series]
