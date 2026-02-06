def calculate_kd():
    tax_rate = float(input("Enter the effective tax rate (as a decimal): "))

    st_debt = float(input("Enter the market value of short-term debt: "))
    lt_debt = float(input("Enter the market value of long-term debt: "))
    total_debt = st_debt + lt_debt

    if total_debt == 0:
        print("Total debt cannot be zero.")
        return 0, 0

    cost_st = float(input("Enter the pre-tax cost of short-term debt (as a decimal): "))
    cost_lt = float(input("Enter the pre-tax cost of long-term debt (as a decimal): "))

    weighted_pre_tax_kd = (st_debt / total_debt) * cost_st + (lt_debt / total_debt) * cost_lt
    after_tax_kd = weighted_pre_tax_kd * (1 - tax_rate)

    print(f"Weighted Pre-Tax Cost of Debt = {weighted_pre_tax_kd:.4f}")
    print(f"After-Tax Cost of Debt (kd) = {after_tax_kd:.4f}")

    return after_tax_kd, total_debt


def calculate_ke():
    rf = float(input("Enter Risk-Free Rate (as decimal): "))
    beta = float(input("Enter Beta: "))
    rm = float(input("Enter Market Rate of Return (as decimal): "))

    ke = rf + beta * (rm - rf)
    print(f"Cost of Equity (ke) = {ke:.4f}")
    return ke

def calculate_equity_value():
    shares_outstanding = float(input("Enter the number of shares outstanding: "))
    stock_price = float(input("Enter the current stock price: "))

    equity_value = shares_outstanding * stock_price
    print(f"Market Value of Equity = {equity_value:.2f}")
    return equity_value
def main():
    kd, total_debt = calculate_kd()
    ke = calculate_ke()

    equity_value = calculate_equity_value()
    total_value = equity_value + total_debt

    we = equity_value / total_value
    wd = total_debt / total_value

    wacc = we * ke + wd * kd

    print(f"Weight of Equity = {we:.4f}")
    print(f"Weight of Debt = {wd:.4f}")
    print(f"Weighted Average Cost of Capital (WACC) = {wacc*100:.2f}%")


if __name__ == "__main__":
    main()
