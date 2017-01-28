# -*- coding: utf-8 -*-
from factory.alchemy import SQLAlchemyModelFactory

from solarpi.database import db


class BaseFactory(SQLAlchemyModelFactory):
    FACTORY_SESSION = db.session

    @classmethod
    def _create(cls, target_class, *args, **kwargs):
        """Create an instance of the model, and save it to the database."""
        session = cls.FACTORY_SESSION
        obj = target_class(*args, **kwargs)
        session.add(obj)
        session.commit()
        return obj
