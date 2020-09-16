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
    today_format = year + month + day
    quarter = 'QTR' + str(int((int(month)-1)/3 + 1))
    res['today'] = today
    res['year'] = year
    res['month'] = month
    res['day'] = day
    res['today_format'] = today_format
    res['quarter'] = quarter
    print("Current Date: " + today.strftime('%m/%d/%y'))
    return res

def searchForOptions(report):
    file_path = report[-2]
    file_date = report[-3]
    cik = report[-4]
    report = report[1:len(report)-4]
    temp = ' '.join(report)
    company_name = temp.report('/')[0].split('\\')[0]

    optionsReport = {}

    # Is company listed on NASDAQ?
    if company_ticker['Company Name'].str.contains(company_name).sum() <= 0:
        return None

    try:
        file_path = file_path.split('/')
        folder = [''.join(file_path[3].split('-')).split('.')[0]]	
        file_path = '/'.join(file_path[:len(file_path)-1] + folder)
        form_url = base_url + file_path
        r = requests.get(form_url)
        form4_path = re.search('(\/)([a-zA-Z0-9_-])*(.xml)', r.text)
        final_url = form_url + form4_path.group(0)

        # Grab the company's Form 4 and its derivative table.
        form_filing = urllib.request.urlopen(final_url)
        html = form_filing.read().decode('utf-8')
        root = ET.fromstring(html)
        derivativeTable = root.find('derivativeTable')

        # Search for option acquisitions
        strike_price = []
        exp_date = []
        amt = []
        if derivativeTable:
            for transaction in derivativeTable.findall('derivativeTransaction'):
                securityTitle = transaction.find('securityTitle')
                price = transaction.find('conversionOrExercisePrice')
                transactionAmounts = transaction.find('transactionAmounts')
                expirationDate = transaction.find('expirationDate')

                if 'Stock Option' in securityTitle[0].text and 'A' in transactionAmounts.find('transactionAcquiredDisposedCode')[0].text:
                    strike_price += [price[0].text]
                    exp_date += [expirationDate[0].text]
                    amt += [transactionAmounts.find('transactionShares')[0].text]

                if len(strike_price) > 0:
                    # res.write('Option found for ' + company + '\n')
                    # res.write('Strikes are: ' + '\t'.join(strike_price) + '\n')
                    # res.write('Exp dates are: ' + '\t'.join(exp_date) + '\n')
                    # res.write('Amts are: ' + '\t'.join(amt) + '\n\n')
                    print(final_url)
                    print('Current Company form: ' + company_name)
                    print(strike_price)
                    print(exp_date)
                    print(amt)    

    except:
        print('Failed on: ' + company_name)
        return None

    pass

date = getDate()
base_url = 'https://www.sec.gov/Archives/'
daily_url = base_url + 'edgar/daily-index/' + date['year'] + '/' + date['quarter'] + '/form.' + date['today_format'] + '.idx'
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
    exit()

rows = file.readlines()[11:]
company_ticker = pd.read_csv('ticker-company.csv', header = 0)
# res = open('./daily_results/' + today_format + '.txt.', 'w')

# Search for companies with form 4 filled out
for line in rows:
    str_line = line.decode('utf-8')
    str_split = [splits for splits in str_line.split(' ') if splits is not '']
    form_type = str_split[0]
    # Might need a list to hold all options option_list = []

    if form_type == '4':
        # current_options = searchForOptions(str_split)
        # if current_options: option_list += current_options
        file_path = str_split[-2]
        file_date = str_split[-3]
        cik = str_split[-4]
        str_split = str_split[1:len(str_split)-4]
        temp = ' '.join(str_split)
        company_name = temp.split('/')[0].split('\\')[0]
        
        try:
            # Is company listed on Nasdaq?
            if company_ticker['Company Name'].str.contains(company_name).sum() > 0:
                file_path = file_path.split('/')
                folder = [''.join(file_path[3].split('-')).split('.')[0]]	
                file_path = '/'.join(file_path[:len(file_path)-1] + folder)
                form_url = base_url + file_path
                r = requests.get(form_url)
                form4_path = re.search('(\/)([a-zA-Z0-9_-])*(.xml)', r.text)
                final_url = form_url + form4_path.group(0)

                # Grab the company's Form 4 and its derivative table.
                form_filing = urllib.request.urlopen(final_url)
                html = form_filing.read().decode('utf-8')
                root = ET.fromstring(html)
                derivativeTable = root.find('derivativeTable')
                
                # Search for option acquisitions
                strike_price = []
                exp_date = []
                amt = []
                if derivativeTable:
                    for transaction in derivativeTable.findall('derivativeTransaction'):
                        securityTitle = transaction.find('securityTitle')
                        price = transaction.find('conversionOrExercisePrice')
                        transactionAmounts = transaction.find('transactionAmounts')
                        expirationDate = transaction.find('expirationDate')

                        if 'Stock Option' in securityTitle[0].text and 'A' in transactionAmounts.find('transactionAcquiredDisposedCode')[0].text:
                            strike_price += [price[0].text]
                            exp_date += [expirationDate[0].text]
                            amt += [transactionAmounts.find('transactionShares')[0].text]

                        if len(strike_price) > 0:
                            # res.write('Option found for ' + company + '\n')
                            # res.write('Strikes are: ' + '\t'.join(strike_price) + '\n')
                            # res.write('Exp dates are: ' + '\t'.join(exp_date) + '\n')
                            # res.write('Amts are: ' + '\t'.join(amt) + '\n\n')
                            print(final_url)
                            print('Current Company form: ' + company_name)
                            print(strike_price)
                            print(exp_date)
                            print(amt)                                                
        except:
            print('Failed on: ' + company_name)
            continue