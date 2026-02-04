import yfinance as yf
import pandas as pd
import datetime as dt
import os as os

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
            print(f"CFO found using label '{label}': {cfo}")
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

    # Calculate present value of projected FCF
    pv = 0
    for year in range(1, years + 1):
        projected = fcf * ((1 + growth_rate) ** year)
        pv += projected / ((1 + discount_rate) ** year)

    dcf_per_share = pv / shares
    return dcf_per_share

def compute_wacc(equityValue,debtValue, costOfEquity, costOfDebt, taxRate):
    totalValue = equityValue + debtValue
    wacc = (equityValue / totalValue) * costOfEquity + (debtValue / totalValue) * costOfDebt * (1 - taxRate)
    print(f"WACC:{wacc*100:.2f}%")
    return wacc

def main():
    # Read Excel, first row is data
    df = pd.read_excel("watchlist.xlsx", header=None)

    # Get tickers from first column safely
    tickers = df.iloc[:, 0].astype(str).str.upper().tolist()
    print("Tickers:", tickers)
    years = int(input("Enter the number of years for projection (e.g., 5): "))
    results = []
    for ticker in tickers:
        try:
            stock = yf.Ticker(ticker)
            current_price = stock.info.get('currentPrice')
            if current_price is None:
                raise ValueError("Current price missing")
            equityValue = stock.info.get('marketCap')
            debtValue = stock.info.get('totalDebt', 0)
            costOfEquity = float(input(f"Enter the cost of equity in decimal for {ticker}: "))
            costOfDebt = float(input(f"Enter the cost of debt in decimal for {ticker}: "))
            taxRate = float(input(f"Enter the tax rate in decimal for {ticker}: "))
            discount_rate = compute_wacc(equityValue, debtValue, costOfEquity, costOfDebt, taxRate)
            growth_rate = float(input(f"Enter the assumed growth rate in decimal for {ticker}: "))
            dcf_value = get_dcf_value(ticker, discount_rate, growth_rate, years)
            upside = ((dcf_value - current_price) / current_price) * 100

            print(f"{ticker} computed")
            results.append({
                'Ticker': ticker,
                'Current Price': current_price,
                'DCF Value': round(dcf_value, 2),
                'Upside (%)': round(upside, 2)
            })

        except Exception as e:
            print(f"Skipping {ticker} due to error: {e}")

    df_out = pd.DataFrame(results)
    print(df_out)
    date = dt.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    output_dir = r"C:\Users\delic\OneDrive\Desktop\pythonvaluationmodel\valuations"
    os.makedirs(output_dir, exist_ok=True)
    file_path = os.path.join(output_dir, f"{date}_valuation.csv")
    dt.date
    df_out.to_csv(file_path, index=False)
    print(f"Saved to {file_path}")

if __name__ == "__main__":
    main()