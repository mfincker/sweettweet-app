"""
application.py
- creates a Flask app instance and registers the database object
"""

from flask import Flask
from flask_cors import CORS
import tensorflow as tf

def create_app(app_name='SWEETTWEET'):
  app = Flask(app_name)
  app.config.from_object('sweettweet.config.BaseConfig')

  cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

  from sweettweet.api import api
  app.register_blueprint(api, url_prefix="/api")
  from sweettweet.services.lstm_model import LstmModel
  app.model = LstmModel()
  app.graph = tf.get_default_graph()
  return app