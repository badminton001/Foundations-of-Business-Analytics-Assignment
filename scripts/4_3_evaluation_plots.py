"""
scripts/4_3_evaluation_plots.py
Step 4.3: Evaluation Visualisations — Style matches all Phase 2 plots
  • Engine:   Plotly Express + Graph Objects
  • Template: plotly_white
  • Font:     Arial, size=14
  • Title:    x=0.5, xanchor='center'
  • Export:   write_image(scale=2)
"""

import os, sys, json, pickle
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from sklearn.metrics import confusion_matrix, roc_curve, precision_recall_curve, auc

# ── Paths ─────────────────────────────────────────────────────────────────────
BASE     = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MDL_DIR  = os.path.join(BASE, "data", "models")
PLOT_DIR = os.path.join(BASE, "plots", "predictive")
os.makedirs(PLOT_DIR, exist_ok=True)

# ── Load eval data ────────────────────────────────────────────────────────────
with open(os.path.join(MDL_DIR, "eval_data.json")) as f:
    ev = json.load(f)

reg_data = ev["reg"]
clf_data = ev["clf"]
feature_names = reg_data["feature_names"]

y_test_reg  = np.array(reg_data["y_test"])
y_pred_reg  = np.array(reg_data["y_pred"])
y_test_clf  = np.array(clf_data["y_test"])
y_pred_clf  = np.array(clf_data["y_pred"])
y_proba_clf = np.array(clf_data["y_proba"])

with open(os.path.join(MDL_DIR, "best_reg_model.pkl"), "rb") as f:
    best_reg_model = pickle.load(f)
with open(os.path.join(MDL_DIR, "best_clf_model.pkl"), "rb") as f:
    best_clf_model = pickle.load(f)

# ── Shared style helpers ──────────────────────────────────────────────────────
PALETTE = {
    "teal":   "#06D6A0",
    "navy":   "#073B4C",
    "coral":  "#EF476F",
    "amber":  "#FFD166",
    "blue":   "#118AB2",
    "green":  "#2D6A4F",
    "light":  "#40916C",
}

def polish(fig, title, x_title=None, y_title=None, show_legend=False):
    """Identical to the project-wide polish_layout used in Phase 2 scripts."""
    fig.update_layout(
        title=dict(text=title, x=0.5, xanchor="center"),
        template="plotly_white",
        font=dict(family="Arial", size=14),
        showlegend=show_legend,
        bargap=0.1,
    )
    if x_title:
        fig.update_xaxes(title_text=x_title, showgrid=False)
    if y_title:
        fig.update_yaxes(title_text=y_title, showgrid=True, gridcolor="lightgray")
    else:
        fig.update_yaxes(showgrid=True, gridcolor="lightgray")
    return fig

def save(fig, name: str, w=900, h=650):
    path = os.path.join(PLOT_DIR, name)
    fig.write_image(path, scale=2, width=w, height=h)
    print(f"  Saved: {path}")


# ═══════════════════════════════════════════════════════════════════════════════
# REGRESSION PLOTS
# ═══════════════════════════════════════════════════════════════════════════════

# ── Plot 1: Actual vs Predicted scatter ───────────────────────────────────────
residuals = y_test_reg - y_pred_reg
df_reg = pd.DataFrame({"Actual": y_test_reg, "Predicted": y_pred_reg, "Residual": residuals})
lo = min(y_test_reg.min(), y_pred_reg.min()) - 1
hi = max(y_test_reg.max(), y_pred_reg.max()) + 1

