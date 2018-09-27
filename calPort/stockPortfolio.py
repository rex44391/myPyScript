# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import requests, bs4, re, pandas, numpy, time, datetime

#get portfolio from excel
port1 = pandas.read_csv('portfolio2.csv')

#compute the value of each portfolio
names = []
prices = []
values = []

#get price of each tick in portfolio
price_regex = re.compile(r'[+-]?([0-9]*[.])?[0-9]+')
name_regex = re.compile(r'">[0-9]+.*?</a>')

for i in range(len(port1.index)):
    tick_str = ""
    if port1.ticks[i] == 56 or port1.ticks[i] == 646:
        tick_str = "00" + str(port1.ticks[i])
    else:
        tick_str = str(port1.ticks[i])
    req = requests.get('https://tw.stock.yahoo.com/q/q?s=' + tick_str)
    soup = bs4.BeautifulSoup(req.text, 'html.parser', from_encoding='utf-8')
    price_str = str(soup.select('td[align=center] > b'))
    re_price = price_regex.search(price_str)
    if(re_price):
        prices.append(float(re_price[0]))
    else:
        prices.append(numpy.NaN)
    
    #get name of each tick
    name_str = str(soup.select('td[width=105] > a'))
    re_name = name_regex.search(name_str)
    name_str = re_name[0][:-4]
    name_str = name_str[name_str.find(tick_str) + len(tick_str):]
    if(name_str):
        names.append(name_str)
    else:
        names.append("NoName")
    
#get values of each tick in portfolio
for i in range(len(port1.index)):
    values.append(port1.holdings[i] * prices[i])

#write the prices and values back to portfolio's panda table
port1['names'] = pandas.Series(names, index=port1.index)
port1['prices'] = pandas.Series(prices, index=port1.index)
port1['values'] = pandas.Series(values, index=port1.index)

ts = time.time()
st = datetime.datetime.fromtimestamp(ts).strftime('%Y_%m_%d_%H_%M')
port1.to_csv('portfolio1_' + st + '.csv', sep=',', encoding='utf_8_sig')