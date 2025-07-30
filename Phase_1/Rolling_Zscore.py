from qr_proj.data_loader import TickerReader
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import os

reader = TickerReader()
ticker_histMap = reader.ticker_hists_return()
window_size = 20
z_scores = {}

def Z_score(prices, window):
    rolling_mean = prices.rolling(window, min_periods=window).mean()
    rolling_std  = prices.rolling(window, min_periods=window).std()
    Z_score = (prices - rolling_mean) / rolling_std
    return Z_score

for ticker in ticker_histMap.keys():
    ticker_price_df = ticker_histMap[ticker]["Close"]
    z_scores[ticker] = Z_score(ticker_price_df,window_size)



for ticker, zscore_series in z_scores.items():
    df = zscore_series.to_frame(name="Z")  # Convert to DataFrame for filtering
    df['Year'] = df.index.year

    for year in sorted(df['Year'].dropna().unique()):
        yearly_data = df[df['Year'] == year]["Z"]
        if yearly_data.dropna().empty:
            continue  # skip empty years

        # Create directory if it doesn't exist
        outdir = f"E:\\QR_Proj\\Phase_1\\plots\\Rolling_Zscores\\{ticker}"
        os.makedirs(outdir, exist_ok=True)

        # Plot
        plt.figure(figsize=(12, 5))
        plt.plot(yearly_data, label=f"{ticker} Z-Score ({window_size}-day) - {year}")
        plt.axhline(0, color='black', linestyle='--', linewidth=1)
        plt.axhline(2, color='red', linestyle='--', linewidth=0.8)
        plt.axhline(-2, color='red', linestyle='--', linewidth=0.8)
        plt.title(f"{ticker} Rolling Z-Score - {year}")
        plt.xlabel("Date")
        plt.ylabel("Z-Score")
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

