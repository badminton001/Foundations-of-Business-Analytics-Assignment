# Phase 1: Step 1.1 - Data Loading & Cleaning Report (数据加载与清洗报告)

## 1. Data Shape & Quality Inspection (数据形状与质量检查)

**English:**
The raw dataset `StudentPerformanceFactors.csv` was successfully loaded. The initial dataset contains **6,607 rows** and **20 columns**. 
Upon inspection, three categorical columns contained missing values: `Teacher_Quality`, `Parental_Education_Level`, and `Distance_from_Home`. Additionally, an anomaly was detected in the target variable `Exam_Score`, where 1 record exceeded the logical maximum score of 100 (value = 101). 

**中文:**
成功加载原始数据集 `StudentPerformanceFactors.csv`。初始数据集包含 **6,607 行** 和 **20 列**。
经检查，三个类别型特征存在缺失值：老师质量 (`Teacher_Quality`)、父母教育水平 (`Parental_Education_Level`) 和 通勤距离 (`Distance_from_Home`)。此外，在目标变量 `Exam_Score` 中检测到一处异常值，有 1 条记录的成绩超出了逻辑满分 100 分 (分数为 101)。

---

## 2. Rigorous Preprocessing Strategy (严谨的预处理策略)

**English:**
To strictly adhere to data science first principles and absolutely prevent **Data Leakage** prior to the Train-Test Split in Phase 4, the following scientific strategies were applied:
1. **Anomaly Handling:** The single `Exam_Score` > 100 was clipped to exactly 100 to maintain domain validity. Any potential negative values in numerical columns were also safeguarded by clipping them to 0.
2. **Missing Value Imputation without Leakage:** Rather than computing the mathematical mode across the entire dataset (which would cause target/future data leakage), missing values in the categorical columns were filled with a constant placeholder class: `"Unknown"`. This completely neutralizes missingness seamlessly and securely.

The cleaned dataset has been successfully exported to `/data/StudentPerformanceFactors_cleaned.csv` while perfectly retaining the original dimensions of **(6607, 20)**.

**中文:**
为了恪守数据科学第一性原理，并绝对防止在 Phase 4 进行训练集-测试集划分前发生**数据泄露 (Data Leakage)**，我们采取了以下科学严谨的处理策略：
1. **异常值处理：** 出于业务逻辑考量，将唯一一条大于 100 的 `Exam_Score` 直接截断 (clip) 回最高分 100。此外，在数值型列中添加了防止出现负数的逻辑截断机制。
2. **防泄露的缺失值填补：** 未在现阶段使用全体数据集计算众数 (Mode) 填补（此举会引发使用未来的测试集数据来参与填补，导致数据泄露）。而是为缺失的类别型特征统一创建一个新的占位类：`"Unknown"`。此方法完美化解了缺失样本问题，同时绝对安全。

清洗后的最终数据已成功导出至 `/data/StudentPerformanceFactors_cleaned.csv`，且完美保留了初始的 **(6607, 20)** 数据维度。

---

*Table 1: Summary of Missing Values Handled (已处理的缺失值总结)*

| Column (列名) | Missing Count (缺失数量) | Handling Strategy (处理策略) |
| :--- | :--- | :--- |
| Teacher_Quality | 78 | Replaced with "Unknown" |
| Parental_Education_Level | 90 | Replaced with "Unknown" |
| Distance_from_Home | 67 | Replaced with "Unknown" |
