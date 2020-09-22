#!/usr/bin/env python

from flask import Flask
from flask import request
from flask import jsonify
from stock_retrieval import retrieveOptions
import sys

app = Flask(__name__)

@app.route("/")
def index():
    return "Usage: http://<hostname>[:<prt>]/api/retrieveOptions"

@app.route("/api/retrieveOptions")
def getOptions():
    inputDate = request.args.get('inputDate', None)
    print("THIS IS THE INPUT DATE:", inputDate, file=sys.stderr)
    app.logger.info('This is the inputDate parameter: ', inputDate)
    res = retrieveOptions(inputDate)
    return res

app.run(host = '0.0.0.0')
