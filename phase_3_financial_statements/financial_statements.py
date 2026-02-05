import yfinance as yf
import pandas as pd

user_input = input("Enter Tickers separated by commas: ")
tickers = [t.strip().upper() for t in user_input.split(",")]
all_data = []
for t in tickers:
    ticker = yf.Ticker(t)
    df = ticker.financials.T
    if df.empty:
        print(f"No financials foudn fopr {t}")
        continue
    df["Ticker"] =t
    all_data.append(df)
combined = pd.concat(all_data).set_index("Ticker",append=True)
combined = combined.reorder_levels(["Ticker", combined.index.names[0]])
combined.to_csv("all_income_statements.csv")
print("Saved combined dataset")
