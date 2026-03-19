# Phase 2: Step 2.1 - Statistical Summary Report (连续变量统计量表与分析报告)

## 1. Descriptive Statistics of Numerical Variables (数值变量描述性统计量)

**Caption:**
Table 1: Descriptive Statistics of Numerical Variables

| Variable (变量名) | Mean (均值) | Median (中位数) | Mode (众数) | Std_Dev (标准差) | Min (最小值) | Q1 (25th %) | Q3 (75th %) | Max (最大值) | Skewness (偏度) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| Hours_Studied | 19.98 | 20.00 | 20.00 | 5.99 | 1.00 | 16.00 | 24.00 | 44.00 | 0.01 |
| Attendance | 79.98 | 80.00 | 67.00 | 11.55 | 60.00 | 70.00 | 90.00 | 100.00 | 0.01 |
| Sleep_Hours | 7.03 | 7.00 | 7.00 | 1.47 | 4.00 | 6.00 | 8.00 | 10.00 | -0.02 |
| Previous_Scores | 75.07 | 75.00 | 66.00 | 14.40 | 50.00 | 63.00 | 88.00 | 100.00 | 0.00 |
| Tutoring_Sessions | 1.49 | 1.00 | 1.00 | 1.23 | 0.00 | 1.00 | 2.00 | 8.00 | 0.82 |
| Physical_Activity | 2.97 | 3.00 | 3.00 | 1.03 | 0.00 | 2.00 | 4.00 | 6.00 | -0.03 |
| Exam_Score | 67.24 | 67.00 | 68.00 | 3.89 | 55.00 | 65.00 | 69.00 | 100.00 | 1.64 |

*(The complete analytical output has been successfully exported to `/data/Numerical_Statistical_Summary.csv`)*

---

## 2. Bilingual Analytical Insights (双语分析论述)

**English Insight:**
How do these statistics describe the dataset?
The descriptive statistics reveal several core behavioral patterns in the student cohort:
1. **Near-Symmetric Distributions:** Key academic inputs like `Hours_Studied` and `Sleep_Hours` demonstrate near-perfect symmetry (Skewness close to 0), with mean and median very closely aligned. The IQR for `Hours_Studied` spans 16–24 hours per week (Q1=16, Q3=24), confirming that the middle 50% of students study within an 8-hour range — a compact behavioral cluster. `Sleep_Hours` shows a similarly tight IQR of 6–8 hours, with no student sleeping fewer than 4 or more than 10 hours.
2. **Right-Skewed Behavior:** `Tutoring_Sessions` is notably right-skewed (0.82) with Q1=Q3=1–2 sessions, while the maximum reaches 8. This confirms that the vast majority of students receive very little tutoring, with a small high-engagement tail pulling the mean above the mode.
3. **Target Variable Characteristics:** `Exam_Score` has a mean of 67.24 and a very tight IQR of only 4 points (Q1=65, Q3=69), meaning half of all students score within a 4-point band. Despite the narrow IQR, the maximum reaches 100 and skewness is 1.64, confirming a thin but extreme high-performing right tail. The minimum of 55 indicates no student scored catastrophically below 50%, suggesting the cohort has a solid performance floor.
4. **Wide Spread in Previous Scores:** `Previous_Scores` shows the widest IQR (63–88, range=25) of all numerical variables, spanning the full 50–100 range. This contrast with the narrow IQR of `Exam_Score` (IQR=4) suggests that prior academic history is a poor predictor of current exam performance — students with very different past scores converge on similar final outcomes.

**中文分析:**
这些统计量如何精准描绘当前的数据集分布全貌？
通过描述性统计量，我们可以深刻洞察该学生群体的核心行为模式：
1. **近似对称分布特征：** `Hours_Studied`（每周学习时长）与 `Sleep_Hours`（睡眠时间）等关键学业投入变量展现出近似对称分布特征（偏度接近 0），均值与中位数高度接近。`Hours_Studied` 的四分位距（IQR）为 16–24 小时/周（Q1=16，Q3=24），说明中间 50% 的学生学习时长集中在 8 小时的紧凑区间内。`Sleep_Hours` 的 IQR 同样紧凑（6–8 小时），无学生睡眠少于 4 小时或超过 10 小时。
2. **右偏分布特征：** `Tutoring_Sessions`（辅导次数）呈显著右偏（偏度 0.82），Q1=1、Q3=2，最大值达 8 次。这证实绝大多数学生几乎不参加辅导，少数高频参加辅导的学生形成长尾，将均值拉高至超过众数。
3. **目标变量诊断：** `Exam_Score`（期末成绩）均值 67.24，IQR 极为紧凑（仅 4 分，Q1=65，Q3=69），一半学生的成绩集中在 4 分带宽内。尽管 IQR 极窄，最大值达 100 分，偏度 1.64，证实存在极端高分长尾。最低分 55 分说明没有学生得分低于 50%，该群体整体具备扎实的成绩下限。
4. **历史成绩的宽幅分布：** `Previous_Scores`（历史成绩）的 IQR 高达 25 分（Q1=63，Q3=88），是所有数值变量中最宽的，且覆盖了 50–100 的完整范围。与 `Exam_Score` 的极窄 IQR（4 分）形成鲜明对比，说明学生的历史成绩对当前期末成绩的预测力很弱——历史成绩差异悬殊的学生最终趋向于相似的期末结果。
