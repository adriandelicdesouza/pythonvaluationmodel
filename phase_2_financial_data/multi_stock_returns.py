import yfinance as yf
import pandas as pd

def simple_return(start_price, end_price):
    return((end_price - start_price)/start_price)
def annualized_return(start_price,end_price,years):
    return((end_price - start_price)**(1/years)-1)
def main():
    print("Script started")
    tickers = input("Enter Tickers separated by commas : ").upper().split(",")
    start_date = input("Enter the start date yyyy-mm-dd : ")
    end_date = input("Enter the end date yy-mm-dd : ")

    data = yf.download(tickers, start=start_date, end=end_date, group_by='ticker')

    results =[]

    for ticker in tickers:
        if ticker not in data.columns.get_level_values(0):
            print(f"No data for {ticker}")
            continue
        df = data[ticker] if isinstance(data.columns, pd.MultiIndex) else data
        start_price = df['Adj Close'].iloc[0] if 'Adj Close' in df.columns else df['Close'].iloc[0]
        end_price = df['Adj Close'].iloc[-1] if 'Adj Close' in df.columns else df['Close'].iloc[-1]
        years = (df.index[-1] - df.index[0]).days / 365.25
        
        results.append({
            'Ticker' : ticker,
            'Simple Return' : round(simple_return(start_price,end_price)*100,2),
            'Annualized Return' : round (annualized_return(start_price,end_price,years)*100,2)
        }) 

    df_results = pd.DataFrame(results)
    print(df_results)
    df_results.to_csv("msr.csv",index=False)

if __name__ == "__main__":
    main()