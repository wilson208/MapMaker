"""
The flask application package.
"""

from flask import Flask

app = Flask(__name__)
app.config.from_object('MapMaker.configmodule.BaseConfig')

import MapMaker.views
