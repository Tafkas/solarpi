# -*- coding: utf-8 -*-
from flask_assets import Bundle, Environment

css = Bundle(
    # "libs/bootstrap/dist/css/bootstrap.css",
    # "libs/weather-icons/css/weather-icons.css",
    "css/sb-admin-2.css",
    filters="cssmin",
    output="public/css/common.css"
)

js = Bundle(
    # "libs/jQuery/dist/jquery.js",
    # "libs/bootstrap/dist/js/bootstrap.js",
    # "libs/highcharts/highcharts.js",
    # "libs/metisMenu/metisMenu.js",
    "js/plugins.js",
    "js/sb-admin-2.js",
    filters='jsmin',
    output="public/js/common.js"
)

assets = Environment()

assets.register("js_all", js)
assets.register("css_all", css)
