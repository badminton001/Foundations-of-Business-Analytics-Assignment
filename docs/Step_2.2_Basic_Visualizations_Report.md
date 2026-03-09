# Phase 2: Step 2.2 — Basic Visualizations Report
## Bilingual Insights & Captions — with Embedded Data Values

> All numerical values embedded below are extracted directly from `StudentPerformanceFactors_cleaned.csv` (n = 6,607 students). This dataset has already been cleaned in Step 1.1.

---

## 1. Histograms: Core Target & Input Distributions

**Caption:** Histogram illustrating the distribution of Exam Scores across the student population.
*(Insert `plots/histograms/Histogram_Exam_Score.png`)*

**Key Data:**
| Statistic | Value |
|---|---|
| Sample size (n) | 6,607 |
| Mean | 67.24 |
| Median | 67.0 |
| Std Dev | 3.89 |
| Min | 55 |
| 25th percentile (Q1) | 65 |
| 75th percentile (Q3) | 70 |
| Max | 100 |

**English Insight:** The distribution of `Exam_Score` is right-skewed, with the vast majority of students scoring between 65–70 (IQR = 5 points only). A thin but notable high-performing tail extends above 80, reaching as far as 100. The very narrow IQR relative to the full range (55–100) confirms that most statistical variation is driven by a small subset of **high-achieving outliers in the right tail** — the positive skewness (1.64) means the right tail extends far more than the left. This non-normal shape means models trained purely through MSE (which penalizes outliers heavily) may not generalise well.

**中文洞察:** 目标变量 `Exam_Score` 呈现出典型的右偏态分布。绝大多数学生聚集在 65–70 这个极其狭窄的四分位区间内（IQR 仅为 5 分），均值 67.24、中位数 67.0 几乎重合，说明分布高度聚集。然而从 80 分往上延伸的细长高分尾，是整体成绩方差的主要驱动力。这种非正态形状在建模时要特别注意：以均方误差为损失函数的模型对这条高分尾会产生过度惩罚，建议评估鲁棒回归或基于树的模型。

---

**Caption:** Histogram illustrating the distribution of Class Attendance percentages.
*(Insert `plots/histograms/Histogram_Attendance.png`)*

**Key Data:**
| Statistic | Value |
|---|---|
| Mean | 79.98% |
| Median | 80.0% |
| Std Dev | 11.54% |
| Min | 60% |
| Q1 | 70% |
| Q3 | 90% |
| Max | 100% |

**English Insight:** The distribution of `Attendance` is approximately uniform across the 60–95% range, with each 5-point bin containing roughly 830 students. There is a sharp drop at the 100% bin (near-perfect attendance is rare). The skewness of **0.01** confirms that the distribution is nearly perfectly symmetric — not left- or right-skewed. The mean (79.98%) and median (80.0%) are virtually identical, further confirming the flat, even spread. The minimum of 60% indicates that the dataset contains no cases of extreme absenteeism. Correlation with Exam Score is **r = 0.581** (the single strongest predictor in the dataset).

**中文洞察:** `Attendance`（出勤率）在 60%–95% 范围内的分布近乎均匀，每个 5 分组区间约有 830 名学生。100% 出勤的档位明显偏少（近乎满勤属于少数）。**偏度值仅为 0.01**，证实分布高度对称，既非左偏也非右偏。均值（79.98%）与中位数（80.0%）几乎完全重合，进一步印证了分布的平坦均匀形态。数据集中的最低出勤率为 60%，说明不存在极端缺课的情况。出勤率与期末成绩的皮尔逊相关系数高达 **r = 0.581**，是整个数据集中对目标变量预测力最强的单一变量。

---

**Caption:** Histogram illustrating the distribution of Previous Scores.
*(Insert `plots/histograms/Histogram_Previous_Scores.png`)*

**Key Data:**
| Statistic | Value |
|---|---|
| Mean | 75.07 |
| Median | 75.00 |
| Std Dev | 14.40 |
| Min | 50 |
| Q1 | 63 |
| Q3 | 88 |
| Max | 100 |

