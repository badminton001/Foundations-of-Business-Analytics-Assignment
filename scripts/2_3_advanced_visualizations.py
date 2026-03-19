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
fig_s1.update_traces(line=dict(width=2.5), selector=dict(mode='lines'))
fig_s1 = polish_layout(fig_s1, "Exam Score vs Class Attendance by Motivation Level",
                        "Attendance (%)", "Exam Score")
fig_s1.update_layout(xaxis3=dict(title_text=''))  # suppress duplicate x-label on top marginal
fig_s1.update_layout(
    legend=dict(title_text="Motivation Level", yanchor="top", y=1, xanchor="left", x=1.05,
                bgcolor="rgba(255,255,255,0.85)"),
    margin=dict(r=20),
    xaxis=dict(domain=[0, 0.68])   # reserve 32% for right marginal panel
)
fig_s1.write_image(os.path.join(plots_dir, "scatter_plots", "Scatter_Attendance_Score.png"), scale=2)

color_peer   = {"Positive": "#06D6A0", "Neutral": "#FFD166", "Negative": "#EF476F"}
ordinal_peer = ["Negative", "Neutral", "Positive"]

fig_s2 = px.scatter(
    df, x="Previous_Scores_Jittered", y="Exam_Score", color="Peer_Influence",
    color_discrete_map=color_peer,
    category_orders={"Peer_Influence": ordinal_peer},
    opacity=0.5, trendline="ols",
    marginal_x="histogram", marginal_y="box"
)
fig_s2.update_traces(marker=dict(size=6, line=dict(width=0.5, color='white')), selector=dict(mode='markers', type='scatter'))
fig_s2.update_traces(line=dict(width=2.5), selector=dict(mode='lines'))
fig_s2 = polish_layout(fig_s2, "Exam Score vs Previous Scores by Peer Influence",
                        "Previous Score", "Exam Score")
