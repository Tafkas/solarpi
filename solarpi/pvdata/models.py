# -*- coding: utf-8 -*-
import datetime as dt

from solarpi.database import (
    Column,
    db,
    Model,
    SurrogatePK,
)


class PVData(SurrogatePK, Model):
    __tablename__ = 'pvdata'

    id = Column(db.Integer(), nullable=False, primary_key=True)
    created_at = Column(db.Text(), nullable=False, default=dt.datetime.utcnow)
    dc_1_u = Column(db.Integer(), nullable=True)
    dc_1_i = Column(db.Float(), nullable=True)
    ac_1_u = Column(db.Integer(), nullable=True)
    ac_1_p = Column(db.Integer(), nullable=True)
    dc_2_u = Column(db.Integer(), nullable=True)
    dc_2_i = Column(db.Float(), nullable=True)
    ac_2_u = Column(db.Integer(), nullable=True)
    ac_2_p = Column(db.Integer(), nullable=True)
    dc_3_u = Column(db.Integer(), nullable=True)
    dc_3_i = Column(db.Float(), nullable=True)
    ac_3_u = Column(db.Integer(), nullable=True)
    ac_3_p = Column(db.Integer(), nullable=True)
    current_power = Column(db.Integer(), nullable=True)
    daily_energy = Column(db.Float(), nullable=True)
    total_energy = Column(db.Integer(), nullable=True)


def __init__(self):
    db.Model.__init__(self)