**English Insight:** `Previous_Scores` shows a far wider distribution (std = 14.4) compared to `Exam_Score` (std = 3.89). The Q3–Q1 range of 25 points reflects substantial heterogeneity in student baseline abilities entering the course. Interestingly, despite being a historical performance metric, its correlation with Exam_Score is only **r = 0.175**, which is unexpectedly weak — suggesting external factors actively reshape student rankings during the current term.

**中文洞察:** 过往成绩的标准差（14.40）是最终成绩标准差（3.89）的约 3.7 倍，分布范围从 50 到 100，极度扁平。这揭示了学生群体在入学时拥有极大的基础性差异。但意外的是，过往成绩与最终成绩的相关系数仅为 **r = 0.175**，远低于出勤率（0.581）等行为类指标。这暗示了历史成绩并非本数据集中最终成绩的主要推手，当期的行为习惯（出勤、学习时长）才是核心杠杆。

---

**Caption:** Histogram illustrating the distribution of Weekly Study Hours across the student population.
*(Insert `plots/histograms/Histogram_Hours_Studied.png`)*

**Key Data:**
| Statistic | Value |
|---|---|
| Sample size (n) | 6,607 |
| Mean | 19.98 |
| Median | 20.0 |
| Std Dev | 5.99 |
| Min | 1 |
| Q1 | 16 |
| Q3 | 24 |
| Max | 44 |

**English Insight:** The `Hours_Studied` distribution approximates a natural bell curve centered perfectly around 20 hours (mean=19.98, median=20.0). The visible left and right tails spread relatively evenly, capturing the minority of students who study either exceptionally little (near 0) or an intense amount (upwards of 40 hours). The integer binning (width=5) clearly highlights the concentration in the 15–25 hours central range.

**中文洞察:** `Hours_Studied` (每周学习时长) 的分布呈现出极其标准的钟形曲线，完美对称地以 20 小时为中心点（均值19.98，中位数20.0）。可见的左右尾部均匀散开，捕捉到了极少数几乎不学习（接近0小时）或学习强度极大（高达40小时以上）的极端学生群体。取整的分箱（距宽=5）清晰地突显了绝大多数学生集中在 15-25 小时的中间地带。

---

## 2. Violin & Box Plots: Categorical Drivers of Exam Score

> All violin/box plots use `box=True` and `points="outliers"`. Y-axis represents Exam Score (range 55–100). Ordinal categories are sorted High → Medium → Low; binary categories sorted by logical convention (Yes→No, No→Yes as appropriate).

> **Design note:** For any categorical feature vs. the target variable (`Exam_Score`), violin/box plots are exclusively used. Mean-bar charts were deliberately excluded — they mask distribution structure and suppress IQR/outlier information.

---

### 2a. Ordinal Categorical Variables

**Caption:** Violin plot illustrating the distribution of Exam Scores across Motivation Levels (High / Medium / Low).
*(Insert `plots/box_violin_plots/BoxViolin_Motivation_Level.png`)*

**Caption:** Violin plot illustrating the distribution of Exam Scores across Teacher Quality levels (High / Medium / Low / Unknown).
*(Insert `plots/box_violin_plots/BoxViolin_Teacher_Quality.png`)*

**Caption:** Violin plot illustrating the distribution of Exam Scores across Parental Involvement levels.
*(Insert `plots/box_violin_plots/BoxViolin_Parental_Involvement.png`)*

**Key Data — Medians, Means & IQR by ordinal level:**

