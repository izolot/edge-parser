from config import Config
from edge_parser import Parser
from flask import Flask


app = Flask(__name__.split('.')[0])
print("Initialization Parser....")
Parser.root_path = Config.ARCHIVE_PATH
Parser.init_camera_folders()
print("Parser initialized")

from api import routes