fig = go.Figure()
fig.add_trace(go.Scatter(
    x=df_reg["Actual"], y=df_reg["Predicted"],
    mode="markers",
    marker=dict(color=PALETTE["blue"], size=5, opacity=0.35, line=dict(width=0)),
    name="Predictions"
))
# Perfect fit line
fig.add_trace(go.Scatter(
    x=[lo, hi], y=[lo, hi],
    mode="lines",
    line=dict(color=PALETTE["coral"], dash="dash", width=2),
    name="Perfect Fit (y = x)"
))
# ±1 band
fig.add_trace(go.Scatter(
    x=[lo, hi, hi, lo], y=[lo-1, hi-1, hi+1, lo+1],
    fill="toself", fillcolor=f"rgba(239,71,111,0.08)",
    line=dict(width=0), showlegend=False, name="±1 band"
))
fig.add_annotation(
    x=0.05, y=0.90, xref="paper", yref="paper",
    text=f"RMSE = {reg_data['RMSE']:.3f}<br>R² = {reg_data['R2']:.3f}",
    showarrow=False, align="left",
    bgcolor="white", bordercolor=PALETTE["navy"], borderwidth=1,
    font=dict(family="Arial", size=13)
)
fig = polish(fig, "Regression: Actual vs Predicted Exam Score", "Actual Exam Score", "Predicted Exam Score", show_legend=True)
fig.update_layout(legend=dict(x=0.72, y=0.08, bgcolor="rgba(255,255,255,0.8)", bordercolor="lightgray", borderwidth=1))
save(fig, "Reg_ActualVsPredicted.png")


# ── Plot 2: Residual Distribution ─────────────────────────────────────────────
fig2 = px.histogram(
    df_reg, x="Residual", nbins=35,
    color_discrete_sequence=[PALETTE["teal"]]
)
fig2 = polish(fig2, "Regression: Residual Distribution", "Residual (Actual − Predicted)", "Count of Students")
fig2.update_traces(marker_line_width=0.5, marker_line_color="white")
fig2.add_vline(x=0,               line_dash="dash", line_color=PALETTE["coral"],  line_width=2,
               annotation_text="Zero", annotation_position="top right",
               annotation_font=dict(family="Arial", size=12))
fig2.add_vline(x=float(residuals.mean()), line_dash="solid", line_color=PALETTE["amber"], line_width=2,
               annotation_text=f"Mean = {residuals.mean():.3f}", annotation_position="top left",
               annotation_font=dict(family="Arial", size=12))
save(fig2, "Reg_ResidualDistribution.png")


# ── Plot 3: Feature Importance (Regressor) ────────────────────────────────────
if hasattr(best_reg_model, "feature_importances_"):
    importances = best_reg_model.feature_importances_
    imp_label   = "Feature Importance (Gini)"
elif hasattr(best_reg_model, "coef_"):
    importances = np.abs(best_reg_model.coef_)
    imp_label   = "Absolute Coefficient Magnitude"
else:
    importances = np.ones(len(feature_names))
    imp_label   = "Importance"

idx     = np.argsort(importances)
top_n   = min(15, len(idx))
idx_top = idx[-top_n:]

colors = [PALETTE["teal"] if i == idx[-1] else PALETTE["blue"] for i in idx_top]
df_imp = pd.DataFrame({
    "Feature":    [feature_names[i] for i in idx_top],
    "Importance": importances[idx_top],
    "Color":      colors,
})

fig3 = go.Figure(go.Bar(
    x=df_imp["Importance"], y=df_imp["Feature"],
    orientation="h",
    marker_color=df_imp["Color"],
    marker_line_width=0,
))
fig3 = polish(fig3, f"Feature Importance — Regression Model ({reg_data['name']})",
              imp_label, None)
fig3.update_layout(height=600)
save(fig3, "Reg_FeatureImportance.png", w=900, h=620)


# ═══════════════════════════════════════════════════════════════════════════════
# CLASSIFICATION PLOTS
# ═══════════════════════════════════════════════════════════════════════════════

# ── Plot 4: Confusion Matrix ──────────────────────────────────────────────────
cm      = confusion_matrix(y_test_clf, y_pred_clf)
cm_norm = cm.astype(float) / cm.sum(axis=1, keepdims=True)
labels  = ["Below Average", "Above Average"]
text    = [[f"{cm[i][j]}<br>({cm_norm[i][j]*100:.1f}%)" for j in range(2)] for i in range(2)]

fig4 = go.Figure(go.Heatmap(
    z=cm_norm,
    x=labels, y=labels,
    colorscale=[[0, "#f0f8ff"], [1, PALETTE["blue"]]],
    zmin=0, zmax=1,
    text=text, texttemplate="%{text}",
    textfont=dict(family="Arial", size=16, color=PALETTE["navy"]),
    colorbar=dict(title="Rate"),
    showscale=True,
))
fig4.update_layout(
    title=dict(text="Confusion Matrix (Normalised %)", x=0.5, xanchor="center"),
    template="plotly_white",
    font=dict(family="Arial", size=14),
    xaxis=dict(title="Predicted Label", showgrid=False),
    yaxis=dict(title="Actual Label",    showgrid=False, autorange="reversed"),
)
save(fig4, "Clf_ConfusionMatrix.png", w=700, h=600)


