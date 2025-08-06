# 📊 Quant Research Project: AI & Semiconductor Stocks

## 🧠 Project Focus
This project explores quantitative signals in the AI hardware and semiconductor sector, focusing on the relative performance and predictive features of key companies directly tied to the AI supply chain.

### ✅ Core Tickers
- **Nvidia (NVDA)** – Leading AI GPU manufacturer
- **AMD (AMD)** – GPU/CPU competitor to Nvidia
- **TSMC (TSM)** – World's largest chip foundry (Nvidia supplier)
- **Supermicro (SMCI)** – AI server manufacturer
- **iShares SOXX ETF (SOXX)** – Semiconductor index benchmark

---

## 🎯 Project Goals

### Phase 0.5: Setup & Data Pipeline
- [x] Set up Python environment using Conda
- [x] Install packages: `yfinance`, `pandas`, `numpy`, `matplotlib`, `seaborn`
- [x] Retrieve historical daily data for all tickers using Yahoo Finance
- [x] Align, clean, and merge into a unified time series DataFrame

---

### Phase 1: Feature Engineering
- [x] Compute N-day log returns for N = 5, 10, 21
  - Completed, not the best way of doing so, could definitely be more efficient but what I've done works. One interesting thing was how the datetime was not cleaned to consider the daylight savings. Some trading days ended at 4 and others at 5. This caused a periodic error from June till some point later in the year every year. Diagnosing the problem was simple, by checking to see if rows with the specific time that was missing existed.

- [x] Calculate 20-day **rolling Z-scores** of returns to normalize momentum
  - Completed, Using pandas rolling function with min_periods to create a rolling window for days provided there are N amount of days previously available for the rolling window calculation.

- [x] Implement Relative Strength Index (RSI) for each ticker
  - Completed, using 20 day windows, with markers at 30,50,70 per ticker per year. Rolling and where from pandas are great functions! 
  
- [x] Track Nvidia’s **outperformance vs AMD/TSMC/SOXX** over time
  - Completed, nothng to note really, this one was just pretty simple and interesting.
---

### Phase 2: Signal Construction
- [x] Define simple alpha signals:
  - Go long Nvidia if its 10-day return z-score > AMD & TSMC
  - Go long Nvidia if it outperforms SOXX by > 1.5%
    - Completed, this strategy isn't very good to be honest, but it works as some dummy strategy for now... 

- [x] Construct signal time series for backtesting
  - Completed. This is just the daily close data I am currently using...
---

### Phase 3: Backtest and Evaluation

The previous code is pretty messy and annoying to use so I am going to rewrite it.


- [x] Build simple backtester for daily rebalancing
- [x] Calculate performance metrics:
  - Sharpe Ratio
  - Max Drawdown
  - Equity Curve vs Benchmark (SOXX)
- Completed, this one was interesting, learning new ways to represent portfolios and strategies was fun. There seem to be alof of functions with numpy and pandas that are extremely good at processing the data in ways that this kind of analysis kills for. I think for this work I will continue with notebooks since it's mostly just strategy development.
---

### Phase 4: Insights and Strategy Development
- [x] Identify strongest lead/lag relationships
  - Completed, pretty simple really, 
- [x] Test cross-correlation: Does NVDA lead AMD or vice versa?
  - Completed during part one of phase 4, again simple but also interesting.
- [ ] Propose simple rules-based trading strategy based on findings
  -  Given that TSM leads NVDA, we could try comparing $500 per month regardless vs 500 (which rolls onto next month if unused) whenever TSM has an anomalous rally? 
---

## 🛠 Tech Stack
- Python 3.10+
- Jupyter Notebook / VSCode
- Yahoo Finance (`yfinance`)
- `pandas`, `numpy`, `matplotlib`, `seaborn`
- Optional: `backtrader`, `statsmodels`, `scikit-learn`

---

## 🔭 Stretch Goals
- Add fundamental data (earnings, P/E ratios) via FinancialModelingPrep
- Add Google Trends or Reddit sentiment analysis for AI-related terms
- Implement a risk model and beta-neutral long/short portfolio

---

## 📌 Author
This project is part of a personal Quant Research initiative to explore factor-based alpha strategies in tech and AI stocks.

## TODO
- add a config file to store things like an array of tickers and window sizes for the class rather then defining them inside the class.