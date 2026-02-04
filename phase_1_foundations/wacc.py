def initialize():
    print("WACC Calculation Initialized")
    input("Press Enter to continue...")

    t_interest_expense = float(input("Enter Total Interest Expense: "))
    t_debt = float(input("Enter Total Debt: "))
    tax_rate = float(input("Enter Tax Rate (as decimal): "))
    rf = float(input("Enter Risk-Free Rate (as decimal): "))
    beta = float(input("Enter Beta: "))
    rm = float(input("Enter Market Rate of Return (as decimal): "))
    price = float(input("Enter Price per Share: "))
    shares_outstanding = float(input("Enter Shares Outstanding: "))
    d = float(input("Enter Market Value of Debt: "))

    return t_interest_expense, t_debt, tax_rate, rf, beta, rm, price, shares_outstanding, d


def equity_value(price, shares_outstanding):
    e_val = price * shares_outstanding
    print(f"Market Value of Equity (E) = {e_val}")
    return e_val


def kd(t_interest_expense, t_debt, tax_rate):
    kd_val = (t_interest_expense / t_debt) * (1 - tax_rate)
    print(f"After-Tax Cost of Debt (kd) = {kd_val}")
    return kd_val


def ke(rf, beta, rm):
    ke_val = rf + beta * (rm - rf)
    print(f"Cost of Equity (ke) = {ke_val}")
    return ke_val


def cap_structure(e, d):
    v = e + d
    we = e / v
    wd = d / v
    print(f"Weight of Equity (we) = {we}")
    print(f"Weight of Debt (wd) = {wd}")
    return we, wd


def wacc(t_interest_expense, t_debt, tax_rate, rf, beta, rm, price, shares_outstanding, d):
    kd_value = kd(t_interest_expense, t_debt, tax_rate)
    ke_value = ke(rf, beta, rm)
    e_val = equity_value(price, shares_outstanding)
    we, wd = cap_structure(e_val, d)

    wacc_val = (we * ke_value) + (wd * kd_value)
    print(f"Weighted Average Cost of Capital (WACC) = {wacc_val*100:.2f}%")
    return wacc_val


def main():
    inputs = initialize()
    wacc(*inputs)


if __name__ == "__main__":
    main()
