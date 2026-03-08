import numpy as np
import pandas as pd


def calculate_woe_iv(df: pd.DataFrame, feature_col: str, target_col: str, eps: float = 1e-6):

    temp = df[[feature_col, target_col]].copy()
    temp[feature_col] = temp[feature_col].astype("object").fillna("MISSING")

    grouped = temp.groupby(feature_col, dropna=False, observed=False)[target_col].agg(["count", "sum"])
    grouped.columns = ["total", "bad"]
    grouped["good"] = grouped["total"] - grouped["bad"]

    total_good = grouped["good"].sum()
    total_bad = grouped["bad"].sum()

    grouped["dist_good"] = grouped["good"] / max(total_good, eps)
    grouped["dist_bad"] = grouped["bad"] / max(total_bad, eps)

    grouped["woe"] = np.log((grouped["dist_good"] + eps) / (grouped["dist_bad"] + eps))
    grouped["iv_component"] = (grouped["dist_good"] - grouped["dist_bad"]) * grouped["woe"]

    return grouped["woe"].to_dict(), grouped["iv_component"].sum()


class WOEProcessor:
    def __init__(self, num_cols, max_bins: int = 10, min_unique: int = 2):
        self.num_cols = num_cols
        self.max_bins = max_bins
        self.min_unique = min_unique

        self.bin_edges_dict = {}
        self.woe_dict = {}
        self.iv_dict = {}
        self.skipped_cols = {}

    def _make_single_bin_edges(self, x: pd.Series):
        x_non_null = x.dropna()

        if x_non_null.empty:
            return np.array([-np.inf, np.inf], dtype=float)

        val_min = x_non_null.min()
        val_max = x_non_null.max()

        if val_min == val_max:
            return np.array([-np.inf, np.inf], dtype=float)

        return np.array([-np.inf, val_max, np.inf], dtype=float)

    def fit(self, X: pd.DataFrame, y: pd.Series):
        X = X.copy()
        y = y.copy()

        for col in self.num_cols:
            x = X[col]

            nunique = x.nunique(dropna=True)

            if nunique < self.min_unique:
                bin_edges = self._make_single_bin_edges(x)
                self.skipped_cols[col] = f"if only few unique values ({nunique})"
            else:
                q = min(self.max_bins, nunique)

                try:
                    _, bin_edges = pd.qcut(
                        x,
                        q=q,
                        duplicates="drop",
                        retbins=True
                    )

                    if len(bin_edges) < 2:
                        bin_edges = self._make_single_bin_edges(x)
                        self.skipped_cols[col] = "qcut returned invalid bin edges check"

                except Exception as e:
                    bin_edges = self._make_single_bin_edges(x)
                    self.skipped_cols[col] = f"qcut failed: {e}"

            bin_edges = np.asarray(bin_edges, dtype=float)
            bin_edges[0] = -np.inf
            bin_edges[-1] = np.inf

            self.bin_edges_dict[col] = bin_edges

            bin_col = f"{col}_bin"
            X[bin_col] = pd.cut(
                x,
                bins=bin_edges,
                include_lowest=True,
                duplicates="drop"
            )

            df_temp = pd.concat([X[bin_col], y.rename("target")], axis=1)
            woe_map, iv = calculate_woe_iv(df_temp, bin_col, "target")

            self.woe_dict[col] = woe_map
            self.iv_dict[col] = iv

        return self

    def transform(self, X: pd.DataFrame) -> pd.DataFrame:
        X = X.copy()

        for col in self.num_cols:
            bin_col = f"{col}_bin"
            woe_col = f"{col}_woe"

            X[bin_col] = pd.cut(
                X[col],
                bins=self.bin_edges_dict[col],
                include_lowest=True,
                duplicates="drop"
            )

            X[woe_col] = pd.to_numeric(
                X[bin_col].map(self.woe_dict[col]),
                errors="coerce"
            ).fillna(0.0)

        return X

    def fit_transform(self, X: pd.DataFrame, y: pd.Series) -> pd.DataFrame:
        return self.fit(X, y).transform(X)