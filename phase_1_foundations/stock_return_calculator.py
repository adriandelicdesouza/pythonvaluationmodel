import yfinance as yf
import pandas as pd

def simple_return(start_price, end_price):
    return (end_price - start_price) / start_price

def annualized_return(start_price, end_price, years):
    return (end_price / start_price) ** (1 / years) - 1

def main():
    print("=== Stock Return Calculator ===")

    ticker = input("Enter Stock Ticker Symbol: ").upper()
    start_date = input("Start Date (YYYY-MM-DD): ")
    end_date = input("End Date (YYYY-MM-DD): ")

    data = yf.download(ticker, start=start_date, end=end_date)

    if data.empty:
        print("No data found for this ticker/dates.")
        return

    print(data.columns)  # optional: see column structure

    # Handle MultiIndex columns from yfinance
    if isinstance(data.columns, pd.MultiIndex):
        adj_col = ('Adj Close', ticker) if ('Adj Close', ticker) in data.columns else ('Close', ticker)
        start_price = data[adj_col].iloc[0]
        end_price = data[adj_col].iloc[-1]
    else:
        start_price = data['Adj Close'].iloc[0] if 'Adj Close' in data.columns else data['Close'].iloc[0]
        end_price = data['Adj Close'].iloc[-1] if 'Adj Close' in data.columns else data['Close'].iloc[-1]

    years = (data.index[-1] - data.index[0]).days / 365.25

    s_return = simple_return(start_price, end_price)
    a_return = annualized_return(start_price, end_price, years)

    print(f"\nSimple Return: {s_return*100:.2f}%")
    print(f"Annualized Return: {a_return*100:.2f}%")

if __name__ == "__main__":
    main()
