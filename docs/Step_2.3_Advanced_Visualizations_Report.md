# Phase 2: Step 2.3 — Advanced Visualizations Report
## Bilingual Insights, Chart Relevance Justification & Captions — with Embedded Data Values

> All numerical values are extracted directly from `StudentPerformanceFactors_cleaned.csv` (n = 6,607 students).

---

## 1. Scatter Plots with Marginal Distributions

> Jitter (±0.4) applied to discrete integer X-axes to prevent striational overplotting. Opacity = 0.3. OLS trendlines applied. Legends anchored outside the plot area (right side, x=1.05) to prevent overlap with marginal panels.

**Caption:** Scatter plot with marginal histogram (X-axis) and box plot (Y-axis), illustrating the relationship between Exam Score and Class Attendance, stratified by Motivation Level.
*(Insert `plots/scatter_plots/Scatter_Attendance_Score.png`)*

**Caption:** Scatter plot with marginal histogram (X-axis) and box plot (Y-axis), illustrating the relationship between Exam Score and Previous Scores, stratified by Internet Access status.
*(Insert `plots/scatter_plots/Scatter_Previous_Score.png`)*

**Caption:** Scatter plot with marginal histogram (X-axis) and box plot (Y-axis), illustrating the relationship between Exam Score and Weekly Study Hours, stratified by Family Income.
*(Insert `plots/scatter_plots/Scatter_Hours_Score.png`)*

**Key Data — Pairwise Correlations:**

| Variable Pair | Pearson r | Interpretation |
|---|---|---|
| Attendance vs Exam_Score | **0.581** | Strong positive — the #1 predictor |
| Hours_Studied vs Exam_Score | **0.446** | Moderate positive — the #2 predictor |
| Previous_Scores vs Exam_Score | **0.175** | Weak positive — surprisingly low |

**Why Relevant to This Dataset / 为何与本数据集高度相关:**
This dataset contains multiple continuous numerical variables (Attendance, Previous_Scores, Hours_Studied, Exam_Score) whose pairwise relationships are unknown prior to analysis. A scatter plot is the standard tool for detecting linear association between two quantitative variables; the OLS trendline makes the slope direction and gradient immediately visible. The marginal distributions reveal both axes simultaneously, exposing not just correlation but the non-overlapping density zones that reveal subgroup differences. With n = 6,607 observations, overplotting is severe without jitter and opacity adjustments — both of which are applied here.

本数据集包含多个连续数值变量（出勤率、过往成绩、学习时长、期末成绩），其两两关系在分析前未知。散点图是检测两个定量变量线性关联关系的标准工具，OLS 拟合线使斜率方向与梯度直接可读。边缘分布同时揭示两个轴的密度形态，不仅展示相关性，还暴露揭示群体差异的非重叠密度区域。在 n=6,607 的大样本下，若不施加抖动（jitter）和透明度调整，点图会严重重叠，上述处理均已应用。

**English Insight:** The scatter plot for Attendance reveals the strongest linear relationship in the entire dataset (r = 0.581). The OLS trendline rises sharply as attendance increases from 60% to 100%, and the marginal box plots on the Y-axis confirm that high-motivation students (green) hold a visibly tighter upper IQR versus low-motivation (red), though all tiers share overlapping cores. The `Hours_Studied` scatter (r = 0.446) shows the second-strongest positive slope: the trendlines for all three income groups (High, Medium, Low) are nearly parallel, confirming that the return on study hours is approximately equal across income groups — effort, not background, drives score improvement here. The `Previous_Scores` scatter is unexpectedly diffuse (r = 0.175) — the cloud of points shows far more vertical spread than one would expect from a "prior performance" predictor, suggesting that historical scores are poor proxies for current-term outcomes in this cohort.

**中文洞察:** 出勤率散点图揭示了整个数据集中最强的线性关系（**r = 0.581**），OLS 拟合线从 60% 出勤率到 100% 呈明显上升趋势。右侧边缘箱线图进一步揭示：高动力学生（绿）的 Q3 略高于低动力学生（红），尽管三组核心分布高度重叠。学习时长散点图（**r = 0.446**）展示了第二强的正向斜率：高、中、低收入三个群体的 OLS 拟合线近乎平行，说明学习时长对成绩的回报率在不同收入背景下基本一致——努力程度而非家庭背景，才是这一区间内推动成绩提升的驱动力。过往成绩散点图的结论更为反直觉：**r = 0.175 的极弱相关性**意味着历史成绩对当期成绩的预测力极为有限——竖直方向的超大离散度说明同等历史成绩的学生，期末表现可以相差悬殊。

