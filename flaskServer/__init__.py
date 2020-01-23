from flask import Flask, session
from flask_cors import CORS
app = Flask(__name__)

app.config.update(
    TWILIO_SID='AC12ea4ead65949c96274b7179cf8da553',
    TWILIO_TOKEN='03e80ba78f1eecdc6977d36ad40f44d8',
    TWILIO_PHONE_NUMBER='+12055123711',
    SESSION_TYPE='filesystem',
    SECRET_KEY='reds209ndsldssdsljdsldsdslj32f09uakdvweqwdkjvr40'
)

# session.init_app(app)
# app.secret_key()


# Cross origin allowed on /api/* routes
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

from flaskServer import views
