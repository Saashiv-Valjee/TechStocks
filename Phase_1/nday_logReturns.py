import yfinance as yf
import inspect
import matplotlib.pyplot as plt 
import numpy as np
import pandas as pd
import matplotlib.dates as mdates
from datetime import datetime

tickers = ['nvda','tsm','amd','soxx','smci']
ticker_obj = {}
ticker_hists = {}

for ticker in tickers:
    ticker_obj[ticker] = yf.Ticker(ticker)
    ticker_hists[ticker] = ticker_obj[ticker].history(period='max')

def get_price(df, date_str):
    # Try both -05:00 and -04:00 timezone-aware strings
    for tz in ["-05:00", "-04:00"]:
        full_date = f"{date_str} 00:00:00{tz}"
        if full_date in df.index:
            return df.loc[full_date]['Close']
    return None  # Not found

# Generate only real calendar days
all_dates = pd.date_range(start='1999-01-01', end='2025-12-31', freq='D')
unique_years = []

daily_price_map = {}
for ticker in tickers:
    print(f"reading in {ticker}")
    daily_price_map[ticker] = []
    for date_obj in all_dates:
        date_str = date_obj.strftime('%Y-%m-%d')
        year = date_str[:4]
        if year not in unique_years:
            print(year)
            unique_years.append(year)
        daily_close = get_price(ticker_hists[ticker], date_str)
        if daily_close is not None:
            daily_price_map[ticker].append((date_str, daily_close))
    unique_years = []

def nday_with_dates(price_tuples, ndays_offset):
    dates = [d for d, p in price_tuples]
    prices = [p for d, p in price_tuples]
    new_prices = prices[ndays_offset-1:] + [0]*(ndays_offset-1)
    returns = np.log(np.array(new_prices) / np.array(prices))
    return list(zip(dates, returns))

nday_prices = {} 
noffset_returns = {}
nday_offsets = [5,10,21]

for ticker in tickers:
    for offset in nday_offsets:
        noffset_returns[ticker, offset] = nday_with_dates(daily_price_map[ticker], offset)[:-offset+1]

for ticker in tickers:
    fig, axes = plt.subplots(len(nday_offsets),1)
    for i, n in enumerate(nday_offsets):
        dates, returns = zip(*noffset_returns[ticker, n])
        dates = [datetime.strptime(d, "%Y-%m-%d") for d in dates]

        ax = axes[i]
        ax.plot(dates, returns)
        ax.set_xlabel("Date")
        ax.set_ylabel("Return")
        ax.set_title(f"{ticker.upper()} {n}-day Offset Returns")
        fig.autofmt_xdate()

    plt.tight_layout()
    plt.savefig(f'E:\QR_Proj\Phase_1\plots/nday_logReturns/{ticker.upper()}')
    