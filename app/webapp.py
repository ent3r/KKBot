"""The webapp for the KKBot"""

from flask import render_template
from app import KKWEBAPP


@KKWEBAPP.route("/")
def index():
    """Function for the index page of the site"""
    return render_template("site.html")
