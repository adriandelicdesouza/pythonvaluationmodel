import pandas as pd
def initialize():
    print("WACC Calculation Initialized")
    input("Press Enter to continue...")

    interest_expense = float(input("Enter Total Interest Expense: "))
    t_debt = float(input("Enter Total Debt: "))
    tax_rate = float(input("Enter Tax Rate (as decimal): "))
    rf = float(input("Enter Risk-Free Rate (as decimal): "))
    beta = float(input("Enter Beta: "))
    rm = float(input("Enter Market Rate of Return (as decimal): "))
    price = float(input("Enter Price per Share: "))
    shares_outstanding = float(input("Enter Shares Outstanding: "))

    return interest_expense, t_debt, tax_rate, rf, beta, rm, price, shares_outstanding

def sensitivity_analysis(base_inputs, var_name, var_range):
    results = []
    for var_value in var_range:
        inputs = list(base_inputs)
        if var_name == 'tax_rate':
            inputs[2] = var_value
        elif var_name == 'rf':
            inputs[3] = var_value
        elif var_name == 'beta':
            inputs[4] = var_value
        elif var_name == 'rm':
            inputs[5] = var_value
        elif var_name == 'price':
            inputs[6] = var_value
        elif var_name == 'shares_outstanding':
            inputs[7] = var_value

        wacc_value = wacc(*inputs)
        results.append((var_value, wacc_value))

    df = pd.DataFrame(results, columns=[var_name, 'WACC'])
    print(df)
    return df

def market_value_of_debt(interest_expense, t_debt):
    if t_debt <= 0:
        raise ValueError("Total Debt must be greater than zero.")

    avg_interest_rate = interest_expense / t_debt
    years = 5
    mv_debt = 0

    for t in range(1, years + 1):
        mv_debt += interest_expense / ((1 + avg_interest_rate) ** t)

    mv_debt += t_debt / ((1 + avg_interest_rate) ** years)

    print(f"Market Value of Debt (D) = {mv_debt}")
    return mv_debt


def equity_value(price, shares_outstanding):
    e_val = price * shares_outstanding
    print(f"Market Value of Equity (E) = {e_val}")
    return e_val


def kd(interest_expense, t_debt, tax_rate):
    kd_val = (interest_expense / t_debt) * (1 - tax_rate)
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


def wacc(interest_expense, t_debt, tax_rate, rf, beta, rm, price, shares_outstanding):
    kd_value = kd(interest_expense, t_debt, tax_rate)
    ke_value = ke(rf, beta, rm)
    e_val = equity_value(price, shares_outstanding)

    d_val = market_value_of_debt(interest_expense, t_debt)

    we, wd = cap_structure(e_val, d_val)

    wacc_val = (we * ke_value) + (wd * kd_value)
    print(f"Weighted Average Cost of Capital (WACC) = {wacc_val*100:.2f}%")
    return wacc_val



def main():
    inputs = initialize()
    wacc(*inputs)


if __name__ == "__main__":
    main()
