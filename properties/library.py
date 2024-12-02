import numpy as np

class HomeLoan:
    def __init__(self) -> None:
        pass

    def calculate_emi(self, loan_amount, annual_rate, tenure_years):
        monthly_rate = annual_rate / (12 * 100)
        tenure_months = tenure_years * 12
        emi = (loan_amount * monthly_rate * np.power(1 + monthly_rate, tenure_months)) / (np.power(1 + monthly_rate, tenure_months) - 1)
        return emi

    def calculate_eligibility(self, monthly_income, monthly_expenses, interest_rate, tenure_years):
        net_monthly_income = monthly_income - monthly_expenses
        max_emi = net_monthly_income * 0.5
        monthly_rate = interest_rate / (12 * 100)
        tenure_months = tenure_years * 12
        if monthly_rate > 0:
            max_loan_amount = max_emi * ((1 + monthly_rate) ** tenure_months - 1) / (monthly_rate * (1 + monthly_rate) ** tenure_months)
        else:
            max_loan_amount = max_emi * tenure_months
        return max_loan_amount, monthly_income, monthly_expenses, interest_rate, tenure_years

    def calculate_affordability(self, monthly_income, monthly_expenses, interest_rate, tenure_years):
        net_monthly_income = monthly_income - monthly_expenses
        max_emi = net_monthly_income * 0.5
        monthly_rate = interest_rate / (12 * 100)  # Convert annual interest rate to monthly
        tenure_months = tenure_years * 12
        if monthly_rate > 0:
            max_property_price = max_emi * ((1 + monthly_rate) ** tenure_months - 1) / (monthly_rate * (1 + monthly_rate) ** tenure_months)
        else:
            max_property_price = max_emi * tenure_months  # In case of 0% interest rate
        return max_property_price, monthly_income, monthly_expenses, interest_rate, tenure_years

    def calculate_total_payable(self, tenure_years, annual_rate, loan_amount):
        monthly_rate = annual_rate / (12 * 100)
        tenure_months = tenure_years * 12
        emi = (loan_amount * monthly_rate * ((1 + monthly_rate) ** tenure_months)) / (((1 + monthly_rate) ** tenure_months) - 1)
        total_payable = emi * tenure_months
        total_interest = total_payable - loan_amount
        return total_payable, total_interest, emi, tenure_years, annual_rate, loan_amount