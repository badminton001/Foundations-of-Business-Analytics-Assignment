"""
app.py — Academic Performance Dashboard
"""

import sys, os
sys.path.insert(0, os.path.dirname(__file__))

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

from utils.chart_helpers import (
    load_data, polish_layout,
    COLOR_MOTIVATION, COLOR_INCOME, COLOR_INTERNET,
    COLOR_SCHOOL, COLOR_DISABILITY,
    ORDINAL_MOTIVATION
)

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Academic Performance Dashboard",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Global CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
/* Narrow sidebar */
[data-testid="stSidebar"] { min-width: 180px !important; max-width: 180px !important; }
[data-testid="stSidebarContent"] { padding: 1rem 0.5rem; }

/* Remove top padding */
.block-container { padding-top: 1rem !important; padding-bottom: 1rem !important; }

/* Clean, readable page header */
.dash-header {
    background-color: #f8f9fa;
    color: #073B4C; 
    padding: 12px 20px; 
    border-radius: 6px;
    margin-bottom: 15px;
    border-left: 6px solid #06D6A0;
}
.dash-header h1 { margin: 0; font-size: 1.5rem; font-weight: 700; letter-spacing: 0.01em; color: #073B4C; }
.dash-header p  { margin: 4px 0 0; font-size: 0.85rem; color: #555; }

/* Section headers */
.sec-hdr {
    font-size: 1.0rem; font-weight: 700; color: #073B4C;
    border-bottom: 2px solid #e4e8ee; padding-bottom: 4px;
    margin: 15px 0 10px; text-transform: uppercase; letter-spacing: 0.05em;
}

/* KPI cards */
div[data-testid="metric-container"] {
    background: #ffffff; border: 1px solid #e4e8ee;
    border-radius: 6px; padding: 10px 14px !important;
    box-shadow: 0 1px 3px rgba(0,0,0,0.02);
}

/* Tighter chart margins */
.js-plotly-plot { margin-bottom: 0 !important; }
</style>
""", unsafe_allow_html=True)


# ── Data ──────────────────────────────────────────────────────────────────────
df_full = load_data()

# ── Sidebar filters ───────────────────────────────────────────────────────────
sb = st.sidebar
sb.markdown("**Filters**")

def sb_sel(label, col, options):
    return sb.selectbox(label, ["All"] + options, key=col)

sel_school   = sb_sel("School Type",    "School_Type",     sorted(df_full["School_Type"].unique()))
sel_income   = sb_sel("Family Income",  "Family_Income",   ["Low","Medium","High"])
sel_motiv    = sb_sel("Motivation",     "Motivation_Level",["High","Medium","Low"])
sel_internet = sb_sel("Internet Access","Internet_Access", ["Yes","No"])

df = df_full.copy()
if sel_school   != "All": df = df[df["School_Type"]      == sel_school]
if sel_income   != "All": df = df[df["Family_Income"]    == sel_income]
if sel_motiv    != "All": df = df[df["Motivation_Level"] == sel_motiv]
if sel_internet != "All": df = df[df["Internet_Access"]  == sel_internet]

sb.markdown("---")
sb.metric("Students", f"{len(df):,}")

# ── Dynamic helpers ───────────────────────────────────────────────────────────
np.random.seed(42)
df_plot = df.copy()
df_plot["Att_J"]  = df_plot["Attendance"]      + np.random.uniform(-0.4, 0.4, len(df_plot))
df_plot["Prev_J"] = df_plot["Previous_Scores"] + np.random.uniform(-0.4, 0.4, len(df_plot))

# ── HEADER ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="dash-header">
  <h1>Academic Performance Dashboard</h1>
  <p>Audience: School Administrators &amp; Education Policy Makers | Focus: Discovery of Core Drivers &amp; Systemic Inequalities</p>
</div>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# 1. OVERVIEW: CURRENT PERFORMANCE LANDSCAPE
# ═══════════════════════════════════════════════════════════════════════════════
c1,c2,c3,c4,c5 = st.columns(5)
c1.metric("Students in View",   f"{len(df):,}")
c2.metric("Mean Exam Score",    f"{df['Exam_Score'].mean():.2f}")
c3.metric("Avg Attendance",     f"{df['Attendance'].mean():.1f}%")
c4.metric("Avg Study Hours",    f"{df['Hours_Studied'].mean():.1f}")
c5.metric("Avg Previous Score", f"{df['Previous_Scores'].mean():.1f}")

st.markdown('<div class="sec-hdr">01 / Score &amp; Attendance Baseline</div>', unsafe_allow_html=True)
h1, h2 = st.columns(2)

with h1:
    fig = px.histogram(df, x="Exam_Score", nbins=20, color_discrete_sequence=["#2D6A4F"])
    fig = polish_layout(fig, "Exam Score Distribution", "Exam Score", "Count of Students")
    fig.update_traces(marker_line_width=0.5, marker_line_color="white")
    fig.update_layout(height=260, margin=dict(t=40,b=30,l=50,r=10))
    st.plotly_chart(fig, use_container_width=True)

with h2:
    fig = px.histogram(df, x="Attendance", nbins=20, color_discrete_sequence=["#40916C"])
    fig = polish_layout(fig, "Class Attendance Distribution", "Attendance (%)", "Count of Students")
    fig.update_traces(marker_line_width=0.5, marker_line_color="white")
    fig.update_layout(height=260, margin=dict(t=40,b=30,l=50,r=10))
    st.plotly_chart(fig, use_container_width=True)

# ═══════════════════════════════════════════════════════════════════════════════
# 2. PERFORMANCE DRIVERS: IDENTIFYING THE LEVERS 
# ═══════════════════════════════════════════════════════════════════════════════
st.markdown('<div class="sec-hdr">02 / Behavioural &amp; Resource Drivers</div>', unsafe_allow_html=True)

# Row A: Trend Lines (3 cols)
l1, l2, l3 = st.columns(3)
bins = [0, 8, 16, 24, 32, df["Hours_Studied"].max()+1 if len(df)>0 else 100]
labels = ["0-8","9-16","17-24","25-32","33+"]
df_line = df.copy()
df_line["Hrs_Bin"] = pd.cut(df_line["Hours_Studied"], bins=bins, labels=labels, right=True)

with l1:
    ldf1 = df_line.groupby("Hrs_Bin", observed=True)["Exam_Score"].mean().reset_index()
    fig1 = px.line(ldf1, x="Hrs_Bin", y="Exam_Score", markers=True)
    fig1.update_traces(line=dict(color="#118AB2", width=3), marker=dict(size=8, color="#073B4C"))
    fig1 = polish_layout(fig1, "Avg Score by Weekly Study Hours", "Study Hours", "Avg Exam Score")
    if not ldf1.empty: fig1.update_yaxes(range=[60, 75])
    fig1.update_layout(height=240, margin=dict(t=40,b=30,l=50,r=10))
    st.plotly_chart(fig1, use_container_width=True)

with l2:
    ldf2 = df.groupby("Sleep_Hours")["Exam_Score"].mean().reset_index()
    fig2 = px.line(ldf2, x="Sleep_Hours", y="Exam_Score", markers=True)
    fig2.update_traces(line=dict(color="#EF476F", width=3), marker=dict(size=8, color="#073B4C"))
    fig2 = polish_layout(fig2, "Avg Score by Nightly Sleep", "Sleep Hours", "Avg Exam Score")
    fig2.update_xaxes(tick0=4, dtick=1)
    if not ldf2.empty: fig2.update_yaxes(range=[65, 70])
    fig2.update_layout(height=240, margin=dict(t=40,b=30,l=50,r=10))
    st.plotly_chart(fig2, use_container_width=True)

with l3:
    ldf3 = df.groupby("Tutoring_Sessions")["Exam_Score"].mean().reset_index()
    fig3 = px.line(ldf3, x="Tutoring_Sessions", y="Exam_Score", markers=True)
    fig3.update_traces(line=dict(color="#06D6A0", width=3), marker=dict(size=8, color="#073B4C"))
    fig3 = polish_layout(fig3, "Avg Score by Tutoring Sessions", "Tutoring Sessions", "Avg Exam Score")
    fig3.update_xaxes(tick0=0, dtick=1)
    if not ldf3.empty: fig3.update_yaxes(range=[64, 74])
    fig3.update_layout(height=240, margin=dict(t=40,b=30,l=50,r=10))
    st.plotly_chart(fig3, use_container_width=True)

# Row B: Advanced Bubble & Scatter (2 cols)
s1, s2 = st.columns([1.2, 0.8])
with s1:
    fig_bub = px.scatter(
        df_plot, x="Att_J", y="Exam_Score",
        size="Hours_Studied", color="Motivation_Level",
        color_discrete_map=COLOR_MOTIVATION,
        category_orders={"Motivation_Level": ORDINAL_MOTIVATION},
        opacity=0.4, size_max=22,
    )
    fig_bub = polish_layout(
        fig_bub,
        "Synergy: Attendance &times; Study Hours (Bubble Size) &times; Motivation",
        "Attendance (%)", "Exam Score", show_legend=True,
    )
    fig_bub.update_layout(
        height=320, margin=dict(t=40,b=30,l=50,r=10),
        legend=dict(title="Motivation", orientation="h", y=-0.25, x=0, font=dict(size=11))
    )
    st.plotly_chart(fig_bub, use_container_width=True)

with s2:
    fig_s2 = px.scatter(
        df_plot, x="Prev_J", y="Exam_Score", color="Internet_Access",
        color_discrete_map=COLOR_INTERNET,
        category_orders={"Internet_Access": ["Yes","No"]},
        opacity=0.3, trendline="ols",
    )
    fig_s2.update_traces(marker=dict(size=4), selector=dict(mode="markers"))
    fig_s2 = polish_layout(fig_s2, "Exam Score vs Previous Scores (Baseline)", "Previous Score", "Exam Score", show_legend=True)
    fig_s2.update_layout(
        height=320, margin=dict(t=40,b=30,l=50,r=10),
        legend=dict(title="Internet", orientation="h", y=-0.25, x=0, font=dict(size=11))
    )
    st.plotly_chart(fig_s2, use_container_width=True)


# ═══════════════════════════════════════════════════════════════════════════════
# 3. EQUITY & SYSTEMIC PIPELINE
# ═══════════════════════════════════════════════════════════════════════════════
st.markdown('<div class="sec-hdr">03 / Equity Analysis &amp; Systemic Outcomes</div>', unsafe_allow_html=True)

# Row A: Demographics (4 cols)
d1, d2, d3, d4 = st.columns(4)

def donut(data, col, name, colors):
    if len(data) == 0: return go.Figure()
    pf = data[col].value_counts().reset_index()
    pf.columns = [col, "Count"]
    pf = pf.sort_values("Count", ascending=False)
    fig = px.pie(pf, values="Count", names=col,
                 color_discrete_sequence=colors, hole=0.45)
    fig.update_traces(textposition="inside", textinfo="percent+label",
                      marker=dict(line=dict(color="#fff", width=2)))
    fig = polish_layout(fig, f"{name}")
    fig.update_layout(showlegend=False, height=220, margin=dict(t=30,b=5,l=5,r=5))
    return fig

with d1:
    st.plotly_chart(donut(df, "Family_Income", "Family Income", ["#EF476F","#FFD166","#06D6A0"]), use_container_width=True)
with d2:
    st.plotly_chart(donut(df, "School_Type", "School Type", ["#118AB2","#EF476F"]), use_container_width=True)
with d3:
    st.plotly_chart(donut(df, "Learning_Disabilities", "Learning Disabilities", ["#118AB2","#EF476F"]), use_container_width=True)
with d4:
    cl = df.groupby(["School_Type","Internet_Access"]).size().reset_index(name="Count")
    if not cl.empty:
        fig_cb = px.bar(cl, x="School_Type", y="Count", color="Internet_Access",
                        barmode="group", color_discrete_map=COLOR_INTERNET)
        fig_cb = polish_layout(fig_cb, "School Type x Internet Access", "School Type", "Students", show_legend=True)
        fig_cb.update_yaxes(range=[0, cl["Count"].max()*1.15])
        fig_cb.update_layout(
            legend=dict(title="Internet", orientation="h", y=-0.3, x=0, font=dict(size=10)),
            height=220, margin=dict(t=30,b=20,l=40,r=10),
        )
        st.plotly_chart(fig_cb, use_container_width=True)

# Row B: Advanced Flow & Heatmap (2 cols)
adv1, adv2 = st.columns([1.3, 0.7])

with adv1:
    par_df = df.copy()
    if len(par_df) > 2:
        par_df["Outcome_Bin"] = pd.qcut(par_df["Exam_Score"], q=3, labels=["Lower 33%","Middle 33%","Top 33%"])
        for col, order in [
            ("Family_Income",       ["Low","Medium","High"]),
            ("Access_to_Resources", ["Low","Medium","High"]),
            ("Motivation_Level",    ["Low","Medium","High"]),
        ]:
            if col in par_df.columns:
                par_df[col] = pd.Categorical(par_df[col], categories=order, ordered=True)

        fig_par = px.parallel_categories(
            par_df,
            dimensions=["Family_Income","Access_to_Resources","Motivation_Level","Outcome_Bin"],
            color="Exam_Score", color_continuous_scale=px.colors.sequential.Teal,
        )
        fig_par.update_layout(
            title=dict(text="Systemic Pipeline: Socioeconomic Origin &rarr; Academic Outcome", x=0.5, xanchor="center", font=dict(size=14)),
            font=dict(family="Arial", size=11),
            height=300,
            margin=dict(l=40, r=110, t=50, b=30),
            coloraxis_colorbar=dict(x=1.02, y=0.55, len=0.6, title=dict(text="Score", side="top")),
            paper_bgcolor="rgba(0,0,0,0)",
        )
        st.plotly_chart(fig_par, use_container_width=True)

with adv2:
    num_df = df.select_dtypes(include=[np.number])
    if len(num_df.columns) > 1 and len(df) > 1:
        corr_mat = num_df.corr().round(2)
        fig_heat = px.imshow(corr_mat, text_auto=True, aspect="auto",
                             color_continuous_scale="RdBu_r", zmin=-1, zmax=1)
        fig_heat.update_layout(
            title=dict(text="Feature Correlation Matrix", x=0.5, xanchor="center", font=dict(size=14)),
            font=dict(family="Arial", size=9),
            height=300, margin=dict(t=50,b=10,l=10,r=10),
            paper_bgcolor="rgba(0,0,0,0)"
        )
        st.plotly_chart(fig_heat, use_container_width=True)
