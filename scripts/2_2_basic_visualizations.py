import pandas as pd
import numpy as np
import plotly.express as px
import os

base_dir = r"C:\Users\Y\Desktop\Foundations-of-Business-Analytics-Assignment"
data_path = os.path.join(base_dir, "data", "StudentPerformanceFactors_cleaned.csv")
plots_dir = os.path.join(base_dir, "plots")

df = pd.read_csv(data_path)

# Ensure output subdirectories exist
for sub in ["histograms", "box_violin_plots", "pie_charts", "line_charts", "bar_charts"]:
    os.makedirs(os.path.join(plots_dir, sub), exist_ok=True)

def polish_layout(fig, title_text, x_title=None, y_title=None, y_range=None):
    fig.update_layout(
        title=dict(text=title_text, x=0.5, xanchor='center'),
        template="plotly_white",
        font=dict(family="Arial", size=14),
        showlegend=False,
        bargap=0.1
    )
    if x_title: fig.update_xaxes(title_text=x_title, showgrid=False)
    if y_title: fig.update_yaxes(title_text=y_title, showgrid=True, gridcolor='lightgray')
    else: fig.update_yaxes(showgrid=True, gridcolor='lightgray')
    if y_range: fig.update_yaxes(range=y_range)
    return fig


# =============================================================================
# 1. HISTOGRAMS — Pure-count distributions of key numeric inputs
# Titles: direct business labels, NO chart-type prefix
# Core Rules: 5-20 non-overlapping bins, equal bin width=(Max-Min)/Bins, span full range.
# =============================================================================
def create_strict_histogram(df, col, title, x_label, color, num_bins,
                            override_min=None, override_max=None, x_dtick=None, x_range=None):
    col_min = override_min if override_min is not None else df[col].min()
    col_max = override_max if override_max is not None else df[col].max()
    bin_width = (col_max - col_min) / num_bins
    tick_step = x_dtick if x_dtick is not None else bin_width

    fig = px.histogram(df, x=col, color_discrete_sequence=[color])
    fig.update_traces(
        xbins=dict(start=col_min, end=col_max, size=bin_width),
        marker_line_color='black',
        marker_line_width=1.5
    )

    fig.update_layout(
        title=dict(text=title, x=0.5, xanchor='center'),
        template="plotly_white",
        font=dict(family="Arial", size=14),
        bargap=0,
        showlegend=False
    )

    x_axis = dict(
        title_text=x_label,
        showgrid=False,
        showline=True, linewidth=1.5, linecolor='black',
        ticks='outside', tickwidth=1.5, tickcolor='black', ticklen=6,
        tickmode='linear', tick0=col_min, dtick=tick_step,
    )
    if x_range:
        x_axis['range'] = x_range
    fig.update_xaxes(**x_axis)

    fig.update_yaxes(
        title_text="Count of Students",
        showgrid=False,
        showline=True, linewidth=1.5, linecolor='black',
        ticks='outside', tickwidth=1.5, tickcolor='black', ticklen=6,
        rangemode='tozero'
    )

    return fig

# 1. Exam_Score: range 55-100. Using 55-100 (span 45), 45 bins (width=1.0) to reveal the sharp right-skew tail
fig1 = create_strict_histogram(df, "Exam_Score", "Distribution of Exam Scores", "Exam Score", "#9BC2E6", 45, 55, 100,
                               x_dtick=5, x_range=[55, 100])
fig1.write_image(os.path.join(plots_dir, "histograms", "Histogram_Exam_Score.png"), scale=2)

# 2. Attendance: range 60-100. Using 60-100 (span 40), 8 bins (width=5.0)
fig2 = create_strict_histogram(df, "Attendance", "Distribution of Class Attendance (%)", "Attendance Percentage", "#9BC2E6", 8, 60, 100)
fig2.write_image(os.path.join(plots_dir, "histograms", "Histogram_Attendance.png"), scale=2)

# 3. Previous_Scores: range 50-100. Using 50-100 (span 50), 10 bins (width=5.0)
fig3 = create_strict_histogram(df, "Previous_Scores", "Distribution of Previous Scores", "Previous Score", "#9BC2E6", 10, 50, 100)
fig3.write_image(os.path.join(plots_dir, "histograms", "Histogram_Previous_Scores.png"), scale=2)

# 4. Hours_Studied: range 1-44. Using 0-45 (span 45), 9 bins (width=5.0)
fig4 = create_strict_histogram(df, "Hours_Studied", "Distribution of Weekly Study Hours", "Hours Studied (hrs/week)", "#9BC2E6", 9, 0, 45)
fig4.write_image(os.path.join(plots_dir, "histograms", "Histogram_Hours_Studied.png"), scale=2)

