#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
import subprocess
from flask_script import Manager, Shell, Server
from flask_migrate import MigrateCommand

from solarpi.app import create_app
from solarpi.settings import DevConfig, ProdConfig
from solarpi.database import db

if os.environ.get("SOLARPI_ENV") == "prod":
    app = create_app(ProdConfig)
else:
    app = create_app(DevConfig)

manager = Manager(app)
TEST_CMD = "py.test tests"


def _make_context():
    """Return context dict for a shell session so you can access
    app, db, and the User model by default.
    """
    return {"app": app, "db": db}


@manager.command
def test():
    """Run the tests."""
    status = subprocess.call(TEST_CMD, shell=True)
    sys.exit(status)


manager.add_command("server", Server())
manager.add_command("shell", Shell(make_context=_make_context))
manager.add_command("db", MigrateCommand)

if __name__ == "__main__":
    manager.run()
