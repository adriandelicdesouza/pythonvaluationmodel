import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def pull_is(ticker_symbol):
    ticker = yf.Ticker(ticker_symbol)
    income_stmt = ticker.financials

    revenue = income_stmt.loc["Total Revenue"]
    revenue_df = revenue.to_frame(name="Revenue")

    revenue_df["Revenue"] = pd.to_numeric(revenue_df["Revenue"], errors="coerce")
    revenue_df.index = pd.to_datetime(revenue_df.index).year

    revenue_df = revenue_df.dropna()
    revenue_df = revenue_df.sort_index()

    last5 = revenue_df.tail(5).copy()
    return last5

def calc_cagr(last5):
    initial = last5["Revenue"].iloc[0]
    final = last5["Revenue"].iloc[-1]
    years = len(last5) - 1

    if initial <= 0 or years <= 0:
        raise ValueError("Invalid revenue data for CAGR calculation.")

    cagr_value = (final / initial) ** (1 / years) - 1
    return cagr_value

def estimate_decay(last5):
    last5["YoY Growth"] = last5["Revenue"].pct_change()
    yoy_growth = last5["YoY Growth"].dropna()

    x = np.arange(len(yoy_growth))
    y = yoy_growth.values
    slope, intercept = np.polyfit(x, y, 1)
    decay_per_year = slope 
    print(f"Estimated decay per year: {decay_per_year:.4f}")
    return decay_per_year

def project_revenue(last5, cagr_value, decay_per_year, years_ahead=3):
    final_revenue = last5["Revenue"].iloc[-1]
    projections = []
    current_revenue = final_revenue
    decay_Amplitude = 1.1
    for i in range(years_ahead):
        adjusted_cagr = cagr_value - (decay_Amplitude*decay_per_year * i)
        adjusted_cagr = max(0, adjusted_cagr)
        current_revenue *= (1 + adjusted_cagr)
        projections.append(current_revenue)

    future_years = range(last5.index[-1] + 1, last5.index[-1] + 1 + years_ahead)
    projection_df = pd.DataFrame({"Revenue": projections}, index=future_years)
    return projection_df

def combine_data(last5, projection_df):
    return pd.concat([last5, projection_df])

def display_formatting(df):
    df["Revenue ($)"] = df["Revenue"].map(lambda x: f"${x:,.0f}")
    return df

def plot_revenue(df, projection_start_year):

    hist_df = df[df.index < projection_start_year]
    proj_df = df[df.index >= projection_start_year]
    plt.figure(figsize=(10, 6))
    plt.plot(hist_df.index, hist_df["Revenue"], marker='o', label='Historical Revenue')
    plt.plot(proj_df.index, proj_df["Revenue"], marker='s', label='Projected Revenue')
    plt.axvline(x=projection_start_year - 0.5, color='r', linestyle='--', label='Projection Start')
    plt.title('Revenue Projection')
    plt.xlabel('Year')
    plt.ylabel('Revenue ($)')
    plt.xticks(df.index)
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()

def main(ticker_symbol):
    last5 = pull_is(ticker_symbol)

    cagr_value = calc_cagr(last5)
    decay_per_year = estimate_decay(last5)
    projection_df = project_revenue(last5, cagr_value, decay_per_year)

    combined_df = combine_data(last5, projection_df)
    formatted_df = display_formatting(combined_df)
    projection_start_year = projection_df.index[0]
    plot_revenue(combined_df, projection_start_year)

    print("\nHistorical + Projected Revenue:\n")
    print(formatted_df)

if __name__ == "__main__":
    t = input("Enter ticker symbol (e.g., AAPL): ").strip().upper()
    main(t)
