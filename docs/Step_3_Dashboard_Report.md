# Phase 3: Step 3 — Streamlit Dashboard Report (仪表盘构建报告)
## Audience Definition, Design Logic, Chart Justification & Key Insights / 受众定义、设计逻辑、图表依据与核心洞察

---

## 1. Dashboard Audience & Purpose / 仪表盘受众与目标

**Primary Audience / 核心受众:**
School Administrators and Education Policy Makers (学校管理者与教育政策制定者)

**Why This Audience? Justification / 为何选定此受众群体？论证**

School administrators and policy makers are responsible for allocating teaching resources, designing intervention programmes, and formulating equity policies — yet they typically lack direct access to granular student-level data analysis. They need a tool that translates raw data into **decision-ready evidence** without requiring statistical expertise. This dashboard is specifically designed to answer three strategic management questions that are beyond the scope of classroom teachers but are critical for institutional leadership: (a) how is the cohort performing relative to itself, (b) which controllable inputs offer the highest return on intervention investment, and (c) where do systemic inequalities fracture opportunity pipelines.

学校管理者和政策制定者承担着分配教学资源、设计干预方案与制定公平政策的职责——然而他们通常缺乏直接获取细粒度学生数据分析的渠道，需要一个能将原始数据转化为**决策级证据**的工具，且无需统计学专业知识背景。本仪表盘专为回答三项超越课堂层级、但对机构领导层至关重要的战略管理问题而设计：(a) 该学生群体相对自身的表现状态，(b) 哪些可控投入要素能提供最高的干预回报率，以及 (c) 系统性不平等在何处断裂了机会管道。

**Core Business Questions the Dashboard Answers / 仪表盘解答的核心商业问题:**
1. **What is the current performance landscape? (当前的学业表现全貌是怎样的？)**
   Baseline score and attendance distribution across the cohort. (整个学生群体的基线成绩与出勤率分布图景。)
2. **What behaviours and resources drive exam scores? (哪些行为与资源切实驱动了期末成绩？)**
   Elasticity of attendance, study hours, and tutoring against static historical baselines. (出勤率、学习时长、辅导次数相较于静态历史基线的拉动弹性。)
3. **Are outcomes equal across student subgroups? (各弱势或细分群体的最终学业结果公平吗？)**
   Demographic composition, resource access gaps, and systemic flow paths from socioeconomic origin to academic outcome. (人口构成、资源获取鸿沟，以及从社会经济出身到最终学业成果的系统性流向路径。)


---

## 2. Logical Dashboard Narrative (Section Sequence) / 仪表盘叙事逻辑 (功能分区顺序)

The dashboard strictly adheres to the course's *Principle #4 (Story Telling with Data)*, establishing a highly dense, 3-section policy narrative without relying on excessive text descriptions (maximizing Data-Ink-Ratio):
仪表盘严格遵循课程标准中的 *原则4 (用数据讲故事)*，构建了一个高密度、强逻辑的三段式政策分析叙事，且摒弃了冗长的文字赘述（实现数据墨水比最大化）：

```text
① SCORE & ATTENDANCE BASELINE (Context) / 成绩与出勤基线 (背景设定)
       ↓ What does "normal" look like in this cohort? (在这个学生群体中，"常态"究竟是何种表现水平？)
② BEHAVIOURAL & RESOURCE DRIVERS (Analysis) / 行为与资源驱动要素 (深度分析)
       ↓ Which controllable inputs offer the highest ROI? (哪些可控的主观投入要素具有最高的投资回报率？)
③ EQUITY ANALYSIS & SYSTEMIC OUTCOMES (Action) / 公平性分析与系统性结果 (支撑行动导向)
       ↓ How does socioeconomic origin shape the final outcome distribution? (社会经济出身如何潜移默化地塑造了最终的成绩分布结构？)
```

---

## 3. Interactive Global Filters (Sidebar) / 全局交互过滤器 (侧边栏)

