# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import requests, bs4, re, pandas, numpy, time, datetime

#get portfolio from excel
port1 = pandas.read_csv('portfolio1.csv')

#TODO: compute the value of each portfolio
prices = []
values = []

#get price of each tick in portfolio
for i in range(len(port1.index)):
    req = requests.get('https://tw.stock.yahoo.com/q/q?s=' + str(port1.ticks[i]))
    soup = bs4.BeautifulSoup(req.text, 'html.parser', from_encoding='utf-8')
    price_str = str(soup.select('td[align=center] > b'))
    price_regex = re.compile(r'[+-]?([0-9]*[.])?[0-9]+')
    re_price = price_regex.search(price_str)
    if(re_price):
        prices.append(float(re_price[0]))
    else:
        prices.append(numpy.NaN)
    
#get values of each tick in portfolio
for i in range(len(port1.index)):
    values.append(port1.holdings[i] * prices[i])

#write the prices and values back to portfolio's panda table
port1['prices'] = pandas.Series(prices, index=port1.index)
port1['values'] = pandas.Series(values, index=port1.index)

ts = time.time()
st = datetime.datetime.fromtimestamp(ts).strftime('%Y_%m_%d_%H_%M')
port1.to_csv('portfolio1_' + st + '.csv', sep=',', encoding='utf-8')