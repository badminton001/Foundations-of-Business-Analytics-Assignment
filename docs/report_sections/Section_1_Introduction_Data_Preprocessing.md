# 1.0 Introduction & Data Preprocessing

## 1.1 Project Objective & Scope

This report analyses 6,607 student records to identify the behavioural, environmental, and socioeconomic factors that most strongly influence examination performance. By combining descriptive statistics, visual analytics, an interactive dashboard, and predictive modelling, the analysis aims to equip the academic affairs office with evidence-based insights for designing targeted interventions, optimising resource allocation, and establishing an early-warning system for at-risk students.

**Target variable:** `Exam_Score` (continuous, range 55--100).

**Data dictionary (20 columns):**

| # | Variable | Type | Description |
|---|----------|------|-------------|
| 1 | Hours_Studied | Numerical | Weekly study hours |
| 2 | Attendance | Numerical | Class attendance percentage |
| 3 | Parental_Involvement | Categorical | Level of parental academic support (Low / Medium / High) |
| 4 | Access_to_Resources | Categorical | Learning resource availability (Low / Medium / High) |
| 5 | Extracurricular_Activities | Binary | Participation in extracurricular activities (Yes / No) |
| 6 | Sleep_Hours | Numerical | Average nightly sleep duration (hours) |
| 7 | Previous_Scores | Numerical | Past academic performance (score) |
| 8 | Motivation_Level | Categorical | Student motivation level (Low / Medium / High) |
| 9 | Internet_Access | Binary | Internet availability status (Yes / No) |
| 10 | Tutoring_Sessions | Numerical | Weekly extra tutoring frequency |
| 11 | Family_Income | Categorical | Family income level (Low / Medium / High) |
| 12 | Teacher_Quality | Categorical | Teacher quality level (Low / Medium / High) |
| 13 | School_Type | Categorical | School type (Public / Private) |
| 14 | Peer_Influence | Categorical | Peer influence direction (Negative / Neutral / Positive) |
| 15 | Physical_Activity | Numerical | Weekly physical activity sessions |
| 16 | Learning_Disabilities | Binary | Whether the student has a learning disability (Yes / No) |
| 17 | Parental_Education_Level | Categorical | Parent education level (High School / College / Postgraduate) |
| 18 | Distance_from_Home | Categorical | School-to-home distance (Near / Moderate / Far) |
| 19 | Gender | Categorical | Student gender (Male / Female) |
| 20 | Exam_Score | Numerical | **Target** -- Examination score (0--100) |

## 1.2 Data Loading & Quality Inspection

The raw dataset comprises **6,607 rows and 20 columns**. An initial quality audit identified two categories of data-quality issues:

- **Missing values** in three categorical columns: `Teacher_Quality` (78 records, 1.18%), `Parental_Education_Level` (90 records, 1.36%), and `Distance_from_Home` (67 records, 1.01%).
- **Invalid value**: one record contained an `Exam_Score` of 101, exceeding the maximum possible score of 100.

No negative values, duplicate rows, or structural inconsistencies were detected.

## 1.3 Data Cleaning Strategy

The following cleansing procedures were applied to ensure dataset accuracy, consistency, and analytical readiness:

**a. Invalid Value Correction**

The single record with `Exam_Score > 100` was clipped to exactly 100. This retains the observation while restoring logical validity. A protective check was also applied to all numerical columns to confirm the absence of negative values, which carry no meaning in this educational context.

**b. Missing Value Handling**

Missing entries in `Teacher_Quality`, `Parental_Education_Level`, and `Distance_from_Home` were replaced with a dedicated placeholder category, `"Unknown"`. This strategy was chosen for three reasons:

1. The missing counts are small (67--90 records each, under 1.4% of total rows); row deletion would cause unnecessary information loss.
2. The `"Unknown"` label preserves all 6,607 rows in the analysis pipeline without distorting distributions of other variables.
3. In subsequent modelling, `"Unknown"` is treated as an independent category during encoding, which is more information-preserving than discarding the affected records entirely.

**c. Result**

The cleaned dataset retains its original dimensions of **6,607 rows x 20 columns**; zero rows were removed.

**Table 1: Summary of Data Quality Issues and Remediation**

| Column | Issue | Count | % of Total | Handling Strategy |
|--------|-------|------:|----------:|-------------------|
| Teacher_Quality | Missing values | 78 | 1.18% | Replaced with "Unknown" |
| Parental_Education_Level | Missing values | 90 | 1.36% | Replaced with "Unknown" |
| Distance_from_Home | Missing values | 67 | 1.01% | Replaced with "Unknown" |
| Exam_Score | Value > 100 | 1 | 0.02% | Clipped to 100 |
