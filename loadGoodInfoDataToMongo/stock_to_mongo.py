# -*- coding: utf-8 -*-
"""
Created on Thu Sep 27 14:22:00 2018

@author: rex44391
"""
import requests, bs4, re, pandas, numpy, time, datetime
from pymongo import MongoClient

#load date from csv file
#you can download the file from goodinfo.com
table1 = pandas.read_csv('K_Chart.csv')
table1['tick'] = "2330"
table1['name'] = "台積電"

#convert 交易日期 to panda's datetime object
con_date = []
for i in range(len(table1.index)):
    date_str = "2018-"
    re_date = re.findall("\d+", str(table1.交易日期[i]))
    date_str += re_date[0]
    date_str += "-"
    date_str += re_date[1]
    con_date.append(date_str)
table1['date'] = pandas.to_datetime(con_date)
table1.rename(columns={'開盤價': 'Open'}, inplace=True)
table1.rename(columns={'最高價': 'High'}, inplace=True)
table1.rename(columns={'最低價': 'Low'}, inplace=True)
table1.rename(columns={'收盤價': 'Close'}, inplace=True)
table1.rename(columns={'成交億元': 'Volume'}, inplace=True)
#connect to database
client = MongoClient()
db = client['stock']
collection = db['daily_trade']
