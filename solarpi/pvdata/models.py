# -*- coding: utf-8 -*-
import datetime as dt

from solarpi.database import (
    Column,
    db,
    Model,
    SurrogatePK,
)


class Data(SurrogatePK, Model):
    __tablename__ = 'pvdata'

    created_at = Column(db.Text(), nullable=False, default=dt.datetime.utcnow)
    ac_1_u = Column(db.Integer(), nullable=True)
    ac_1_i = Column(db.Float(), nullable=True)
    dc_1_u = Column(db.Integer(), nullable=True)
    dc_1_p = Column(db.Integer(), nullable=True)
    ac_2_u = Column(db.Integer(), nullable=True)
    ac_2_i = Column(db.Float(), nullable=True)
    dc_2_u = Column(db.Integer(), nullable=True)
    dc_2_p = Column(db.Integer(), nullable=True)
    ac_3_u = Column(db.Integer(), nullable=True)
    ac_3_i = Column(db.Float(), nullable=True)
    dc_3_u = Column(db.Integer(), nullable=True)
    dc_3_p = Column(db.Integer(), nullable=True)
    current_power = Column(db.Integer(), nullable=True)
    daily_energy = Column(db.Float(), nullable=True)
    total_energy = Column(db.Integer(), nullable=True)


def __init__(self, username, email, password=None, **kwargs):
    db.Model.__init__(self, **kwargs)