# 5. Sleep_Hours: discrete integers 4-10. Bins centered on each integer value (width=1).
fig5 = create_strict_histogram(df, "Sleep_Hours", "Distribution of Nightly Sleep Hours", "Sleep Hours (hrs/night)", "#9BC2E6", 7, 3.5, 10.5)
fig5.update_xaxes(tickmode='array', tickvals=list(range(4, 11)), ticktext=[str(i) for i in range(4, 11)])
fig5.write_image(os.path.join(plots_dir, "histograms", "Histogram_Sleep_Hours.png"), scale=2)

# 6. Tutoring_Sessions: discrete integers 0-8. Bins centered on each integer value (width=1).
fig6 = create_strict_histogram(df, "Tutoring_Sessions", "Distribution of Weekly Tutoring Sessions", "Number of Tutoring Sessions", "#9BC2E6", 9, -0.5, 8.5)
fig6.update_xaxes(tickmode='array', tickvals=list(range(0, 9)), ticktext=[str(i) for i in range(0, 9)])
fig6.write_image(os.path.join(plots_dir, "histograms", "Histogram_Tutoring_Sessions.png"), scale=2)

# 7. Physical_Activity: discrete integers 0-6. Bins centered on each integer value (width=1).
fig7 = create_strict_histogram(df, "Physical_Activity", "Distribution of Weekly Physical Activity", "Physical Activity (sessions/week)", "#9BC2E6", 7, -0.5, 6.5)
fig7.update_xaxes(tickmode='array', tickvals=list(range(0, 7)), ticktext=[str(i) for i in range(0, 7)])
fig7.write_image(os.path.join(plots_dir, "histograms", "Histogram_Physical_Activity.png"), scale=2)


# =============================================================================
# 2. VIOLIN / BOX PLOTS — Categorical features vs Exam_Score
# NO mean-bar charts. ONLY violin+box for any category vs target variable.
# Ordinal categories sorted logically: High → Medium → Low
# =============================================================================
ordinal_order = ["High", "Medium", "Low"]

for col, name, cat_palette in [
    ('Motivation_Level',    'Motivation Level',    {"High": "#06D6A0", "Medium": "#118AB2", "Low": "#EF476F"}),
    ('Teacher_Quality',     'Teacher Quality',     {"High": "#06D6A0", "Medium": "#118AB2", "Low": "#EF476F"}),
    ('Parental_Involvement','Parental Involvement', {"High": "#06D6A0", "Medium": "#118AB2", "Low": "#EF476F"}),
    ('Family_Income',       'Family Income',       {"High": "#06D6A0", "Medium": "#FFD166", "Low": "#EF476F"}),
    ]:
    # Exclude "Unknown" entries (data artefact from cleaning — not a meaningful quality level)
    df_plot = df[df[col] != 'Unknown'] if 'Unknown' in df[col].values else df
    fig_v = px.violin(
        df_plot, x=col, y="Exam_Score", color=col,
        color_discrete_map=cat_palette,
        box=True, points="outliers",
        category_orders={col: ordinal_order}
    )
    fig_v = polish_layout(fig_v, f"Distribution of Exam Scores by {name}", name, "Exam Score")
    fig_v.update_layout(showlegend=False)
    fig_v.write_image(os.path.join(plots_dir, "box_violin_plots", f"BoxViolin_{col}.png"), scale=2)

# Binary / nominal categories — sorted logically as Yes→No or appropriate
for col, name, cat_palette, order in [
    ('Internet_Access',            'Internet Access',            {"Yes": "#06D6A0", "No": "#EF476F"},              ["Yes", "No"]),
    ('Learning_Disabilities',      'Learning Disabilities',      {"No": "#118AB2",  "Yes": "#EF476F"},             ["No", "Yes"]),
    ('School_Type',                'School Type',                {"Public": "#118AB2", "Private": "#FFD166"},      ["Public", "Private"]),
    ('Extracurricular_Activities', 'Extracurricular Activities', {"Yes": "#06D6A0", "No": "#EF476F"},              ["Yes", "No"]),
    ]:
    fig_v = px.violin(
        df, x=col, y="Exam_Score", color=col,
        color_discrete_map=cat_palette,
        box=True, points="outliers",
        category_orders={col: order}
    )
    fig_v = polish_layout(fig_v, f"Distribution of Exam Scores by {name}", name, "Exam Score")
    fig_v.update_layout(showlegend=False)
    fig_v.write_image(os.path.join(plots_dir, "box_violin_plots", f"BoxViolin_{col}.png"), scale=2)

