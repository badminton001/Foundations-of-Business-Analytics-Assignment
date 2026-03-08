# Phase 2: Step 2.1 - Statistical Summary Report (连续变量统计量表与分析报告)

## 1. Descriptive Statistics of Numerical Variables (数值变量描述性统计量)

**Caption:**
Table 1: Descriptive Statistics of Numerical Variables

| Variable (变量名) | Mean (均值) | Median (中位数) | Mode (众数) | Std_Dev (标准差) | Skewness (偏度) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| Hours_Studied | 19.98 | 20.00 | 20.00 | 5.99 | 0.01 |
| Attendance | 79.98 | 80.00 | 67.00 | 11.55 | 0.01 |
| Sleep_Hours | 7.03 | 7.00 | 7.00 | 1.47 | -0.02 |
| Previous_Scores | 75.07 | 75.00 | 66.00 | 14.40 | 0.00 |
| Tutoring_Sessions | 1.49 | 1.00 | 1.00 | 1.23 | 0.82 |
| Physical_Activity | 2.97 | 3.00 | 3.00 | 1.03 | -0.03 |
| Exam_Score | 67.24 | 67.00 | 68.00 | 3.89 | 1.64 |

*(The complete analytical output has been successfully exported to `/data/Numerical_Statistical_Summary.csv`)*

---

## 2. Bilingual Analytical Insights (双语分析论述)

**English Insight:**
How do these statistics describe the dataset? 
The descriptive statistics reveal several core behavioral patterns in the student cohort:
1. **Near-Symmetric Distributions:** Key academic inputs like `Hours_Studied` and `Sleep_Hours` demonstrate near-perfect symmetry (Skewness close to 0), with mean and median very closely aligned. This indicates that most students share similar behavioral patterns, with minimal variance in daily academic routines.
2. **Right-Skewed Behavior:** Extra `Tutoring_Sessions` is notably right-skewed (0.82) with a mode of 1.0 and mean of 1.49, indicating most students take minimal tutoring, while a small tail takes significantly more.
3. **Target Variable Characteristics:** The target variable `Exam_Score` has a mean of 67.24 and median of 67.0, maintaining a tight standard deviation of 3.89. However, it shows a positive skewness of 1.64, suggesting a presence of high-performing outliers stretching the upper bounds. This insight is critical for model baseline assumptions, as most students score clustered tightly around 67.

**中文分析:**
这些统计量如何精准描绘当前的数据集分布全貌？
通过描述性统计量，我们可以深刻洞察该学生群体的核心行为模式：
1. **近似对称分布特征：** `Hours_Studied` (每周学习时长) 与 `Sleep_Hours` (睡眠时间) 等关键学业投入变量展现出近似对称分布特征 (偏度接近 0)，均值与中位数高度接近。这表明绝大多数学生的日常作息高度相近，行为方差极小。
2. **右偏分布特征：** `Tutoring_Sessions` (辅导次数) 呈现显著的右偏态分布 (偏度 0.82)，众数仅为 1 次，而均值被少数高频参加辅导的学生拉高至 1.49 次。这意味着绝大多数群体不依赖密集辅导，存在“辅导依赖长尾”。
3. **目标变量诊断：** 核心预测变量 `Exam_Score` (考试成绩) 均值为 67.24，中位数 67.00，标准差极低 (仅为 3.89)。值得注意的是，其呈现出 1.64 的正偏度，暗示虽然成绩主要紧密聚集在 67 分附近，但存在少数斩获极高分的拔尖学生。这对于我们后期设定回归基线与不平衡检测具有极佳的指导意义。
