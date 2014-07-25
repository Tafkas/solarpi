# -*- coding: utf-8 -*-
'''Public section, including homepage and signup.'''
from flask import (Blueprint, request, render_template)

from solarpi.public.forms import LoginForm

blueprint = Blueprint('public', __name__, static_folder="../static")


@blueprint.route("/")
def home():
    return render_template("public/home.html")


@blueprint.route("/about/")
def about():
    form = LoginForm(request.form)
    return render_template("public/about.html")