"""
app.py — Academic Performance Dashboard (PIXEL-PERFECT FINAL EDITION V7)
Definitive axial flushing, borderless KPIs, and spatial balance for Heatmap/Scatter.
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import os

# -----------------------------------------------------------------------------
# 1. Page Config & CSS Styling
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Academic Analytics Dashboard",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
    section[data-testid="stSidebar"] { width: 260px !important; }
    /* Global container styling */
    div[data-testid="stVerticalBlockBorderWrapper"] {
        border-radius: 8px !important;
        border: 1px solid #E3E5E8 !important;
        padding: 12px !important;
        margin-bottom: 15px !important;
    }
    .sec-hdr {
        font-size: 0.95rem; font-weight: 800; color: #6B7280;
        margin-bottom: 8px; text-transform: capitalize; letter-spacing: 0.05em;
    }
    .kpi-box {
        text-align: center; padding: 12px; background: #FFFFFF; 
        border: 1px solid #EDF0F3; border-radius: 8px; min-height: 90px;
    }
    .kpi-val { font-size: 1.8rem; font-weight: 700; color: #111827; margin-bottom: 2px; }
    .kpi-lbl { font-size: 0.75rem; color: #6B7280; text-transform: uppercase; font-weight: 600; }
    .stPlotlyChart { margin-bottom: -15px !important; }
</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 2. Data Loading & Sidebar
# -----------------------------------------------------------------------------
@st.cache_data
def load_data():
    return pd.read_csv("data/StudentPerformanceFactors_cleaned.csv")

df_raw = load_data()

st.sidebar.markdown("### Selection Filters")
sel_school = st.sidebar.selectbox("Institution Type", ["All"] + sorted(df_raw["School_Type"].unique()))
sel_gender = st.sidebar.selectbox("Student Gender",  ["All"] + sorted(df_raw["Gender"].unique()))

df = df_raw.copy()
if sel_school != "All": df = df[df["School_Type"] == sel_school]
if sel_gender != "All": df = df[df["Gender"]      == sel_gender]

# -----------------------------------------------------------------------------
# 3. VERBATIM HELPERS (TRUE AXIAL FLUSHING)
# -----------------------------------------------------------------------------
def polish_layout(fig, title_text, x_title=None, y_title=None, height=280):
    fig.update_layout(
        title=dict(text=title_text, x=0.5, xanchor='center', font=dict(size=14)),
        template="plotly_white", font=dict(family="Arial", size=12),
        showlegend=False, bargap=0.1, height=height,
        margin=dict(t=50, b=50, l=60, r=40)
    )
    if x_title: fig.update_xaxes(title_text=x_title, showgrid=False)
    if y_title: fig.update_yaxes(title_text=y_title, showgrid=True, gridcolor='lightgray')
    else: fig.update_yaxes(showgrid=True, gridcolor='lightgray')
    return fig

def create_true_flush_histogram(df, col, title, x_label, color, bins_meta):
    c_min, c_max, n_bins = bins_meta
    
    fig = px.histogram(df, x=col, color_discrete_sequence=[color])
    fig.update_traces(xbins=dict(start=c_min, end=c_max, size=5), marker_line_width=1.0, marker_line_color='black')
    
    fig.update_layout(
        bargap=0, bargroupgap=0,
        title=dict(text=title, x=0.5, xanchor='center', font=dict(size=16, color='#1F2937')),
        template="plotly_white", font=dict(family="Arial", size=13),
        showlegend=False, height=380,
        margin=dict(t=50, b=50, l=70, r=30)
    )
    
    fig.update_xaxes(
        range=[c_min, c_max], constrain='domain',
        title_text=x_label, showgrid=False,
        showline=True, linewidth=2, linecolor='black',
        ticks='outside', tickwidth=2, tickcolor='black', ticklen=8,
        tickmode='linear', tick0=c_min, dtick=5,
        zeroline=False, fixedrange=True
    )
    fig.update_yaxes(
        rangemode='tozero',
        title_text="Count of Students", showgrid=False,
        showline=True, linewidth=2, linecolor='black',
        ticks='outside', tickwidth=2, tickcolor='black', ticklen=8,
        zeroline=False, fixedrange=True
    )
    return fig

# -----------------------------------------------------------------------------
# 4. RENDER DASHBOARD
# -----------------------------------------------------------------------------
st.markdown("<h2>Academic Performance Analytics Dashboard</h2>", unsafe_allow_html=True)

# KPI Section - NO Container Border as requested
k1, k2, k3, k4 = st.columns(4)
with k1: st.markdown(f'<div class="kpi-box"><div class="kpi-val">{len(df):,}</div><div class="kpi-lbl">Total Students</div></div>', unsafe_allow_html=True)
with k2: st.markdown(f'<div class="kpi-box"><div class="kpi-val">{df["Exam_Score"].mean():.1f}</div><div class="kpi-lbl">Mean Exam Score</div></div>', unsafe_allow_html=True)
with k3: st.markdown(f'<div class="kpi-box"><div class="kpi-val">{df["Attendance"].mean():.1f}%</div><div class="kpi-lbl">Avg Attendance</div></div>', unsafe_allow_html=True)
with k4: st.markdown(f'<div class="kpi-box"><div class="kpi-val">{df["Hours_Studied"].mean():.1f}h</div><div class="kpi-lbl">Study Hours</div></div>', unsafe_allow_html=True)

# Section 1
st.markdown('<div class="sec-hdr">01 / Frequency Distribution & Baseline Profiles</div>', unsafe_allow_html=True)
with st.container(border=True):
    col_h1, col_h2 = st.columns(2)
    with col_h1:
        st.plotly_chart(create_true_flush_histogram(df, "Exam_Score", "Distribution of Exam Scores", "Final Exam Score Result", "#9BC2E6", (55, 100, 9)), use_container_width=True)
    with col_h2:
        st.plotly_chart(create_true_flush_histogram(df, "Attendance", "Distribution of Class Attendance (%)", "Course Attendance Percentage", "#9BC2E6", (60, 100, 8)), use_container_width=True)

# Section 2
st.markdown('<div class="sec-hdr">02 / Demographic Segmentation & Socioeconomic Context</div>', unsafe_allow_html=True)
with st.container(border=True):
    c1, c2, c3, c4 = st.columns(4)
    pie_configs = [
        ('Family_Income', 'Family Income', ["#EF476F", "#FFD166", "#06D6A0"], ["Low", "Medium", "High"]),
        ('School_Type', 'School Type', ["#118AB2", "#EF476F"], None),
        ('Learning_Disabilities', 'Disabilities', ["#118AB2", "#FFD166"], None),
        ('Parental_Education_Level', 'Parent Education', ["#EF476F", "#FFD166", "#06D6A0", "#118AB2", "#073B4C"], None),
    ]
    for idx, (col, name, colors, order) in enumerate(pie_configs):
        p_df = df[col].value_counts().reset_index(); p_df.columns = [col, 'Count']
        if order: p_df[col] = pd.Categorical(p_df[col], categories=order, ordered=True); p_df = p_df.sort_values(col)
        else: p_df = p_df.sort_values('Count', ascending=False)
        f_p = px.pie(p_df, values='Count', names=col, color_discrete_sequence=colors, hole=0.4)
        f_p.update_traces(textposition='inside', textinfo='percent+label', marker=dict(line=dict(color='#FFFFFF', width=2)))
        f_p = polish_layout(f_p, f"Distribution by {name}", height=250)
        f_p.update_layout(showlegend=False, margin=dict(t=30, b=20, l=10, r=10))
        target = [c1, c2, c3, c4][idx]
        with target: st.plotly_chart(f_p, use_container_width=True)

# Section 3
st.markdown('<div class="sec-hdr">03 / Behavioral Dynamics: Performance Drivers</div>', unsafe_allow_html=True)
with st.container(border=True):
    temp_df = df.copy(); np.random.seed(42)
    temp_df['Attendance_Jittered'] = temp_df['Attendance'] + np.random.uniform(-0.4, 0.4, size=len(temp_df))
    o_mot = ["Low", "Medium", "High"]
    c_mot = {"High": "#06D6A0", "Medium": "#118AB2", "Low": "#EF476F"}
    
    f_s1 = px.scatter(temp_df, x="Attendance_Jittered", y="Exam_Score", color="Motivation_Level",
                      color_discrete_map=c_mot, category_orders={"Motivation_Level": o_mot},
                      opacity=0.6, marginal_y="box", trendline="ols", trendline_scope="overall")
    
    # Precise trace correction for professional aesthetics
    for trace in f_s1.data:
        if trace.type == 'box':
            # Remove messy individual points to make the box plots clean
            trace.update(line=dict(width=2), opacity=0.9, boxpoints=False)
        if "Trendline" in getattr(trace, 'name', ''):
            # Ensure bold black contrast on the main plot
            trace.update(line=dict(color='black', width=3.5), xaxis='x1', yaxis='y1')
            
    f_s1.update_traces(marker=dict(size=5, line=dict(width=0.3, color='white')), selector=dict(mode='markers', type='scatter', xaxis='x1'))
    
    f_s1.update_layout(
        title=dict(text="Analysis of Course Attendance and Motivation on Exam Outcomes", x=0.5, xanchor='center', font=dict(size=16)),
        template="plotly_white", font=dict(family="Arial", size=12), height=450,
        showlegend=True,
        legend=dict(
            orientation="h", y=1.01, x=0.5, xanchor="center", yanchor="bottom", title="",
            font=dict(size=12)
        ),
        margin=dict(r=30, t=70, b=50, l=80),
        xaxis=dict(domain=[0, 0.78], title="Course Attendance Percentage (%)", showgrid=False, range=[59, 101]),
        yaxis=dict(title="Final Exam Score Requirement", showgrid=True, gridcolor='#F3F4F6', range=[55, 105]),
        xaxis2=dict(domain=[0.82, 1.0], title=None, showticklabels=False, showline=False, showgrid=False),
        yaxis2=dict(title=None, showticklabels=False)
    )
    st.plotly_chart(f_s1, use_container_width=True)

with st.container(border=True):
    t1, t2, t3 = st.columns(3)
    with t1:
        line_df = df.groupby('Sleep_Hours', as_index=False, observed=True)['Exam_Score'].mean()
        f_l = px.line(line_df, x='Sleep_Hours', y="Exam_Score", markers=True)
        f_l.update_traces(line=dict(color='#EF476F', width=3), marker=dict(size=10, color="#1F2937"))
        f_l.update_xaxes(tickmode='linear', tick0=4, dtick=1, range=[3.5, 10.5])
        f_l.update_yaxes(range=[59, 76], tickmode='array', tickvals=[60, 65, 70, 75])
        st.plotly_chart(polish_layout(f_l, "Trend of Average Exam Score by Nightly Sleep Hours", "Nightly Sleep Hours", "Average Exam Score", height=300), use_container_width=True)
    with t2:
        # Binned Study Hours
        bins = [0, 8, 16, 24, 32, 44]
        labels = ['0-8 hrs', '9-16 hrs', '17-24 hrs', '25-32 hrs', '33-44 hrs']
        df_copy = df.copy()
        df_copy['Hours_Studied_Bin'] = pd.cut(df_copy['Hours_Studied'], bins=bins, labels=labels, right=True, include_lowest=True)
        line_df2 = df_copy.groupby('Hours_Studied_Bin', as_index=False, observed=True)['Exam_Score'].mean()
        f_l2 = px.line(line_df2, x='Hours_Studied_Bin', y="Exam_Score", markers=True)
        f_l2.update_traces(line=dict(color='#118AB2', width=3), marker=dict(size=10, color="#1F2937"))
        f_l2.update_xaxes(range=[-0.5, 4.5])
        f_l2.update_yaxes(range=[63, 73], tickmode='array', tickvals=[64, 66, 68, 70, 72])
        st.plotly_chart(polish_layout(f_l2, "Trend of Average Exam Score by Weekly Study Hours", "Weekly Study Hours Category", "Average Exam Score", height=300), use_container_width=True)
    with t3:
        l_df3 = df.groupby('Tutoring_Sessions', as_index=False, observed=True)['Exam_Score'].mean()
        f_l3 = px.line(l_df3, x='Tutoring_Sessions', y="Exam_Score", markers=True)
        f_l3.update_traces(line=dict(color='#06D6A0', width=3), marker=dict(size=10, color="#1F2937"))
        f_l3.update_xaxes(tickmode='linear', tick0=0, dtick=1, range=[-0.5, 8.5])
        f_l3.update_yaxes(range=[65, 73], tickmode='array', tickvals=[66, 68, 70, 72])
        st.plotly_chart(polish_layout(f_l3, "Trend of Average Exam Score by Tutoring Frequency", "Number of Tutoring Sessions", "Average Exam Score", height=300), use_container_width=True)

# Section 4
st.markdown('<div class="sec-hdr">04 / Systemic Analysis: Inequity & Interdependency</div>', unsafe_allow_html=True)
with st.container(border=True):
    a1, a2 = st.columns([1.1, 1])
    with a1:
        f_c = px.density_contour(df, x="Previous_Scores", y="Exam_Score", marginal_x="histogram", marginal_y="histogram", color_discrete_sequence=['#EF476F'])
        f_c.update_layout(
            title=dict(text="Density Distribution of Final Exam by Previous Scores", x=0.5, xanchor='center', font=dict(size=14)),
            height=360,
            xaxis=dict(title="Previous Exam Scores"),
            yaxis=dict(title="Final Exam Score")
        )
        st.plotly_chart(f_c, use_container_width=True)
    with a2:
        num_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        c_m = df[num_cols].corr().round(2)
        f_h = px.imshow(c_m, text_auto=True, color_continuous_scale="RdBu_r", zmin=-1, zmax=1)
        # Centering heatmap and colorbar
        f_h.update_layout(title=dict(text="Pairwise Correlation Analysis of Key Metrics", x=0.5, xanchor='center', font=dict(size=15)),
                          font=dict(size=10), height=360, margin=dict(t=60, b=20, l=50, r=80),
                          coloraxis_colorbar=dict(x=0.88, thickness=15, len=0.85, title="Correlation"))
        st.plotly_chart(f_h, use_container_width=True)

with st.container(border=True):
    bx1, bx2 = st.columns(2)
    with bx1:
        f_v = px.box(df, x='Access_to_Resources', y="Exam_Score", color='Access_to_Resources',
                     color_discrete_map={"High": "#06D6A0", "Medium": "#118AB2", "Low": "#EF476F"},
                     category_orders={'Access_to_Resources': ["High", "Medium", "Low"]})
        st.plotly_chart(polish_layout(f_v, "Distribution of Exam Score by Resource Equity", "Resource Equity Level", "Final Exam Score", height=320), use_container_width=True)
    with bx2:
        peer_df = df.groupby('Peer_Influence', as_index=False)['Exam_Score'].mean().sort_values('Exam_Score', ascending=False)
        f_p2 = px.bar(peer_df, x='Peer_Influence', y='Exam_Score', color='Peer_Influence',
                      color_discrete_sequence=["#118AB2", "#FFD166", "#EF476F"])
        f_p2 = polish_layout(f_p2, "Average Exam Score by Peer Influence", "Peer Influence Level", "Average Exam Score", height=320)
        f_p2.update_yaxes(range=[60, 72])
        st.plotly_chart(f_p2, use_container_width=True)
