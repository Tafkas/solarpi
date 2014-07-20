# -*- coding: utf-8 -*-
from flask import Blueprint, render_template
from flask.ext.login import login_required

blueprint = Blueprint("data", __name__, url_prefix='/data',
                      static_folder="../static")


@blueprint.route("/")
def index():
    return render_template("data/index.html")