---

## 2. 2D Density Contour

**Caption:** 2D density contour plot with marginal histograms, visualising the joint density distribution between Previous Scores and final Exam Scores.
*(Insert `plots/scatter_plots/DensityContour_Previous_Exam.png`)*

**Key Data:**
- X-axis (`Previous_Scores`): range 50–100, mean 75.07, std 14.40
- Y-axis (`Exam_Score`): range 55–100, mean 67.24, std 3.89
- Pearson r (Previous vs Exam): **0.175**

**Why Relevant to This Dataset / 为何与本数据集高度相关:**
With 6,607 individual points on a scatter plot, coincident observations cause severe overplotting — points pile on top of one another and the true density structure becomes invisible. A 2D density contour replaces individual dots with nested iso-density curves (analogous to a topographic map), accurately representing the probability mass of the joint distribution. This chart is specifically chosen because this dataset's extremely narrow Exam_Score range (std = 3.89) compresses nearly all points into a band just 8 points wide on the Y-axis, which standard scatter plots render as an undifferentiated mass. Contour curves allow the true centre of mass to be precisely located.

在 6,607 个点的散点图中，重叠观测造成了严重的过度绘制问题——点层叠在一起，真实密度结构变得不可见。2D 密度等高线图用嵌套等密度曲线（类似地形图）替代了单个点，准确呈现联合分布的概率密度分布。该图表被特别选用，是因为本数据集极窄的 Exam_Score 分布（std=3.89）将几乎所有点压缩进 Y 轴上仅 8 分宽的区间，标准散点图会将其渲染为一团无法区分的密集点云。等高线使真实的质量中心得以精确定位。

**English Insight:** The density contour solves the overplotting problem inherent in n = 6,607 scatter plots. The innermost contour ring — the highest-density region — is centred at approximately Previous_Score ≈ 75–80, Exam_Score ≈ 65–68. This is where the bulk of the student population resides. The elongated, near-horizontal orientation of the contour ellipses (wide in X, compressed in Y — rather than a diagonal 45° slope) visually confirms the weak r = 0.175 correlation: across the entire range of prior scores (50–100), the final exam scores remain packed into the same narrow band of approximately 63–72, confirming that historical scores have almost no locking effect on current outcomes.

**中文洞察:** 2D 密度等高线图从根本上解决了 6,607 个数据点的极度密集重叠问题。最内圈的最高密度坐标区域集中在 Previous_Score ≈ 75–80、Exam_Score ≈ 65–68 的交叉地带，这是学生群体的真实人口质心。等高线椭圆呈**横向扁平拉伸**的形态（X 轴方向宽而 Y 轴方向窄），而非理想相关下的 45° 斜向带状——这以视觉语言直接证实了 **r = 0.175 的弱相关性**：在 50–100 的整个历史成绩范围内，期末成绩始终被压缩在约 63–72 的同一窄带中，说明历史成绩对当期终点几乎没有锁定效应。

---

## 3. Multi-Dimensional Bubble Chart

**Caption:** Bubble chart illustrating the joint relationship between Attendance, Exam Score, Study Hours (bubble size), and Motivation Level (colour), simultaneously encoding four variables.
*(Insert `plots/advanced/Bubble_Attendance_Score_Hrs.png`)*

**Key Data — Bubble dimensions:**

| Visual Element | Variable (source) | Range in data |
|---|---|---|
| X-axis | Attendance (%) | 60–100 |
| Y-axis | Exam Score | 55–100 |
| Bubble size | Hours_Studied (weekly) | 1–44 hrs |
| Colour | Motivation_Level | High / Medium / Low |

**Key summary statistics:**

| Motivation | Avg Exam Score | Avg Attendance (%) | Avg Hrs Studied |
|---|---|---|---|
| High | 67.70 | 79.71 | 19.73 |
| Medium | 67.33 | 80.11 | 20.08 |
| Low | 66.75 | 79.93 | 19.96 |

