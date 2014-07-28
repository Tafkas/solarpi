from flask import Blueprint, render_template
from sqlalchemy import extract

from solarpi.weather.models import Weather

blueprint = Blueprint("weather", __name__, url_prefix='/weather',
                      static_folder="../static")