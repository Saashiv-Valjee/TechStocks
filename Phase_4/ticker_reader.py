import yfinance as yf
import pandas as pd
from datetime import datetime
import yaml
import numpy as np

class ReadTickers:
    def __init__(self, tickers=None):
        if tickers == None:
            with open("config.yaml", "r") as f:
                config = yaml.safe_load(f)
                self.tickers = config["tickers"]
        self.ticker_map = {}
        for ticker in self.tickers:
            ticker_obj = yf.Ticker(ticker)
            self.ticker_map[ticker] = ticker_obj.history(period='max')
            self.ticker_map[ticker].index = self.ticker_map[ticker].index.tz_localize(None).normalize()
    
    def latest_start(self):
        aligned_tickers = {}
        start_dates = []
        for ticker in self.tickers:
            df = self.ticker_map[ticker]
            first_date = df.index.min()
            start_dates.append(first_date)
        common_start = max(start_dates)
        for ticker in self.tickers:
            aligned_tickers[ticker] = self.ticker_map[ticker].loc[self.ticker_map[ticker].index >= common_start]
        return aligned_tickers


    def strategy(self,Z_window,R_window):
        for ticker in self.tickers:
            temp = self.ticker_map[ticker]
            prices = temp['Close']
            
            # for each ticker, use daily closing prices to compute z score over window
            # as well as the rolling returns over a potentially different window 
            # add these to the corresponding ticker dataframes within the ticker map
            rolling_mean = prices.rolling(Z_window, min_periods=Z_window).mean()
            rolling_std  = prices.rolling(Z_window, min_periods=Z_window).std()
            Z_score = (prices - rolling_mean) / rolling_std
            self.ticker_map[ticker]['zscore'] = Z_score
            self.ticker_map[ticker]['R_return'] = prices.pct_change(periods=R_window)



