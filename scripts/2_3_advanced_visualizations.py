import pandas as pd
import numpy as np
import plotly.express as px
import os

base_dir = r"C:\Users\Y\Desktop\Foundations-of-Business-Analytics-Assignment"
data_path = os.path.join(base_dir, "data", "StudentPerformanceFactors_cleaned.csv")
plots_dir = os.path.join(base_dir, "plots")

df = pd.read_csv(data_path)
# Shuffle dataframe globally to prevent Z-order category overlap in scatter/bubble plots
df = df.sample(frac=1, random_state=42).reset_index(drop=True)

# Ensure output subdirectories exist
for sub in ["scatter_plots", "advanced", "heatmaps"]:
    os.makedirs(os.path.join(plots_dir, sub), exist_ok=True)

def polish_layout(fig, title_text, x_title=None, y_title=None):
    """Apply consistent, professional layout. Title must be pure business label — no chart-type prefix."""
    fig.update_layout(
        title=dict(text=title_text, x=0.5, xanchor='center'),
        template="plotly_white",
        font=dict(family="Arial", size=14)
    )
    if x_title: fig.update_xaxes(title_text=x_title, showgrid=False)
    if y_title: fig.update_yaxes(title_text=y_title, showgrid=True, gridcolor='lightgray')
    else: fig.update_yaxes(showgrid=True, gridcolor='lightgray')
    return fig

# Jitter arrays for discrete integer axes (display-only, not stored in source data)
np.random.seed(42)
df['Attendance_Jittered']     = df['Attendance']     + np.random.uniform(-0.4, 0.4, size=len(df))
df['Previous_Scores_Jittered']= df['Previous_Scores']+ np.random.uniform(-0.4, 0.4, size=len(df))

# To fix Z-order overplotting without ugly hollow rings:
# We sort the order so that the largest/densest class ('Low' red) is drawn LAST in the list (which means First on canvas/Bottom layer)
# and 'High' (green) is drawn FIRST in the list (Last on canvas/Top layer).
ordinal_motivation = ["Low", "Medium", "High"]
color_motivation   = {"High": "#06D6A0", "Medium": "#118AB2", "Low": "#EF476F"}


# =============================================================================
# 1. SCATTER PLOTS WITH MARGINAL DISTRIBUTIONS
# Legend anchored OUTSIDE the plot area (x=1.05) — never overlaps Data-Ink
# Title = pure business label — no "Scatter Plot with Marginals:" prefix
# =============================================================================
fig_s1 = px.scatter(
    df, x="Attendance_Jittered", y="Exam_Score", color="Motivation_Level",
    color_discrete_map=color_motivation,
    category_orders={"Motivation_Level": ordinal_motivation},
    opacity=0.5, trendline="ols",
    marginal_x="histogram", marginal_y="box"
)
fig_s1.update_traces(marker=dict(size=6, line=dict(width=0.5, color='white')), selector=dict(mode='markers', type='scatter'))
fig_s1.update_traces(line=dict(color="#073B4C", width=4), selector=dict(mode='lines'))
fig_s1 = polish_layout(fig_s1, "Exam Score vs Class Attendance by Motivation Level",
                        "Attendance (%)", "Exam Score")
fig_s1.update_layout(
    legend=dict(yanchor="top", y=1, xanchor="left", x=1.05,
                bgcolor="rgba(255,255,255,0.85)"),
    margin=dict(r=20),
    xaxis=dict(domain=[0, 0.68])   # reserve 32% for right marginal panel
)
fig_s1.write_image(os.path.join(plots_dir, "scatter_plots", "Scatter_Attendance_Score.png"), scale=2)

fig_s2 = px.scatter(
    df, x="Previous_Scores_Jittered", y="Exam_Score", color="Internet_Access",
    color_discrete_map={"Yes": "#118AB2", "No": "#EF476F"},
    category_orders={"Internet_Access": ["Yes", "No"]},
    opacity=0.5, trendline="ols",
    marginal_x="histogram", marginal_y="box"
)
fig_s2.update_traces(marker=dict(size=6, line=dict(width=0.5, color='white')), selector=dict(mode='markers', type='scatter'))
fig_s2.update_traces(line=dict(color="#073B4C", width=4), selector=dict(mode='lines'))
fig_s2 = polish_layout(fig_s2, "Exam Score vs Previous Scores by Internet Access",
                        "Previous Score", "Exam Score")
