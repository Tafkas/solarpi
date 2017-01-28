# -*- coding: utf-8 -*-
"""Extensions module. Each extension is initialized in the app factory located
in app.py
"""

from flask.ext.bcrypt import Bcrypt
from flask.ext.cache import Cache
from flask.ext.debugtoolbar import DebugToolbarExtension
from flask.ext.login import LoginManager
from flask.ext.migrate import Migrate
from flask.ext.sqlalchemy import SQLAlchemy

login_manager = LoginManager()
bcrypt = Bcrypt()
db = SQLAlchemy()
migrate = Migrate()
cache = Cache()
debug_toolbar = DebugToolbarExtension()
