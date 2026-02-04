import yfinance as yf
import pandas as pd
import datetime as dt
import os

def get_info(ticker):
    stock = yf.Ticker(ticker)
    info = stock.info
    return info
def main():
    ticker = input("Enter stock ticker: ").upper()
    try:
        info = get_info(ticker)
        for key, value in info.items():
            print(f"{key}: {value}")
        print(f"\n")
        print(f"Long Name: {info.get('longName', 'N/A')}")
        print(f"Listed On: {info.get('exchange', 'N/A')}")
    except Exception as e:
        print(f"Error retrieving info for {ticker}: {e}")
if __name__ == "__main__":
    main()