| Variable | Level | Median | Mean | Q1 | Q3 | IQR |
|---|---|---|---|---|---|---|
| Motivation_Level | High | 67 | 67.70 | 65 | 70 | 5 |
| Motivation_Level | Medium | 67 | 67.33 | 65 | 69 | 4 |
| Motivation_Level | Low | 67 | 66.75 | 64 | 69 | 5 |
| Teacher_Quality | High | 68 | 67.68 | 65 | 70 | 5 |
| Teacher_Quality | Medium | 67 | 67.11 | 65 | 69 | 4 |
| Teacher_Quality | Low | 67 | 66.75 | 64 | 69 | 5 |
| Teacher_Quality | Unknown | 66 | 66.64 | 65 | 69 | 4 |
| Parental_Involvement | High | 68 | 68.09 | 66 | 70 | 4 |
| Parental_Involvement | Medium | 67 | 67.10 | 65 | 69 | 4 |
| Parental_Involvement | Low | 66 | 66.36 | 64 | 69 | 5 |

**English Insight:** The ordinal variables all show a consistent monotonic pattern: the `High` tier holds a higher median than `Low` in every case. However, the absolute differences are small — at most 2 points in median between extremes (e.g., Parental_Involvement High=68 vs Low=66). The IQRs are nearly identical across levels (4–5 points), and the violin shapes show that all tiers share essentially the same distribution shape. Notably, `Teacher_Quality` includes an `Unknown` category (n=78 students with missing teacher quality records), whose median (66) is marginally lower than the `Low` category (67), suggesting that lack of information about teacher quality may itself be a mild negative signal. This suggests these categorical factors provide a *systematic but modest* directional push, rather than acting as decisive sorting mechanisms. Their true value may lie in interaction effects with other variables.

**中文洞察:** 三个有序分类变量均呈现出一致的单调梯度模式：`High` 层级的中位数始终高于 `Low`。但绝对差异极为有限——极端分组间的中位数差距最大仅为 2 分（父母参与度 High=68 vs Low=66）。各等级的 IQR 也几乎一致（4–5 分），小提琴形态高度相似。尤其将注意的是，`Teacher_Quality` 包含一个 `Unknown` 类别（n=78，教师质量缺失记录的学生），其中位数（66）略低于 `Low` 类别（67），暴露出数据缺失本身可能是轻度负面信号。总体而言，这些类别变量对成绩提供的是**稳定但微弱的方向性推力**，而非决定性筛选机制。它们的真正价値可能在于与其他特征的交互效应上，单独使用其预测力有限。

---

### 2b. Binary / Nominal Categorical Variables

**Caption:** Violin plot illustrating the distribution of Exam Scores by Internet Access status (Yes / No).
*(Insert `plots/box_violin_plots/BoxViolin_Internet_Access.png`)*

**Caption:** Violin plot illustrating the distribution of Exam Scores by Learning Disability status (No / Yes).
*(Insert `plots/box_violin_plots/BoxViolin_Learning_Disabilities.png`)*

**Caption:** Violin plot illustrating the distribution of Exam Scores by School Type (Public / Private).
*(Insert `plots/box_violin_plots/BoxViolin_School_Type.png`)*

**Key Data — Binary feature comparisons:**

| Variable | Group | Median | Mean | Q1 | Q3 |
|---|---|---|---|---|---|
| Internet_Access | Yes | 67 | 67.29 | 65 | 70 |
| Internet_Access | No | 66 | 66.53 | 64 | 69 |
| Learning_Disabilities | No | 67 | 67.35 | 65 | 70 |
| Learning_Disabilities | Yes | 66 | 66.27 | 64 | 68 |
| School_Type | Private | 67 | 67.29 | 65 | 70 |
| School_Type | Public | 67 | 67.21 | 65 | 69 |

**English Insight:** All three binary features show nearly identical medians (each at 66–67). The mean differences are tiny: Internet Access (0.76 pts), Learning Disabilities (1.08 pts), School Type (0.08 pts). School Type in particular has virtually zero impact on median score. The slight penalisation for `Learning_Disabilities = Yes` (mean 66.27 vs 67.35) is plausibly an underestimate due to survivorship bias — students with severe disabilities may have been excluded from the original sample. These findings counter intuitions about strong group-level penalties and suggest that *behaviour and resource allocation*, not group membership, are the primary score drivers.