To adhere to *Best Practice: Interactivity*, a narrow (180px) global sidebar allows continuous drill-down without consuming horizontal chart space.
为匹配 *最佳实践：交互性设计*，我们采用了极窄设定 (180px) 的全局侧边栏，它允许受众持续进行数据下钻，同时最大程度保留横向的图表空间资源。

| Filter (过滤器) | Variable (变量字段) | Values (可选项) |
|---|---|---|
| School Type (学校类型) | `School_Type` | Public (公立) / Private (私立) |
| Family Income (家庭收入) | `Family_Income` | Low (低) / Medium (中) / High (高) |
| Motivation Level (学习动力) | `Motivation_Level` | High (高) / Medium (中) / Low (低) |
| Internet Access (网络接入) | `Internet_Access` | Yes (有) / No (无) |

---

## 4. Section-by-Section Chart Justification / 分区图表设计依据

### Section ①: Score & Attendance Baseline (成绩与出勤基线)

| Chart (图表模块) | Course Principle Alignment & Justification (课程原则对齐与选用依据) |
|---|---|
| KPI Metric Cards (关键指标卡) | **Clarity & Simplicity (清晰与极简)**: Immediate quantitative grounding (n=6,607, Mean Score=67.24, Avg Attendance=80%). <br> 提供最直白的量化锚点。 |
| Exam Score Histogram (期末成绩直方图) | **Distribution Analysis (分布分析)**: Reveals the shape of outcomes—a tight IQR (65–70) with a right-skewed high-performing tail. <br> 揭示成绩的总体形态结构（右偏的高分长尾）。 |
| Attendance Histogram (出勤率直方图) | **Distribution Analysis (分布分析)**: Identifies the behavioral baseline—heavily left-skewed, confirming most students attend >70% of classes. <br> 明确行为基线：严重左偏，证实绝大多数学生出勤率>70%。 |
| Previous Scores Histogram (过往成绩直方图) | **Distribution Analysis (分布分析)**: Establishes the historical academic baseline for comparison against final outcomes. <br> 确立历史学业基准，以便与期末最终成绩对标。 |

### Section ②: Behavioural & Resource Drivers (行为与资源驱动要素)

| Chart (图表模块) | Course Principle Alignment & Justification (课程原则对齐与选用依据) |
|---|---|
| 3x Line Charts (Trend vs Score) <br> (3组折线图：核心行为投入趋势对分数的拉动) | **Line Chart Best Practices (折线图最佳实践)**: Y-axis does not artificially start at 0 (allows trend visibility); clear markers applied to avoid over-smoothing. Highlights strong positive ROI for Study Hours (Δ +7.59 pts) vs near-zero ROI for Sleep Hours.<br> **依据**：Y轴并未强行从0起步以凸显真实起伏趋势，使用数值点标记拒绝平滑曲线。直观暴露了学习时长的强ROI与睡眠时长的零ROI。 |
| Scatter: Score vs Attendance<br> (散点图：出勤率与分数) | **Scatterplot Principles (散点图原则)**: Uses OLS trendline to prove positive correlation; Attendance is the strongest predictor. <br> **依据**：通过直角坐标与拟合线直观展示两组数值的“正相关”关系；出勤率是极强预测指标。 |
| Scatter: Score vs Previous<br> (散点图：历史成绩与分数) | **Scatterplot Principles (散点图原则)**: Proves a surprisingly weak positive correlation visually.<br> **依据**：在直观视觉上反常地展现出极其微弱的相关性，证明“历史成绩”不是期末成绩的强决定器。 |
| 4D Bubble Chart<br> (四维气泡图) | **Advanced Charts (高级图表)**: Simultaneously plots Attendance, Exam Score, Study Hours (Size), and Motivation (Colour), leveraging multiple preattentive attributes to reveal a compounding synergy effect.<br> **依据**：在一个平面内同时整合4个维度，完美利用了人眼的“前注意属性(颜色/大小)”，揭示出“高出勤+高学习时长+高动力”对高分垄断的复合协同暴击。 |

