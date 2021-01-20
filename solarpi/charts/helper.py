import calendar
from datetime import datetime


def get_timestamps(series):
    return [
        1000
        * (
            calendar.timegm(
                datetime.strptime(d.created_at.split(".")[0], "%Y-%m-%dT%H:%M:%S").replace(second=0).timetuple()
            )
        )
        for d in series
    ]


def get_daily_pv_chart_data(pv):
    timestamps_pv = get_timestamps(pv)
    return [list(x) for x in zip(timestamps_pv, [(int(d.current_power or 0)) for d in pv])]
