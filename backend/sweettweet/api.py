"""
api.py
- provides the API endpoints for consuming and producing 
  REST requests and responses
"""

from flask import Flask, render_template, jsonify, json, Response, request, session

# from sweettweet import app #????
from flask import Blueprint

from twilio.base.exceptions import TwilioRestException
from .services.twilio_service import TwilioService
# from .services.lstm_model import LstmModel
from flask import current_app as app

import os.path

##############
# API ROUTES #
##############
api = Blueprint('api', __name__)

# Get initial live glucose data
@api.route('/glucose-data/', methods = ['GET'])
def api_getGlucoseData():
    SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
    data_url = os.path.join(SITE_ROOT, 'static/data', 'glucose_data_example_vega.json')

    data = json.load(open(data_url))

    resp = jsonify({'data' : data})
    resp.status_code = 200

    return resp


# Update and model glucose data
@api.route('/update-glucose/', methods = ['POST'])
def api_updateGlucose():

	req_data = request.get_json()
	newBG = req_data['newBG']
	past_data = req_data['data']
	past_alarm = req_data['alarm']
	user_info = req_data['userInfo']

	# lstm_model = LstmModel()

	data, alarm = app.model.forecast(past_data, user_info, newBG)

	sent_alarm = 0
	if alarm == 1 and past_alarm == 0:
		if user_info['phoneNumber']:
			send_alert(phone_number)
			sent_alarm = 1
		else:
			sent_alarm = 0

	resp = jsonify({'data': json.loads(data),
    				'newBG' : '',
    				'userInfo' : user_info,
    				'alarm' : alarm,
    				'sent_alarm' : sent_alarm})
	resp.status_code = 200

	return resp



def send_alert(phone_number):
	'Send SMS alert using Twilio service'
	if phone_number:
		print("Alert sent")

		message = 'Your blood sugar level is likely to dip below 70 in the next half hour. How about some orange juice?'

		twilio_service = TwilioService()

		try:
			twilio_service.send_message(message, phone_number)
			
		except TwilioRestException as e:
			print(e)
			# flash('Oops! There was an error. Please try again.', 'danger')
	else:
		print("No alert sent - missing phone number")

