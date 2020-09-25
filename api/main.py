#!/usr/bin/env python

from flask import Flask, request, jsonify
from stock_retrieval import retrieveOptions
import sys

app = Flask(__name__)

@app.route("/")
def index():
    return "Usage: http://<hostname>[:<prt>]/api/retrieveOptions"

@app.route("/api/retrieveOptions")
def getOptions():
    inputDate = request.args.get('inputDate', None)
    app.logger.info('This is the inputDate parameter: ', inputDate)
    res = retrieveOptions(inputDate)
    return _corsify_response(jsonify(res)) 

def _corsify_response(response):
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

app.run(host = '0.0.0.0')
