import streamlit as st

class IncomeTaxCalculator:
    def __init__(self, income, regime="new"):
        self.income = income
        self.regime = regime.lower()
        self.standard_deduction = 75000  # Updated standard deduction
        self.rebate_limit = 1200000  # Rebate applicable up to this income limit
        self.rebate_amount = 25000  # Maximum rebate under the new tax regime

    def calculate_tax_old(self):
        tax = 0
        slabs = [(250000, 0.05), (500000, 0.1), (1000000, 0.2), (float('inf'), 0.3)]
        limit = 250000
        for slab in slabs:
            if self.income > limit:
                taxable = min(self.income - limit, slab[0] - limit)
                tax += taxable * slab[1]
                limit = slab[0]
        return tax

    def calculate_tax_new(self):
        tax = 0
        slabs = [
            (400000, 0.05),
            (800000, 0.1),
            (1200000, 0.15),
            (1600000, 0.2),
            (2000000, 0.25),
            (2400000, 0.3),
            (float('inf'), 0.3)
        ]
        limit = 0
        taxable_income = self.income - self.standard_deduction
        if taxable_income <= 0:
            return 0
        for slab in slabs:
            if taxable_income > limit:
                taxable = min(taxable_income - limit, slab[0] - limit)
                tax += taxable * slab[1]
                limit = slab[0]
        
        # Apply rebate if applicable
        if self.income <= self.rebate_limit:
            tax = max(0, tax - self.rebate_amount)
        
        return tax

    def apply_marginal_relief(self, tax):
        if self.income > self.rebate_limit and self.income <= (self.rebate_limit + self.rebate_amount):
            excess_income = self.income - self.rebate_limit
            tax_reduction = min(tax, excess_income)
            tax -= tax_reduction
        return tax

    def calculate_tax(self):
        if self.regime == "old":
            tax = self.calculate_tax_old()
        else:
            tax = self.calculate_tax_new()
        return self.apply_marginal_relief(tax)


# Streamlit UI
st.title("Income Tax Calculator - FY 2025-26")
st.subheader("Calculate your tax under the new and old regimes")

income = st.number_input("Enter your annual income (₹)", min_value=0, step=1000)
regime = st.radio("Choose your tax regime:", ["New", "Old"])

if st.button("Calculate Tax"):
    calculator = IncomeTaxCalculator(income, regime.lower())
    tax_amount = calculator.calculate_tax()
    st.success(f"Your tax liability under the {regime} regime is: ₹{tax_amount:.2f}")