**Why Relevant to This Dataset / 为何与本数据集高度相关:**
This dataset uniquely contains four variables hypothesised to interact — Attendance, Hours_Studied, Motivation_Level, and Exam_Score. Standard 2D plots can reveal only two of these relationships at once, obscuring the compounding or moderating effects. A bubble chart is the correct multi-dimensional extension: it uses the preattentive attributes of position (X, Y), size (bubble), and colour (motivation) simultaneously — directly aligned with the course principle of leveraging preattentive attributes to reduce cognitive load. This chart is specifically justified because the interaction of Attendance × Hours_Studied is central to the study's equity hypothesis: students who maintain high attendance *and* invest high study hours are predicted to show disproportionately superior outcomes.

本数据集独特地包含四个被假设存在交互效应的变量——出勤率、学习时长、动力水平与期末成绩。标准的二维图表每次只能揭示其中两种关系，会遮蔽复合或调节效应。气泡图是正确的多维扩展工具：它同时使用位置（X、Y）、大小（气泡）和颜色（动力）三种前注意属性，与课程原则中"利用前注意属性降低认知负荷"直接对应。该图的选用基于明确依据：出勤率与学习时长的交互效应是本研究公平性假说的核心——同时维持高出勤率和高学习时长投入的学生，预期展现不成比例的压倒性优势。

**English Insight:** The bubble chart compresses four dimensions into a single 2D view. While the overall point cloud occupies the same diagonal band (confirming the attendance–score correlation of r=0.581), the bubble sizes reveal a second dimension: larger bubbles tend to cluster toward the upper-right quadrant, confirming that study hours amplify the attendance effect. Students with high motivation, high attendance *and* large bubble sizes consistently appear in the top-right zone. This interaction effect between attendance and study hours is not visible in simple scatter plots or violin charts — it requires this 4D encoding to emerge.

**中文洞察:** 气泡图将四个维度压缩进同一张二维画面。整体点云沿对角线分布（印证了出勤率与成绩 r=0.581 的相关性），但气泡大小揭示了第二个维度：大气泡（高学习时长）系统性地向右上角聚集，证明了**学习时长对出勤率效应的放大作用**（交互效应）。同时拥有高动力、高出勤率、大气泡的学生，集中盘踞在高分区的右上角。这种出勤 × 学习时长的协同效应，在简单散点图或小提琴图中均无法直接观察到，是 4D 编码独有的洞察。

---

## 3b. Clustered Bar Chart: Cross-Tabulation of Categorical Features

**Caption:** Clustered bar chart showing the count of students segmented by School Type and Internet Access status, with Y-axis starting at zero per best practice.
*(Insert `plots/advanced/ClusteredBar_SchoolType_Internet.png`)*

**Key Data — Exact counts:**

| School Type | Internet Access | Count | % of Total |
|---|---|---|---|
| Public | Yes | 4,261 | 64.5% |
| Public | No | 337 | 5.1% |
| Private | Yes | 1,847 | 28.0% |
| Private | No | 162 | 2.5% |

**Key observations:**
- Overall internet coverage rate: **92.5%** of all 6,607 students have internet access
- Public school internet coverage: 4,261 / (4,261+337) = **92.7%**
- Private school internet coverage: 1,847 / (1,847+162) = **91.9%**
- Internet access rates are nearly identical across school types (92.7% vs 91.9%)

**Why Relevant to This Dataset / 为何与本数据集高度相关:**
A common assumption in education research is that private schools provide better technological infrastructure, creating an internet access gap between public and private students. This dataset contains both `School_Type` and `Internet_Access` as categorical variables, making a cross-tabulation essential to test this assumption directly. A clustered bar chart is the optimal chart type for comparing frequencies across two categorical variables simultaneously: Y-axis starts at zero (mandatory bar chart rule), bars are grouped side-by-side enabling direct visual comparison, and absolute counts are immediately readable. A stacked bar would obscure within-group proportions; a table alone would lack visual immediacy.

