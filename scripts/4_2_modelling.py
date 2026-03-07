"""
scripts/4_2_modelling.py
Step 4.2: Train & Evaluate Regression + Classification Models
Quality Gate: RMSE < 3.5, R² > 0.20 | F1 > 0.60, ROC-AUC > 0.65
"""

import os, sys, json, pickle
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

import numpy as np
import pandas as pd
from sklearn.linear_model import Ridge, LogisticRegression
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier, GradientBoostingClassifier
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.metrics import (
    mean_squared_error, mean_absolute_error, r2_score,
    f1_score, precision_score, recall_score, roc_auc_score,
    classification_report
)

# ── Paths ────────────────────────────────────────────────────────────────────
BASE     = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_OUT = os.path.join(BASE, "data", "processed")
MDL_OUT  = os.path.join(BASE, "data", "models")
os.makedirs(MDL_OUT, exist_ok=True)

# ── Load preprocessed data ───────────────────────────────────────────────────
X_train = np.load(os.path.join(DATA_OUT, "X_train_scaled.npy"))
X_test  = np.load(os.path.join(DATA_OUT, "X_test_scaled.npy"))
y_train_reg = np.load(os.path.join(DATA_OUT, "y_train_reg.npy"))
y_test_reg  = np.load(os.path.join(DATA_OUT, "y_test_reg.npy"))
y_train_clf = np.load(os.path.join(DATA_OUT, "y_train_clf.npy"))
y_test_clf  = np.load(os.path.join(DATA_OUT, "y_test_clf.npy"))
with open(os.path.join(DATA_OUT, "meta.json")) as f:
    meta = json.load(f)
feature_names = meta["feature_names"]

print("=" * 60)
print("TASK 1: REGRESSION  (predict Exam_Score)")
print("=" * 60)

# ── Regression models ────────────────────────────────────────────────────────
reg_models = {
    "Ridge Regression":         Ridge(alpha=1.0),
    "Random Forest Regressor":  RandomForestRegressor(n_estimators=300, max_depth=10, random_state=42, n_jobs=-1),
    "Gradient Boosting Regressor": GradientBoostingRegressor(n_estimators=300, learning_rate=0.05, max_depth=5, random_state=42),
}

reg_results = {}
for name, mdl in reg_models.items():
    mdl.fit(X_train, y_train_reg)
    preds = mdl.predict(X_test)
    rmse = np.sqrt(mean_squared_error(y_test_reg, preds))
    mae  = mean_absolute_error(y_test_reg, preds)
    r2   = r2_score(y_test_reg, preds)
    reg_results[name] = {"RMSE": rmse, "MAE": mae, "R2": r2, "model": mdl, "preds": preds}
    print(f"  {name:<35}  RMSE={rmse:.4f}  MAE={mae:.4f}  R²={r2:.4f}")

# ── Select best regression model ──────────────────────────────────────────────
best_reg_name = min((n for n in reg_results), key=lambda n: reg_results[n]["RMSE"])
best_reg      = reg_results[best_reg_name]
print(f"\n  Best: {best_reg_name}")
print(f"  RMSE={best_reg['RMSE']:.4f}  MAE={best_reg['MAE']:.4f}  R²={best_reg['R2']:.4f}")

# ══ Quality Gate ══════════════════════════════════════════════════════════════
REG_RMSE_GATE = 3.5
REG_R2_GATE   = 0.20
if best_reg["RMSE"] > REG_RMSE_GATE or best_reg["R2"] < REG_R2_GATE:
    print("\n🚨 QUALITY GATE FAILED (Regression)")
    print(f"   RMSE={best_reg['RMSE']:.4f} (gate <{REG_RMSE_GATE}) | R²={best_reg['R2']:.4f} (gate >{REG_R2_GATE})")
    sys.exit(1)
else:
    print(f"\n✓ Quality gate passed (RMSE<{REG_RMSE_GATE}, R²>{REG_R2_GATE})")

print("\n" + "=" * 60)
print("TASK 2: CLASSIFICATION  (predict Above/Below Average)")
print("=" * 60)

