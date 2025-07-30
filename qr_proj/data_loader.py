import yfinance as yf
import pandas as pd
from datetime import datetime

class TickerReader:
    def __init__(self, tickers=None):
        if tickers is None:
            tickers = ['NVDA', 'TSM', 'AMD', 'SOXX', 'SMCI']
        self.tickers = tickers
        self.ticker_obj = {}
        self.ticker_hists = {}

        for ticker in self.tickers:
            print(f"Fetching {ticker}")
            obj = yf.Ticker(ticker)
            self.ticker_obj[ticker] = obj
            self.ticker_hists[ticker] = obj.history(period='max')

    def ticker_hists_return(self):
        return self.ticker_hists

    @staticmethod
    def get_price(df, date_str):
        # Try both -05:00 and -04:00 timezone-aware strings
        for tz in ["-05:00", "-04:00"]:
            full_date = f"{date_str} 00:00:00{tz}"
            if full_date in df.index:
                return df.loc[full_date]['Close']
        return None

    def build_daily_price_map(self):
        all_dates = pd.date_range(start='1999-01-01', end='2025-12-31', freq='D')
        daily_price_map = {}

        for ticker in self.tickers:
            print(f"Processing {ticker}")
            daily_price_map[ticker] = []
            for date_obj in all_dates:
                date_str = date_obj.strftime('%Y-%m-%d')
                daily_close = self.get_price(self.ticker_hists[ticker], date_str)
                if daily_close is not None:
                    daily_price_map[ticker].append((date_str, daily_close))

        return daily_price_map
