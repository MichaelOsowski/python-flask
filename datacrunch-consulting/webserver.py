# .\venv\Scripts\activate.ps1
# python .\datacrunch-consulting\webserver.py

import newrelic.agent
newrelic.agent.initialize()

# Import the logging module and the New Relic log formatter
import logging
from newrelic.agent import NewRelicContextFormatter

from flask import Flask, render_template, jsonify

# Instantiate a new log handler, and set logging level
handler = logging.StreamHandler()
handler.setLevel(logging.INFO)

# Instantiate the log formatter and add it to the log handler
formatter = NewRelicContextFormatter()
handler.setFormatter(formatter)

# Get the root logger, set logging level, and add the handler to it
root_logger = logging.getLogger()
root_logger.setLevel(logging.INFO)
root_logger.addHandler(handler)

import requests
# Flask Web Application
flaskapp = Flask(__name__, static_url_path="/")

# Navigation
@flaskapp.route("/")
def index():
    return render_template("index.html", title="Flask Web Application")

@flaskapp.route("/external/source")
def external_source():
    return "Hello, fellow humans!\n"

@flaskapp.route("/ping/", strict_slashes=False)
def ping():
    return jsonify(ping="pong")

@flaskapp.route("/about")
def about():
    return render_template("about.html", title="Datacrunch - About")

@flaskapp.route("/projects/")
def projects():
    return render_template("projects.html", title="Datacrunch - Projects")

@flaskapp.route("/projects/statuspage", strict_slashes=False)
def statuspage():
    return render_template("projects/statuspage.html", title="Simple Statuspage")

# API to convert Fahrenheit to Celcius
@flaskapp.route("/projects/convertC/<tempF>")
def convertC(tempF):
    tempC = (5/9*(float(tempF))-32)
    root_logger.info(f"[INFO] Converted {tempF}°F to {tempC:.2f}°C.")
    return f"{tempF}°F is {tempC:.2f}°C."

# API to convert Celcius to Fahrenheit
@flaskapp.route("/projects/convertF/<tempC>")
def convertF(tempC):
    try:
        tempF = 9/5*(float(tempC))+32
        root_logger.info(f"[INFO] Converted {tempC}°F to {tempF:.2f}°C.")
        return f"{tempC}°C is {tempF:.2f}°F."
    except:
        root_logger.warning("[WARN] Invalid temperature!")

### Add Applications Here ###

# API to calculate the nth prime number and how long it takes
from projects.prime import prime
flaskapp.register_blueprint(prime)

# API to calculate the nth fibonacci number
from projects.fibonacci import fibonacci
flaskapp.register_blueprint(fibonacci)

# API to validate credit card numbers
from projects.luhn import luhn
flaskapp.register_blueprint(luhn)

# Get COVID data and plot on chart
from projects.covid import covid
flaskapp.register_blueprint(covid)

# Get COVID data and plot on chart with Plotly
from projects.covid2 import covid2
flaskapp.register_blueprint(covid2)

# Test redis-py in App
from projects.redispy import redispy
flaskapp.register_blueprint(redispy)

# Input number to check divisibility
from projects.divisibility import divisibility
flaskapp.register_blueprint(divisibility)

# Import Plotly Dash application into Flask
from projects.dashboard import init_dashboard
app = init_dashboard(flaskapp)

# This will exceed memory quota on Heroku
# from projects.barchart import init_barchart
# app = init_barchart(flaskapp)

# Run Flask Web Application, new comment
if __name__ == "__main__":
    flaskapp.run()