**中文洞察:** 三个二元特征的中位数几乎重叠（均在 66–67 之间）。均值差距极小：网络访问权限差距仅 0.76 分、学习障碍差距 1.08 分、学校类型差距仅 0.08 分——**School_Type 对成绩的影响实际上接近于零**。Learning_Disabilities 对成绩的轻微惩罚（66.27 vs 67.35）可能被幸存者偏差低估——有严重学习障碍的学生可能根本没有出现在数据集中。这组发现的核心结论是：**群体身份标签（学校类型、网络、障碍状态）对成绩的直接贡献远小于行为习惯变量（出勤、学习时长）**，这对资源干预策略具有重要的现实政策含义。

---

## 3. Donut Charts: Demographic Sub-population Proportions

> Ordinal categories (Family_Income) are sorted Low → Medium → High. Nominal categories (School_Type, Learning_Disabilities) are sorted by descending count (course rule: "Values must be sorted").

**Caption:** Donut chart illustrating the proportional breakdown of the student sample by Family Income level.
*(Insert `plots/pie_charts/Pie_Family_Income.png`)*

**Key Data:**

| Income Level | Count | % |
|---|---|---|
| Low | 2,672 | 40.4% |
| Medium | 2,666 | 40.4% |
| High | 1,269 | 19.2% |

**Caption:** Donut chart illustrating the proportional breakdown of the student sample by School Type.
*(Insert `plots/pie_charts/Pie_School_Type.png`)*

**Key Data:**

| School Type | Count | % |
|---|---|---|
| Public | 4,598 | 69.6% |
| Private | 2,009 | 30.4% |

**Caption:** Donut chart illustrating the proportional breakdown of students by Learning Disability status.
*(Insert `plots/pie_charts/Pie_Learning_Disabilities.png`)*

**Key Data:**

| Status | Count | % |
|---|---|---|
| No | 5,912 | 89.5% |
| Yes | 695 | 10.5% |

**English Insight:** The sample is heavily skewed: Low and Medium income groups each account for ~40% while High income is under-represented at 19.2%. Public schools dominate at 69.6%. Students with learning disabilities are a small minority at 10.5%. These imbalances must be flagged during modelling: an algorithm optimising average performance may *systematically neglect minority subgroups* (High income, Private school, Learning Disabilities = Yes) unless stratified sampling or weighted metrics are applied in Phase 4.

**中文洞察:** 样本结构存在严重偏斜：低收入和中等收入各约占 40%，高收入家庭仅占 19.2%，严重不足。公立学校以 69.6% 的绝对多数主导样本。有学习障碍的学生仅占 10.5%。这些类别不平衡在建模阶段具有重要含义：未经处理的标准损失函数会将高收入、私立学校、学习障碍群体的损失稀释进整体均值中，使得模型在核心多数群体上表现良好，但在关键少数群体上系统性失效。Phase 4 中必须采用分层抽样或类别权重调整来解决此问题。

---

## 4. Line Charts: Attendance & Time Allocation vs Exam Score

**Caption:** Line chart showing the trend of average Exam Score by weekly Study Hours (binned).
*(Insert `plots/line_charts/Line_Hours_Studied.png`)*

**Key Data:**

| Study Hours Bin | Avg Exam Score |
|---|---|
| 0–8 hrs/week | 63.66 |
| 9–16 hrs/week | 65.31 |
| 17–24 hrs/week | 67.34 |
| 25–32 hrs/week | 69.51 |
| 33+ hrs/week | 71.25 |

**Caption:** Line chart showing the trend of average Exam Score by nightly Sleep Hours.
*(Insert `plots/line_charts/Line_Sleep_Hours.png`)*

**Key Data:**

| Sleep Hours | Avg Exam Score |
|---|---|
| 4 hrs | 67.63 |
| 5 hrs | 67.30 |
| 6 hrs | 67.19 |
| 7 hrs | 67.24 |
| 8 hrs | 67.22 |
| 9 hrs | 67.15 |
| 10 hrs | 67.14 |