# ── Plot 5: ROC Curve ─────────────────────────────────────────────────────────
fpr, tpr, _ = roc_curve(y_test_clf, y_proba_clf)
roc_auc     = auc(fpr, tpr)

fig5 = go.Figure()
fig5.add_trace(go.Scatter(
    x=fpr, y=tpr, mode="lines",
    line=dict(color=PALETTE["blue"], width=3),
    fill="tozeroy", fillcolor=f"rgba(17,138,178,0.10)",
    name=f"ROC Curve (AUC = {roc_auc:.3f})"
))
fig5.add_trace(go.Scatter(
    x=[0, 1], y=[0, 1], mode="lines",
    line=dict(color="gray", dash="dash", width=1.5),
    name="Random Classifier"
))
fig5 = polish(fig5, "ROC Curve — Classification Model", "False Positive Rate", "True Positive Rate (Recall)", show_legend=True)
fig5.update_layout(legend=dict(x=0.55, y=0.08, bgcolor="rgba(255,255,255,0.8)", bordercolor="lightgray", borderwidth=1))
save(fig5, "Clf_ROCCurve.png")


# ── Plot 6: Precision-Recall Curve ────────────────────────────────────────────
prec_arr, rec_arr, _ = precision_recall_curve(y_test_clf, y_proba_clf)
pr_auc               = auc(rec_arr, prec_arr)
baseline             = float(y_test_clf.mean())

fig6 = go.Figure()
fig6.add_trace(go.Scatter(
    x=rec_arr, y=prec_arr, mode="lines",
    line=dict(color=PALETTE["teal"], width=3),
    fill="tozeroy", fillcolor=f"rgba(6,214,160,0.10)",
    name=f"PR Curve (AUC = {pr_auc:.3f})"
))
fig6.add_hline(
    y=baseline,
    line_dash="dash", line_color=PALETTE["coral"], line_width=1.5,
    annotation_text=f"Baseline (prevalence = {baseline:.2f})",
    annotation_position="bottom right",
    annotation_font=dict(family="Arial", size=12)
)
fig6 = polish(fig6, "Precision-Recall Curve — Classification Model", "Recall", "Precision", show_legend=True)
fig6.update_layout(legend=dict(x=0.02, y=0.08, bgcolor="rgba(255,255,255,0.8)", bordercolor="lightgray", borderwidth=1))
save(fig6, "Clf_PRCurve.png")


# ── Plot 7: Feature Importance (Classifier) ──────────────────────────────────
if hasattr(best_clf_model, "feature_importances_"):
    clf_imp   = best_clf_model.feature_importances_
    clf_label = "Feature Importance (Gini)"
elif hasattr(best_clf_model, "coef_"):
    clf_imp   = np.abs(best_clf_model.coef_[0])
    clf_label = "Absolute Coefficient Magnitude"
else:
    clf_imp   = np.ones(len(feature_names))
    clf_label = "Importance"

idx_c     = np.argsort(clf_imp)
top_n_c   = min(15, len(idx_c))
idx_c_top = idx_c[-top_n_c:]
colors_c  = [PALETTE["coral"] if i == idx_c[-1] else PALETTE["amber"] for i in idx_c_top]

df_clf_imp = pd.DataFrame({
    "Feature":    [feature_names[i] for i in idx_c_top],
    "Importance": clf_imp[idx_c_top],
    "Color":      colors_c,
})

fig7 = go.Figure(go.Bar(
    x=df_clf_imp["Importance"], y=df_clf_imp["Feature"],
    orientation="h",
    marker_color=df_clf_imp["Color"],
    marker_line_width=0,
))
fig7 = polish(fig7, f"Feature Importance — Classification Model ({clf_data['name']})",
              clf_label, None)
fig7.update_layout(height=600)
save(fig7, "Clf_FeatureImportance.png", w=900, h=620)


print("\n✓ All 7 evaluation plots saved to plots/predictive/ (Plotly, plotly_white, Arial 14)")