# Access_to_Resources — violin (consistent with all other ordinal categorical variables)
for col, name, cat_palette, order in [
    ('Access_to_Resources', 'Access to Resources', {"High": "#06D6A0", "Medium": "#118AB2", "Low": "#EF476F"}, ["High", "Medium", "Low"]),
    ]:
    fig_v = px.violin(
        df, x=col, y="Exam_Score", color=col,
        color_discrete_map=cat_palette,
        box=True, points="outliers",
        category_orders={col: order}
    )
    fig_v = polish_layout(fig_v, f"Distribution of Exam Scores by {name}", name, "Exam Score")
    fig_v.update_layout(showlegend=False)
    fig_v.write_image(os.path.join(plots_dir, "box_violin_plots", f"BoxViolin_{col}.png"), scale=2)

# Peer_Influence — ordinal: Negative → Neutral → Positive
peer_order   = ["Negative", "Neutral", "Positive"]
peer_palette = {"Positive": "#06D6A0", "Neutral": "#FFD166", "Negative": "#EF476F"}
fig_v = px.violin(
    df, x="Peer_Influence", y="Exam_Score", color="Peer_Influence",
    color_discrete_map=peer_palette, box=True, points="outliers",
    category_orders={"Peer_Influence": peer_order}
)
fig_v = polish_layout(fig_v, "Distribution of Exam Scores by Peer Influence", "Peer Influence", "Exam Score")
fig_v.update_layout(showlegend=False)
fig_v.write_image(os.path.join(plots_dir, "box_violin_plots", "BoxViolin_Peer_Influence.png"), scale=2)

# Distance_from_Home — ordinal: Near → Moderate → Far (filter Unknown = 67 rows, 1%)
dist_order   = ["Near", "Moderate", "Far"]
dist_palette = {"Near": "#06D6A0", "Moderate": "#FFD166", "Far": "#EF476F"}
df_dist = df[df["Distance_from_Home"] != "Unknown"]
fig_v = px.violin(
    df_dist, x="Distance_from_Home", y="Exam_Score", color="Distance_from_Home",
    color_discrete_map=dist_palette, box=True, points="outliers",
    category_orders={"Distance_from_Home": dist_order}
)
fig_v = polish_layout(fig_v, "Distribution of Exam Scores by Distance from Home", "Distance from Home", "Exam Score")
fig_v.update_layout(showlegend=False)
fig_v.write_image(os.path.join(plots_dir, "box_violin_plots", "BoxViolin_Distance_from_Home.png"), scale=2)

# Parental_Education_Level — ordinal: Postgraduate > College > High School
edu_order   = ["Postgraduate", "College", "High School"]
edu_palette = {"Postgraduate": "#06D6A0", "College": "#FFD166", "High School": "#EF476F"}
df_edu = df[~df["Parental_Education_Level"].isin(["Unknown", "Others"])]
fig_v = px.violin(
    df_edu, x="Parental_Education_Level", y="Exam_Score", color="Parental_Education_Level",
    color_discrete_map=edu_palette, box=True, points="outliers",
    category_orders={"Parental_Education_Level": edu_order}
)
fig_v = polish_layout(fig_v, "Distribution of Exam Scores by Parental Education Level", "Parental Education Level", "Exam Score")
fig_v.update_layout(showlegend=False)
fig_v.write_image(os.path.join(plots_dir, "box_violin_plots", "BoxViolin_Parental_Education_Level.png"), scale=2)


# =============================================================================
# 3. DONUT CHARTS — Proportional demographic sub-population breakdown
# Sort rule: ordinal categories sorted Low→Medium→High;
#            nominal categories sorted by descending count (course rule: values must be sorted)
# =============================================================================
for col, name, colors, order in [
    ('Family_Income',        'Family Income Levels', ["#EF476F", "#FFD166", "#06D6A0"], ["Low", "Medium", "High"]),
    ('School_Type',          'School Type',           ["#118AB2", "#EF476F"],             None),
    ('Learning_Disabilities','Learning Disabilities', ["#118AB2", "#FFD166"],             None),
    ('Parental_Education_Level', 'Parental Education', ["#EF476F", "#FFD166", "#06D6A0", "#118AB2", "#073B4C"], None),
    ]:
    pie_df = df[col].value_counts().reset_index()
    pie_df.columns = [col, 'Count']
    # Rename "Unknown" to "Others" per course rule: "Club minor items under 'Others'"
    pie_df[col] = pie_df[col].replace('Unknown', 'Others')
    if order:
        # Ordinal: sort by logical tier order
        pie_df[col] = pd.Categorical(pie_df[col], categories=order, ordered=True)
        pie_df = pie_df.sort_values(col)
    else:
        # Nominal: sort by descending count (course requirement: "Values must be sorted")
        pie_df = pie_df.sort_values('Count', ascending=False)
    fig_pie = px.pie(pie_df, values='Count', names=col, color_discrete_sequence=colors, hole=0.4)
    fig_pie.update_traces(
        textposition='inside', textinfo='percent+label',
        marker=dict(line=dict(color='#FFFFFF', width=2))
    )
    fig_pie = polish_layout(fig_pie, f"Demographic Distribution of {name}")
    fig_pie.update_layout(showlegend=False)
    fig_pie.write_image(os.path.join(plots_dir, "pie_charts", f"Pie_{col}.png"), scale=2)


