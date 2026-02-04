from matplotlib import ticker
import yfinance as yf
import pandas as pd
import datetime as dt
import os

def project_fcf(fcf,high_growth,low_growth,high_years,total_years):
    cashflows = []
    current_fcf = fcf
    for year in range(1, total_years + 1):
        if year <= high_years:
            growth = high_growth
        else:
            growth = low_growth
        current_fcf *= (1 + growth)
        cashflows.append(current_fcf)
    return cashflows
def get_cost_of_equity(stock, risk_free, market_return=0.10):
    beta = stock.info.get('beta', 1)
    print(f"Beta: {beta}")
    return risk_free + beta * (market_return - risk_free)
def get_cost_of_debt(stock):
    fin = stock.financials
    debt = stock.info.get("totalDebt", 0)

    if "Interest Expense" in fin.index and debt > 0:
        interest = abs(fin.loc["Interest Expense"].dropna().iloc[0])
        return interest / debt
    return 0.05  # fallback
def get_fcf(stock):
    cashflow = stock.cashflow

    if cashflow.empty:
        raise ValueError("No cashflow data available")

    cfo_labels = [
        'Cash Flow From Continuing Operating Activities'
    ]
    cfo = None
    for label in cfo_labels:
        if label in cashflow.index:
            cfo_series = cashflow.loc[label].dropna().head(3)
            cfo = cfo_series.mean()
        break
    if cfo is None:
        raise ValueError("Operating cash flow not found")

    capex_labels = [
    'Capital Expenditures',
    'Capital Expenditure',
    'Purchase Of Property Plant Equipment',
    'Purchases Of Property And Equipment'
    ]
    capex = 0
    revenue_labels = ['Total Revenue', 'Revenue']
    revenue = None
    for label in revenue_labels:
        if label in cashflow.index:
            revenue_series = cashflow.loc[label].dropna().head(3)
            revenue = revenue_series.mean()
        break


    for label in capex_labels:
        if label in cashflow.index:
            capex_series = cashflow.loc[label].dropna().head(3)
            capex = capex_series.mean()
        break

    fcf = cfo + capex
    if fcf == 0 or fcf is None:
        raise ValueError("FCF is zero or missing")

    return fcf
def get_dcf_value(ticker, wacc, high_growth, low_growth, years_high, years_total, tax_rate):
    stock = yf.Ticker(ticker)

    try:
        fcf = get_fcf(stock)
        print(f"FCF: {fcf}")
        shares = stock.info.get('sharesOutstanding')
        print(f"Shares Outstanding: {shares}")
        cash = stock.info.get("totalCash", 0)
        print(f"Total Cash: ${cash}")
        debt = stock.info.get("totalDebt", 0)
        print(f"Total Debt: ${debt}")

        if shares is None or shares == 0:
            raise ValueError("Shares outstanding missing or zero")

    except Exception as e:
        raise ValueError(f"Error fetching financials for {ticker}: {e}")

    # --- Project cash flows (multi-stage) ---
    cashflows = project_fcf(fcf, high_growth, low_growth, years_high, years_total)

    # --- Discount projected cash flows ---
    pv_fcf = 0
    for year, cf in enumerate(cashflows, start=1):
        pv_fcf += cf / ((1 + wacc) ** year)

    # --- Terminal Value (Gordon Growth) ---
    terminal_fcf = cashflows[-1] * (1 + low_growth)

    if low_growth >= wacc:
        raise ValueError("Terminal growth must be less than WACC")

    terminal_value = terminal_fcf / (wacc - low_growth)
    pv_terminal = terminal_value / ((1 + wacc) ** years_total)

    enterprise_value = pv_fcf + pv_terminal

    # --- Convert Enterprise Value → Equity Value ---
    equity_value = enterprise_value + cash - debt

    dcf_per_share = equity_value / shares
    return dcf_per_share, enterprise_value, pv_terminal


def compute_wacc(equityValue,debtValue, costOfEquity, costOfDebt, taxRate):
    totalValue = equityValue + debtValue
    # wacc = (equityValue / totalValue) * costOfEquity + (debtValue / totalValue) * costOfDebt * (1 - taxRate)
    wacc = float(input("Enter WACC in decimal (e.g., 0.08 for 8%): "))
    print(f"WACC:{wacc*100:.2f}%")
    return wacc

