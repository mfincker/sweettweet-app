from flask import Flask
from flask_cors import CORS
app = Flask(__name__)

# Cross origin allowed on /api/* routes
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

from flaskServer import views
