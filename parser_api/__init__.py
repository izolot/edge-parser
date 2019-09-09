# -*- coding: utf-8 -*-
from flask import Flask

app = Flask(__name__.split('.')[0])

from parser_api import routes