fig_s2.update_layout(
    legend=dict(yanchor="top", y=1, xanchor="left", x=1.05,
                bgcolor="rgba(255,255,255,0.85)"),
    margin=dict(r=20),
    xaxis=dict(domain=[0, 0.68])
)
fig_s2.write_image(os.path.join(plots_dir, "scatter_plots", "Scatter_Previous_Score.png"), scale=2)

# Hours_Studied vs Exam_Score — stratified by Family_Income
df['Hours_Studied_Jittered'] = df['Hours_Studied'] + np.random.uniform(-0.4, 0.4, size=len(df))
color_income = {"Low": "#EF476F", "Medium": "#FFD166", "High": "#06D6A0"}
ordinal_income = ["High", "Medium", "Low"]

fig_s3 = px.scatter(
    df, x="Hours_Studied_Jittered", y="Exam_Score", color="Family_Income",
    color_discrete_map=color_income,
    category_orders={"Family_Income": ordinal_income},
    opacity=0.5, trendline="ols",
    marginal_x="histogram", marginal_y="box"
)
fig_s3.update_traces(marker=dict(size=6, line=dict(width=0.5, color='white')), selector=dict(mode='markers', type='scatter'))
fig_s3.update_traces(line=dict(color="#073B4C", width=4), selector=dict(mode='lines'))
fig_s3 = polish_layout(fig_s3, "Exam Score vs Weekly Study Hours by Family Income",
                        "Weekly Study Hours", "Exam Score")
fig_s3.update_layout(
    legend=dict(yanchor="top", y=1, xanchor="left", x=1.05,
                bgcolor="rgba(255,255,255,0.85)"),
    margin=dict(r=20),
    xaxis=dict(domain=[0, 0.68])
)
fig_s3.write_image(os.path.join(plots_dir, "scatter_plots", "Scatter_Hours_Score.png"), scale=2)



# =============================================================================
# 2. 2D DENSITY CONTOUR
# =============================================================================
fig_contour = px.density_contour(
    df, x="Previous_Scores", y="Exam_Score",
    color_discrete_sequence=['#E63946'],
    marginal_x="histogram", marginal_y="histogram"
)
fig_contour = polish_layout(fig_contour,
    "Density Distribution: Previous Scores and Final Exam Score",
    "Previous Score", "Exam Score")
fig_contour.write_image(os.path.join(plots_dir, "scatter_plots", "DensityContour_Previous_Exam.png"), scale=2)


# =============================================================================
# 3. MULTI-DIMENSIONAL BUBBLE CHART (FACETED)
# =============================================================================
fig_bubble = px.scatter(
    df, x="Attendance_Jittered", y="Exam_Score",
    size="Hours_Studied", color="Motivation_Level",
    color_discrete_map=color_motivation,
    category_orders={"Motivation_Level": ordinal_motivation},
    facet_col="Motivation_Level",
    labels={
        "Exam_Score": "Exam Score",
        "Attendance_Jittered": "Attendance (%)"
    },
    opacity=0.45, size_max=18,
    render_mode="svg"
)
# Make points slightly translucent but vibrant, no borders required since they are faceted
fig_bubble.update_traces(marker=dict(line=dict(width=0)), selector=dict(mode='markers', type='scatter'))

# Layout polishing specific to facets
fig_bubble.update_layout(
    title=dict(text="Exam Score vs Attendance by Motivation Level (Bubble Size = Study Hours)", x=0.5, xanchor='center'),
    template="plotly_white",
    width=1000, height=600,   # Widen to give 3 facets enough breathing room
    font=dict(family="Arial", size=14),
    showlegend=False
)
# Simply update gridlines and boundaries globally; Plotly Express automatically 
# handles deduplicating the Y-axis and X-axis titles natively on facets if left alone.
fig_bubble.update_yaxes(showgrid=True, gridcolor='lightgray', range=[50, 105])
fig_bubble.update_xaxes(showgrid=False, range=[58, 102])

# Clean up facet subplot titles (remove the 'Motivation_Level=' prefix)
fig_bubble.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))

