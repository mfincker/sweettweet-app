from flask import Flask, render_template, jsonify, json, Response, request, session
# from flask_session import Session
from flask_cors import CORS
from flaskServer import app

from twilio.base.exceptions import TwilioRestException
from .services.twilio_service import TwilioService

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

    # Initialize session with past data
    if 'past_data' not in session.keys():
    	session.past_data = json.load(open(json_url))

    # js = json.dumps(session.data)

    resp = jsonify(session.past_data)
    resp.status_code = 200
    # resp.headers['Link'] = 'http://luisrei.com'

    return resp

# Set phone number to which alerts should be sent
@app.route('/api/change-phone-number', methods = ['POST'])
def api_changePhoneNumber():
	# session.phone_number = '' # don't know yet how to save phone number to server

	# Initialize phone number?
	if 'phone_number' not in session.keys():
		session.phone_number = ''

	req_data = request.get_json()
	# print(req_data)

	print('old phone number: ' + session.phone_number + '\n')
	session.phone_number = req_data['phoneNumber']
	print('new phone number: ' + session.phone_number + '\n')

	resp = jsonify({'phoneNumber' : session.phone_number})
	resp.status_code = 200

	return resp

@app.route('/send-alert', methods = ['GET'])
def private_send_alert():
	phone_number = '+16508627015'
	message = 'Your blood sugar level are likely to deep below 70 in the next half hour. How about some orange juice?'

	twilio_service = TwilioService()

	try:
		twilio_service.send_message(message, phone_number)
		
	except TwilioRestException as e:
		print(e)
		# flash('Oops! There was an error. Please try again.', 'danger')

	return status.HTTP_200_OK





