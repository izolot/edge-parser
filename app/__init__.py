import config
from flask import Flask
from . import model


app = Flask(__name__)
app.config.from_object('config.DevelopmentConfig')


from app import api_routes
from app import model