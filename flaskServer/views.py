from flask import Flask, render_template, jsonify, json, Response, request, session
from flask_session import Session
from flask_cors import CORS
from flaskServer import app
import os.path

# @app.route('/')
# @app.route('/index')

# def index():
#    user = { 'nickname': 'Miguel' } # fake user
#    return render_template("index.html", user = user)


##############
# API ROUTES #
##############

# Get initial live glucose data
@app.route('/api/glucose-data', methods = ['GET'])
def api_getGlucoseData():
    SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
    json_url = os.path.join(SITE_ROOT, 'static/data', 'sample_glucose.json')
    data = json.load(open(json_url))

    js = json.dumps(data)

    resp = jsonify(data)
    resp.status_code = 200
    # resp.headers['Link'] = 'http://luisrei.com'

    return resp

# Set phone number to which alerts should be sent
@app.route('/api/change-phone-number', methods = ['POST'])
def api_changePhoneNumber():
	phone_number = '' # don't know yet how to save phone number to server

	req_data = request.get_json()
	print(req_data)

	print('old phone number: ' + phone_number + '\n')
	phone_number = req_data['phoneNumber']
	print('new phone number: ' + phone_number + '\n')
	resp = jsonify(req_data)
	resp.status_code = 200

	return resp


