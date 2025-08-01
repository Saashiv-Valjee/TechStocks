from qr_proj.data_loader import TickerReader
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import os

reader = TickerReader()
ticker_histMap = reader.ticker_hists_return()
chosen_ticker = 'NVDA'

for ticker in ticker_histMap.keys(): 
    if ticker == chosen_ticker:
        continue
    # storage if necessary for later use
    ticker_histMap[chosen_ticker][f'vs_{ticker}'] = ticker_histMap[chosen_ticker]['Close'] / ticker_histMap[ticker]['Close']
    outdir = f"E:\\QR_Proj\\Phase_1\\plots\\nvda_comp"
    os.makedirs(outdir, exist_ok=True)
    outpath = os.path.join(outdir, f"nvda_vs_{ticker}.png")

    # plotting the above
    plt.figure(figsize=(12, 6))
    plt.plot(
        ticker_histMap[chosen_ticker].index, 
        ticker_histMap[chosen_ticker][f'vs_{ticker}'], 
        label=f'NVDA / {ticker}' , color = 'black'
    )

    plt.plot(
        ticker_histMap[chosen_ticker].index, 
        ticker_histMap[chosen_ticker]['Close'], 
        label=f'{chosen_ticker}', color = 'green'
    )
    plt.plot(
        ticker_histMap[ticker].index, 
        ticker_histMap[ticker]['Close'], 
        label=f'{ticker}', color = 'red'
    )
    plt.xlabel('Date')
    plt.ylabel('Relative Performance')
    plt.title(f'NVDA Outperformance vs {ticker}')
    plt.legend()
    plt.yscale('log')
    plt.tight_layout()
    plt.savefig(outpath)
    