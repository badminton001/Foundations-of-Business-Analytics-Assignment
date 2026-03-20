# 4.0 Advanced Visual Analytics: Multi-Dimensional Interactions

The foundational charts in Section 3 examined one variable at a time against the target. This section introduces multi-dimensional techniques, including scatter plots with marginal distributions, density contours, bubble charts, stacked/clustered bars, and heatmaps. These charts reveal interaction effects, compound disadvantages, and systemic patterns that single-variable analyses cannot surface.

Each scatter plot below consists of three integrated panels: the main scatter with per-group OLS trendlines (coloured to match group identity), a marginal histogram on the top edge showing x-variable density, and a marginal box plot on the right edge showing y-variable spread by group.

---

## 4.1 Primary Behavioural Driver: Attendance x Exam Score by Motivation

[Insert Figure: Scatter_Attendance_Score.png]

**Figure 14:** Exam Score vs. Class Attendance, stratified by Motivation Level (r = 0.581).

Attendance is the dominant predictor of exam performance (Pearson r = 0.581). The OLS trendlines for all three motivation groups slope upward at similar gradients, confirming that the attendance-performance relationship holds regardless of motivation level.

The marginal box plot on the right reveals that while median scores are similar across motivation tiers, the **high-motivation group has a longer upper tail**, producing more outlier high-achievers. Conversely, the low-motivation group has a heavier lower tail. This suggests that motivation does not shift the average student's performance substantially, but it amplifies the variance: highly motivated students are more likely to convert attendance into exceptional outcomes.

The marginal histogram on top shows that attendance distributions overlap heavily across motivation groups, meaning that motivation does not systematically drive students to attend more or fewer classes. The academic implication is clear: attendance improvement programmes should target all students regardless of their motivation profile.

---

## 4.2 Socioeconomic Lens: Study Hours x Exam Score by Family Income

[Insert Figure: Scatter_Hours_Score.png]

**Figure 15:** Exam Score vs. Weekly Study Hours, stratified by Family Income (r = 0.446).

The second-strongest behavioural predictor (r = 0.446) is study duration. The trendlines for High, Medium, and Low income groups are **nearly parallel**, indicating that the academic return on study time is largely independent of family income. However, at equivalent study hours, high-income students consistently score marginally higher. This suggests that income operates through supplementary channels (better resources, tutoring access, home environment) rather than by altering study efficiency itself.

The marginal box plot confirms that the income-driven performance gap exists but is modest: all three groups share a similar median, with income primarily widening the upper tail. The marginal histogram shows no meaningful difference in study-hour distributions across income tiers -- students from all backgrounds invest comparable time.

**Policy implication:** Since study time effectiveness is income-neutral, effort-based interventions (study-skill workshops, time management training) will benefit students across all socioeconomic backgrounds equally. However, closing the residual income gap requires addressing structural factors such as resource access (see Section 4.4).

---

## 4.3 Social Dimension: Previous Scores x Exam Score by Peer Influence

[Insert Figure: Scatter_Previous_Score.png]

**Figure 16:** Exam Score vs. Previous Scores, stratified by Peer Influence (r = 0.175).

Previous academic performance is a surprisingly weak predictor of current scores (r = 0.175). The scatter shows massive vertical dispersion: students with the same prior score (e.g., 75) can achieve current exam scores ranging from 60 to 80+. This confirms the statistical finding from Section 2.2.5 that historical grades are poor anchors for present outcomes.

The colour stratification by Peer Influence reveals a consistent but subtle pattern: students with positive peer influence cluster slightly higher in the score distribution, while those with negative influence cluster lower. The effect is modest (mean gap = 1.06 points) but directionally consistent, supporting the case for structured peer learning programmes.

---

## 4.4 Compound Socioeconomic Disadvantage

[Insert Figure: StackedBar_Income_Resources.png]

**Figure 17:** Resource Access composition by Family Income level.

The stacked bar chart shows that resource access is distributed approximately uniformly across all three income groups: roughly 19--20% of students fall into the "Low" resource tier regardless of family income. This means that income and resource access are largely **independent** variables in this cohort.