### Section ③: Equity Analysis & Systemic Outcomes (公平性分析与系统性结果)

| Chart (图表模块) | Course Principle Alignment & Justification (课程原则对齐与选用依据) |
|---|---|
| 3x Donut Charts<br> (3组环形占比图) | **Pie Chart Rules (饼图标准)**: Categories ≤ 5; Values are strictly sorted in descending order.<br> **依据**：分类数皆在5以内，同时按降序排列数值；精准揭示高收入家庭(19.2%)及学习障碍群体(10.5%)为绝对的少数派。 |
| Clustered Bar: School Type × Internet<br> (簇状条形图：学校×网络) | **Advanced Charts / Bar Rules (高级图表规范)**: Y-axis strictly starts at 0; compares totals across two categorical features.<br> **依据**：Y轴严密守住从0开始底线；对比了两项类别变量，证明无论公私立，网路铺设(92%+)几乎无差别，排除了“网沟定律”。 |
| Parallel Categories Diagram<br> (平行类别流动图) | **Story Telling (数据讲故事)**: Traces the systemic pipeline: Family Income → Access to Resources → Motivation Level → Score Bin.<br> **依据**：如同一张社会漏斗，强叙事性地追踪了不同阶层起步的学生，是如何经历资源与动机分化，最终掉落进高低分水岭。 |
| Correlation Heatmap<br> (相关矩阵热力图) | **Advanced Charts / Colour Rules (高级图表色彩规范)**: Uses a continuous diverging palette (`RdBu_r`) centered on 0.<br> **依据**：严格使用了以0为中轴的发散色盘（红蓝对撞），极快排查所有数字特征间的共线性与隐性关联，也是为Phase 4建模埋下伏笔。 |

---

## 5. Deriving Key Insights through the Dashboard / 受众如何通过仪表盘获取关键洞察

The dashboard is structured as a **guided analytical journey** — each section actively leads the audience to a specific conclusion, rather than presenting passive data:

此仪表盘以**引导式分析旅程**的形式构建，每一分区都主动将受众引向特定结论，而非被动呈现数据：

---

**Section 01 — Establishing "What Does Normal Look Like?" (建立"正常是什么样的？"的基准感知)**

An administrator opens the dashboard and immediately sees the five KPI cards: 6,607 students; mean score = 67.24; average attendance = 80.1%. The three histograms then show that exam scores are **tightly compressed** around the mean (std = 3.89, IQR = 4 pts). This tells administrators that the ceiling is reachable and that even small improvements in student inputs can shift a student across the critical class-average threshold — making marginal interventions worthwhile.

管理者打开仪表盘，立即接收五项KPI指标：6,607人；均分=67.24；平均出勤率=80.1%。三组直方图揭示成绩在均值附近被高度压缩（std=3.89，IQR=4分），告知管理者：成绩上限触手可及，即使是微小的学生投入改善，也可能将其推过"是否达到班级均值"的临界线——边际干预物有所值。

> **Insight derived (获得洞察):** The performance distribution is not bimodal (no irreversible failure cluster); targeted effort can move most students upward. / 成绩分布并非双峰（无不可逆的失败聚落），定向努力可以将大多数学生向上推移。

---

**Section 02 — Identifying "Where to Invest Intervention Resources?" (识别"将干预资源投向何处？")**

Reading the three line charts together, administrators directly compare the ROI of different behaviours: Study Hours deliver Δ+7.59 pts from the lowest to highest bin; Tutoring plateaus sharply after 6 sessions; Sleep shows near-zero slope. The 4D Bubble Chart then reveals the **compounding advantage**: students in the top-right quadrant (high attendance + large bubbles = high study hours) overwhelmingly appear in green (High Motivation), monopolising all scores above 85.

