from flask import Flask, render_template, jsonify, json, Response, request, session
# from flask_session import Session
from flask_cors import CORS
from flaskServer import app

from twilio.base.exceptions import TwilioRestException
from .services.twilio_service import TwilioService
from .services.arima_model import ArimaModel

import os.path

# @app.route('/')
# @app.route('/index')

# def index():
#    user = { 'nickname': 'Miguel' } # fake user
#    return render_template("index.html", user = user)

# SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
# past_data_url = os.path.join(SITE_ROOT, 'static/data', 'past_glucose.json')
# forecast_data_url = os.path.join(SITE_ROOT, 'static/data', 'forecast_glucose.json')

# past_data = json.load(open(past_data_url))
# forecast_data = json.load(open(forecast_data_url))
# phone_number = ''

##############
# API ROUTES #
##############

# Get initial live glucose data
@app.route('/api/glucose-data', methods = ['GET'])
def api_getGlucoseData():
    SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
    past_data_url = os.path.join(SITE_ROOT, 'static/data', 'past_glucose.json')
    forecast_data_url = os.path.join(SITE_ROOT, 'static/data', 'forecast_glucose.json')

    # Initialize session with past data
    # if 'past_data' not in session.keys():
    # 	session['past_data'] = json.load(open(past_data_url))

    # if 'forecast_data' not in session.keys():
    # 	session['forecast_data'] = json.load(open(forecast_data_url))

    past_data = json.load(open(past_data_url))
    past_data = past_data[-100:]
    forecast_data =  json.load(open(forecast_data_url))

    # js = json.dumps(session.data)

    # resp = jsonify({'pastData': session['past_data'],
    # 				'forecastData' : session['forecast_data']})
    resp = jsonify({'pastData': past_data,
    				'forecastData' : forecast_data})
    resp.status_code = 200
    # resp.headers['Link'] = 'http://luisrei.com'

    return resp

# Don't need this, because I'm not using sessions at all
# # Set phone number to which alerts should be sent
# @app.route('/api/change-phone-number', methods = ['POST'])
# def api_changePhoneNumber():
# 	# session.phone_number = '' # don't know yet how to save phone number to server

# 	# Initialize phone number?
# 	# if 'phone_number' not in session.keys():
# 	# 	session['phone_number'] = ''

# 	req_data = request.get_json()
# 	# print(req_data)

# 	# print('old phone number: ' + phone_number + '\n')
# 	# session['phone_number'] = req_data['phoneNumber']
# 	session['phone_number'] = req_data['phoneNumber']
# 	session.modified = True
# 	print('new phone number: ' + session['phone_number'] + '\n')

# 	resp = jsonify({'phoneNumber' : session['phone_number']})
# 	resp.status_code = 200

# 	return resp

# @app.route('/send-alert', methods = ['GET'])
# def private_send_alert():
# 	phone_number = '+16508627015'
# 	message = 'Your blood sugar level are likely to deep below 70 in the next half hour. How about some orange juice?'

# 	twilio_service = TwilioService()

# 	try:
# 		twilio_service.send_message(message, phone_number)
		
# 	except TwilioRestException as e:
# 		print(e)
# 		# flash('Oops! There was an error. Please try again.', 'danger')

# 	return status.HTTP_200_OK


# Update and model glucose data
@app.route('/api/update-glucose', methods = ['POST'])
def api_updateGlucose():
	# session.phone_number = '' # don't know yet how to save phone number to server

	req_data = request.get_json()
	newBG = req_data['newBG']
	past_data = req_data['pastData']
	phone_number = req_data['phoneNumber']
	past_alarm = req_data['alarm']

	# print('new BG: ' + str(newBG))
	# print(past_data)
	# print(session['phone_number'])
	# print(past_data[-1])
	# print(past_data[-1]['Timestamp'])
	# newTimestamp = past_data[-1]['Timestamp'] + 5 * 60
	# Remove first data point
	# past_data = past_data[1:]
	# past_data.append({'Timestamp' : newTimestamp, 'Glucose' : newBG})
	# print(past_data[-1])

	arima_model = ArimaModel()

	past_data, forecast_data, alarm = arima_model.forecast(past_data, newBG)

	if alarm == 1 and past_alarm == 0:
		send_alert(phone_number)


	# print(req_data)

	# print('old phone number: ' + session.phone_number + '\n')
	# session.phone_number = req_data['phoneNumber']
	# print('new phone number: ' + session.phone_number + '\n')
	# print(forecast_data)
	resp = jsonify({'pastData': json.loads(past_data),
    				'forecastData' : json.loads(forecast_data),
    				'newBG' : '',
    				'phoneNumber' : phone_number,
    				'alarm' : alarm})
	resp.status_code = 200

	return resp

def send_alert(phone_number):

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





