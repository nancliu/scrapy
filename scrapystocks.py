# -*- coding: utf-8 -*-
"""
Created on Thu Jan 12 17:40:50 2017
scrap stock data from snowball
@author: ln
"""

from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
import pandas.io.data as web
import pandas as pd
#from openpyxl import load_workbook 
import datetime
#import matplotlib.pyplot as plt
import csv

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
    source = 'yahoo'
    ff = web.DataReader(stockCode,source,start,end)
    return ff

def extractStocks(fromFile,toFile):
    pass
    
def getStocksbyList(tickerList):
    start = datetime.datetime(2017,1,1)
    end = datetime.date.today()
    
#    book =load_workbook('files\Stocks.xlsx')    #write append to a exist excel
#    writer = pd.ExcelWriter('files\Stocks.xlsx',engine='openpyxl') 

    writer = pd.ExcelWriter('files\Stocks.xlsx')
    global ff_s
    for ticker in tickerList:
        ff = getStockDetails(ticker,start,end)
        ff.to_excel(writer,ticker,encoding='utf-8')
        
        #extract simple stock info
        if len(ff_s)==0:
            ff_s=ff[['Close']].copy()
            ff_s['ratio']=
        else:
            ff1=ff[['Close']].copy()
            ff_s=ff_s.join(ff1,lsuffix='_caller',rsuffix='_other')
                      
        print('-----get '+ticker+'------')
    writer.save()
    ff_s.columns=tickerList
    writer = pd.ExcelWriter('files\Stocks_Simple.xlsx')
    ff_s.to_excel(writer,encoding='utf-8')
    writer.save()    

    
tickerList=['INTC','AMZN','MSFT','GOOG']

getStocksbyList(tickerList)

    