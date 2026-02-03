import yfinance as yf
import pandas as pd
def get_fcf(stock):
    """Return the most recent free cash flow from yfinance Ticker object."""
    cashflow = stock.cashflow

    if cashflow.empty:
        raise ValueError("No cashflow data available")

    # Possible labels for CFO
    cfo_labels = ['Total Cash From Operating Activities', 'Operating Cash Flow']
    cfo = None
    for label in cfo_labels:
        if label in cashflow.index:
            # Take the first valid number in that row
            cfo = cashflow.loc[label].dropna().iloc[0]
            break
    if cfo is None:
        raise ValueError("Operating cash flow not found")

    # CapEx
    capex_labels = ['Capital Expenditures']
    capex = 0
    for label in capex_labels:
        if label in cashflow.index:
            capex = cashflow.loc[label].dropna().iloc[0]
            break

    fcf = cfo + capex
    if fcf == 0 or fcf is None:
        raise ValueError("FCF is zero or missing")

    return fcf

def get_dcf_value(ticker, discount_rate, growth_rate, years):
    stock = yf.Ticker(ticker)
    try:
        fcf = get_fcf(stock)
        shares = stock.info.get('sharesOutstanding')
        if shares is None or shares == 0:
            raise ValueError("Shares outstanding missing or zero")
    except Exception as e:
        raise ValueError(f"Error fetching financials for {ticker}: {e}")

    pv = 0
    for year in range(1, years + 1):
        projected = fcf * ((1 + growth_rate) ** year)
        pv += projected / ((1 + discount_rate) ** year)

    return pv / shares

def main():
    tickers = input("Enter tickers separated by commas: ").upper().split(",")
    discount_rate = float(input("Enter the assumed discount rate in decimal: "))
    growth_rate = float(input("Enter the assumed growth rate in decimal: "))
    years = int(input("Enter the number of years "))
    results = []
    for ticker in tickers:
        try:
            value = get_dcf_value(ticker,discount_rate,growth_rate,years)
            results.append({'Ticker':ticker,'DCF Value':value})
        except Exception as e:
            print(f"Skpping {ticker} due to error {e}")
    df = pd.DataFrame(results)
    print(df)
    df.to_csv("valuation.csv",index=False)
    print("Saved to valuation.csv")
if __name__ == "__main__":
    main()