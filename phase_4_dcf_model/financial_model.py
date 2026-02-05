from phase_3_financial_statements import revenue_projection as rp
import yfinance as yf

t = input("Enter the ticker symbol (e.g., AAPL): ").strip().upper()
pull_is = rp.pull_is(t)
name = yf.Ticker(t).info['shortName']

def main(t):
    print(f"Projecting {name}...")
    rp.main(t)
    print(f"CAGR : {rp.calc_cagr(pull_is)*100:.2f}%")


if __name__ == "__main__":
    main(t)
