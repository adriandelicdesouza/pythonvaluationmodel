print('Compound Interest Calculator')
principal = float(input("Intial Investment ($): "))
rate_percent = float(input("Expected Annual Return (%): "))
Years = int(input("Years Invested: "))
rate_decimal = rate_percent / 100
future_value = principal * (1+rate_decimal) ** Years

print("\nResults:")
print("Future Value: ", round(future_value,2))
print("Profit: ",round(future_value - principal,2))
