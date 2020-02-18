"""
api.py
- provides the API endpoints for getting initial glucose value 
and model predictions
"""

from flask import Flask, render_template, jsonify, json, Response, request, session

from flask import Blueprint

from twilio.base.exceptions import TwilioRestException
from .services.twilio_service import TwilioService

from flask import current_app as app

import os.path

##############
# API ROUTES #
##############

# Define api routes
api = Blueprint('api', __name__)

# Get initial live glucose data
@api.route('/get-glucose/', methods = ['GET'])

def api_getGlucoseData():
    '''
    Return 12 h of cgm data from a user to prepopulate the glucose
    visualization component.
    '''
    SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
    data_url = os.path.join(SITE_ROOT, 'static/data', 'glucose_data_example_vega.json')

    data = json.load(open(data_url))

    resp = jsonify({'data' : data})
    resp.status_code = 200

    return resp


# Update and model glucose data
@api.route('/forecast-glucose/', methods = ['POST'])

def api_updateGlucose():
    '''
    Get glucose data from request and return the glucose predictions 
    for the next 30 mins (6 timepoints).
    
    Also send an SMS alert if model predicts hypoglycemia in the next
    30 mins if user provides a phone number.
    '''

    # Extract data from request
    req_data = request.get_json()
    newBG = req_data['newBG']
    past_data = req_data['data']
    past_alarm = req_data['alarm']
    user_info = req_data['userInfo']


    # Update glucose data with new predictions and return alarm state
    data, alarm = app.model.forecast(past_data, user_info, newBG)

    # Decide whether to send an SMS alert or not
    sent_alarm = 0
    if alarm == 1 and past_alarm == 0:
        if user_info['phoneNumber']:
            send_alert(user_info['phoneNumber'])
            sent_alarm = 1

    # Return response with predicted data
    resp = jsonify({'data': json.loads(data),
                    'newBG' : '',
                    'userInfo' : user_info,
                    'alarm' : alarm,
                    'sent_alarm' : sent_alarm})

    print(resp)
    resp.status_code = 200

    return resp



def send_alert(phone_number):
    '''
    Send an SMS alert to @phone_number to warn about 
    impending hypoglycemia using Twilio service
    '''
    if phone_number:

        message = 'Your blood sugar level is likely to dip below 70 in the next half hour. How about some orange juice?'

        twilio_service = TwilioService()

        try:
            twilio_service.send_message(message, phone_number)
            
        except TwilioRestException as e:
            print(e)

    else:
        print("No alert sent - missing phone number")


