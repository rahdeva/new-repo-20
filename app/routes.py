from app import app
from app.controller import SVRController
from flask import request

@app.route('/')
def index():
    return 'Hello Flask App'

@app.route('/forecastSVR', methods=['POST'])
def forecastSVR():
    return SVRController.predict()