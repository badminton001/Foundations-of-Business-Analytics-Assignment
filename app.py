"""
app.py — Academic Performance Analytics Dashboard
Narrative: Equity, Effort, and Engagement
Audience:  Education policymakers and school administrators
All charts faithfully match the parameters in 2_2_basic_visualizations.py
and 2_3_advanced_visualizations.py (font size 14, marker sizes, colours,
gridcolor='lightgray', ticks, etc.).
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# =============================================================================
# PAGE CONFIG
# =============================================================================
st.set_page_config(
    page_title="Academic Performance Analytics",
    layout="wide",
    initial_sidebar_state="expanded",
)

# =============================================================================
# CSS
# =============================================================================
st.markdown("""
<style>
html, body, [data-testid="stAppViewContainer"] { background: #EEF2F7; }
[data-testid="stAppViewContainer"] > .main   { background: #EEF2F7; padding-top: 0 !important; }
[data-testid="stHeader"]                      { background: transparent; }
.block-container { padding: 0 2.4rem 3.5rem 2.4rem !important; max-width: 100% !important; }
div[data-testid="stVerticalBlockBorderWrapper"] { border: none !important; padding: 0 !important; }
.stPlotlyChart { margin-bottom: 0 !important; }

/* Hero */
.dash-hero {
    background: linear-gradient(130deg, #073B4C 0%, #0A5C78 55%, #118AB2 100%);
    padding: 32px 44px 28px 44px;
    border-radius: 0 0 20px 20px;
    margin: 0 -2.4rem 30px -2.4rem;
}
.dash-hero h1 {
    font-size: 1.62rem; font-weight: 800; color: #FFFFFF;
    margin: 0 0 7px 0; letter-spacing: -0.025em; font-family: Arial, sans-serif;
}
.dash-hero .sub {
    font-size: 0.84rem; color: rgba(255,255,255,0.72);
    line-height: 1.55; font-family: Arial, sans-serif; margin: 0;
}

/* KPI strip */
.kpi-strip { display: flex; gap: 14px; margin-bottom: 30px; }
.kpi-card {
    flex: 1; background: #FFFFFF; border-radius: 12px;
    padding: 18px 22px 15px 22px;
    border-top: 4px solid #118AB2;
    box-shadow: 0 2px 8px rgba(0,0,0,0.06);
}
.kpi-card.c-teal  { border-top-color: #06D6A0; }
.kpi-card.c-amber { border-top-color: #FFD166; }
.kpi-card.c-navy  { border-top-color: #073B4C; }
.kpi-card.c-blue  { border-top-color: #118AB2; }
.kpi-val { font-size: 1.90rem; font-weight: 800; color: #0D1B2A; line-height: 1; margin-bottom: 6px; }
.kpi-lbl { font-size: 0.68rem; color: #64748B; text-transform: uppercase; font-weight: 700; letter-spacing: 0.09em; }
.kpi-sub { font-size: 0.75rem; color: #94A3B8; margin-top: 3px; }

/* Section headers */
.sec-wrap { margin: 36px 0 14px 0; }
.sec-eyebrow { font-size: 0.66rem; font-weight: 800; color: #118AB2;
               letter-spacing: 0.16em; text-transform: uppercase; margin-bottom: 4px; }
.sec-title { font-size: 1.08rem; font-weight: 800; color: #0D1B2A;
             margin: 0 0 5px 0; font-family: Arial, sans-serif; }
.sec-desc  { font-size: 0.81rem; color: #64748B; margin: 0; line-height: 1.50; }
.sec-rule  { border: none; border-top: 1.5px solid #DDE3EC; margin: 12px 0 18px 0; }

/* Sidebar */
[data-testid="stSidebar"]   { background: #0D2B3E !important; }
[data-testid="stSidebar"] * { color: #CBD5E1 !important; }
[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] h3 { color: #FFFFFF !important; }
[data-testid="stSidebar"] .stSelectbox > div > div {
    background: #1A3A50; border-color: #2D5068; border-radius: 7px;
}
[data-testid="stSidebar"] hr { border-color: #1E4060; }
</style>
""", unsafe_allow_html=True)

# =============================================================================
# DATA  — mirror 2_3_advanced_visualizations.py exactly
# =============================================================================
@st.cache_data
def load_data():
    df = pd.read_csv("data/StudentPerformanceFactors_cleaned.csv")
    # Shuffle to prevent z-order overplotting (same as script: random_state=42)
    df = df.sample(frac=1, random_state=42).reset_index(drop=True)
    # Jitter arrays (same seed & magnitude as script)
    np.random.seed(42)
    df["Attendance_Jittered"]      = df["Attendance"]      + np.random.uniform(-0.4, 0.4, len(df))
    df["Previous_Scores_Jittered"] = df["Previous_Scores"] + np.random.uniform(-0.4, 0.4, len(df))
    df["Hours_Studied_Jittered"]   = df["Hours_Studied"]   + np.random.uniform(-0.4, 0.4, len(df))
    return df

df_raw = load_data()

# =============================================================================
# SIDEBAR
# =============================================================================
with st.sidebar:
    st.markdown("### Filters")
    st.markdown("---")
    sel_school = st.selectbox(
        "Institution Type",
        ["All"] + sorted(df_raw["School_Type"].dropna().unique()),
    )
    sel_income = st.selectbox("Family Income", ["All", "High", "Medium", "Low"])
    sel_motiv  = st.selectbox("Motivation Level", ["All", "High", "Medium", "Low"])

df = df_raw.copy()
if sel_school != "All": df = df[df["School_Type"] == sel_school]
if sel_income != "All": df = df[df["Family_Income"] == sel_income]
if sel_motiv  != "All": df = df[df["Motivation_Level"] == sel_motiv]

# =============================================================================
# CHART HELPERS — parameters copied verbatim from the static scripts
# =============================================================================

# ── Matches polish_layout() in both static scripts (font size=14, lightgray) ──
def polish_layout(fig, title_text, x_title=None, y_title=None, h=320):
    fig.update_layout(
        title=dict(text=title_text, x=0.5, xanchor="center"),
        template="plotly_white",
        font=dict(family="Arial", size=14),
        showlegend=False,
        bargap=0.1,
        height=h,
    )
    if x_title:
        fig.update_xaxes(title_text=x_title, showgrid=False)
    if y_title:
        fig.update_yaxes(title_text=y_title, showgrid=True, gridcolor="lightgray")
    else:
        fig.update_yaxes(showgrid=True, gridcolor="lightgray")
    return fig


# ── Matches create_strict_histogram() in 2_2_basic_visualizations.py ──
# Dashboard uses numpy pre-computed bins + px.bar (instead of px.histogram) so that
# each bar's position and width are explicitly specified — this eliminates the
# Plotly.js auto-range gap that appears when bins start exactly at the axis edge.
def make_histogram(col, title, x_label, color, num_bins,
                   override_min=None, override_max=None,
                   x_dtick=None, x_range=None, h=370):
    col_min   = override_min if override_min is not None else df[col].min()
    col_max   = override_max if override_max is not None else df[col].max()
    bin_width = (col_max - col_min) / num_bins
    tick_step = x_dtick if x_dtick is not None else bin_width

    # Pre-compute with numpy. go.Bar (not px.bar) is used so x is a true linear
    # numeric axis — px.bar coerces numeric x to categorical, breaking range/width.
    counts, edges = np.histogram(df[col].dropna(), bins=num_bins, range=(col_min, col_max))
    midpoints = (edges[:-1] + edges[1:]) / 2  # bar centres; bar 1 centre=55.5 → left edge=55.0

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=midpoints,
        y=counts,
        width=bin_width,
        marker_color=color,
        marker_line_color="black",
        marker_line_width=1.5,
    ))
    effective_range = x_range if x_range else [col_min, col_max]
    fig.update_layout(
        title=dict(text=title, x=0.5, xanchor="center"),
        template="plotly_white",
        font=dict(family="Arial", size=14),
        bargap=0,
        bargroupgap=0,
        showlegend=False,
        height=h,
    )
    fig.update_xaxes(
        title_text=x_label,
        showgrid=False,
        showline=True, linewidth=1.5, linecolor="black",
        ticks="outside", tickwidth=1.5, tickcolor="black", ticklen=6,
        tickmode="linear", tick0=col_min, dtick=tick_step,
        range=effective_range,
        autorange=False,
    )
    fig.update_yaxes(
        title_text="Count of Students",
        showgrid=False,
        showline=True, linewidth=1.5, linecolor="black",
        ticks="outside", tickwidth=1.5, tickcolor="black", ticklen=6,
        rangemode="tozero",
    )
    return fig


# ── Matches violin block in 2_2_basic_visualizations.py ──
def make_violin(col, title, x_label, color_map, cat_order,
                filter_vals=None, h=330):
    d = df if filter_vals is None else df[~df[col].isin(filter_vals)]
    fig = px.violin(
        d, x=col, y="Exam_Score", color=col,
        color_discrete_map=color_map,
        box=True, points="outliers",
        category_orders={col: cat_order},
    )
    fig = polish_layout(fig, title, x_label, "Exam Score", h=h)
    fig.update_layout(showlegend=False)
    return fig


# ── Matches line-chart block in 2_2_basic_visualizations.py ──
def make_line(x_col, title, color, x_label,
              bin_spec=None, int_ticks=False, h=290):
    if bin_spec:
        bins, labels = bin_spec
        tmp = df.copy()
        tmp[x_col] = pd.cut(tmp[x_col], bins=bins, labels=labels, right=True)
        ld = tmp.groupby(x_col, as_index=False, observed=True)["Exam_Score"].mean()
    else:
        ld = df.groupby(x_col, as_index=False, observed=True)["Exam_Score"].mean()

    fig = px.line(ld, x=x_col, y="Exam_Score", markers=True, line_shape="linear")
    fig.update_traces(
        mode="lines+markers+text",
        line=dict(color=color, width=4),
        marker=dict(size=12, color=color),
        text=[f"{v:.1f}" for v in ld["Exam_Score"]],
        textposition="top center",
        textfont=dict(size=11, color="#1F2937"),
    )
    fig = polish_layout(fig, title, x_label, "Average Exam Score", h=h)
    y_lo = max(50, int(ld["Exam_Score"].min()) - 3)
    y_hi = int(ld["Exam_Score"].max()) + 4
    fig.update_yaxes(range=[y_lo, y_hi])
    if int_ticks:
        fig.update_xaxes(tick0=0, dtick=1, zeroline=False)
    else:
        fig.update_xaxes(zeroline=False)
    return fig


# =============================================================================
# HERO
# =============================================================================
st.markdown("""
<div class="dash-hero">
  <h1>Academic Performance Analytics Dashboard</h1>
  <p class="sub">
    Examining behavioral, environmental, and socioeconomic drivers of student exam outcomes
    to identify evidence-based interventions for administrators and policymakers.
  </p>
</div>
""", unsafe_allow_html=True)

# =============================================================================
# KPI STRIP
# =============================================================================
n          = len(df)
avg_score  = df["Exam_Score"].mean()
avg_attend = df["Attendance"].mean()
avg_hours  = df["Hours_Studied"].mean()
pct_inet   = (df["Internet_Access"] == "Yes").mean() * 100

st.markdown(f"""
<div class="kpi-strip">
  <div class="kpi-card c-navy">
    <div class="kpi-val">{n:,}</div>
    <div class="kpi-lbl">Students Analysed</div>
  </div>
  <div class="kpi-card c-blue">
    <div class="kpi-val">{avg_score:.1f}</div>
    <div class="kpi-lbl">Mean Exam Score</div>
    <div class="kpi-sub">out of 100</div>
  </div>
  <div class="kpi-card c-teal">
    <div class="kpi-val">{avg_attend:.1f}%</div>
    <div class="kpi-lbl">Avg Class Attendance</div>
  </div>
  <div class="kpi-card c-amber">
    <div class="kpi-val">{avg_hours:.1f} h</div>
    <div class="kpi-lbl">Avg Study Hours / Wk</div>
  </div>
  <div class="kpi-card c-teal">
    <div class="kpi-val">{pct_inet:.1f}%</div>
    <div class="kpi-lbl">Internet Access</div>
  </div>
</div>
""", unsafe_allow_html=True)

# =============================================================================
# SECTION 1 — PERFORMANCE BASELINE
# Two charts: score histogram + primary scatter (attendance × score by motivation)
# =============================================================================
st.markdown("""
<div class="sec-wrap">
  <div class="sec-eyebrow">01 — Performance Baseline</div>
  <div class="sec-title">Score Distribution and the Engagement-Performance Link</div>
  <div class="sec-desc">
    The exam score distribution reveals a tight cluster around 65–69 (IQR = 4 points), exposing a performance ceiling.
    Plotting attendance against scores, coloured by motivation level, confirms that the positive
    attendance-performance relationship holds consistently across all motivation levels.
  </div>
</div>
<hr class="sec-rule">
""", unsafe_allow_html=True)

col_h, col_s1 = st.columns([1, 1.65])

with col_h:
    # Chart 1 — Exam Score Histogram
    # Matches: num_bins=45, override_min=55, override_max=100, color="#9BC2E6"
    fig1 = make_histogram(
        "Exam_Score", "Distribution of Exam Scores",
        "Exam Score", "#9BC2E6", 45, 55, 100,
        x_dtick=5, x_range=[55, 100], h=430
    )
    st.plotly_chart(fig1, use_container_width=True)

with col_s1:
    # Chart 2 — Scatter: Attendance × Score by Motivation
    # Matches: Scatter_Attendance_Score.png parameters exactly
    ordinal_motivation = ["Low", "Medium", "High"]
    color_motivation   = {"High": "#06D6A0", "Medium": "#118AB2", "Low": "#EF476F"}

    fig2 = px.scatter(
        df, x="Attendance_Jittered", y="Exam_Score",
        color="Motivation_Level",
        color_discrete_map=color_motivation,
        category_orders={"Motivation_Level": ordinal_motivation},
        opacity=0.5, trendline="ols",
        marginal_x="histogram", marginal_y="box",
        labels={"Attendance_Jittered": "Attendance (%)",
                "Exam_Score": "Exam Score"},
    )
    fig2.update_traces(
        marker=dict(size=6, line=dict(width=0.5, color="white")),
        selector=dict(mode="markers", type="scatter"),
    )
    fig2.update_traces(
        line=dict(width=2.5),
        selector=dict(mode="lines"),
    )
    fig2 = polish_layout(fig2,
        "Exam Score vs Class Attendance by Motivation Level",
        "Attendance (%)", "Exam Score", h=430)
    fig2.update_layout(
        showlegend=True,
        legend=dict(title_text="Motivation Level",
                    yanchor="top", y=1, xanchor="left", x=1.05,
                    bgcolor="rgba(255,255,255,0.85)"),
        margin=dict(r=140),
        xaxis=dict(domain=[0, 0.68]),
    )
    fig2.update_layout(xaxis3=dict(title_text=""))
    st.plotly_chart(fig2, use_container_width=True)

# =============================================================================
# SECTION 2 — BEHAVIORAL ANALYSIS
# Scatter Hours × Score by Income + two line charts stacked
# =============================================================================
st.markdown("""
<div class="sec-wrap">
  <div class="sec-eyebrow">02 — Behavioral Levers</div>
  <div class="sec-title">Study Hours, Tutoring, and the Socioeconomic Lens</div>
  <div class="sec-desc">
    Additional study hours produce steady score gains, while tutoring follows an inverted-U
    pattern that is beneficial up to about 6 sessions, after which returns diminish.
    Stratifying hours by family income reveals that at equivalent study time, high-income
    students score marginally higher, suggesting structural resource advantages beyond raw effort.
  </div>
</div>
<hr class="sec-rule">
""", unsafe_allow_html=True)

col_s2, col_lines = st.columns([1.5, 1])

with col_s2:
    # Chart 3 — Scatter: Study Hours × Score by Family Income
    # Matches: Scatter_Hours_Score.png parameters exactly
    color_income   = {"Low": "#EF476F", "Medium": "#FFD166", "High": "#06D6A0"}
    ordinal_income = ["High", "Medium", "Low"]

    fig3 = px.scatter(
        df, x="Hours_Studied_Jittered", y="Exam_Score",
        color="Family_Income",
        color_discrete_map=color_income,
        category_orders={"Family_Income": ordinal_income},
        opacity=0.5, trendline="ols",
        marginal_x="histogram", marginal_y="box",
        labels={"Hours_Studied_Jittered": "Weekly Study Hours",
                "Exam_Score": "Exam Score"},
    )
    fig3.update_traces(
        marker=dict(size=6, line=dict(width=0.5, color="white")),
        selector=dict(mode="markers", type="scatter"),
    )
    fig3.update_traces(
        line=dict(width=2.5),
        selector=dict(mode="lines"),
    )
    fig3 = polish_layout(fig3,
        "Exam Score vs Weekly Study Hours by Family Income",
        "Weekly Study Hours", "Exam Score", h=430)
    fig3.update_layout(
        showlegend=True,
        legend=dict(title_text="Family Income",
                    yanchor="top", y=1, xanchor="left", x=1.05,
                    bgcolor="rgba(255,255,255,0.85)"),
        margin=dict(r=140),
        xaxis=dict(domain=[0, 0.68]),
    )
    fig3.update_layout(xaxis3=dict(title_text=""))
    st.plotly_chart(fig3, use_container_width=True)

with col_lines:
    # Chart 4 — Line: Study Hours → Score
    # Matches: Line_Hours_Studied.png — bins and labels from script
    hrs_max = int(df["Hours_Studied"].max())  # 44
    fig4 = make_line(
        "Hours_Studied",
        "Trend of Average Exam Score by Weekly Study Hours",
        "#118AB2", "Weekly Study Hours",
        bin_spec=(
            [0, 8, 16, 24, 32, df["Hours_Studied"].max()],
            ["0–8 hrs", "9–16 hrs", "17–24 hrs", "25–32 hrs", f"33–{hrs_max} hrs"],
        ),
        h=205,
    )
    st.plotly_chart(fig4, use_container_width=True)

    # Chart 5 — Line: Tutoring Sessions → Score
    # Matches: Line_Tutoring_Sessions.png — tick0=0, dtick=1
    fig5 = make_line(
        "Tutoring_Sessions",
        "Trend of Average Exam Score by Tutoring Sessions",
        "#06D6A0", "Number of Tutoring Sessions",
        int_ticks=True, h=205,
    )
    st.plotly_chart(fig5, use_container_width=True)

# =============================================================================
# SECTION 3 — SUPPORT ENVIRONMENT
# 3 violin plots: Motivation, Parental Involvement, Teacher Quality
# =============================================================================
st.markdown("""
<div class="sec-wrap">
  <div class="sec-eyebrow">03 — Support Environment</div>
  <div class="sec-title">Motivation, Parental Involvement, and Teacher Quality</div>
  <div class="sec-desc">
    Motivation level widens the performance variance without substantially shifting the median.
    Parental involvement and teacher quality each independently shift the score distribution
    upward, with higher levels consistently associated with better outcomes.
  </div>
</div>
<hr class="sec-rule">
""", unsafe_allow_html=True)

v1, v2, v3 = st.columns(3)
ORD = ["High", "Medium", "Low"]
PAL = {"High": "#06D6A0", "Medium": "#118AB2", "Low": "#EF476F"}

with v1:
    # Chart 6 — Violin: Motivation Level
    st.plotly_chart(
        make_violin("Motivation_Level",
                    "Distribution of Exam Scores by Motivation Level",
                    "Motivation Level", PAL, ORD),
        use_container_width=True,
    )
with v2:
    # Chart 7 — Violin: Parental Involvement
    st.plotly_chart(
        make_violin("Parental_Involvement",
                    "Distribution of Exam Scores by Parental Involvement",
                    "Parental Involvement", PAL, ORD),
        use_container_width=True,
    )
with v3:
    # Chart 8 — Violin: Teacher Quality  (filter Unknown)
    st.plotly_chart(
        make_violin("Teacher_Quality",
                    "Distribution of Exam Scores by Teacher Quality",
                    "Teacher Quality", PAL, ORD, filter_vals=["Unknown"]),
        use_container_width=True,
    )

# =============================================================================
# SECTION 4 — SOCIOECONOMIC IMPACT
# 3 violin plots: Family Income, Access to Resources, Parental Education Level
# =============================================================================
st.markdown("""
<div class="sec-wrap">
  <div class="sec-eyebrow">04 — Socioeconomic Impact</div>
  <div class="sec-title">Income, Resource Access, and Intergenerational Education Effects</div>
  <div class="sec-desc">
    Family income, access to learning resources, and parental education collectively
    define the structural ceiling on student performance. These factors represent
    systemic equity gaps that cannot be closed by effort alone and require policy-level interventions.
  </div>
</div>
<hr class="sec-rule">
""", unsafe_allow_html=True)

e1, e2, e3 = st.columns(3)

with e1:
    # Chart 9 — Violin: Family Income
    # Family Income uses Medium=#FFD166 (amber), not #118AB2 blue
    pal_income = {"High": "#06D6A0", "Medium": "#FFD166", "Low": "#EF476F"}
    st.plotly_chart(
        make_violin("Family_Income",
                    "Distribution of Exam Scores by Family Income",
                    "Family Income", pal_income, ORD),
        use_container_width=True,
    )
with e2:
    # Chart 10 — Violin: Access to Resources
    st.plotly_chart(
        make_violin("Access_to_Resources",
                    "Distribution of Exam Scores by Access to Resources",
                    "Access to Resources", PAL, ORD),
        use_container_width=True,
    )
with e3:
    # Chart 11 — Violin: Parental Education Level  (filter Unknown / Others)
    pal_edu = {"Postgraduate": "#06D6A0", "College": "#FFD166", "High School": "#EF476F"}
    edu_order = ["Postgraduate", "College", "High School"]
    st.plotly_chart(
        make_violin("Parental_Education_Level",
                    "Distribution of Exam Scores by Parental Education Level",
                    "Parental Education Level", pal_edu, edu_order,
                    filter_vals=["Unknown", "Others"]),
        use_container_width=True,
    )

# =============================================================================
# SECTION 5 — SYSTEMIC ANALYSIS
# Correlation heatmap (left) + Cross-tab heatmap Motivation × Parental (right)
# Replaces Parallel Categories: the cross-tab is cleaner and more actionable.
# =============================================================================
st.markdown("""
<div class="sec-wrap">
  <div class="sec-eyebrow">05 — Systemic Analysis</div>
  <div class="sec-title">Correlations and the Compound Effect of Motivation and Parental Support</div>
  <div class="sec-desc">
    The correlation matrix quantifies all pairwise numerical relationships. Attendance and
    study hours emerge as the two strongest predictors. The cross-tab reveals that
    parental involvement can partially compensate for low motivation: a student with low
    motivation but high parental involvement (67.7) outperforms a highly motivated student
    with low parental support (66.8).
  </div>
</div>
<hr class="sec-rule">
""", unsafe_allow_html=True)

sys_l, sys_r = st.columns(2)

with sys_l:
    # Chart 12 — Correlation Heatmap
    # Matches: Heatmap_Correlation.png exactly (textfont=13, font=14, RdBu_r, thickness=18, len=0.85)
    num_df = df.select_dtypes(include=[np.number]).drop(
        columns=["Attendance_Jittered", "Previous_Scores_Jittered",
                 "Hours_Studied_Jittered", "Sleep_Hours_Jittered"],
        errors="ignore",
    )
    corr_matrix = num_df.corr().round(2)
    label_map = {
        "Hours_Studied": "Hours Studied", "Attendance": "Attendance",
        "Sleep_Hours": "Sleep Hours", "Previous_Scores": "Previous Scores",
        "Tutoring_Sessions": "Tutoring Sessions",
        "Physical_Activity": "Physical Activity", "Exam_Score": "Exam Score",
    }
    corr_display = corr_matrix.rename(index=label_map, columns=label_map)

    fig12 = px.imshow(
        corr_display, text_auto=".2f", aspect="auto",
        color_continuous_scale="RdBu_r", zmin=-1, zmax=1,
    )
    fig12.update_traces(textfont=dict(size=13))
    fig12.update_layout(
        title=dict(text="Pairwise Correlations among Numerical Variables",
                   x=0.5, xanchor="center"),
        template="plotly_white",
        font=dict(family="Arial", size=14),
        height=440,
        margin=dict(t=52, b=30, l=140, r=30),
        paper_bgcolor="white",
        coloraxis_colorbar=dict(
            title=dict(text="Correlation", side="top"),
            thickness=18, len=0.85,
        ),
    )
    st.plotly_chart(fig12, use_container_width=True)

with sys_r:
    # Chart 13 — Cross-tab Heatmap: Motivation × Parental Involvement → Mean Exam Score
    # Matches: Heatmap_MeanScore_Motivation_Parental.png exactly
    # (textfont=16, font=14, RdYlGn, zmin/zmax from data, thickness=18, len=0.8)
    cross_order_mot = ["Low", "Medium", "High"]
    cross_order_par = ["Low", "Medium", "High"]
    pivot_df = (
        df.groupby(["Motivation_Level", "Parental_Involvement"], observed=True)["Exam_Score"]
        .mean().round(1).reset_index()
        .pivot(index="Motivation_Level", columns="Parental_Involvement", values="Exam_Score")
    )
    pivot_df = pivot_df.loc[cross_order_mot, cross_order_par]

    fig13 = px.imshow(
        pivot_df, text_auto=True, aspect="auto",
        color_continuous_scale="RdYlGn",
        zmin=pivot_df.values.min() - 0.5,
        zmax=pivot_df.values.max() + 0.5,
        labels=dict(x="Parental Involvement",
                    y="Motivation Level", color="Avg Exam Score"),
    )
    fig13.update_traces(textfont=dict(size=16))
    fig13.update_layout(
        title=dict(text="Average Exam Score by Motivation Level and Parental Involvement",
                   x=0.5, xanchor="center"),
        template="plotly_white",
        font=dict(family="Arial", size=14),
        height=440,
        margin=dict(t=52, b=30, l=110, r=30),
        paper_bgcolor="white",
        coloraxis_colorbar=dict(
            title=dict(text="Avg Score", side="top"),
            thickness=18, len=0.8,
        ),
        xaxis=dict(title_text="Parental Involvement", side="bottom"),
        yaxis=dict(title_text="Motivation Level"),
    )
    st.plotly_chart(fig13, use_container_width=True)

# =============================================================================
# FOOTER
# =============================================================================
st.markdown("""
<hr style="border:none;border-top:1.5px solid #DDE3EC;margin:40px 0 18px 0;">
<p style="text-align:center;font-size:0.73rem;color:#94A3B8;font-family:Arial;">
    Academic Performance Analytics Dashboard &nbsp;&nbsp;|&nbsp;&nbsp;
    Foundations of Business Analytics
</p>
""", unsafe_allow_html=True)
