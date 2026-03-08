import streamlit as st
import numpy as np

st.set_page_config(page_title="Credit Risk App", layout="wide")
st.title("Credit Risk Prediction")

t1, t2 = st.columns((0.05,1)) 

t1.image('image/image.png', width = 220)
st.divider()

logo = 'image/image.png'
st.logo(logo, size="medium", link=None, icon_image=None)

a1,a2,a3 = st.columns((1.,0.1,1))


loan_amount = a1.number_input("Loan amount *", min_value=0.0, value=0.0)
existing_klarna_debt = a1.number_input("Existing Klarna debt", min_value=0.0, value=0.0)
card_expiry_month=a1.selectbox("Card expiry month", [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12])
card_expiry_year=a1.selectbox("Card expiry year", np.arange(2026, 2035))
num_active_loans = a1.number_input("Number of active loans", min_value=0, value=0)
days_since_first_loan = a1.number_input("Days since first loan", min_value=0, value=0)
new_exposure_7d = a1.number_input("New exposure in the last 7 days", min_value=0.0, value=0.0)
new_exposure_14d= a1.number_input("New exposure in the last 14 days", min_value=0.0, value=0.0)
num_confirmed_payments_3m = a1.number_input("Number of confirmed payments in the last 3 months", min_value=0, value=0)
num_confirmed_payments_6m= a1.number_input("Number of confirmed payments in the last 6 months", min_value=0, value=0)
num_failed_payments_3m = a3.number_input("Number of failed payments in the last 3 months", min_value=0, value=0)
num_failed_payments_6m  = a3.number_input("Number of failed payments in the last 6 months", min_value=0, value=0)
num_failed_payments_1y = a3.number_input("Number of failed payments in the last 1 year", min_value=0, value=0)
amount_repaid_14d = a3.number_input("Amount repaid in the last 14 days", min_value=0.0, value=0.0)
amount_repaid_1m = a3.number_input("Amount repaid in the last 1 month", min_value=0.0, value=0.0)
amount_repaid_3m = a3.number_input("Amount repaid in the last 3 months", min_value=0.0, value=0.0)
amount_repaid_6m= a3.number_input("Amount repaid in the last 6 months", min_value=0.0, value=0.0)
amount_repaid_1y= a3.number_input("Amount repaid in the last 1 year", min_value=0.0, value=0.0)
merchant_group = a3.selectbox("Merchant group", ["Group A", "Group B", "Group C"])
merchant_category = a3.selectbox("Merchant category",["Group A", "Group B", "Group C"])

st.divider()

a1,a2,a3 = st.columns((0.5,0.1,1))
a1.button("Predict", type="primary", use_container_width=True)