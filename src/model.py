# model.py
import os
import joblib
import numpy as np
import pandas as pd

from sklearn.model_selection import train_test_split
#Splits data into training and test sets.
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
#Model evaluation metrics.
from sklearn.compose import ColumnTransformer
#Allows preprocessing different column types differently.
from sklearn.pipeline import Pipeline
#Chains preprocessing + model into one object.
from sklearn.preprocessing import OneHotEncoder, StandardScaler
#Converts categorical variables into numeric dummy variables.
#Standardizes numeric features (mean = 0, std = 1).
from sklearn.linear_model import LinearRegression
#The model itself.
from db_manager import query_all  
#Custom function (from your previous script) — fetches cleaned data from SQLite database.

#Paths 
MODELS_DIR = "models"
MODEL_PATH = os.path.join(MODELS_DIR, "price_linear_pipeline.joblib")

#  Feature schema (DEMO version)
# For the demo, we train on exactly the fields you collect in the CLI:
CATEGORICAL_FEATURES = ["fuel_type"]
NUMERIC_FEATURES = ["mfg_year", "km", "hp", "doors", "automatic"]
TARGET = "price"
ALL_FEATURES = CATEGORICAL_FEATURES + NUMERIC_FEATURES


def build_preprocessor() -> ColumnTransformer:
    """One-hot encode categoricals; scale numeric features; dense output."""
    # Dense output for encoder across sklearn versions
    
    ohe = OneHotEncoder(handle_unknown="ignore", sparse_output=False)
        #prevents errors for unseen categories during prediction.
    

    preprocessor = ColumnTransformer(
        transformers=[
            ("cat", ohe, CATEGORICAL_FEATURES),
            ("num", StandardScaler(), NUMERIC_FEATURES),
        ],
        remainder="drop"
    )
    return preprocessor


def build_pipeline() -> Pipeline:
    """Preprocessing + Linear Regression in one pipeline."""
    return Pipeline(steps=[
        ("preprocessor", build_preprocessor()),
        ("model", LinearRegression())
    ])


# ------------------------------ Data -----------------------------------------
def load_training_data() -> pd.DataFrame:
    """
    Pull the cleaned data from SQLite (inserted earlier by db_manager).
    Validates required columns exist.
    """
    df = query_all()
    needed = set(ALL_FEATURES + [TARGET])
    missing = needed - set(df.columns)
    if missing:
        raise ValueError(f"Missing required columns in DB DataFrame: {missing}")
    return df


# ----------------------------- Training --------------------------------------
def train_and_evaluate(save_path: str = MODEL_PATH) -> dict:
    """Train pipeline, evaluate on holdout, save the fitted pipeline."""
    os.makedirs(MODELS_DIR, exist_ok=True)

    df = load_training_data()
    X = df[ALL_FEATURES]
    y = df[TARGET]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    pipe = build_pipeline()
    pipe.fit(X_train, y_train)

    preds = pipe.predict(X_test)

    mae = mean_absolute_error(y_test, preds)
    rmse = np.sqrt(mean_squared_error(y_test, preds))  # version-proof RMSE
    r2 = r2_score(y_test, preds)

    joblib.dump(pipe, save_path)

    # Optional: show top coefficients (interpretable insight)
    coef_table = []
    try:
        pre: ColumnTransformer = pipe.named_steps["preprocessor"]
        feature_names = list(pre.get_feature_names_out())
        coefs = pipe.named_steps["model"].coef_  # key is "model" in this pipeline
        coef_table = sorted(
            zip(feature_names, coefs),
            key=lambda t: abs(t[1]),
            reverse=True
        )[:10]
    except Exception:
        pass

    report = {
        "samples_train": len(X_train),
        "samples_test": len(X_test),
        "MAE": round(mae, 2),
        "RMSE": round(rmse, 2),
        "R2": round(r2, 3),
        "model_path": save_path,
        "top_coefficients": coef_table
    }

    print("\n=== Model Evaluation ===")
    for k, v in report.items():
        if k != "top_coefficients":
            print(f"{k}: {v}")
    if coef_table:
        print("\nTop 10 coefficient magnitudes (feature, weight):")
        for name, w in coef_table:
            print(f"  {name:35s} {w:+.4f}")

    return report


# ---------------------------- Inference --------------------------------------
def load_pipeline(path: str = MODEL_PATH):
    if not os.path.exists(path):
        raise FileNotFoundError(
            f"Trained pipeline not found at '{path}'. Train the model first."
        )
    return joblib.load(path)


def predict_price_from_dict(features: dict, path: str = MODEL_PATH) -> float:
    """
    Predict price for a single record.
    "features" must include keys in CATEGORICAL_FEATURES + NUMERIC_FEATURES.
    Unknown categorical levels are handled by the encoder.
    """
    pipe = load_pipeline(path)
    # Build a 1-row DataFrame with exact expected columns; fill missing with NaN
    row = {**{c: np.nan for c in ALL_FEATURES}, **features}
    X = pd.DataFrame([row], columns=ALL_FEATURES)
    pred = pipe.predict(X)[0]
    return float(round(pred, 2))


def example_payload() -> dict:
    """A minimal, ready-to-use template for demo/CLI input."""
    return {
        "fuel_type": "Petrol",  # categorical
        "mfg_year": 2002,
        "km": 65000,
        "hp": 90,
        "doors": 4,
        "automatic": 0
    }


# --------------------------- Script entrypoint -------------------------------
if __name__ == "__main__":
    # 1) Train + evaluate + save
    report = train_and_evaluate()

    # 2) Quick sanity-check prediction
    sample = example_payload()
    y_hat = predict_price_from_dict(sample)
    print(f"\nPrediction for sample payload: €{y_hat}")