fig_s2.update_layout(xaxis3=dict(title_text=''))  # suppress duplicate x-label on top marginal
fig_s2.update_layout(
    legend=dict(title_text="Peer Influence", yanchor="top", y=1, xanchor="left", x=1.05,
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
fig_s3.update_traces(line=dict(width=2.5), selector=dict(mode='lines'))
fig_s3 = polish_layout(fig_s3, "Exam Score vs Weekly Study Hours by Family Income",
                        "Weekly Study Hours", "Exam Score")
fig_s3.update_layout(xaxis3=dict(title_text=''))  # suppress duplicate x-label on top marginal
fig_s3.update_layout(
    legend=dict(title_text="Family Income", yanchor="top", y=1, xanchor="left", x=1.05,
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
fig_contour.write_image(os.path.join(plots_dir, "advanced", "DensityContour_Previous_Exam.png"), scale=2)


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
# 4b. STACKED BAR CHART (course-required advanced chart type)
# Shows how Access_to_Resources composition varies across Family_Income tiers.
# Reveals compound socioeconomic disadvantage: low-income students also tend to
# have lower resource access. Y-axis starts at 0 (bar chart best practice).
# =============================================================================
stack_df = df.groupby(['Family_Income', 'Access_to_Resources']).size().reset_index(name='Count')
income_order   = ['Low', 'Medium', 'High']
resource_order = ['Low', 'Medium', 'High']
stack_df['Family_Income']       = pd.Categorical(stack_df['Family_Income'],       categories=income_order,   ordered=True)
stack_df['Access_to_Resources'] = pd.Categorical(stack_df['Access_to_Resources'], categories=resource_order, ordered=True)
stack_df = stack_df.sort_values(['Family_Income', 'Access_to_Resources'])

fig_stack = px.bar(
    stack_df, x='Family_Income', y='Count', color='Access_to_Resources',
    barmode='stack',
    color_discrete_map={'Low': '#EF476F', 'Medium': '#118AB2', 'High': '#06D6A0'},
    category_orders={'Access_to_Resources': resource_order, 'Family_Income': income_order},
    text='Count',
)
fig_stack.update_traces(
    marker_line_color='white', marker_line_width=1.2,
    textposition='inside', textfont=dict(size=12, color='white'),
)
fig_stack = polish_layout(
    fig_stack,
    'Resource Access Composition by Family Income Level',
    'Family Income', 'Number of Students'
)
fig_stack.update_yaxes(range=[0, stack_df.groupby('Family_Income')['Count'].sum().max() * 1.08])
fig_stack.update_layout(
    showlegend=True,
    legend=dict(title='Access to Resources', yanchor='top', y=0.99, xanchor='right', x=0.99),
    bargap=0.35,
)
fig_stack.write_image(os.path.join(plots_dir, 'advanced', 'StackedBar_Income_Resources.png'), scale=2)


# =============================================================================
# 4. PARALLEL CATEGORIES DIAGRAM (Sankey-lite)
# Use go.Parcats for explicit per-dimension categoryarray control so that
# Low→Mid→High and Low Scorers→Mid Scorers→High Scorers are always top-to-bottom.
# =============================================================================
import plotly.graph_objects as go

par_df = df.copy()
par_df['Score_Bin'] = pd.qcut(par_df['Exam_Score'], q=3,
                               labels=["Low Scorers", "Mid Scorers", "High Scorers"])

dim_specs = [
    ('Family Income',        'Family_Income',       ['Low', 'Medium', 'High']),
    ('Access to Resources',  'Access_to_Resources', ['Low', 'Medium', 'High']),
    ('Motivation Level',     'Motivation_Level',    ['Low', 'Medium', 'High']),
    ('Academic Outcome',     'Score_Bin',           ['Low Scorers', 'Mid Scorers', 'High Scorers']),
]
dimensions = [
    go.parcats.Dimension(
        label=label,
        values=par_df[col],
        categoryarray=order,
    )
    for label, col, order in dim_specs
]

fig_par = go.Figure(go.Parcats(
    dimensions=dimensions,
    line=dict(
        color=par_df['Exam_Score'],
        colorscale=px.colors.sequential.Teal,
        showscale=True,
        colorbar=dict(
            x=1.05, y=0.6, len=0.6,
            title=dict(text="Exam Score", side="top"),
        ),
    ),
    arrangement='freeform',
))
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
    columns=['Attendance_Jittered', 'Previous_Scores_Jittered', 'Hours_Studied_Jittered',
             'Sleep_Hours_Jittered'], errors='ignore'
)
corr_matrix = num_df.corr().round(2)

label_map = {
    'Hours_Studied': 'Hours Studied', 'Attendance': 'Attendance',
    'Sleep_Hours': 'Sleep Hours', 'Previous_Scores': 'Previous Scores',
    'Tutoring_Sessions': 'Tutoring Sessions', 'Physical_Activity': 'Physical Activity',
    'Exam_Score': 'Exam Score',
}
corr_display = corr_matrix.rename(index=label_map, columns=label_map)

fig_heat = px.imshow(
    corr_display, text_auto=".2f", aspect="auto",
    color_continuous_scale="RdBu_r", zmin=-1, zmax=1
)
fig_heat.update_traces(textfont=dict(size=13))
fig_heat.update_layout(
    title=dict(text="Pairwise Correlations among Numerical Variables", x=0.5, xanchor='center'),
    template="plotly_white",
    font=dict(family="Arial", size=14),
    width=700, height=600,
    coloraxis_colorbar=dict(
        title=dict(text="Correlation", side="top"),
        thickness=18, len=0.85,
    )
)
fig_heat.write_image(os.path.join(plots_dir, "heatmaps", "Heatmap_Correlation.png"), scale=2)


# =============================================================================
# 6. CROSS-TAB MEAN SCORE HEATMAP
# Shows compound effect of Motivation Level × Parental Involvement on mean Exam Score.
# Reveals whether high motivation + high parental support creates amplified benefit.
# =============================================================================
cross_order_mot = ["Low", "Medium", "High"]
cross_order_par = ["Low", "Medium", "High"]
pivot_df = (
    df.groupby(["Motivation_Level", "Parental_Involvement"], observed=True)["Exam_Score"]
    .mean()
    .round(1)
    .reset_index()
    .pivot(index="Motivation_Level", columns="Parental_Involvement", values="Exam_Score")
)
pivot_df = pivot_df.loc[cross_order_mot, cross_order_par]

fig_cross = px.imshow(
    pivot_df,
    text_auto=True,
    color_continuous_scale="RdYlGn",
    zmin=pivot_df.values.min() - 0.5,
    zmax=pivot_df.values.max() + 0.5,
    aspect="auto",
    labels=dict(x="Parental Involvement", y="Motivation Level", color="Avg Exam Score"),
)
fig_cross.update_traces(textfont=dict(size=16))
fig_cross.update_layout(
    title=dict(text="Average Exam Score by Motivation Level and Parental Involvement", x=0.5, xanchor="center"),
    template="plotly_white",
    font=dict(family="Arial", size=14),
    width=620, height=480,
    coloraxis_colorbar=dict(
        title=dict(text="Avg Score", side="top"),
        thickness=18, len=0.8,
    ),
    xaxis=dict(title_text="Parental Involvement", side="bottom"),
    yaxis=dict(title_text="Motivation Level"),
)
fig_cross.write_image(os.path.join(plots_dir, "heatmaps", "Heatmap_MeanScore_Motivation_Parental.png"), scale=2)

print("Advanced Visualizations fully regenerated.")