对比三组折线图，管理者可直接比较不同行为的投资回报率：学习时长从最低到最高区间带来 +7.59分增益；辅导次数在6次后急剧平坦；睡眠时长近乎零斜率。4D气泡图进一步揭示**复合优势**：右上象限（高出勤+大气泡=高学习时长）的学生大量呈现为绿色（高动力），垄断了85分以上的全部成绩。

> **Insight derived (获得洞察):** Prioritise attendance improvement and deep study hours before allocating more tutoring slots. The synergy of attendance × study hours creates a non-linear advantage. / 在分配更多辅导名额之前，优先提升出勤率与学习深度。出勤率与学习时长的协同效应创造了非线性优势。

---

**Section 03 — Answering "Who Is Being Left Behind, and Why?" (回答"谁正在被遗忘，以及为什么？")**

The four demographic charts answer a different management question: are our resources reaching students who need them most? The Donut charts show High-income students are only 19.2% of the cohort, and students with Learning Disabilities only 10.5%. The Parallel Categories diagram then shows how students starting at Low Family Income are **systematically more likely** to flow through Low Resource Access and Low Motivation, ending up in the lower score bin — visualising a structural pipeline fracture that aggregate averages would mask.

第三区回答了另一个管理命题：我们的资源是否真正惠及了最需要的学生？环形图显示高收入家庭学生仅占19.2%，有学习障碍的学生仅占10.5%。平行类别图揭示低收入家庭学生**系统性地更可能**经历低资源获取与低动力的分流，最终落入低分组——将总体均值会掩盖的结构性管道断裂以可见方式呈现。

> **Insight derived (获得洞察):** Equity programmes should target the resource access–motivation pipeline specifically, not income alone. Internet access (~92% universal) is no longer the priority gap. / 公平方案应具体针对资源获取–动力管道，而非仅关注收入。网络接入（约92%普及）已不再是优先差距。

---

### Consolidated Insight Table / 洞察汇总表

| # | Key Insight (English) | 核心洞察（中文）|
|---|---|---|
| 1 | **Attendance is the #1 lever** — dominant predictor; steep positive correlation from 60% to 100% | **出勤率是首要杠杆** — 核心预测变量，从60%至100%呈现陡峭正相关 |
| 2 | **Prior scores are a weak predictor** — current behaviours override historical baselines | **历史成绩是弱预测器** — 当期行为可覆盖历史基线 |
| 3 | **Study Hours: compounding ROI** — Δ+7.59 pts; monopolises top scores when combined with high attendance | **学习时长：复合ROI** — Δ+7.59分；与高出勤叠加后垄断顶层成绩 |
| 4 | **Tutoring: returns plateau after 6 sessions** — scheduling beyond 6 yields no measurable gain | **辅导：6次后收益趋平** — 超过6次后无可测量增益 |
| 5 | **Structural inequality channels paths, not outcomes** — low-income pipeline fractures at motivation level; median gap only ±2 pts | **结构性不平等导引路径而非锁定结果** — 低收入管道在动力层级断裂，中位数分差仅±2分 |
| 6 | **Internet access gap is closed** — ~92% across both school types; equity focus must shift | **网络接入差距已弥合** — 两种学校类型均约92%，公平重点需转移 |


---

## 6. Technical Stack & Execution Instructions / 技术栈与部署说明

| Component (组件) | Architecture (技术架构实现) |
|---|---|
| Dashboard Framework (基础框架) | Streamlit (executed via `streamlit run app.py`) |
| Visualisation Library (可视化图库) | Plotly Express + Graph Objects (interactive rendering 高度交互渲染) |
| UI/UX Constraints (界面强约束) | CSS-forced narrow sidebar (180px); no emojis; high-density charting (CSS强定极窄侧边、全剔除Emoji、高密度排版) |
| Shared Utilities (核心挂载类) | `utils/chart_helpers.py` (caching, layout polishing, color constants) |
| Dataset Dependency (依赖原表) | `data/StudentPerformanceFactors_cleaned.csv` (n=6,607) |
