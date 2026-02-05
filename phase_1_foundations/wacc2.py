def calculate_kd():
    tax_rate = float(input("Enter the effective tax rate (as a decimal): "))

    st_debt = float(input("Enter the market value of short-term debt: "))
    lt_debt = float(input("Enter the market value of long-term debt: "))
    total_debt = st_debt + lt_debt

    if total_debt == 0:
        print("Total debt cannot be zero.")
        return 0

    cost_st = float(input("Enter the pre-tax cost of short-term debt (as a decimal): "))
    cost_lt = float(input("Enter the pre-tax cost of long-term debt (as a decimal): "))

    weighted_pre_tax_kd = (st_debt / total_debt) * cost_st + (lt_debt / total_debt) * cost_lt
    after_tax_kd = weighted_pre_tax_kd * (1 - tax_rate)

    print(f"Weighted Pre-Tax Cost of Debt = {weighted_pre_tax_kd:.4f}")
    print(f"After-Tax Cost of Debt (kd) = {after_tax_kd:.4f}")

    return after_tax_kd

def calculate_ke():
    rf = float(input("Enter Risk-Free Rate (as decimal): "))
    beta = float(input("Enter Beta: "))
    rm = float(input("Enter Market Rate of Return (as decimal): "))

    ke = rf + beta * (rm - rf)
    print(f"Cost of Equity (ke) = {ke:.4f}")
    return ke

def main():
    kd = calculate_kd()
    ke = calculate_ke()
    print(f"Weighted Average Cost of Capital (WACC) = {kd + ke:.4f}")

if __name__ == "__main__":
    main()
