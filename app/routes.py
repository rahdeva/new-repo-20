from app import app
from app.controller import SVRController
from flask import request

@app.route('/')
def index():
    return 'Hello Flask App'

@app.route('/test', methods=['POST'])
def forecastSVR():
    return SVRController.test()

# @app.route('/forecastSVR', methods=['POST'])
# def forecastSVR():
#     return SVRController.predictData()