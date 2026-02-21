

import sys
import time

import pandas as pd
import joblib
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, r2_score



CLEAN_DATA_PATH   = "clean_salary_dataset.csv"
MODEL_OUTPUT_PATH = "salary_predictor.pkl"
COLS_OUTPUT_PATH  = "model_columns.pkl"

FEATURE_COLUMNS   = ["experience_level", "job_title", "remote_ratio"]
TARGET_COLUMN     = "salary_in_usd"

TEST_SIZE         = 0.20
RANDOM_STATE      = 42


# ==============================================================================
# HELPERS
# ==============================================================================

def section(title: str) -> None:
    """Print a clearly visible section header to the terminal."""
    print(f"\n{'=' * 70}")
    print(f"  {title}")
    print(f"{'=' * 70}")


def step(number: int, message: str) -> None:
    """Print a numbered progress step."""
    print(f"\n[{number}/6] {message}")


# ==============================================================================
# MAIN PIPELINE
# ==============================================================================

def main() -> None:

    print("\n" + "=" * 70)
    print("  CareerScout | Model Training Pipeline")
    print("=" * 70)

    # ── STEP 1 : Loading Data ────────────────────────────────────────────────────
    step(1, f"Loading clean dataset from '{CLEAN_DATA_PATH}' ...")

    try:
        df = pd.read_csv(CLEAN_DATA_PATH)
    except FileNotFoundError:
        print(f"\n  ❌  ERROR: '{CLEAN_DATA_PATH}' not found.")
        print("       Run 1_data_prep_and_eda.py first to generate it.")
        sys.exit(1)

    print(f"     Rows loaded : {len(df):,}")
    print(f"     Columns     : {list(df.columns)}")


    # ── STEP 2 : Selecting Features & Target ────────────────────────────────────
    step(2, "Selecting features and target ...")

    X = df[FEATURE_COLUMNS].copy()
    y = df[TARGET_COLUMN].copy()

    print(f"     Features (X) : {FEATURE_COLUMNS}")
    print(f"     Target   (y) : '{TARGET_COLUMN}'")
    print(f"     X shape      : {X.shape}")
    print(f"     y shape      : {y.shape}")
    print(f"\n     Unique values per feature:")
    for col in FEATURE_COLUMNS:
        print(f"       • {col:<20} {X[col].nunique():>4} unique values")


    # ── STEP 3 : Encoding Categorical Columns ───────────────────────────────────
    step(3, "Encoding categorical features with pd.get_dummies ...")

    X = pd.get_dummies(X, drop_first=True)

    print(f"     Encoded feature matrix shape : {X.shape}")
    print(f"     Total columns after encoding : {X.shape[1]}")
   


    # ── STEP 4 : Save Encoded Column Names ───────────────────────────────────
    step(4, f"Saving encoded column names → '{COLS_OUTPUT_PATH}' ...")

    model_columns = list(X.columns)
    joblib.dump(model_columns, COLS_OUTPUT_PATH)

    
    print(f"     ✓ {len(model_columns)} column names saved.")
    print(f"       Sample columns : {model_columns[:5]} ...")


    # ── STEP 5 : Train / Test Split ───────────────────────────────────────────
    step(5, f"Splitting data  ({int((1-TEST_SIZE)*100)}% train / {int(TEST_SIZE*100)}% test, random_state={RANDOM_STATE}) ...")

    X_train, X_test, y_train, y_test = train_test_split(
        X, y,
        test_size=TEST_SIZE,
        random_state=RANDOM_STATE
    )

    print(f"     Training samples : {len(X_train):,}")
    print(f"     Testing  samples : {len(X_test):,}")


    # ── STEP 6 : Training Model ──────────────────────────────────────────────────
    step(6, "Training RandomForestRegressor  (this may take 30–60 seconds) ...")

    model = RandomForestRegressor(
        n_estimators=100,       # 100 decision trees in the forest
        random_state=RANDOM_STATE,
        n_jobs=-1               # use all available CPU cores
    )

    start = time.time()
    model.fit(X_train, y_train)
    elapsed = time.time() - start

    print(f"     ✓ Training complete in {elapsed:.1f}s")


    # ── EVALUATING : MAE & R² ───────────────────────────────────────────────────
    section("Model Evaluation Results")

    y_pred = model.predict(X_test)

    mae = mean_absolute_error(y_test, y_pred)
    r2  = r2_score(y_test, y_pred)

    print(f"\n  Mean Absolute Error (MAE) : ${mae:>12,.2f}")
    print(f"  R² Score                  : {r2:>15.4f}")

    # Interpreting the scores for the reader
    print("\n  What this means:")
    print(f"  ┌─ MAE  → On average, predictions are off by ~${mae:,.0f}")
    print(f"  └─ R²   → The model explains {r2*100:.1f}% of salary variance")

    # Feature importance – top 10 most influential features
    importances = (
        pd.Series(model.feature_importances_, index=model_columns)
        .sort_values(ascending=False)
        .head(10)
    )
    print("\n  Top 10 Most Influential Features:")
    for feat, score in importances.items():
        bar = "█" * int(score * 300)
        print(f"    {feat:<45} {score:.4f}  {bar}")


    # ── SAVING MODEL ────────────────────────────────────────────────────────────
    section("Saving Artefacts")

    joblib.dump(model, MODEL_OUTPUT_PATH)
    print(f"\n  ✓ Trained model saved  → '{MODEL_OUTPUT_PATH}'")
    print(f"  ✓ Column names saved   → '{COLS_OUTPUT_PATH}'")

    print(f"""
  ┌─────────────────────────────────────────────────────────────┐
  │  Pipeline complete! Two files are ready for the app:        │
  │                                                             │
  │    📦  {MODEL_OUTPUT_PATH:<51}│
  │    📋  {COLS_OUTPUT_PATH:<51}│
  │                                                             │
  │  Next step → build the Streamlit app (app.py)               │
  └─────────────────────────────────────────────────────────────┘
""")


# ==============================================================================
# ENTRY POINT
# ==============================================================================

if __name__ == "__main__":
    main()