教育研究中一个普遍假设是私立学校提供更好的技术基础设施，造成公私立学生之间的网络访问差距。本数据集同时包含 `School_Type` 和 `Internet_Access` 两个类别变量，使交叉制表成为直接检验这一假设的必要手段。簇状条形图是同时比较两个类别变量频率的最优图表类型：Y 轴从零开始（条形图强制规则），条形并排显示便于直接视觉比较，绝对计数即时可读。堆叠条形图会遮蔽组内比例信息；单纯的表格缺乏视觉直观性。

**English Insight:** This chart reveals a critical structural finding: internet access is ubiquitous across both school types, with coverage rates of 92.7% (Public) and 91.9% (Private). The difference between school types is entirely driven by sample size, not by access disparity. This means `School_Type` and `Internet_Access` are NOT meaningfully correlated with each other, validating that they measure independent dimensions of student circumstances. For modelling in Phase 4, both variables can be included without multi-collinearity concerns, though their individual predictive power is low (mean score difference of only 0.76 pts for internet access and 0.08 pts for school type).

**中文洞察:** 这张图揭示了一个反直觉的关键事实：两类学校的网络访问覆盖率**几乎完全相同**（公立 92.7% vs 私立 91.9%），差距仅不足 1 个百分点。两类学校在图表上的绝对数量差异，完全来自样本规模不同（公立 4,598 人 vs 私立 2,009 人），而非访问率差异。这个发现有重要建模含义：`School_Type` 与 `Internet_Access` 两个变量并不相互关联，代表了学生处境的两个独立维度，可放心同时纳入 Phase 4 模型而无多重共线性之忧。

---

## 4. Parallel Categories Diagram

> Ordinal categories sorted logically: Family Income (Low → Medium → High), Access to Resources (Low → Medium → High), Motivation Level (Low → Medium → High). Colour intensity proportional to Exam Score.

**Caption:** Parallel Categories diagram tracing the flow of student demographic background (Family Income → Resource Access → Motivation Level) through to final academic outcome (Score Bin).
*(Insert `plots/advanced/ParallelCategories_BackgroundFlow.png`)*

**Key Data — Score distribution by bin (qcut tertiles):**

| Score Bin | Approximate range | % of students |
|---|---|---|
| Low Scorers | 55–66 | ~43% |
| Mid Scorers | 67–69 | ~32% |
| High Scorers | 70–100 | ~25% |

**Key Data — Underlying distributions by Income:**

| Family Income | Count | % |
|---|---|---|
| Low | 2,672 | 40.4% |
| Medium | 2,666 | 40.4% |
| High | 1,269 | 19.2% |

**Why Relevant to This Dataset / 为何与本数据集高度相关:**
This dataset captures a socioeconomic pipeline: Family Income influences Access to Resources, which shapes Motivation Level, which ultimately affects Exam Score. This is a causal chain hypothesis that cannot be tested with simple bivariate charts — it requires tracing the *flow* of students across multiple categorical stages simultaneously. A Parallel Categories diagram is the ideal tool for this: it represents each student as a flow ribbon through sequential categorical axes, enabling aggregated pathway analysis that a heat map or grouped bar chart cannot provide. The colour encoding by Exam Score allows the outcome to be embedded directly into the flow, making the inequality cascade immediately perceptible. This chart is uniquely justified by the dataset's multi-stage socioeconomic hypothesis.

本数据集捕捉了一条社会经济管道：家庭收入影响资源获取能力，资源获取能力塑造动力水平，动力水平最终影响期末成绩。这是一个因果链假设，无法用简单的二元图表检验——需要同时追踪学生在多个类别阶段之间的**流动路径**。平行类别图是实现这一目标的理想工具：它将每位学生表示为穿越连续类别轴的流动带，提供热力图或分组条形图无法实现的聚合路径分析。按期末成绩对颜色编码，使得结果直接嵌入流动图中，不平等级联效应即时可见。本图的选用基于数据集多阶段社会经济假说的独特需要。

**English Insight:** The Parallel Categories diagram depicts the demographic pipeline from socioeconomic origin to academic outcome. The key narrative: High-income students who access high-quality resources and develop high motivation predominantly converge in the "High Scorers" bin. Conversely, the Low-income flow attaches disproportionately to lower resource and motivation tiers, feeding more mass into the "Low Scorers" pool. The colour scale (teal intensity = higher score) makes this inequality cascade immediately perceptible. This single chart is the most complete argument for this project's socioeconomic inequality hypothesis.

