# utils/chart_helpers.py
# Shared utilities for the Student Performance Dashboard (Phase 3)
# Audience: School Administrators & Education Policy Makers

import pandas as pd
import numpy as np
import streamlit as st

# ── Colour palettes ──────────────────────────────────────────────────────────
COLOR_MOTIVATION = {"High": "#06D6A0", "Medium": "#118AB2", "Low": "#EF476F"}
COLOR_INCOME     = {"Low": "#EF476F", "Medium": "#FFD166", "High": "#06D6A0"}
COLOR_INTERNET   = {"Yes": "#06D6A0", "No": "#EF476F"}
COLOR_SCHOOL     = {"Public": "#118AB2", "Private": "#FFD166"}
COLOR_DISABILITY = {"No": "#118AB2", "Yes": "#EF476F"}

ORDINAL_MOTIVATION = ["High", "Medium", "Low"]
ORDINAL_INCOME     = ["Low", "Medium", "High"]

# ── Data loader (cached) ─────────────────────────────────────────────────────
@st.cache_data
def load_data():
    return pd.read_csv(
        r"data/StudentPerformanceFactors_cleaned.csv"
    )

# ── Global sidebar filter ────────────────────────────────────────────────────
def render_sidebar_filters(df):
    """Render sidebar filter widgets and return the filtered dataframe."""
    st.sidebar.header("🔍 Filter Students")

    school_opts  = ["All"] + sorted(df["School_Type"].unique().tolist())
    income_opts  = ["All"] + ["Low", "Medium", "High"]
    motiv_opts   = ["All"] + ["High", "Medium", "Low"]
    internet_opts = ["All", "Yes", "No"]

    sel_school   = st.sidebar.selectbox("School Type",    school_opts)
    sel_income   = st.sidebar.selectbox("Family Income",  income_opts)
    sel_motiv    = st.sidebar.selectbox("Motivation Level", motiv_opts)
    sel_internet = st.sidebar.selectbox("Internet Access", internet_opts)

    fdf = df.copy()
    if sel_school   != "All": fdf = fdf[fdf["School_Type"]     == sel_school]
    if sel_income   != "All": fdf = fdf[fdf["Family_Income"]   == sel_income]
    if sel_motiv    != "All": fdf = fdf[fdf["Motivation_Level"] == sel_motiv]
    if sel_internet != "All": fdf = fdf[fdf["Internet_Access"] == sel_internet]

    st.sidebar.markdown("---")
    st.sidebar.metric("Students in view", f"{len(fdf):,} / {len(df):,}")
    return fdf

# ── Shared Plotly layout ─────────────────────────────────────────────────────
def polish_layout(fig, title_text, x_title=None, y_title=None, y_range=None, show_legend=False):
    fig.update_layout(
        title=dict(text=title_text, x=0.5, xanchor="center", font=dict(size=16)),
        template="plotly_white",
        font=dict(family="Arial", size=13),
        showlegend=show_legend,
        margin=dict(t=60, b=40, l=60, r=40),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
    )
    if x_title:
        fig.update_xaxes(title_text=x_title, showgrid=False, zeroline=False)
    if y_title:
        fig.update_yaxes(title_text=y_title, showgrid=True, gridcolor="#e8e8e8", zeroline=True)
    if y_range:
        fig.update_yaxes(range=y_range)
    return fig