def sensitivity_analysis(ticker, wacc, high_growth, low_growth, years_high, years_total, tax_rate):
    wacc_range = [wacc - 0.01, wacc, wacc + 0.01]
    growth_range = [low_growth - 0.005, low_growth, low_growth + 0.005]

    results = {}

    for g in growth_range:
        row = []
        for r in wacc_range:
            try:
                value, _, _ = get_dcf_value(
                    ticker,
                    r,
                    high_growth,
                    g,
                    years_high,
                    years_total,
                    tax_rate
                )
                row.append(round(value, 2))
            except:
                row.append(None)
        results[f"g={round(g*100,2)}%"] = row

    df = pd.DataFrame(
        results,
        index=[f"WACC {round(r*100,2)}%" for r in wacc_range]
    )

    return df

def main():
    # Read Excel, first row is data
    df = pd.read_excel("watchlist.xlsx", header=None)
    # Get tickers from first column safely
    tickers = df.iloc[:, 0].astype(str).str.upper().tolist()
    print("Tickers:", tickers)
    years = int(input("Enter the number of years for projection (e.g., 5): "))
    results = []
    risk_free = yf.Ticker("^TNX").history(period="1d")["Close"].iloc[-1] / 100
    print(f"Risk-free rate: {risk_free*100:.2f}%")
    for ticker in tickers:
        try:
            stock = yf.Ticker(ticker)
            current_price = stock.info.get('currentPrice')
            print(f"${current_price}")
            if current_price is None:
                raise ValueError("Current price missing")
            equityValue = stock.info.get('marketCap')
            print(f"Equity Value ${equityValue}")
            print(equityValue)
            debtValue = stock.info.get('totalDebt', 0)
            print(f"Debt Value ${debtValue}")
            print(debtValue)
            costOfEquity = get_cost_of_equity(stock, risk_free)
            print(f"Cost of Equity {costOfEquity*100:.2f}%")
            print(costOfEquity)
            costOfDebt = get_cost_of_debt(stock)
            print(f"Cost of Debt {costOfDebt*100:.2f}%")
            print(costOfDebt)
            taxRate = float(input(f"Enter the tax rate in decimal for {ticker}: "))
            discount_rate = compute_wacc(equityValue, debtValue, costOfEquity, costOfDebt, taxRate)
            high_growth = float(input(f"High growth rate for {ticker}: "))
            low_growth = float(input(f"Terminal growth rate (g) for {ticker}: "))
            years_high = int(input("Years of high growth (typically 5 years): "))
            years_total = int(input("Total projection years (e.g., 10): "))

            dcf_value, enterprise_value, terminal_value = get_dcf_value(
            ticker, discount_rate, high_growth, low_growth, years_high, years_total, taxRate
            )
            sens_df = sensitivity_analysis(
            ticker,
            discount_rate,
            high_growth,
            low_growth,
            years_high,
            years_total,
            taxRate
            )

            print("\nSensitivity Analysis (Value per Share):")
            print(sens_df)

            upside = ((dcf_value - current_price) / current_price) * 100



            print(f"{ticker} computed")
            mos_price = dcf_value * 0.75
            terminal_weight = terminal_value / enterprise_value * 100

            results.append({
            'Ticker': ticker,
            'Price': current_price,
            'DCF Value': round(dcf_value, 2),
            'Upside %': round(upside, 2),
            'MOS Price (25%)': round(mos_price, 2),
            'WACC %': round(discount_rate * 100, 2),
            'Terminal Value % of EV': round(terminal_weight, 1)
            })

        except Exception as e:
            print(f"Skipping {ticker} due to error: {e}")

    df_out = pd.DataFrame(results)
    print(df_out)
    date = dt.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    output_dir = r"C:\Users\delic\OneDrive\Desktop\pythonvaluationmodel\valuations"
    os.makedirs(output_dir, exist_ok=True)
    file_path = os.path.join(output_dir, f"{date}_valuation.csv")
    df_out.to_csv(file_path, index=False)
    print(f"Saved to {file_path}")

if __name__ == "__main__":
    main()