fig_bubble.write_image(os.path.join(plots_dir, "advanced", "Bubble_Attendance_Score_Hrs.png"), scale=2)



# =============================================================================
# 4a. CLUSTERED BAR CHART (course-required advanced chart type)
# Shows COUNT of students across two categorical dimensions simultaneously.
# Demonstrates Preattentive Attribute of length; Y-axis starts at 0 per best practice.
# =============================================================================
cluster_df = df.groupby(['School_Type', 'Internet_Access']).size().reset_index(name='Count')
# Enforce logical ordering
cluster_df['School_Type']     = pd.Categorical(cluster_df['School_Type'],     categories=['Public','Private'],   ordered=True)
cluster_df['Internet_Access'] = pd.Categorical(cluster_df['Internet_Access'], categories=['Yes','No'],           ordered=True)
cluster_df = cluster_df.sort_values(['School_Type', 'Internet_Access'])

fig_cluster = px.bar(
    cluster_df, x='School_Type', y='Count', color='Internet_Access',
    barmode='group',
    color_discrete_map={'Yes': '#06D6A0', 'No': '#EF476F'},
    category_orders={'Internet_Access': ['Yes', 'No']}
)
fig_cluster = polish_layout(
    fig_cluster,
    'Student Count by School Type and Internet Access',
    'School Type', 'Number of Students'
)
fig_cluster.update_yaxes(range=[0, cluster_df['Count'].max() * 1.15])
fig_cluster.update_layout(
    showlegend=True,
    legend=dict(title='Internet Access', yanchor='top', y=0.99, xanchor='right', x=0.99)
)
fig_cluster.write_image(os.path.join(plots_dir, 'advanced', 'ClusteredBar_SchoolType_Internet.png'), scale=2)


# =============================================================================
# 4. PARALLEL CATEGORIES DIAGRAM (Sankey-lite)
# Ordinal dims sorted: Family_Income Low→Med→High; Motivation High→Med→Low
# =============================================================================
par_df = df.copy()
par_df['Score_Bin'] = pd.qcut(par_df['Exam_Score'], q=3,
                               labels=["Low Scorers", "Mid Scorers", "High Scorers"])
# Enforce ordinal ordering
for col, order in [
    ('Family_Income',       ['Low','Medium','High']),
    ('Access_to_Resources', ['Low','Medium','High']),
    ('Motivation_Level',    ['Low','Medium','High']),
]:
    par_df[col] = pd.Categorical(par_df[col], categories=order, ordered=True)

fig_par = px.parallel_categories(
    par_df,
    dimensions=['Family_Income', 'Access_to_Resources', 'Motivation_Level', 'Score_Bin'],
    color="Exam_Score", color_continuous_scale=px.colors.sequential.Teal
)
fig_par.update_layout(
    title=dict(text="Student Background Flow to Academic Outcome", x=0.5, xanchor='center'),
    font=dict(family="Arial", size=14),
    width=900,          # slightly wider than default (~700), not as wide as 1100
    margin=dict(l=80, r=160, t=80, b=60),
    coloraxis_colorbar=dict(
        x=1.05,
        y=0.6, len=0.6,
        title=dict(text="Exam Score", side="top")
    )
)
fig_par.write_image(os.path.join(plots_dir, "advanced", "ParallelCategories_BackgroundFlow.png"), scale=2)


# =============================================================================
# 5. CORRELATION HEATMAP
# =============================================================================
num_df = df.select_dtypes(include=[np.number]).drop(
    columns=['Attendance_Jittered', 'Previous_Scores_Jittered', 'Hours_Studied_Jittered'], errors='ignore'
)
corr_matrix = num_df.corr().round(2)

fig_heat = px.imshow(
    corr_matrix, text_auto=True, aspect="auto",
    color_continuous_scale="RdBu_r", zmin=-1, zmax=1
)
fig_heat.update_layout(
    title=dict(text="Pairwise Correlations among Numerical Features", x=0.5, xanchor='center'),
    font=dict(family="Arial", size=12)
)
fig_heat.write_image(os.path.join(plots_dir, "heatmaps", "Heatmap_Correlation.png"), scale=2)

print("Advanced Visualizations fully regenerated.")
