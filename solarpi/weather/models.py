import datetime as dt

from solarpi.database import (
    Column,
    db,
    Model,
    SurrogatePK,
)


class Weather(SurrogatePK, Model):
    __tablename__ = 'weather_data'

    id = Column(db.Integer(), nullable=False, primary_key=True)
    created_at = Column(db.Text(), nullable=False, default=dt.datetime.utcnow)
    temp = Column(db.Float(), nullable=True)
    pressure = Column(db.Integer(), nullable=True)
    temp_min = Column(db.Float(), nullable=True)
    temp_max = Column(db.Float(), nullable=True)
    humidity = Column(db.Integer(), nullable=True)
    wind_speed = Column(db.Float(), nullable=True)
    wind_gust = Column(db.Float(), nullable=True)
    wind_deg = Column(db.Integer(), nullable=True)
    clouds = Column(db.Integer(), nullable=True)
    rain = Column(db.Integer(), nullable=True)
    weather_id = Column(db.Integer(), nullable=True)


def __init__(self):
    db.Model.__init__(self)

