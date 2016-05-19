"""
Routes and views for the flask application.
"""

from decimal import Decimal
from datetime import datetime
from flask import render_template
from flask import request
from flask import redirect
from MapMaker import app

@app.route('/')
@app.route('/home')
def home():
    """Renders the home page."""
    return render_template(
        'index.html',
        title='Home Page',
        year=datetime.now().year,
    )

@app.route('/import_text_data', methods=['POST'])
def import_text_data():
    try:        
        locationData = request.form['locationData']
        lines = locationData.split('\r\n')
        final = [l.split(',') for l in lines]
        final = [[Decimal(l[0].strip()), Decimal(l[1].strip())] for l in final]
        return redirect('map')
    except Exception as e:
        print "Unexpected error:", e.message

@app.route('/map')
def map():
    return render_template(
        'map.html',
        title='Map Page',
        year=datetime.now().year,
    )