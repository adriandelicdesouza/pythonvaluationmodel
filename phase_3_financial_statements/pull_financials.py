import yfinance as yf
import pandas as pd
import datetime as dt
import os

def get_cashflow(ticker):
    stock = yf.Ticker(ticker)
    cashflow = stock.cashflow
    return cashflow
def main():
    ticker = input("Enter stock ticker: ").upper()
    try:
        cashflow = get_cashflow(ticker)
        print(cashflow)
    except Exception as e:
        print(f"Error retrieving cashflow for {ticker}: {e}")
if __name__ == "__main__":
    main()