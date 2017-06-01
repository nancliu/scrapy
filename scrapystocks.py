# -*- coding: utf-8 -*-
"""
Created on Thu Jan 12 17:40:50 2017
scrap stock data from snowball
@author: ln
"""

from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
import pandas_datareader.data as web
import pandas as pd
#from openpyxl import load_workbook 
import datetime
#import matplotlib.pyplot as plt
#import csv

ff_s = pd.DataFrame()
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
    
def getStockDetails(stockCode,start,end):
    source = 'google'
    ff = web.DataReader(stockCode,source,start,end)
#     ff = web.DataReader('INTL','yahoo',start,end)
#    print(stockCode)
#    print(ff.head())
    if source =='yahoo':
        index = 'Adj Close'
    elif source == 'google':
        index ='Close'
    
    return ff,index

def extractStocks(fromFile,toFile):
    pass
    
def getStocksbyList(tickerList):

    start = datetime.date(2016,1,1)
    end = datetime.date.today()
    
    if start.month == end.month & start.year == end.year:
        print('No need to update data.')
        return
    
    writer = pd.ExcelWriter('files\Stocks.xlsx')
    global ff_s
    for ticker in tickerList:
        ff,index = getStockDetails(ticker,start,end)
        ff.to_excel(writer,ticker,encoding='utf-8')
        
        #extract simple stock info,ff_s is a Dataframe
        #extract one data every 21 days, so about 12 data from one year
        if len(ff_s)==0:
            ff_s=ff[[index]].copy()[::21]
            ff_s.columns=[ticker]
            ff_s['r_'+ticker] = ff_s.pct_change()
        else:
            ff1=ff[[index]].copy()[::21]
            ff1.columns=[ticker]
            ff1['r_'+ticker] = ff1.pct_change()
            ff_s=ff_s.join(ff1)
        
        print('-----get '+ticker+'------')
#        print(ff_s.head())
    writer.save()
#    ff_s.columns=tickerList
    writer = pd.ExcelWriter('files\Stocks_Simple.xlsx')
    ff_s.to_excel(writer,encoding='utf-8')
    writer.save()    

    #INTL
tickerList=['AMZN','GOOG','MSFT','CTRP','VMW','JD','BABA']

getStocksbyList(tickerList)

    