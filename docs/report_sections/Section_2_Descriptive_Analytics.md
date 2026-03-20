# 2.0 Descriptive Analytics

## 2.1 Descriptive Statistics of Numerical Variables

**Table 2: Descriptive Statistics of Numerical Variables**

| Variable | Mean | Median | Mode | Std Dev | Min | Q1 | Q3 | Max | Skewness |
|----------|-----:|-------:|-----:|--------:|----:|---:|---:|----:|---------:|
| Hours_Studied | 19.98 | 20.00 | 20 | 5.99 | 1 | 16.00 | 24.00 | 44 | 0.01 |
| Attendance | 79.98 | 80.00 | 67 | 11.55 | 60 | 70.00 | 90.00 | 100 | 0.01 |
| Sleep_Hours | 7.03 | 7.00 | 7 | 1.47 | 4 | 6.00 | 8.00 | 10 | -0.02 |
| Previous_Scores | 75.07 | 75.00 | 66 | 14.40 | 50 | 63.00 | 88.00 | 100 | 0.00 |
| Tutoring_Sessions | 1.49 | 1.00 | 1 | 1.23 | 0 | 1.00 | 2.00 | 8 | 0.82 |
| Physical_Activity | 2.97 | 3.00 | 3 | 1.03 | 0 | 2.00 | 4.00 | 6 | -0.03 |
| Exam_Score | 67.24 | 67.00 | 68 | 3.89 | 55 | 65.00 | 69.00 | 100 | 1.64 |

## 2.2 Behavioural Patterns & Academic Discrepancies

### 2.2.1 Study Investment Versus Performance Return

The mean, median, and mode of weekly study hours converge at approximately 20 hours (skewness = 0.01), forming a near-perfect normal distribution with an IQR of 8 hours (Q1 = 16, Q3 = 24). This uniformity indicates that the vast majority of students invest a comparable amount of time in studying.

However, this consistent effort does not translate into proportionally strong outcomes. The mean exam score is only 67.24, and the IQR is remarkably narrow at just 4 points (Q1 = 65, Q3 = 69), meaning that the middle 50% of students are compressed into a 4-point band despite wide variation in study hours (range: 1--44 hours). Furthermore, the sharp contrast between the symmetric study-hours distribution (skewness = 0.01) and the right-skewed exam score distribution (skewness = 1.64) suggests that the source of performance divergence lies not in the quantity of study time but in its quality -- factors such as learning efficiency, cognitive strategy, and access to external support.

### 2.2.2 Attendance: A Deceptive Mean

The mean attendance is 79.98%, yet the mode is only 67% -- a 13-percentage-point gap. The standard deviation of 11.55 is nearly double that of study hours (5.99), and the IQR spans 20 points (Q1 = 70, Q3 = 90). This pattern reveals a dual-peaked cohort: a substantial "low-attendance subgroup" concentrated near 67% pulls the mode downward, while consistently engaged students elevate the mean.

Relying solely on the average attendance rate of 80% would obscure this underlying stratification. The modal group -- attending roughly two-thirds of classes -- is likely to overlap with the lowest-performing students if attendance is positively correlated with exam scores (a relationship confirmed in Section 4.1).

### 2.2.3 Sleep Duration: Uniform but Not Predictive

Sleep hours display an exceptionally tight distribution (mean = 7.03, mode = 7.00, skewness = -0.02, IQR = 2 hours). Nearly all students cluster around 7 hours per night, with no evidence of a subgroup sacrificing sleep for study or oversleeping.

Given this uniformity and the highly skewed exam score distribution, sleep duration cannot be a primary driver of performance differences. High-achieving students are not sleeping less; low-performing students are not sleeping more. Sleep is best understood as a baseline health indicator rather than an academic lever.

### 2.2.4 Tutoring: Diminishing Returns

The mean tutoring frequency is 1.49 sessions per week, but both the median and mode equal 1.00, with a right skewness of 0.82. This confirms that the majority of students attend at most one session, while a small subset attends up to 8 sessions per week, pulling the mean above the mode in a classic long-tail pattern.

If tutoring were uniformly effective, one would expect the exam score distribution to shift leftward (lower skewness) or become more concentrated. The persistence of high score skewness (1.64) alongside moderate tutoring skewness (0.82) suggests that additional tutoring sessions yield diminishing returns, or that their effectiveness is conditional on other factors such as motivation or prior preparation.

### 2.2.5 Previous Scores: The Widest Spread

Previous academic scores exhibit the widest IQR of any numerical variable: 25 points (Q1 = 63, Q3 = 88), spanning the full 50--100 range. The mode (66) falls 9 points below the mean (75.07), indicating a sizeable low-performing subgroup that mirrors the pattern observed in attendance.

Comparing past and present performance reveals a notable compression: the previous-score IQR of 25 points collapses to just 4 points in the current exam. This convergence implies either increasing assessment difficulty that compresses the score range, or a genuine regression-to-the-mean effect where historically divergent students produce similar current outcomes.

### 2.2.6 Physical Activity: Symmetric & Narrow

Physical activity averages 2.97 sessions per week (mode = 3, skewness = -0.03), with an IQR of 2 sessions (Q1 = 2, Q3 = 4). The distribution is nearly perfectly symmetric across a discrete 0--6 range. Like sleep duration, this variable shows too little variation across the cohort to serve as a meaningful differentiator of academic performance.

## 2.3 Core Conclusions of Descriptive Analysis

Three principal findings emerge from the statistical summary:

1. **Efficiency over volume.** Study hours are highly uniform (IQR = 8) yet exam scores diverge sharply (skewness = 1.64). The decisive performance differentiators are not captured by time-input variables alone; they likely reside in learning quality, motivation, and environmental support. Interventions should target *how* students study, not simply *how long*.

2. **Attendance stratification demands attention.** The 13-point gap between mean and modal attendance (80% vs. 67%) signals a hidden at-risk subgroup. Academic affairs should implement attendance monitoring with early-warning thresholds rather than relying on cohort-level averages.

3. **Historical performance is a weak anchor.** The dramatic IQR compression from previous scores (25 points) to current exam scores (4 points) means that past grades are poor predictors of present outcomes. Student support programmes should not rely exclusively on prior academic records for risk identification; current behavioural signals (attendance, study patterns) carry greater diagnostic value.
