import math as m

def add(x, y):
    return x + y

def subtract(x, y):
    return x - y

def multiply(x, y):
    return x * y

def divide(x, y):
    if y == 0:
        raise ValueError("Cannot divide by zero.")
    return x / y

def FCF(ebit, tax_rate, d_a, capex, cnwc):
    return ebit * (1 - tax_rate) + d_a - capex - cnwc
def FFCF(fcf0, discount_rate, periods):
    return fcf0 * (1 + discount_rate) ** periods

def main():
    print("Init...")
    print("Select Opeartion:")
    print("1. Add")
    print("2. Subtract")
    print("3. Multiply")
    print("4. Divide")
    print("5. Free Cashflow")
    print("6. Future Cashflow")
    choice = input("Enter choice(1/2/3/4/5/6): ")
    if choice == '1':
        num1 = float(input("Enter first number: "))
        num2 = float(input("Enter second number: "))
        print(f"{num1} + {num2} = {add(num1, num2)}")
    elif choice == '2':
        num1 = float(input("Enter first number: "))
        num2 = float(input("Enter second number: "))    
        print(f"{num1} - {num2} = {subtract(num1, num2)}")
    elif choice == '3':
        num1 = float(input("Enter first number: "))
        num2 = float(input("Enter second number: "))
        print(f"{num1} * {num2} = {multiply(num1, num2)}")
    elif choice == '4':
        num1 = float(input("Enter first number: "))
        num2 = float(input("Enter second number: "))
        try:
            result = divide(num1, num2)
            print(f"{num1} / {num2} = {result}")
        except ValueError as e:
            print(e)
    elif choice == '5':
        ebit = float(input("Enter EBIT number: "))
        tax_rate = float(input("Enter tax rate (as decimal): "))
        d_a = float(input("Enter Depreciation and Amortization number: "))
        capex = float(input("Enter Capital Expenditure number: "))
        cnwc = float(input("Enter Change in Net Working Capital number: "))
        print(f"Free Cashflow = {FCF(ebit, tax_rate, d_a, capex, cnwc)}")
    elif choice == '6': 
        fcf0 = float(input("Enter Cashflow number: "))
        fv = float(input("Enter Future Value: "))
        periods = int(input("Enter number of Periods: "))
        pv = fcf0
        discount_rate = (fv/pv)**((1/periods)-1)
        print(f"Future Cashflow = {FFCF(fcf0, discount_rate, periods)}")
    else:
        print("Invalid input")

if __name__ == "__main__":
    main()