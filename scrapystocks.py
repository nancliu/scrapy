# -*- coding: utf-8 -*-
"""
Created on Thu Jan 12 17:40:50 2017
scrap stock data from snowball
@author: ln
"""

from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
import pandas.io.data as web
import datetime
import matplotlib.pyplot as plt


#Retrieves a list of stock details found on a page
def getStockDetails_snowball(stockCode):
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}  
    req = Request(url="https://xueqiu.com/S/"+stockCode, 
                                 headers=headers)  
    html = urlopen(req)
    bsObj = BeautifulSoup(html, "html.parser")
    #Finds all links that begin with a "/"
    stockName = bsObj.find("span", {"class":"stockName"})
    print(stockName.get_text())
    print(bsObj.find("div",{"class":"stockQuote"}).find(id="timeInfo").get_text())
    for sibling in bsObj.find("div",{"class":"stockQuote"}).div.next_siblings:
        print(sibling.get_text())
    
def getStockDetails(stockCode):
    pass
        
#getStockDetails("INTC")
tickerList=['INTC','AMZN','MSFT','GOOG']
start = datetime.datetime(2015,1,1)
end = datetime.date.today()
ticker= "INTC"
f = web.DataReader(ticker,'yahoo',start,end)
print(f)
plt.plot(f['Close'])
plt.title(ticker+' Closing Prices')
plt.show()
    