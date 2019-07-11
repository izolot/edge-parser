# -*- coding: utf-8 -*-
from flask import Flask
from parser_api import routes


app = Flask(__name__.split('.')[0])
