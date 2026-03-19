# 3.0 Foundational Visual Analytics: Core Distributions

All visualisations employ a unified colour system: steel-blue (#9BC2E6) for histograms, semantic traffic-light colours for ordinal variables (green = High, blue = Medium, red = Low), and consistent layout standards (font 14 pt, plotly_white template, lightgray gridlines). Chart types follow the course best-practice framework.

---

## 3.1 Target Variable Distribution

[Insert Figure: Histogram_Exam_Score.png]

**Figure 1:** Distribution of Exam Scores (n = 6,607; 45 bins, width = 1 point, range 55--100).

The target variable is sharply right-skewed (skewness = 1.64) with the bulk of scores compressed between 63 and 72. The IQR is only 4 points (Q1 = 65, Q3 = 69), meaning half of all students fall within an extremely narrow band, while a thin right tail extends to 100. This compression suggests the current assessment may lack discriminatory power; introducing tiered question difficulty could improve differentiation.

## 3.2 Input Variable Distributions

The remaining six numerical inputs are presented as a composite panel below. All use identical styling (#9BC2E6, black axis lines, equal-width bins).

[Insert Composite Figure: Histogram_Attendance.png, Histogram_Previous_Scores.png, Histogram_Hours_Studied.png, Histogram_Sleep_Hours.png, Histogram_Tutoring_Sessions.png, Histogram_Physical_Activity.png -- arranged as a 3x2 grid]

**Figure 2:** Distributions of six numerical input variables.

**Table 2: Descriptive Statistics of All Numerical Variables**

| Variable | Mean | Median | Mode | Std Dev | Min | Q1 | Q3 | Max | IQR | Skewness |
|----------|-----:|-------:|-----:|--------:|----:|---:|---:|----:|----:|---------:|
| Hours_Studied | 19.98 | 20.00 | 20 | 5.99 | 1 | 16 | 24 | 44 | 8 | 0.01 |
| Attendance | 79.98 | 80.00 | 67 | 11.55 | 60 | 70 | 90 | 100 | 20 | 0.01 |
| Sleep_Hours | 7.03 | 7.00 | 7 | 1.47 | 4 | 6 | 8 | 10 | 2 | -0.02 |
| Previous_Scores | 75.07 | 75.00 | 66 | 14.40 | 50 | 63 | 88 | 100 | 25 | 0.00 |
| Tutoring_Sessions | 1.49 | 1.00 | 1 | 1.23 | 0 | 1 | 2 | 8 | 1 | 0.82 |
| Physical_Activity | 2.97 | 3.00 | 3 | 1.03 | 0 | 2 | 4 | 6 | 2 | -0.03 |
| Exam_Score | 67.24 | 67.00 | 68 | 3.89 | 55 | 65 | 69 | 100 | 4 | 1.64 |

Key observations from the input distributions:

- **Attendance** has the widest IQR (20 points) and a 13-point gap between mean (80%) and mode (67%), revealing a hidden low-attendance subgroup masked by the cohort average. Approximately one quarter of students attend fewer than 70% of classes.
- **Previous Scores** span the full 50--100 range with an IQR of 25 points -- the widest of any variable -- yet this heterogeneity collapses to just 4 points in the current exam, suggesting historical performance is a weak predictor of present outcomes.
- **Hours Studied** is near-perfectly symmetric (skewness = 0.01, IQR = 8 hours). This uniformity, juxtaposed with the right-skewed exam distribution, is the central paradox of the dataset: similar time investment produces divergent outcomes.
- **Tutoring Sessions** is right-skewed (0.82) with a long tail to 8 sessions, confirming that most students engage minimally while a small subset pursues intensive supplementary instruction.
- **Sleep Hours** and **Physical Activity** are tightly symmetric with narrow IQRs (2 each) and show too little cross-student variation to serve as performance differentiators.

---

## 3.3 Categorical Drivers of Exam Score (Violin & Box Plots)

Combined violin-box plots compare every categorical variable against Exam Score. Violin plots are preferred over mean-bar charts because they reveal the full distribution shape, median, quartiles, and outliers simultaneously. All 12 categorical variables are examined; the three most insightful are presented individually, while the remaining nine are shown as composite panels.

### Key Individual Charts

[Insert Figure: BoxViolin_Access_to_Resources.png]

**Figure 3:** Distribution of Exam Scores by Access to Resources.

[Insert Figure: BoxViolin_Parental_Involvement.png]

**Figure 4:** Distribution of Exam Scores by Parental Involvement.

[Insert Figure: BoxViolin_Family_Income.png]

**Figure 5:** Distribution of Exam Scores by Family Income.

These three variables produce the largest High-Low mean gaps among all categorical features:

| Variable | High Mean | Low Mean | Gap |
|----------|----------:|---------:|----:|
| Access to Resources | 68.09 | 66.20 | **1.89** |
| Parental Involvement | 68.09 | 66.36 | **1.73** |
| Family Income | 67.84 | 66.85 | **0.99** |

For Access to Resources, the "Low" group has a compressed Q3 of only 68, indicating a hard ceiling on performance when resources are scarce. For Parental Involvement, the "High" group's Q1 (66) equals the "Low" group's median -- meaning even the lower-performing students with engaged parents outperform the typical student whose parents are uninvolved. These effects, though individually modest, are likely to compound when multiple disadvantages co-occur (explored in the cross-tab heatmap, Section 4.5).

### Composite Panel: Remaining Violin Plots

[Insert Composite Figure: BoxViolin_Motivation_Level.png, BoxViolin_Teacher_Quality.png, BoxViolin_Parental_Education_Level.png -- arranged as a 1x3 row]

**Figure 6:** Exam Score distributions by Motivation Level, Teacher Quality, and Parental Education Level.

[Insert Composite Figure: BoxViolin_Peer_Influence.png, BoxViolin_Distance_from_Home.png, BoxViolin_Internet_Access.png -- arranged as a 1x3 row]

**Figure 7:** Exam Score distributions by Peer Influence, Distance from Home, and Internet Access.

[Insert Composite Figure: BoxViolin_Learning_Disabilities.png, BoxViolin_School_Type.png, BoxViolin_Extracurricular_Activities.png -- arranged as a 1x3 row]

**Figure 8:** Exam Score distributions by Learning Disabilities, School Type, and Extracurricular Activities.

**Table 3: Full Summary -- All Categorical Variables vs. Exam Score**

| Variable | Level | Median | Mean | Q1 | Q3 |
|----------|-------|-------:|-----:|---:|---:|
| Motivation Level | High / Med / Low | 67 / 67 / 67 | 67.70 / 67.33 / 66.75 | 65 / 65 / 64 | 70 / 69 / 69 |
| Teacher Quality | High / Med / Low | 68 / 67 / 67 | 67.68 / 67.11 / 66.75 | 65 / 65 / 64 | 70 / 69 / 69 |
| Parental Education | Post / College / HS | 68 / 67 / 67 | 67.97 / 67.32 / 66.89 | 66 / 65 / 64 | 70 / 70 / 69 |
| Peer Influence | Pos / Neut / Neg | 67 / 67 / 66 | 67.62 / 67.20 / 66.56 | 65 / 65 / 64 | 70 / 69 / 69 |
| Distance from Home | Near / Mod / Far | 67 / 67 / 66 | 67.51 / 66.98 / 66.46 | 65 / 65 / 64 | 70 / 69 / 68 |
| Internet Access | Yes / No | 67 / 66 | 67.29 / 66.53 | 65 / 64 | 70 / 69 |
| Learning Disabilities | No / Yes | 67 / 66 | 67.35 / 66.27 | 65 / 64 | 70 / 68 |
| School Type | Private / Public | 67 / 67 | 67.29 / 67.21 | 65 / 65 | 70 / 69 |
| Extracurricular | Yes / No | 67 / 67 | 67.44 / 66.93 | 65 / 64 | 70 / 69 |

Notable findings from the composite panels:

- **Parental Education Level** exhibits a clear intergenerational gradient: Postgraduate-parent students score 1.08 points higher than High-School-parent students, with a Q1 of 66 that exceeds the latter group's median.
- **Learning Disabilities** produce the largest binary gap (1.08 points) and a compressed Q3 (68 vs. 70), confirming a performance ceiling for this 10.5% subgroup.
- **School Type** is the least influential variable (mean difference = 0.08 points) -- a counterintuitive finding suggesting that public vs. private schooling alone does not drive performance differences in this cohort.

---

## 3.4 Student Demographics (Donut Charts)

[Insert Composite Figure: Pie_Family_Income.png, Pie_School_Type.png, Pie_Learning_Disabilities.png, Pie_Parental_Education_Level.png -- arranged as a 2x2 grid]

**Figure 9:** Demographic composition of the student cohort by Family Income, School Type, Learning Disability status, and Parental Education Level.

The cohort is socioeconomically diverse: Low and Medium income households each represent approximately 40%, with High income at 19%. Public-school students dominate at roughly 70%. Learning disabilities affect 10.5% of the population. These balanced proportions ensure that the performance differences identified in Section 3.3 are genuine effects rather than sampling artefacts.

---

## 3.5 Behavioural Trends (Line Charts)

Three line charts display the mean Exam Score across ordered levels of key behavioural variables. Each marker carries a measure-driven data label (course best practice); the y-axis does not start at zero (appropriate for line charts per course standards).

[Insert Figure: Line_Attendance.png]

**Figure 10:** Trend of average Exam Score by class attendance rate.

Attendance produces the strongest and most consistent positive trend: scores rise from 63.7 (60--65% attendance) to 70.5 (95--100%), a **6.8-point lift** with an approximately linear gradient across the entire range. Unlike other behavioural variables, there is no visible saturation point, confirming attendance as the single most effective lever for academic improvement.

[Insert Figure: Line_Hours_Studied.png]

**Figure 11:** Trend of average Exam Score by weekly study hours.

Scores increase monotonically from 63.7 (0--8 hours) to 71.3 (33--44 hours), a **7.6-point lift**. However, the gradient flattens beyond 24 hours, suggesting diminishing marginal returns. Institutional guidance should emphasise study quality over raw time accumulation.

[Insert Figure: Line_Tutoring_Sessions.png]

**Figure 12:** Trend of average Exam Score by tutoring session frequency.

Scores rise to a peak near 6 sessions per week, after which performance plateaus or declines. This inverted-U pattern suggests that moderate tutoring is beneficial (3--6 sessions optimal) but excessive tutoring may displace independent study or induce dependency.

---

## 3.6 Student Distribution by Equity Variables (Column Charts)

[Insert Composite Figure: Bar_Access_to_Resources.png, Bar_Parental_Involvement.png -- arranged side by side]

**Figure 13:** Student count distribution by Access to Resources and Parental Involvement.

Both variables are approximately uniformly distributed across Low, Medium, and High tiers (~33% each). This balance ensures that the performance gaps identified in Section 3.3 are not driven by unequal group sizes, and that interventions targeting the "Low" tier would reach a substantial proportion of the student body.
