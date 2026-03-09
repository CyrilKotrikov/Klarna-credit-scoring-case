import numpy as np
import pandas as pd


def transform_basic(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    # new customer
    df["is_new_customer"] = (df["days_since_first_loan"] == -1).astype(int)
    df["days_since_first_loan"] = df["days_since_first_loan"].clip(lower=0)

    # existing_klarna_debt
    df["existing_klarna_debt_missing"] = df["existing_klarna_debt"].isna().astype(int)
    df["existing_klarna_debt"] = df["existing_klarna_debt"].fillna(0)
    df["existing_klarna_debt"] = df["existing_klarna_debt"].clip(lower=0)

    # dates
    df["loan_issue_date"] = pd.to_datetime(df["loan_issue_date"])
    df["loan_dayofweek"] = df["loan_issue_date"].dt.dayofweek + 1
    df["loan_month"] = df["loan_issue_date"].dt.month
    df["loan_week"] = df["loan_issue_date"].dt.isocalendar().week.astype(int)

    # card expiry
    df["months_to_expiry"] = (
        (df["card_expiry_year"] - df["loan_issue_date"].dt.year) * 12
        + (df["card_expiry_month"] - df["loan_issue_date"].dt.month)
    )
    df["card_expiry_risk"] = (df["months_to_expiry"] <= 3).astype(int)

    df = df.drop(columns=["card_expiry_year", "card_expiry_month", "months_to_expiry"], errors="ignore")

    # engineered features
    df["debt_to_loan_ratio"] = df["existing_klarna_debt"] / (df["loan_amount"] + 1)
    df["exposure_growth"] = df["new_exposure_14d"] - df["new_exposure_7d"]

    df["failed_payment_ratio_3m"] = (
        df["num_failed_payments_3m"] / (df["num_confirmed_payments_3m"] + 1)
    )
    df["failed_payment_ratio_6m"] = (
        df["num_failed_payments_6m"] / (df["num_confirmed_payments_6m"] + 1)
    )

    df["payment_reliability"] = (
        df["num_confirmed_payments_6m"] - df["num_failed_payments_6m"]
    )

    df["repayment_speed"] = df["amount_repaid_1m"] / (df["loan_amount"] + 1)
    df["repayment_ratio_6m"] = df["amount_repaid_6m"] / (df["loan_amount"] + 1)
    df["loan_intensity"] = df["num_active_loans"] / (df["days_since_first_loan"] + 1)

    # cleanup
    df = df.drop(columns=["loan_id"], errors="ignore")
    df = df.drop_duplicates(keep=False)

    return df