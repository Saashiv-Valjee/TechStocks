from qr_proj.data_loader import TickerReader
import pandas as pd 
import matplotlib.pyplot as plt 
import matplotlib.dates as dates
import os 
import numpy as np
import yaml

with open("e:/QR_Proj/Phase_2/config.yaml", "r") as f:
    config = yaml.safe_load(f)

# readability 
main_ticker = config['main_ticker'][0]

stock_starts = []

ticker_class = TickerReader(config['tickers'])
ticker_histMap = ticker_class.ticker_hists_return()
for ticker in config['tickers']:
    ticker_histMap[ticker]['Year'] = ticker_histMap[ticker].index.year
    ticker_histMap[ticker]["zscore"] = TickerReader.Z_score(ticker_histMap[ticker]['Close'],config["window_sizes"]["zscore"][1])
    ticker_histMap[ticker]['10D_Returns'] = ticker_histMap[ticker]['Close'].pct_change(periods=9)
    stock_starts.append((ticker_histMap[ticker].index)[0])
    stock_end = (ticker_histMap[ticker].index)[-1]
all_dates = pd.date_range(start=np.array(stock_starts).max(),end=stock_end)

for ticker in config['tickers']:
    ticker_histMap[ticker] = ticker_histMap[ticker][(ticker_histMap[ticker].index).isin(all_dates)]

long_zscores = ticker_histMap[main_ticker][
    (ticker_histMap[main_ticker]['zscore'] > ticker_histMap['AMD']['zscore']) & 
    (ticker_histMap[main_ticker]['zscore'] > ticker_histMap['TSM']['zscore'])
]

long_pct = ticker_histMap[main_ticker][ticker_histMap[main_ticker]['10D_Returns'] > 1.5 * ticker_histMap['SOXX']['10D_Returns']]

for year in sorted(ticker_histMap[main_ticker]['Year'].unique()):
    nvda_year = ticker_histMap[main_ticker][ticker_histMap[main_ticker]['Year'] == year]
    soxx_year = ticker_histMap['SOXX'][ticker_histMap['SOXX']['Year'] == year]
    amd_year = ticker_histMap['AMD'][ticker_histMap['AMD']['Year'] == year]
    tsm_year = ticker_histMap['TSM'][ticker_histMap['TSM']['Year'] == year]

    long_zscores_year = long_zscores[long_zscores.index.year == year]
    long_pct_year = long_pct[long_pct.index.year == year]

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 8), sharex=True)

    # plot the 10D returns 
    # mark the points that meet the signal condition
    ax1.plot(nvda_year.index, nvda_year['10D_Returns'], label='NVDA 10D Return', color='green')
    ax1.plot(soxx_year.index, soxx_year['10D_Returns'], label='SOXX 10D Return', color='blue', alpha=0.6)

    ax1.scatter(long_pct_year.index,
                long_pct_year['10D_Returns'],
                color='green', marker='o', label='Signal: NVDA > SOXX by threshold')

    ax1.set_ylabel("10-Day Return")
    ax1.set_title(f"NVDA Alpha Signals - {year}")
    ax1.grid(True)
    ax1.legend(loc='upper left')

    # plot the zscore of AMD, NVDA and TSM(C) 
    # marks 
    ax2.plot(nvda_year.index, nvda_year['zscore'], label='NVDA z-score', color='green')
    ax2.plot(amd_year.index, amd_year['zscore'], label='AMD z-score', color='blue', alpha=0.4)
    ax2.plot(tsm_year.index, tsm_year['zscore'], label='TSM z-score', color='red', alpha=0.4)

    ax2.scatter(long_zscores_year.index,
                long_zscores_year['zscore'],
                color='green', marker='o', label='Signal: NVDA z > AMD & TSM')

    ax2.set_ylabel("Z-Score")
    ax2.set_xlabel("Date")
    ax2.grid(True)
    ax2.legend(loc='upper left')
    fig.tight_layout()
    outdir = f"E:/QR_Proj/Phase_2/plots/{year}"
    os.makedirs(outdir, exist_ok=True)
    plt.savefig(f"{outdir}/nvda_signals_subplot_{year}.png")
    plt.close()
