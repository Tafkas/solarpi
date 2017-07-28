# -*- coding: utf-8 -*-
"""The app module, containing the app factory function."""
import logging

from flask import Flask, render_template

from solarpi import public, weather, charts, statistics, tables
from solarpi.assets import assets
from solarpi.extensions import cache, db, migrate, debug_toolbar, sentry
from solarpi.settings import ProdConfig


def create_app(config_object=ProdConfig):
    """An application factory, as explained here:
        http://flask.pocoo.org/docs/patterns/appfactories/

    :param config_object: The configuration object to use.
    """
    app = Flask(__name__)
    app.config.from_object(config_object)
    register_extensions(app)
    register_blueprints(app)
    register_errorhandlers(app)
    return app


def register_extensions(app):
    assets.init_app(app)
    cache.init_app(app, config={'CACHE_TYPE': 'simple'})
    db.init_app(app)
    debug_toolbar.init_app(app)
    migrate.init_app(app, db)
    if ProdConfig.SENTRY_DNS is not None:
        sentry.init_app(app, dsn=ProdConfig.SENTRY_DNS, logging=True, level=logging.ERROR)
    return None


def register_blueprints(app):
    app.register_blueprint(charts.views.blueprint)
    app.register_blueprint(public.views.blueprint)
    app.register_blueprint(statistics.views.blueprint)
    app.register_blueprint(tables.views.blueprint)
    app.register_blueprint(weather.views.blueprint)

    return None


def register_errorhandlers(app):
    def render_error(error):
        # If a HTTPException, pull the `code` attribute; default to 500
        error_code = getattr(error, 'code', 500)
        return render_template("{0}.html".format(error_code)), error_code

    for errcode in [401, 404, 500]:
        app.errorhandler(errcode)(render_error)
    return None