# =============================================================================
# 4. LINE CHARTS — Continuous / discrete inputs vs mean Exam_Score
# (Line charts showing a TREND are valid — not bar charts of means)
# =============================================================================
bins  = [0, 8, 16, 24, 32, df['Hours_Studied'].max()]
labels = ['0–8 hrs', '9–16 hrs', '17–24 hrs', '25–32 hrs', f'33–{int(df["Hours_Studied"].max())} hrs']
df['Hours_Studied_Bin'] = pd.cut(df['Hours_Studied'], bins=bins, labels=labels, right=True)

# Attendance binned: 60–65, 65–70, 70–75, 75–80, 80–85, 85–90, 90–95, 95–100
att_bins   = [60, 65, 70, 75, 80, 85, 90, 95, 100]
att_labels = ['60–65%', '65–70%', '70–75%', '75–80%', '80–85%', '85–90%', '90–95%', '95–100%']
df['Attendance_Bin'] = pd.cut(df['Attendance'], bins=att_bins, labels=att_labels, right=True, include_lowest=True)

for col, name, color in [
    ('Hours_Studied_Bin', 'Weekly Study Hours',   '#118AB2'),
    ('Tutoring_Sessions', 'Tutoring Sessions',    '#06D6A0'),
    ('Attendance_Bin',    'Class Attendance (%)', '#40916C'),
    ]:
    line_df = df.groupby(col, as_index=False, observed=True)['Exam_Score'].mean()
    fig_line = px.line(line_df, x=col, y="Exam_Score", markers=True, line_shape="linear")
    # A2 fix: markers match line color instead of hardcoded dark navy
    # A3 fix: measure-driven data labels at each marker (course best practice)
    fig_line.update_traces(
        mode='lines+markers+text',
        line=dict(color=color, width=4),
        marker=dict(size=12, color=color),
        text=[f"{v:.1f}" for v in line_df['Exam_Score']],
        textposition='top center',
        textfont=dict(size=11, color='#1F2937'),
    )
    fig_line = polish_layout(fig_line, f"Trend of Average Exam Score by {name}", name, "Average Exam Score")
    if col in ('Sleep_Hours', 'Tutoring_Sessions', 'Physical_Activity'):
        fig_line.update_xaxes(tick0=0, dtick=1, zeroline=False)
    else:
        fig_line.update_xaxes(zeroline=False)
    # Dynamic y-axis: zoom to actual data range so flat/narrow lines are still readable.
    # Floor at 50 ensures the axis never starts unreasonably high.
    y_lo = max(50, int(line_df['Exam_Score'].min()) - 3)
    y_hi = int(line_df['Exam_Score'].max()) + 4
    fig_line.update_yaxes(range=[y_lo, y_hi])
    fig_line.write_image(
        os.path.join(plots_dir, "line_charts", f"Line_{col.replace('_Bin','')}.png"), scale=2
    )

# =============================================================================
# 5. COLUMN CHARTS — Student count by ordinal categorical variables
# Per course standard: Column chart (vertical) for quantitative ordinal variables.
# Y-axis MUST start at 0 (bar chart best practice).
# These reveal the demographic composition of the student cohort by key equity
# variables that are NOT already covered by the pie chart section.
# =============================================================================
for col, name, colors, order in [
    ('Access_to_Resources', 'Access to Resources',
     {"Low": "#EF476F", "Medium": "#118AB2", "High": "#06D6A0"},
     ["Low", "Medium", "High"]),
    ('Parental_Involvement', 'Parental Involvement',
     {"Low": "#EF476F", "Medium": "#118AB2", "High": "#06D6A0"},
     ["Low", "Medium", "High"]),
]:
    count_df = df.groupby(col, observed=True).size().reset_index(name='Count')
    count_df[col] = pd.Categorical(count_df[col], categories=order, ordered=True)
    count_df = count_df.sort_values(col)

    fig_bar = px.bar(
        count_df, x=col, y='Count', color=col,
        color_discrete_map=colors,
        category_orders={col: order},
        text='Count',
    )
    fig_bar.update_traces(
        marker_line_color='#333333', marker_line_width=1.0,
        textposition='outside', textfont=dict(size=13, color='#1F2937'),
    )
    fig_bar = polish_layout(fig_bar, f'Student Distribution by {name}', name, 'Number of Students')
    fig_bar.update_yaxes(range=[0, count_df['Count'].max() * 1.18])
    fig_bar.update_layout(showlegend=False, bargap=0.35)
    fig_bar.write_image(os.path.join(plots_dir, 'bar_charts', f'Bar_{col}.png'), scale=2)


print("Basic Visualizations fully regenerated.")

