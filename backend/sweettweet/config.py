"""
    config.py
    - settings for the flask application object
    - supply TWILIO SID, TOKEN and PHONE_NUMBER to send SMS alerts
"""

class BaseConfig(object):
    TWILIO_SID=''
    TWILIO_TOKEN=''
    TWILIO_PHONE_NUMBER=''
