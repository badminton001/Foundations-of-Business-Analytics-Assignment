import pandas as pd
import numpy as np
import plotly.express as px
import os

base_dir = r"C:\Users\Y\Desktop\Foundations-of-Business-Analytics-Assignment"
data_path = os.path.join(base_dir, "data", "StudentPerformanceFactors_cleaned.csv")
plots_dir = os.path.join(base_dir, "plots")

df = pd.read_csv(data_path)

# Ensure output subdirectories exist
for sub in ["histograms", "box_violin_plots", "pie_charts", "line_charts"]:
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
def create_strict_histogram(df, col, title, x_label, color, num_bins, override_min=None, override_max=None):
    col_min = override_min if override_min is not None else df[col].min()
    col_max = override_max if override_max is not None else df[col].max()
    bin_width = (col_max - col_min) / num_bins
    
    fig = px.histogram(df, x=col, color_discrete_sequence=[color])
    # Enforce strict bins spanning exact range with equal width, matching image aesthetic
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
    
    fig.update_xaxes(
        title_text=x_label,
        showgrid=False,
        showline=True, linewidth=1.5, linecolor='black', # Add black bottom line
        ticks='outside', tickwidth=1.5, tickcolor='black', ticklen=6,
        tickmode='linear', tick0=col_min, dtick=bin_width
    )
    
    fig.update_yaxes(
        title_text="Count of Students",
        showgrid=False, # Removed gridline to mimic reference image
        showline=True, linewidth=1.5, linecolor='black', # Add black left line
        ticks='outside', tickwidth=1.5, tickcolor='black', ticklen=6,
        rangemode='tozero'
    )
    
    return fig

# 1. Exam_Score: range 55-100. Using 50-100 (span 50), 10 bins (width=5.0)
fig1 = create_strict_histogram(df, "Exam_Score", "Distribution of Exam Scores", "Exam Score", "#9BC2E6", 10, 50, 100)
fig1.write_image(os.path.join(plots_dir, "histograms", "Histogram_Exam_Score.png"), scale=2)

# 2. Attendance: range 60-100. Using 60-100 (span 40), 8 bins (width=5.0)
fig2 = create_strict_histogram(df, "Attendance", "Distribution of Class Attendance (%)", "Attendance Percentage", "#9BC2E6", 8, 60, 100)
fig2.write_image(os.path.join(plots_dir, "histograms", "Histogram_Attendance.png"), scale=2)

# 3. Previous_Scores: range 50-100. Using 50-100 (span 50), 10 bins (width=5.0)
fig3 = create_strict_histogram(df, "Previous_Scores", "Distribution of Previous Scores", "Previous Score", "#9BC2E6", 10, 50, 100)
fig3.write_image(os.path.join(plots_dir, "histograms", "Histogram_Previous_Scores.png"), scale=2)

# 4. Hours_Studied: range 1-44. Using 0-45 (span 45), 9 bins (width=5.0)
fig4 = create_strict_histogram(df, "Hours_Studied", "Distribution of Weekly Study Hours", "Hours Studied", "#9BC2E6", 9, 0, 45)
fig4.write_image(os.path.join(plots_dir, "histograms", "Histogram_Hours_Studied.png"), scale=2)


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
    ]:
    fig_v = px.violin(
        df, x=col, y="Exam_Score", color=col,
        color_discrete_map=cat_palette,
        box=True, points="outliers",
        category_orders={col: ordinal_order}
    )
    fig_v = polish_layout(fig_v, f"Distribution of Exam Scores by {name}", name, "Exam Score")
    fig_v.update_layout(showlegend=False)
    fig_v.write_image(os.path.join(plots_dir, "box_violin_plots", f"BoxViolin_{col}.png"), scale=2)

# Binary / nominal categories — sorted logically as Yes→No or appropriate
for col, name, cat_palette, order in [
    ('Internet_Access',       'Internet Access',       {"Yes": "#06D6A0", "No": "#EF476F"},   ["Yes", "No"]),
    ('Learning_Disabilities', 'Learning Disabilities', {"No": "#118AB2",  "Yes": "#EF476F"},  ["No", "Yes"]),
    ('School_Type',           'School Type',           {"Public": "#118AB2", "Private": "#FFD166"}, ["Public", "Private"]),
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

# Added: Access to Resources Box Plot for Systemic Equity analysis
for col, name, cat_palette, order in [
    ('Access_to_Resources', 'Access to Resources', {"High": "#06D6A0", "Medium": "#118AB2", "Low": "#EF476F"}, ["High", "Medium", "Low"]),
    ]:
    fig_v = px.box(
        df, x=col, y="Exam_Score", color=col,
        color_discrete_map=cat_palette,
        category_orders={col: order}
    )
    fig_v = polish_layout(fig_v, f"Distribution of Exam Scores by {name}", name, "Exam Score")
    fig_v.update_layout(showlegend=False)
    fig_v.write_image(os.path.join(plots_dir, "box_violin_plots", f"BoxViolin_{col}.png"), scale=2)


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
    ('Hours_Studied_Bin', 'Weekly Study Hours',  '#118AB2'),
    ('Sleep_Hours',       'Nightly Sleep Hours', '#EF476F'),
    ('Tutoring_Sessions', 'Tutoring Sessions',   '#06D6A0'),
    ('Attendance_Bin',    'Class Attendance (%)', '#40916C'),
    ]:
    line_df = df.groupby(col, as_index=False, observed=True)['Exam_Score'].mean()
    fig_line = px.line(line_df, x=col, y="Exam_Score", markers=True, line_shape="linear")
    fig_line.update_traces(line=dict(color=color, width=4), marker=dict(size=12, color="#073B4C"))
    fig_line = polish_layout(fig_line, f"Trend of Average Exam Score by {name}", name, "Average Exam Score")
    if col in ('Sleep_Hours', 'Tutoring_Sessions'):
        fig_line.update_xaxes(tick0=0, dtick=1, zeroline=False)
    else:
        fig_line.update_xaxes(zeroline=False)
    fig_line.update_yaxes(range=[50, round(line_df['Exam_Score'].max() + 5)])
    fig_line.write_image(
        os.path.join(plots_dir, "line_charts", f"Line_{col.replace('_Bin','')}.png"), scale=2
    )

print("Basic Visualizations fully regenerated (no mean-bar charts).")

