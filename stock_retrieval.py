#!/usr/bin/env python

import numpy
from numpy import genfromtxt
import urllib.request
import requests
from datetime import date
from datetime import timedelta
import pandas as pd
import re
import xml.etree.ElementTree as ET

today = date.today() - timedelta(days = 0) 

print("Current Date: " + today.strftime('%m/%d/%y'))

year = today.strftime('%Y')
month = today.strftime('%m')
day = today.strftime('%d')
today_format = year + month + day
quarter = 'QTR' + str(int((int(month)-1)/3 + 1))

base_url = 'https://www.sec.gov/Archives/'
daily_url = base_url + 'edgar/daily-index/' + year + '/' + quarter + '/form.' + today_format + '.idx'
print('idx link: ' + daily_url)

HARDCODED_URL = 'https://www.sec.gov/Archives/edgar/daily-index/2020/QTR3/form.20200914.idx'
daily_url = HARDCODED_URL

try:
    file = urllib.request.urlopen(daily_url)
except urllib.error.HTTPError:
    print('ERROR: Report not released yet. Go back a day')
    file = None

if file == None:
    print('No file, exiting')
    exit()

rows = file.readlines()[11:]

#company_tickers needed json format