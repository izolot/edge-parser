from config import Config
from edge_parser import Parser
from flask import Flask


app = Flask(__name__.split('.')[0])


from api import routes
