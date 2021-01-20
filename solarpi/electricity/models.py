# -*- coding: utf-8 -*-
import datetime as dt

from solarpi.database import (
    Column,
    db,
    Model,
    SurrogatePK,
)


class Electricity(SurrogatePK, Model):
    __tablename__ = "electricity_data"
    id = Column(db.Integer(), nullable=False, primary_key=True)
    created_at = Column(db.Text(), nullable=False, default=dt.datetime.utcnow)
    meter_180 = Column(db.Float(), nullable=True)
    meter_280 = Column(db.Float(), nullable=True)
    active_power = Column(db.Float(), nullable=True)


def __init__(self):
    db.Model.__init__(self)
