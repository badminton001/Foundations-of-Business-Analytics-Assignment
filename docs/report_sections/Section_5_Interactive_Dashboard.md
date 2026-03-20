# 5.0 Interactive Data Dashboard

**Dashboard URL:** https://foundations-of-business-analytics-assignment-group1.streamlit.app/

## 5.1 Target Audience & Justification

In this educational context, the institution serves as the equivalent of a company, and the academic affairs office functions as the primary decision-making unit. The dashboard is designed for this office, specifically university administrators and education policymakers responsible for student retention, intervention design, and resource allocation.

This audience is appropriate for three reasons:

1. **Decision-making authority.** Administrators control the institutional levers identified as most impactful in Sections 2--4: attendance monitoring policies, tutoring programme design, parental engagement initiatives, and resource distribution. A dashboard targeting this audience directly connects analytical insights to actionable decisions.

2. **Need for subgroup analysis.** Academic affairs teams must understand not just cohort-level averages but how different student segments perform. The dashboard's interactive filters allow administrators to isolate specific subgroups (e.g., low-income students, or students with low motivation) and observe how performance patterns shift, a capability that static charts cannot provide.

3. **Time constraints.** Senior administrators rarely have time to review a full analytical report. The single-page dashboard format delivers the core narrative in a format that can be consumed in minutes, progressing from performance baseline through behavioural drivers to equity diagnostics.

---

## 5.2 Dashboard Structure & Functionality

The dashboard is organised as a single scrollable page with three key components:

**Sidebar Filters.** Three global filters are provided: Institution Type (Public/Private), Family Income (High/Medium/Low), and Motivation Level (High/Medium/Low). When a filter is applied, all 13 charts and all 5 summary metrics update in real time. For example, an administrator can select "Low" income to immediately see how the score distribution, behavioural trends, and equity patterns change for the most disadvantaged cohort.

**KPI Summary Strip.** Five headline metrics are displayed prominently at the top: Students Analysed, Mean Exam Score, Avg Class Attendance, Avg Study Hours / Wk, and Internet Access. These update dynamically with the filters, providing instant context before the user explores the detailed charts below.

**Five Analytical Modules.** The charts are grouped into five sequential sections that mirror the analytical narrative of this report, progressing from overall performance patterns, through behavioural analysis, to systemic equity diagnostics.

[Insert Figure: Dashboard_Screenshot.png]

**Figure 22:** Full-page screenshot of the Interactive Data Dashboard.

---

## 5.3 Charts Included & Justification

**Table 6: Dashboard Charts and Justification**

| Module | Chart | Type | Justification for Inclusion |
|--------|-------|------|-----------------------------|
| 01 Performance Baseline | Distribution of Exam Scores | Histogram | Establishes the target variable's shape. The narrow IQR of 4 points reveals a "compression problem" that frames the entire analysis |
| 01 Performance Baseline | Attendance vs. Exam Score by Motivation | Scatter plot with trendlines | Visualises the strongest predictor relationship (r = 0.581) and shows it holds across all motivation levels |
| 02 Behavioural Levers | Study Hours vs. Exam Score by Family Income | Scatter plot with trendlines | Tests whether effort pays off equally across income groups. The parallel trendlines confirm income-neutral returns, a key equity finding |
| 02 Behavioural Levers | Trend by Weekly Study Hours | Line chart | Quantifies the optimal study duration and reveals diminishing returns beyond 24 hours/week |
| 02 Behavioural Levers | Trend by Tutoring Sessions | Line chart | Reveals the inverted-U pattern (optimal at 3--6 sessions), essential for setting tutoring dosage recommendations |
| 03 Support Environment | Exam Scores by Motivation Level | Violin + box plot | Shows that motivation widens the performance spread rather than shifting the median |
| 03 Support Environment | Exam Scores by Parental Involvement | Violin + box plot | Demonstrates that engaged parents lift even lower-performing students above the uninvolved group's median |
| 03 Support Environment | Exam Scores by Teacher Quality | Violin + box plot | Confirms a consistent quality gradient, supporting investment in teacher development |
| 04 Socioeconomic Impact | Exam Scores by Family Income | Violin + box plot | Quantifies the income-driven performance gap |
| 04 Socioeconomic Impact | Exam Scores by Access to Resources | Violin + box plot | Identifies resource access as the largest categorical driver (gap = 1.89 points), the strongest equity signal in the dataset |
| 04 Socioeconomic Impact | Exam Scores by Parental Education Level | Violin + box plot | Shows the intergenerational education gradient, informing long-term policy |
| 05 Systemic Analysis | Pairwise Correlation Heatmap | Heatmap | Provides a global ranking of all numerical predictors in a single view, tying together all preceding analyses |
| 05 Systemic Analysis | Motivation x Parental Involvement Cross-Tab | Heatmap | Reveals the report's most actionable finding: parental involvement compensates for low motivation (score 67.7 vs. 66.8) |

---

## 5.4 How the Audience Derives Key Insights

The dashboard supports three primary modes of insight discovery:

**Cohort Overview (No Filters Applied).** When the dashboard loads without filters, the administrator sees the full cohort picture:
- The **KPI strip** immediately communicates the baseline: 6,607 students, mean score 67.2, average attendance 80%.
- The **exam score histogram** reveals that most students cluster in a narrow 65--69 band, raising the question: what separates the few high-achievers from the majority?
- The **attendance scatter plot** answers this question directly: attendance is the dominant lever, and this relationship is consistent across all motivation levels.

**Subgroup Investigation (Filters Applied).** The real power of the dashboard emerges when filters are applied to test specific hypotheses:

- **"Are low-income students differently affected by attendance?"** Selecting Family Income = "Low" updates the attendance scatter plot. The administrator can observe whether the trendline slope changes, and the KPI strip shows how the mean score and attendance shift for this subgroup.
- **"Do low-motivation students benefit from tutoring?"** Selecting Motivation Level = "Low" updates the tutoring line chart, revealing whether the inverted-U pattern persists or changes for unmotivated students.
- **"What does the private school advantage look like?"** Selecting Institution Type = "Private" updates all charts simultaneously, allowing the administrator to compare private-school patterns against the default full-cohort view.

[Insert Figure: Dashboard_KPI_Unfiltered.png]

**Figure 23a:** KPI strip with no filters applied (full cohort).

[Insert Figure: Dashboard_Sidebar_LowIncome.png]

**Figure 23b:** Sidebar filter with Family Income = "Low" selected.

[Insert Figure: Dashboard_KPI_Filtered.png]

**Figure 23c:** KPI strip after filtering, showing how key metrics shift for the low-income subgroup.

**Cross-Module Synthesis.** By scrolling through all five modules in sequence, the administrator builds a layered understanding:

1. **Module 01** establishes *what* the problem is (compressed scores, attendance as the key driver).
2. **Module 02** reveals *how* effort translates to outcomes (study hours and tutoring dosage).
3. **Modules 03--04** expose *who* is most affected (students with low parental involvement, limited resources, or low-income backgrounds).
4. **Module 05** synthesises *why* certain combinations of factors matter more than others (the Motivation x Parental Involvement interaction).

This progressive structure ensures that even an administrator with limited time can extract the core message from Module 01 alone, while those who explore further gain increasingly nuanced and actionable insights.
