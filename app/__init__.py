"""The wrapper to start stuff"""

import importlib
from flask import Flask
KKWEBAPP = Flask(__name__)
from .webapp import KKWEBAPP