**中文洞察:** 平行类别图以上帝视角描绘了从社会经济背景到最终学术成就的完整人口流动管道。核心叙事：高收入家庭 → 高资源获取能力 → 高驱动力 → 高分成果水池，这条黄金通道以最高的通量汇聚了绝大多数高分学生。与此相反，低收入的学生流向低资源、低动力的通道，进而不成比例地流入低分水池。颜色深度（越亮=越高分）让这道不平等瀑布的视觉冲击几乎是即时的。这张图以单页之力，承载了本项目社会经济不平等假说的全部核心论据。

---

## 5. Correlation Heatmap

**Caption:** Correlation heatmap displaying pairwise Pearson correlation coefficients among all numerical features.
*(Insert `plots/heatmaps/Heatmap_Correlation.png`)*

**Key Data — Correlations with Exam_Score (sorted by strength):**

| Feature | r (with Exam_Score) | Interpretation |
|---|---|---|
| Attendance | **0.581** | Strong positive — dominant predictor |
| Hours_Studied | **0.446** | Moderate positive |
| Previous_Scores | **0.175** | Weak positive |
| Tutoring_Sessions | **0.156** | Weak positive |
| Physical_Activity | **0.028** | Negligible |
| Sleep_Hours | **-0.017** | Negligible (near zero) |

**Why Relevant to This Dataset / 为何与本数据集高度相关:**
The dataset contains 7 numerical variables, generating 21 unique pairwise correlations. Reviewing correlation coefficients in table form requires reading 21 numbers sequentially and holding them in working memory — a high cognitive load task. A heatmap encodes all 21 values simultaneously via colour, enabling the audience to identify the strongest and weakest correlations at a glance using pre-attentive colour processing. This is particularly critical as a pre-modelling diagnostic: it screens for both (a) which variables most strongly predict Exam_Score and (b) whether any pair of input variables are dangerously co-linear (which would inflate coefficient estimates in regression). The diverging RdBu_r palette (centred on zero) is the standard choice for correlation matrices, as it visually separates positive and negative correlations with maximum perceptual contrast.

本数据集包含 7 个数值变量，产生 21 对独立的两两相关系数。在表格形式中逐一阅读 21 个数值需要高度的认知努力。热力图通过颜色同时编码全部 21 个值，使受众能够利用前注意颜色处理机制，一眼识别最强和最弱的相关关系。这作为建模前诊断工具尤为关键：它同时检查 (a) 哪些变量对 Exam_Score 的预测力最强，以及 (b) 是否存在危险的输入变量共线性（会在回归中导致系数估计失真）。发散型 RdBu_r 调色板（以零为中轴）是相关矩阵的标准选择，能以最大感知对比度区分正负相关关系。

**English Insight:** The RdBu_r diverging palette heatmap provides the pre-modelling diagnostic blueprint. The key findings: (1) `Attendance` (r=0.581) and `Hours_Studied` (r=0.446) dominate as behavioural predictors; (2) `Previous_Scores` (r=0.175) is surprisingly weak for a historical performance metric; (3) `Sleep_Hours` (r=−0.017) and `Physical_Activity` (r=0.028) contribute essentially nothing to exam score prediction. (4) No pair of *input* features shows dangerously high inter-correlation (no red cells off the diagonal), clearing the dataset of multi-collinearity concerns. All numerical features can be safely included in Phase 4 models without penalty.

**中文洞察:** 红蓝双向对撞色相关热力图是建模前的终极诊断图。核心发现：(1) **行为习惯类变量（出勤 0.581、学习时长 0.446）**毫无争议地主宰了预测力排行榜，远超所有其他特征；(2) 过往成绩（0.175）作为历史表现基线，实际预测力异常的弱；(3) 睡眠时长（-0.017）与体育锻炼（0.028）对成绩几乎没有可测量的直接效应，可能在非线性模型中有间接价值，但在线性回归中贡献极小；(4) 所有输入变量之间均无危险的高度共线性（对角线以外无深红色格子），确认了 Phase 4 可以安全地将所有数值特征全部纳入，无需额外的多重共线性处理。
