"""The webapp for the KKBot"""

from flask import Flask, render_template

APP = Flask(__name__)


@APP.route("/")
def index():
    """Function for the index page of the site"""
    return render_template("site.html")


APP.run("0.0.0.0", 8080)
