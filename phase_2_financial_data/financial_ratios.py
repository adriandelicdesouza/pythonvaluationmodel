import yfinance as yf
import pandas as pd
def get_ratios(ticker):
    stock = yf.Ticker(ticker)
    info = stock.info

    ratios = {}  # create an empty dictionary
    ratios['Ticker'] = ticker
    ratios['PE'] = info.get('trailingPE', None)
    ratios['PB'] = info.get('priceToBook', None)
    ratios['ROE'] = info.get('returnOnEquity', None)
    ratios['Debt/Equity'] = info.get('debtToEquity', None)
    
    return ratios

def main():
    tickers = input("Enter tickers separated by commas: ").upper().split(",")
    results = []
    for ticker in tickers:
        try:
            r = get_ratios(ticker)
            results.append(r)
        except Exception as e:
            print(f"Skipping {ticker} due to error : {e}")
    df = pd.DataFrame(results)
    print(df)
    df.to_csv("fr.csv",index=False)
    print("Saved to fr.csv")
if __name__ == "__main__":
    main()