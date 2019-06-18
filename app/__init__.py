from flask import Flask
import config, parser

app = Flask(__name__)
app.config.from_object(config.DevelopmentConfig)


from app import api_routes