# ── Classification models ────────────────────────────────────────────────────
clf_models = {
    "Logistic Regression":          LogisticRegression(max_iter=1000, random_state=42, class_weight="balanced"),
    "Random Forest Classifier":     RandomForestClassifier(n_estimators=300, max_depth=10, random_state=42,
                                                           class_weight="balanced", n_jobs=-1),
    "Gradient Boosting Classifier": GradientBoostingClassifier(n_estimators=300, learning_rate=0.05,
                                                               max_depth=5, random_state=42),
}

clf_results = {}
for name, mdl in clf_models.items():
    mdl.fit(X_train, y_train_clf)
    preds    = mdl.predict(X_test)
    proba    = mdl.predict_proba(X_test)[:, 1]
    f1       = f1_score(y_test_clf, preds, average="macro")
    prec     = precision_score(y_test_clf, preds, average="macro")
    rec      = recall_score(y_test_clf, preds, average="macro")
    auc      = roc_auc_score(y_test_clf, proba)
    clf_results[name] = {"F1": f1, "Precision": prec, "Recall": rec, "AUC": auc,
                          "model": mdl, "preds": preds, "proba": proba}
    print(f"  {name:<35}  F1={f1:.4f}  Prec={prec:.4f}  Rec={rec:.4f}  AUC={auc:.4f}")

# ── Select best classification model ─────────────────────────────────────────
best_clf_name = max((n for n in clf_results), key=lambda n: clf_results[n]["AUC"])
best_clf      = clf_results[best_clf_name]
print(f"\n  Best: {best_clf_name}")
print(f"  F1={best_clf['F1']:.4f}  Prec={best_clf['Precision']:.4f}  Rec={best_clf['Recall']:.4f}  AUC={best_clf['AUC']:.4f}")
print("\n  Detailed classification report (best model):")
print(classification_report(y_test_clf, best_clf["preds"], target_names=["Below Average","Above Average"]))

# ══ Quality Gate ══════════════════════════════════════════════════════════════
CLF_F1_GATE  = 0.60
CLF_AUC_GATE = 0.65
if best_clf["F1"] < CLF_F1_GATE or best_clf["AUC"] < CLF_AUC_GATE:
    print("\n🚨 QUALITY GATE FAILED (Classification)")
    print(f"   F1={best_clf['F1']:.4f} (gate >{CLF_F1_GATE}) | AUC={best_clf['AUC']:.4f} (gate >{CLF_AUC_GATE})")
    sys.exit(1)
else:
    print(f"\n✓ Quality gate passed (F1>{CLF_F1_GATE}, AUC>{CLF_AUC_GATE})")

# ── Save best models and predictions ─────────────────────────────────────────
print("\n" + "=" * 60)
print("SAVING BEST MODELS")
print("=" * 60)

with open(os.path.join(MDL_OUT, "best_reg_model.pkl"), "wb") as f:
    pickle.dump(best_reg["model"], f)
with open(os.path.join(MDL_OUT, "best_clf_model.pkl"), "wb") as f:
    pickle.dump(best_clf["model"], f)

eval_data = {
    "reg": {
        "name":        best_reg_name,
        "y_test":      y_test_reg.tolist(),
        "y_pred":      best_reg["preds"].tolist(),
        "RMSE":        float(best_reg["RMSE"]),
        "MAE":         float(best_reg["MAE"]),
        "R2":          float(best_reg["R2"]),
        "feature_names": feature_names,
    },
    "clf": {
        "name":        best_clf_name,
        "y_test":      y_test_clf.tolist(),
        "y_pred":      best_clf["preds"].tolist(),
        "y_proba":     best_clf["proba"].tolist(),
        "F1":          float(best_clf["F1"]),
        "Precision":   float(best_clf["Precision"]),
        "Recall":      float(best_clf["Recall"]),
        "AUC":         float(best_clf["AUC"]),
        "feature_names": feature_names,
    }
}
with open(os.path.join(MDL_OUT, "eval_data.json"), "w") as f:
    json.dump(eval_data, f)

print(f"  Saved best regressor:       {best_reg_name}")
print(f"  Saved best classifier:      {best_clf_name}")
print("  eval_data.json saved for plotting script.")
print("\n✓ Step 4.2 complete.")
