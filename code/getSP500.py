import pandas as pd
import pandas_datareader as web
from pandas import DataFrame
import numpy as np
import datetime as dt
import yfinance as yf
import bs4 as bs
import requests


# get Company Tickers
def get_sp500_tickers():
    resp = requests.get('http://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
    soup = bs.BeautifulSoup(resp.text, 'lxml')
    table = soup.find('table', {'class': 'wikitable sortable'})
    tickers = []
    securities = []
    for row in table.findAll('tr')[1:]:
        ticker = row.findAll('td')[0].text
        security = row.findAll('td')[1].text
        tickers.append(ticker)
        securities.append(security)
        tickers = list(map(lambda s: s.strip(), tickers))
        securities = list(map(lambda s: s.strip(), securities))
        tickerdf = pd.DataFrame(tickers, columns = ['ticker'])
        securitydf = pd.DataFrame(securities,columns = ['security'])
        df = pd.concat([tickerdf, securitydf], axis = 1).reindex(tickerdf.index)
    df.to_csv('Stocks10M/SP500tickers.csv')
    return df


# get sp500 stock values
def get_sp500_stock_values(df):
    tickers = df.set_index('security')['ticker'].to_dict()
    start = dt.datetime(2018,1,1)
    end = dt.datetime.now()
    df_stocks = pd.DataFrame()
    for key, value in tickers.items():
        download = yf.download(value, start, end)
        download = pd.DataFrame(download)
        download['Ticker'] = value
        df_stocks = df_stocks.append(download)
    df_stocks.to_csv('Stocks10M/SP500.csv')
    return df_stocks


# get sp500 market caps
def get_sp500_market_cap(df_stocks):
    tickers = df_stocks.Ticker.unique().tolist()
    market_cap_data = web.get_quote_yahoo(tickers)['marketCap']
    marketCapdf = pd.DataFrame(market_cap_data, columns = ['market_cap'])
    marketCapdf.to_csv('Stocks10M/market_cap.csv')

if __name__ == "__main__":
    print("Getting S&P 500 data from the yahoo finance")
    df = get_sp500_tickers()
    df_stocks = get_sp500_stock_values(df)
    get_sp500_market_cap(df_stocks)
    print("Done!")
