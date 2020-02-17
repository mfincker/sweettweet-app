"""
application.py
- creates a Flask app instance and instantiate the predictive models
"""

from flask import Flask
from flask_cors import CORS
import tensorflow as tf

def create_app(app_name='SWEETTWEET'):
  app = Flask(app_name)

  # load config: twilio attributes
  app.config.from_object('sweettweet.config.BaseConfig')

  # allow cross-origin for api routes
  cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

  # load api routes
  from sweettweet.api import api
  app.register_blueprint(api, url_prefix="/api")

  # load LSTM model
  from sweettweet.services.lstm_model import LstmModel
  app.model = LstmModel()
  app.graph = tf.get_default_graph()
  
  return app