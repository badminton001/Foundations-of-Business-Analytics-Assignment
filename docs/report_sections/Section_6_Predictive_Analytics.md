# 6.0 Predictive Analytics

## 6.1 Potential Predictions from the Dataset

The student performance dataset contains 19 input features spanning behavioural habits (study hours, attendance, tutoring), environmental factors (teacher quality, parental involvement), and socioeconomic background (family income, access to resources). These features enable two high-value predictions:

**Prediction 1 — Exam Score Forecasting (Continuous)**

Given a student's profile across all 19 features, the model predicts their expected exam score. This enables academic planners to estimate cohort-level grade distributions before exams take place, identify students whose predicted scores fall below acceptable thresholds, and simulate the impact of hypothetical interventions (e.g., "If this student's attendance increases from 70% to 85%, how much would their predicted score improve?").

**Prediction 2 — At-Risk Student Identification (Binary)**

The model classifies each student as "Above Average" or "Below Average" relative to the cohort mean (67.24). This binary framing directly supports an early-warning system: students flagged as likely below-average can be prioritised for intervention before their exam results materialise.

---

## 6.2 Suitable Predictive Techniques

### Regression for Score Forecasting

Since the target variable (Exam Score) is continuous, **regression** is the appropriate technique. Three regression approaches were evaluated:

**Table 6: Regression Model Candidates**

| Model | Why It Was Considered |
|-------|----------------------|
| Ridge Regression | A linear approach that is simple, interpretable, and well-suited when the relationships between inputs and outcomes are approximately linear — as confirmed by the correlation analysis in Section 4.6 |
| Random Forest | A non-linear approach that can capture complex interactions between features without requiring them to be specified in advance |
| Gradient Boosting | An advanced approach that builds models sequentially, with each new model correcting the errors of the previous one — often the most accurate method for structured data |

**Result:** Ridge Regression achieved the best performance (R² = 0.656, RMSE = 2.44), meaning the model explains 65.6% of the variance in exam scores with an average prediction error of approximately 2.4 points. The fact that the simplest linear model outperformed the more complex alternatives confirms the finding from Section 4.6: the dominant predictors (Attendance, Hours Studied) have straightforward linear relationships with exam scores.

### Classification for At-Risk Identification

Since the target is a binary category (Above/Below Average), **classification** is the appropriate technique. Three classifiers were evaluated:

**Table 7: Classification Model Candidates**

| Model | Why It Was Considered |
|-------|----------------------|
| Logistic Regression | A linear classifier that produces probability scores (e.g., "this student has a 78% probability of scoring below average") — ideal for risk ranking |
| Random Forest Classifier | A non-linear classifier that handles complex feature interactions |
| Gradient Boosting Classifier | An advanced sequential classifier known for high accuracy |

**Result:** Logistic Regression achieved near-perfect discrimination (F1 = 0.980, AUC = 0.995), correctly identifying above- and below-average students with 98% accuracy. Again, the linear model's dominance reinforces the linear nature of the underlying relationships.

---

## 6.3 Model Evaluation

### Regression Evaluation

[Insert Figure: Reg_ActualVsPredicted.png]

**Figure 22:** Actual vs. Predicted Exam Score. The dashed red line represents a perfect prediction; the shaded band shows ±1 point tolerance.

The predicted scores cluster tightly along the diagonal for the majority of students (scores 65--70), confirming accurate predictions in the core range. The model underestimates extreme high-achievers (scores > 80), whose performance is likely driven by factors not captured in the dataset.

[Insert Figure: Reg_ResidualDistribution.png]

**Figure 23:** Distribution of prediction errors (Actual − Predicted).

The errors are centred near zero and approximately normally distributed, confirming that the model does not systematically over- or under-predict. The slight right tail reflects the small number of high-achieving outliers.

[Insert Figure: Reg_FeatureImportance.png]

**Figure 24:** Feature importance ranking — which factors most strongly drive the predicted score.

The feature ranking confirms the insights from the exploratory analysis:
- **Attendance** is the most influential predictor, consistent with its dominant correlation (r = 0.581).
- **Hours Studied** ranks second, reinforcing its role as the primary behavioural lever.
- **Previous Scores** contributes modestly, confirming the finding from Section 4.3 that historical grades are weak predictors of current performance.
- Environmental and socioeconomic variables (Parental Involvement, Access to Resources, Family Income) contribute at a mid-tier level — individually small but collectively significant.
- Sleep Hours, Physical Activity, and Gender have minimal predictive value.

### Classification Evaluation

[Insert Figure: Clf_ConfusionMatrix.png]

**Figure 25:** Confusion matrix showing the proportion of correct and incorrect predictions for each class.

Both classes are predicted with high accuracy. The low and symmetric error rates confirm that the model does not favour one group over the other — it is equally reliable at identifying above-average and below-average students.

[Insert Figure: Clf_ROCCurve.png]

**Figure 26:** ROC curve (AUC = 0.995). The dashed diagonal represents a model making random guesses.

The curve hugs the top-left corner, indicating that the model achieves near-perfect separation between the two groups. An AUC of 0.995 means the model correctly ranks students 99.5% of the time.

[Insert Figure: Clf_PRCurve.png]

**Figure 27:** Precision-Recall curve showing the trade-off between catching at-risk students and avoiding false alarms.

The curve maintains high precision across nearly the entire recall range. For the early-warning application, this means the model can flag the vast majority of at-risk students without generating excessive false alarms that would overwhelm intervention resources.

[Insert Figure: Clf_FeatureImportance.png]

**Figure 28:** Feature importance ranking for the classification model.

The classification feature ranking closely mirrors the regression results: **Attendance and Hours Studied dominate both tasks**. This convergence across two independent modelling approaches strengthens confidence in the actionability of these factors.

---

## 6.4 How These Predictions Benefit the Institution

The two predictive models translate directly into three operational benefits for the academic affairs office:

### Benefit 1: Proactive Early-Warning System

The classification model (98% accuracy) can be deployed as an automated risk-flagging tool. By inputting a student's current behavioural and demographic data at mid-semester, the system generates a risk probability for each student. Those flagged as likely below-average can be prioritised for targeted intervention — counselling sessions, attendance follow-ups, or tutoring referrals — *before* their exam results confirm the problem.

### Benefit 2: Evidence-Based Resource Allocation

The feature importance rankings from both models provide a clear investment hierarchy. The institution now has quantitative evidence that:
- Attendance programmes will yield the highest return per unit of investment.
- Study-skill workshops (targeting quality, not quantity) are the second-highest priority.
- Resource equalisation for low-income students addresses the largest structural equity gap.

This evidence base allows budget decisions to be justified by data rather than intuition.

### Benefit 3: Intervention Impact Simulation

The regression model can be used to simulate "what-if" scenarios. For example:
- *"If we improve this student's attendance from 70% to 85%, how much would their predicted score increase?"* — The model estimates the expected score gain, allowing the institution to quantify the return on specific interventions before committing resources.
- *"Which combination of factors produces the highest predicted improvement for low-income students?"* — The model can rank intervention strategies by their predicted impact on the most disadvantaged subgroups.

These capabilities transform the academic affairs office from a reactive unit (responding to poor results after the fact) into a proactive one (identifying and addressing risk factors before outcomes are determined).
