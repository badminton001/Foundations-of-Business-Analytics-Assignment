"""
scripts/4_1_preprocessing.py
Step 4.1: Train-Test Split + Leak-Free Encoding & Scaling
"""

import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

# ── Paths ────────────────────────────────────────────────────────────────────
BASE       = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_IN    = os.path.join(BASE, "data", "StudentPerformanceFactors_cleaned.csv")
DATA_OUT   = os.path.join(BASE, "data", "processed")
os.makedirs(DATA_OUT, exist_ok=True)

# ── Load ──────────────────────────────────────────────────────────────────────
df = pd.read_csv(DATA_IN)
print(f"Loaded: {df.shape}")

# ── Define targets ────────────────────────────────────────────────────────────
y_reg = df["Exam_Score"].values.astype(float)          # Regression target

MEAN_SCORE = df["Exam_Score"].mean()                   # 67.24 (computed on full set before split is OK
                                                        # because the threshold is fixed, not a statistic
                                                        # fitted on data — analogous to a business rule)
y_clf = (df["Exam_Score"] >= MEAN_SCORE).astype(int).values   # 1 = Above Average, 0 = Below Average
print(f"Classification threshold (mean): {MEAN_SCORE:.2f}")
print(f"  Above average: {y_clf.sum()} ({y_clf.mean()*100:.1f}%)")
print(f"  Below average: {(1-y_clf).sum()} ({(1-y_clf).mean()*100:.1f}%)")

# ── Feature matrix (drop target) ─────────────────────────────────────────────
X_raw = df.drop(columns=["Exam_Score"])

# ── Ordinal maps (domain-driven) ─────────────────────────────────────────────
ORDINAL_MAPS = {
    "Parental_Involvement":   {"Low": 0, "Medium": 1, "High": 2},
    "Access_to_Resources":    {"Low": 0, "Medium": 1, "High": 2},
    "Motivation_Level":       {"Low": 0, "Medium": 1, "High": 2},
    "Family_Income":          {"Low": 0, "Medium": 1, "High": 2},
    "Teacher_Quality":        {"Low": 0, "Medium": 1, "High": 2},       # Unknown handled below
    "Parental_Education_Level": {"High School": 0, "College": 1, "Postgraduate": 2},  # Unknown → mode
    "Distance_from_Home":     {"Far": 0, "Moderate": 1, "Near": 2},     # Unknown → mode
    "School_Type":            {"Public": 0, "Private": 1},
    "Peer_Influence":         {"Negative": 0, "Neutral": 1, "Positive": 2},
}
BINARY_MAPS = {
    "Extracurricular_Activities": {"No": 0, "Yes": 1},
    "Internet_Access":            {"No": 0, "Yes": 1},
    "Learning_Disabilities":      {"No": 0, "Yes": 1},
    "Gender":                     {"Male": 0, "Female": 1},
}

# ── Train / Test split FIRST (80 / 20) ───────────────────────────────────────
X_train_raw, X_test_raw, y_train_reg, y_test_reg, y_train_clf, y_test_clf = train_test_split(
    X_raw, y_reg, y_clf,
    test_size=0.20, random_state=42,
    stratify=y_clf,   # keep class ratio identical in both splits
)
print(f"\nTrain: {len(X_train_raw)}  |  Test: {len(X_test_raw)}")

# ── Encode (fit only on train, then transform both) ───────────────────────────
def encode_split(X_tr: pd.DataFrame, X_te: pd.DataFrame):
    X_tr = X_tr.copy()
    X_te = X_te.copy()

    # Unknown → NaN, then fill with TRAIN mode BEFORE encoding
    for col in ["Teacher_Quality", "Parental_Education_Level", "Distance_from_Home"]:
        X_tr[col] = X_tr[col].replace("Unknown", np.nan)
        X_te[col] = X_te[col].replace("Unknown", np.nan)
        train_mode = X_tr[col].mode()[0]      # only from train
        X_tr[col] = X_tr[col].fillna(train_mode)
        X_te[col] = X_te[col].fillna(train_mode)

    # Ordinal encoding
    for col, mapping in ORDINAL_MAPS.items():
        X_tr[col] = X_tr[col].map(mapping)
        X_te[col] = X_te[col].map(mapping)

    # Binary encoding
    for col, mapping in BINARY_MAPS.items():
        X_tr[col] = X_tr[col].map(mapping)
        X_te[col] = X_te[col].map(mapping)

    return X_tr, X_te

X_train_enc, X_test_enc = encode_split(X_train_raw, X_test_raw)

# Sanity check
assert X_train_enc.isnull().sum().sum() == 0, "NaN in train!"
assert X_test_enc.isnull().sum().sum()  == 0, "NaN in test!"
print("\nEncoding complete. No NaN values.")

# ── Standardise (fit scaler on TRAIN only) ────────────────────────────────────
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train_enc)
X_test_scaled  = scaler.transform(X_test_enc)
print("Scaling complete (fitted on train only — no leakage).")

# ── Save feature names ────────────────────────────────────────────────────────
feature_names = list(X_train_enc.columns)
print(f"\nFeatures ({len(feature_names)}): {feature_names}")

# ── Persist arrays & metadata ─────────────────────────────────────────────────
np.save(os.path.join(DATA_OUT, "X_train_scaled.npy"),  X_train_scaled)
np.save(os.path.join(DATA_OUT, "X_test_scaled.npy"),   X_test_scaled)
np.save(os.path.join(DATA_OUT, "y_train_reg.npy"),     y_train_reg)
np.save(os.path.join(DATA_OUT, "y_test_reg.npy"),      y_test_reg)
np.save(os.path.join(DATA_OUT, "y_train_clf.npy"),     y_train_clf)
np.save(os.path.join(DATA_OUT, "y_test_clf.npy"),      y_test_clf)

import json
meta = {
    "feature_names":           feature_names,
    "classification_threshold": round(float(MEAN_SCORE), 4),
    "class_labels":            {0: "Below Average", 1: "Above Average"},
    "n_train":                 int(len(X_train_scaled)),
    "n_test":                  int(len(X_test_scaled)),
}
with open(os.path.join(DATA_OUT, "meta.json"), "w") as f:
    json.dump(meta, f, indent=2)

print("\n✓ All processed arrays saved to data/processed/")
print("✓ meta.json saved with feature names and threshold info")
