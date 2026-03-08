import joblib
import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_PATH = BASE_DIR / "models" / "credit_logistic_bundle.pkl"

bundle = joblib.load(MODEL_PATH)

model = bundle["model"]
basic_transforms = bundle["basic transforms"]
merchant_encoder = bundle["merchant_encoder"]
woe_processor = bundle["woe_processor"]
threshold = bundle["threshold"]
features = bundle["features"]

def predict_credit_risk(input: dict) -> dict:

    df = pd.DataFrame([input])

    df = basic_transforms(df)

    df = merchant_encoder.transform(df)

    df = woe_processor.transform(df)

    for col in features:
        if col not in df.columns:
            df[col] = 0.0

    df = df[features]

    pd_1 = float(model.predict_proba(df)[0, 1])

    pred_class = int(pd_1 >= threshold)
    #score = round((1 - pd_1) * 1000, 2)

    if pd_1 < 0.1:
        risk_band = "low"
    elif pd_1 < 0.3:
        risk_band = "medium"
    else:
        risk_band = "high"

    return {
        "pd": round(pd_1, 6),
        #"score": score,
        "risk_band": risk_band,
        "prediction": pred_class,
        "threshold": threshold,
    }

