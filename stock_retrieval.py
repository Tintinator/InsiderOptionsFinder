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

# Returns day as dict with keys: year, month, day, quarter, today, and today_format
def getDate():
    res = {}
    today = date.today() - timedelta(days = 0) 
    year = today.strftime('%Y')
    month = today.strftime('%m')
    day = today.strftime('%d')
    today_format = ''.join([year + month + day])
    quarter = 'QTR' + str(int((int(month)-1)/3 + 1))
    res['today'] = today
    res['year'] = year
    res['month'] = month
    res['day'] = day
    res['today_format'] = today_format
    res['quarter'] = quarter
    print("Current Date: " + today.strftime('%m/%d/%y'))
    return res

# (company_name, [(strike, expiration, quantity)])
def searchForOptions(report): # try to return as (Company Name, [strike price, exp date, amount])
    file_path = report[-2]
    file_date = report[-3]
    cik = report[-4]
    report = report[1:len(report)-4]
    temp = ' '.join(report)
    company_name = temp.split('/')[0].split('\\')[0]

    optionList = []

    # Is company listed on NASDAQ?
    if company_ticker['Company Name'].str.contains(company_name).sum() <= 0:
        return None

    try:
        file_path = file_path.split('/')
        folder = [''.join(file_path[3].split('-')).split('.')[0]]	
        file_path = '/'.join(file_path[:len(file_path)-1] + folder)
        form_url = ''.join([base_url,file_path])
        r = requests.get(form_url)
        form4_path = re.search('(\/)([a-zA-Z0-9_-])*(.xml)', r.text)
        final_url = ''.join([form_url,form4_path.group(0)])

        # Grab the company's Form 4 and its derivative table.
        form_filing = urllib.request.urlopen(final_url)
        html = form_filing.read().decode('utf-8')
        root = ET.fromstring(html)
        derivativeTable = root.find('derivativeTable')

        # Search for option acquisitions
        if derivativeTable:
            for transaction in derivativeTable.findall('derivativeTransaction'):
                securityTitle = transaction.find('securityTitle')
                price = transaction.find('conversionOrExercisePrice')
                transactionAmounts = transaction.find('transactionAmounts')
                expirationDate = transaction.find('expirationDate')

                if 'Stock Option' in securityTitle[0].text and 'A' in transactionAmounts.find('transactionAcquiredDisposedCode')[0].text:
                    optionList += (price[0].text, expirationDate[0].text, transactionAmounts.find('transactionShares')[0].text)  

    except:
        print('Failed on: ' + company_name)
    
    return (company_name, optionList) if (len(optionList) > 0) else None

def retrieveDailyOptions():
    
    global base_url
    global company_ticker 

    base_url = 'https://www.sec.gov/Archives/'
    company_ticker = pd.read_csv('ticker-company.csv', header = 0)
    date = getDate()
    res = {}
    daily_url = ''.join([base_url, 'edgar/daily-index/', date['year'], date['quarter'], '/form.', date['today_format'], '.idx']) 
    print('idx link: ' + daily_url)

    # HARDCODED URL. REMOVE SOMETIME##
    HARDCODED_URL = 'https://www.sec.gov/Archives/edgar/daily-index/2020/QTR3/form.20200914.idx'
    daily_url = HARDCODED_URL
    ##################################

    try:
        file = urllib.request.urlopen(daily_url)
    except urllib.error.HTTPError:
        print('ERROR: Report not released yet. Go back a day')
        file = None

    if file == None:
        print('No file, exiting')
        return res

    rows = file.readlines()[11:]

    # Search for companies with form 4 filled out
    for line in rows:
        str_line = line.decode('utf-8')
        str_split = [splits for splits in str_line.split(' ') if splits != '']
        form_type = str_split[0]

        if form_type == '4':
            currentOptions = searchForOptions(str_split)
            if currentOptions:
                if currentOptions[0] in res:
                    res[currentOptions[0]] += currentOptions[1]
                else:
                    res[currentOptions[0]] = currentOptions[1]
    
    return res

company_ticker = None
base_url = None

print(retrieveDailyOptions())