"""
Routes and views for the flask application.
"""

from decimal import Decimal
from datetime import datetime
from flask import render_template
from flask import request
from flask import redirect
from MapMaker import app
from azure.storage.table import TableService, Entity
import random
import json

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
        """ Get locationdata from form, format into array as such [ [lat, lng] [lat, lng] ] """
        locationData = request.form['locationData']
        lines = locationData.split('\r\n')
        final = [l.split(',') for l in lines]
        final = [{"lat": Decimal(l[0].strip()), "lng": Decimal(l[1].strip())} for l in final]
        
        id = sendLocationToStorageReturnId(final)
        return redirect('map/' + id)

    except Exception as e:
        print "Unexpected error:", e.message

@app.route('/map/<id>')
def map(id):
    """ Split id from URL into partition and row keys that makeup composite key in table """
    idSplit = id.split('A')
    partitionKey = idSplit[0]
    rowKey = idSplit[1]

    try:
        markers = getMapMarkers(partitionKey, rowKey)
        return render_template(
            'map.html',
            title='Map Page',
            markers = markers,
            year=datetime.now().year
        )
    except Exception as e:
        print "Unexpected error:", e.message
        raise e

def sendLocationToStorageReturnId(markers):
    table_service = getTableService()
    
    """ Generate partition and row keys based on current time """
    year = datetime.now().year - 2000
    partitionKey = str(year) + datetime.now().strftime("%m%d")
    rowKey = datetime.now().strftime("%H%M%S") + str(random.randint(0, 99))
        
    """ Create entity send to Azure Storage Table. PartitionKey and RowKey make up composite key """
    entity = Entity();
    entity.PartitionKey = partitionKey
    entity.RowKey = rowKey

    """ 
        Azure storage is not able to serialize lists so store as JSON string. Also convert decimals to string as
        python Decimal object cannot be encoded to JSON.
    """
    entity.markers = json.dumps([{"lat": str(m["lat"]), "lng": str(m["lng"])} for m in markers])

    table_service.insert_entity('maps', entity)

    """ Make a final key, consisting of partitionKey and rowKey suitable for use inside URL """
    finalId = partitionKey + "A" + rowKey
    return finalId

def getTableService():
    table_service = TableService(account_name=app.config["AZURE_STORAGE_ACCOUNT_NAME"], account_key=app.config["AZURE_STORAGE_ACCOUNT_KEY"], is_emulated = app.config["AZURE_STORAGE_ACCOUNT_IS_EMULATED"])
    table_service.create_table('maps')
    return table_service

def getMapMarkers(partitionKey, rowKey):    
    table_service = getTableService()   
    map = table_service.get_entity('maps', partitionKey, rowKey)
    markers = json.loads(map.markers)
    markers = [{"lat": m["lat"], "lng": m["lng"]} for m in markers]
    return markers