import pandas as pd

class MerchantRiskEncoder:
    def __init__(self, alpha_category: float = 20.0, alpha_group: float = 50.0):
        self.alpha_category = alpha_category
        self.alpha_group = alpha_group
        self.mean_default_rate_ = None
        self.merchant_category_risk_ = None
        self.merchant_group_risk_ = None

    def _fit_smoothed_rate(self, series: pd.Series, y: pd.Series, alpha: float) -> pd.Series:
        stats = pd.concat([series, y], axis=1).groupby(series.name)[y.name].agg(["mean", "count"])
        stats["smoothed_rate"] = (
            stats["count"] * stats["mean"] + alpha * self.mean_default_rate_
        ) / (stats["count"] + alpha)
        return stats["smoothed_rate"]

    def fit(self, X: pd.DataFrame, y: pd.Series):
        self.mean_default_rate_ = y.mean()

        self.merchant_category_risk_ = self._fit_smoothed_rate(
            X["merchant_category"], y, self.alpha_category
        )

        self.merchant_group_risk_ = self._fit_smoothed_rate(
            X["merchant_group"], y, self.alpha_group
        )

        return self

    def transform(self, X: pd.DataFrame) -> pd.DataFrame:
        X = X.copy()

        X["merchant_default_rate"] = X["merchant_category"].map(self.merchant_category_risk_)
        X["merchant_default_rate"] = X["merchant_default_rate"].fillna(self.mean_default_rate_)

        X["merchant_group_default_rate"] = X["merchant_group"].map(self.merchant_group_risk_)
        X["merchant_group_default_rate"] = X["merchant_group_default_rate"].fillna(self.mean_default_rate_)

        X = X.drop(columns=["merchant_category", "merchant_group"], errors="ignore")

        return X