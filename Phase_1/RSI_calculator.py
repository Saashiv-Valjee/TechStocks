from qr_proj.data_loader import TickerReader
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import os

reader = TickerReader()
ticker_histMap = reader.ticker_hists_return()
window_size = 20
rsi_scores = {}

def find_rsi(prices, window):

    # do N_(n+1) - N_n
    delta = prices.diff()

    # find the prices to consider, replace prices who don't meet condition with 0
    # to keep alignment 

    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)
    avg_gain = gain.rolling(window=window, min_periods=window).mean()
    avg_loss = loss.rolling(window=window, min_periods=window).mean()
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi


for ticker in ticker_histMap.keys():
    ticker_price_df = ticker_histMap[ticker]["Close"]
    rsi_scores[ticker] = find_rsi(ticker_price_df,window_size)

for ticker, ticker_series in rsi_scores.items():
    df = ticker_series.to_frame(name="RSI")  # Convert to DataFrame for filtering
    df['Year'] = df.index.year

    for year in sorted(df['Year'].dropna().unique()):
        yearly_data = df[df['Year'] == year]["RSI"]
        if yearly_data.dropna().empty:
            continue  # skip empty years

        # Create directory if it doesn't exist
        outdir = f"E:\\QR_Proj\\Phase_1\\plots\\RSI\\{ticker}"
        os.makedirs(outdir, exist_ok=True)

        # Plot
        plt.figure(figsize=(12, 5))
        plt.plot(yearly_data, label=f"{ticker} RSI-Score ({window_size}-day) - {year}")
        plt.axhline(70, color='red', linestyle='--', linewidth=0.8)
        plt.axhline(50, color='red', linestyle='--', linewidth=0.8)
        plt.axhline(30, color='red', linestyle='--', linewidth=0.8)
        plt.title(f"{ticker} RSI - {year}")
        plt.xlabel("Date")
        plt.ylabel("RSI")
        plt.legend()
        plt.grid(True)

        ax = plt.gca()
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%b'))  # Short month names
        ax.xaxis.set_major_locator(mdates.MonthLocator(interval=1))
        plt.gcf().autofmt_xdate()

        plt.tight_layout()
        outpath = os.path.join(outdir, f"{year}.png")
        plt.savefig(outpath)
        plt.close()
