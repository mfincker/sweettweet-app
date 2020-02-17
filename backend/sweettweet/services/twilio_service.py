"""
twilio_service.py
- Twilio class to send SMS
"""


from flask import current_app as app
from twilio.rest import Client

class TwilioService:
    '''
    Twilio service client to send sms alert.
    Initialize from app config attirbutes: TWILIO_SID, TWILIO_TOKEN 
    and TWILIO_PHONE_NUMEBR

    Implement a single function `send_message` to send sms.
    '''
    client = None

    def __init__(self):
        # Find these values at https://twilio.com/user/account
        account_sid = app.config['TWILIO_SID']
        auth_token = app.config['TWILIO_TOKEN']
        self.client = Client(account_sid, auth_token)

    def send_message(self, message, agent_phone_number):
        twilio_phone_number = app.config['TWILIO_PHONE_NUMBER']
        self.client.messages.create(to=agent_phone_number,
                                    from_=twilio_phone_number,
                                    body=message)