However, independence does not eliminate risk. Because both low income (mean gap = 0.99 points, Section 3.3) and low resource access (mean gap = 1.89 points, the largest of any categorical variable) independently depress exam scores, students who happen to fall into **both** categories face a compound penalty. The chart confirms that a substantial number of low-income students (approximately 20%) do experience this double disadvantage, even though they are not disproportionately represented. Addressing this overlap requires targeted resource equalisation rather than effort-based interventions alone.

---

## 4.5 Compound Effect: Motivation x Parental Involvement

[Insert Figure: Heatmap_MeanScore_Motivation_Parental.png]

**Figure 18:** Average Exam Score by Motivation Level and Parental Involvement (3x3 cross-tabulation).

This heatmap reveals the most actionable multi-dimensional finding in the dataset. Rather than examining each factor in isolation, the cross-tabulation shows their **joint effect** on mean exam scores. Two critical insights emerge:

1. **Parental involvement matters more than motivation.** A student with low motivation but high parental involvement (67.7) outperforms a student with high motivation but low parental involvement (66.8). This is a counterintuitive finding with direct policy implications: investing in parental engagement programmes may yield greater academic returns than programmes targeting student motivation alone.

2. **The compound effect is additive, not multiplicative.** Moving from the lowest cell (Low/Low = 65.9) to the highest (High/High = 68.4) produces a 2.5-point lift. The transition is gradual across both dimensions, suggesting that improvements in either factor independently contribute to better outcomes, and institutions need not wait for both to improve simultaneously.

---

## 4.6 Global Feature Associations

[Insert Figure: Heatmap_Correlation.png]

**Figure 19:** Pairwise Pearson correlation coefficients among all numerical variables.

**Table 5: Correlations with Exam Score, Ranked by Strength**

| Feature | r (with Exam Score) | Interpretation |
|---------|--------------------:|----------------|
| Attendance | 0.581 | Strong positive, dominant predictor |
| Hours_Studied | 0.446 | Moderate positive |
| Previous_Scores | 0.175 | Weak positive |
| Tutoring_Sessions | 0.156 | Weak positive |
| Physical_Activity | 0.028 | Negligible |
| Sleep_Hours | -0.017 | Negligible (near zero) |

The heatmap confirms the hierarchy established by the scatter and line chart analyses:

- **Behavioural variables dominate**: Attendance (0.581) and study hours (0.446) together account for the strongest linear predictors, far surpassing all other features. These are also the most actionable, as institutions can directly influence both through scheduling, monitoring, and study-skill programmes.
- **Historical performance is a poor proxy**: Previous scores (0.175) carry surprisingly little predictive weight, reinforcing the finding from Section 4.3 that past grades should not be the primary basis for risk identification.
- **Lifestyle variables are noise in the linear context**: Sleep (-0.017) and physical activity (0.028) show virtually zero linear association with scores. While these may contribute indirectly through well-being, they are not levers for academic performance improvement.

---

## 4.7 Supporting Advanced Visualisations

Two additional charts provide supplementary perspectives on the relationships explored above.

[Insert Figure: Figure20_DensityContour_Bubble.png]

**Figure 20:** (Left) Density contour: joint distribution of Previous Scores and Exam Score. (Right) Bubble chart: Attendance vs. Exam Score, faceted by Motivation Level (bubble size = study hours).

- **Density Contour**: The horizontally elongated contour ellipse visually confirms the weak correlation (r = 0.175) between previous and current scores. The population centroid sits at approximately (75, 67), and the narrow Y-axis spread (exam scores concentrated in 63--72) contrasts with the wide X-axis spread (previous scores spanning 50--100).

- **Bubble Chart**: By encoding four variables simultaneously (attendance on X, exam score on Y, study hours as bubble size, motivation as facet), this chart reveals the synergy between engagement and effort. In all three facets, the largest bubbles (highest study hours) cluster in the upper-right quadrant (high attendance, high scores), confirming that the combination of attendance and study duration produces outcomes greater than either factor alone.

[Insert Figure: ClusteredBar_SchoolType_Internet.png]

**Figure 21:** Student count by School Type and Internet Access.

The clustered bar chart tests the common assumption that private schools provide superior technological infrastructure. The data contradicts this expectation: internet access rates are virtually identical between public (92.7%) and private (91.9%) schools, with the difference falling within one percentage point. The apparent gap in absolute counts is entirely attributable to unequal sample sizes (public: 4,598; private: 2,009). This finding suggests that the digital access gap, at least within this cohort, is not a school-type issue.
