# -*- coding: utf-8 -*-
from datetime import datetime, timedelta

from solarpi.weather.models import Weather

WEATHER_ICONS = {211: 'wi-storm-showers',
                 300: 'wi-showers',
                 301: 'wi-showers',
                 310: 'wi-showers',
                 500: 'wi-showers',
                 501: 'wi-showers',
                 502: 'wi-rain',
                 520: 'wi-rain',
                 521: 'wi-rain',
                 701: 'wi-fog',
                 741: 'wi-fog',
                 800: 'wi-day-sunny',
                 801: 'wi-day-sunny-overcast',
                 802: 'wi-day-cloudy',
                 803: 'wi-cloudy',
                 804: 'wi-cloudy'
                 }


def get_current_weather():
    """
    returns the lates entry from the weather table
    """
    return Weather.query.with_entities(Weather.temp, Weather.weather_id).filter(
        Weather.created_at >= (datetime.now() - timedelta(days=2))).order_by(
        Weather.id.desc()).first()


def get_weather_icon(weather_id):
    """returns the corresponding weather icon for a given weather code from
        http://bugs.openweathermap.org/projects/api/wiki/Weather_Condition_Codes"""
    if weather_id not in WEATHER_ICONS:
        return 'wi-alien'  # fallback
    return WEATHER_ICONS[weather_id]
