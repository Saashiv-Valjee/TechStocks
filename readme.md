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

### Phase 1: Setup & Data Pipeline
- [x] Set up Python environment using Conda
- [x] Install packages: `yfinance`, `pandas`, `numpy`, `matplotlib`, `seaborn`
- [x] Retrieve historical daily data for all tickers using Yahoo Finance
- [x] Align, clean, and merge into a unified time series DataFrame

---

### Phase 2: Feature Engineering
- [x] Compute N-day log returns for N = 5, 10, 21
  - Completed, not the best way of doing so, could definitely be more efficient but what I've done works. One interesting thing was how the datetime was not cleaned to consider the daylight savings. Some trading days ended at 4 and others at 5. This caused a periodic error from June till some point later in the year every year. Diagnosing the problem was simple, by checking to see if rows with the specific time that was missing existed.

- [x] Calculate 20-day **rolling Z-scores** of returns to normalize momentum
  - Completed, Using pandas rolling function with min_periods to create a rolling window for days provided there are N amount of days previously available for the rolling window calculation.

- [x] Implement Relative Strength Index (RSI) for each ticker
  - Completed, using 20 day windows, with markers at 30,50,70 per ticker per year. Rolling and where from pandas are great functions! 
  
- [ ] Track Nvidia’s **outperformance vs AMD/TSMC/SOXX** over time

---

### Phase 3: Signal Construction
- [ ] Define simple alpha signals:
  - Go long Nvidia if its 10-day return z-score > AMD & TSMC
  - Go long Nvidia if it outperforms SOXX by > 1.5%
- [ ] Construct signal time series for backtesting

---

### Phase 4: Backtest and Evaluation
- [ ] Build simple backtester for daily rebalancing
- [ ] Calculate performance metrics:
  - Sharpe Ratio
  - Max Drawdown
  - Equity Curve vs Benchmark (SOXX)
- [ ] Plot signal vs returns scatterplots and trend heatmaps

---

### Phase 5: Insights and Strategy Development
- [ ] Identify strongest lead/lag relationships
- [ ] Test cross-correlation: Does NVDA lead AMD or vice versa?
- [ ] Propose simple rules-based trading strategy based on findings

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