**Caption:** Line chart showing the trend of average Exam Score by number of Tutoring Sessions.
*(Insert `plots/line_charts/Line_Tutoring_Sessions.png`)*

**Key Data:**

| Tutoring Sessions | Avg Exam Score |
|---|---|
| 0 | 66.49 |
| 1 | 66.98 |
| 2 | 67.57 |
| 3 | 67.89 |
| 4 | 68.23 |
| 5 | 69.06 |
| 6 | 71.67 |
| 7 | 69.86 |
| 8 | 69.00 |

**Caption:** Line chart showing the trend of average Exam Score by Class Attendance rate (binned into 5-point intervals).
*(Insert `plots/line_charts/Line_Attendance.png`)*

**Key Data:**

| Attendance Bin | Avg Exam Score |
|---|---|
| 60–65% | 63.67 |
| 65–70% | 64.68 |
| 70–75% | 65.81 |
| 75–80% | 66.72 |
| 80–85% | 67.47 |
| 85–90% | 68.67 |
| 90–95% | 69.70 |
| 95–100% | 70.52 |

**English Insight:**
1. **Attendance:** The most consistent and steepest positive slope of all four line charts — the single strongest behavioural predictor (Pearson r = 0.581). Average score rises monotonically from **63.67** (60–65% attendance) to **70.52** (95–100%), a total spread of **+6.85 points**. The relationship is nearly perfectly linear with no plateau or inflection, confirming that every additional percentage point of attendance yields a measurable gain in exam outcome.
2. **Study Hours:** The clearest linear positive elasticity in the entire basic chart set. Students studying 0–8 hours average just 63.66, while 33+ hours yields 71.25 — a spread of **7.59 points** across the full range. This is the largest absolute score delta of any line chart variable.
3. **Sleep Hours:** Debunks the monotonic assumption entirely. The score plateau between 4–10 hours is remarkably flat (67.63 down to 67.14 — a total range of **just 0.49 points**). There is no sweet spot; sleep in this dataset has virtually no measurable impact on exam performance. This may reflect insufficient variance in the `Sleep_Hours` column or confounding with other variables.
4. **Tutoring Sessions:** Shows a generally positive trend (0 sessions = 66.49, 6 sessions = 71.67), but the pattern breaks at 7–8 sessions (69.86, 69.00) suggesting diminishing returns. The peak at 6 sessions (+5.18 points above zero) suggests an optimal dosage effect.

**中文洞察:**
1. **出勤率：** 四张折线图中斜率最一致、最陡峭的正向趋势——也是整个数据集中单一最强的行为预测变量（r = 0.581）。平均分从 60–65% 出勤区间的 **63.67** 单调上升至 95–100% 区间的 **70.52**，全量程跨度达 **+6.85 分**。关系近乎完美线性，无平台期或拐点，证实每提高一个百分点的出勤率均能带来可测量的成绩增益。
2. **学习时长：** 是基础图表集中弹性最清晰的正向线性变量。从 0–8 小时的均分 63.66，到 33+ 小时的均分 71.25，全量程差距高达 **7.59 分**。这是四张折线图中最大的绝对成绩跨度。
3. **睡眠时间：** 彻底颠覆了单调递增的刻板印象。从 4 小时到 10 小时，成绩的整体波动幅度仅为 **0.49 分**（67.63 → 67.14）——几近于零的影响。在这个数据集中，睡眠时间对成绩实际上没有可测量的统计影响，可能存在与其他变量的混淆效应，或该列在数据采集时的精度不足。
4. **辅导次数：** 总体趋势为正（0 次 66.49 → 6 次 71.67），但在 7–8 次时开始下降（69.86、69.00），说明存在**边际收益递减效应**，最优投入量大约在 6 次附近（比零次高出 5.18 分）。

