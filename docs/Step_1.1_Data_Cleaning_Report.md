# Phase 1: Step 1.1 - Data Loading & Cleaning Report (数据加载与清洗报告)

## 1. Data Shape & Quality Inspection (数据形状与质量检查)

**English:**
The raw dataset `StudentPerformanceFactors.csv` was successfully loaded. The initial dataset contains **6,607 rows** and **20 columns**.
Upon inspection, three categorical columns contained missing values: `Teacher_Quality`, `Parental_Education_Level`, and `Distance_from_Home`. Additionally, one record in the target variable `Exam_Score` contained an invalid entry exceeding the maximum possible score of 100 (value = 101).

**中文:**
成功加载原始数据集 `StudentPerformanceFactors.csv`。初始数据集包含 **6,607 行** 和 **20 列**。
经检查，三个类别型字段存在缺失值：教师质量 (`Teacher_Quality`)、父母教育水平 (`Parental_Education_Level`) 及通勤距离 (`Distance_from_Home`)。此外，目标变量 `Exam_Score` 中有 1 条记录的数值（101）超出了满分上限（100），属于无效数据。

---

## 2. Data Cleaning Strategy (数据处理方法与目的)

**English:**
The following cleaning steps were applied to ensure the dataset is accurate, consistent, and ready for analysis:

1. **Invalid Value Correction:** The single record where `Exam_Score` exceeded 100 was corrected to exactly 100, preserving the observation while restoring logical validity. A safeguard was also applied to any numerical column to ensure no negative values exist, as negative scores are not meaningful in this educational context.

2. **Missing Value Handling:** The three columns with missing values (`Teacher_Quality`, `Parental_Education_Level`, `Distance_from_Home`) were handled by filling the gaps with a dedicated placeholder category: `"Unknown"`. This approach was chosen because:
   - The missing counts are small (67–90 records each, under 1.4% of total rows), so removing these rows would cause unnecessary loss of valid information.
   - Replacing with `"Unknown"` preserves the rows in the dataset and allows these records to remain part of the analysis without distorting other variables.
   - The `"Unknown"` category is treated as a separate, legitimate group in subsequent encoding and modelling steps, which is more informative than discarding the data entirely.

The cleaned dataset retains the original dimensions of **(6,607 rows × 20 columns)** — no rows were deleted.

**中文:**
以下清洗步骤用于确保数据的准确性、一致性，并为后续分析做好准备：

1. **无效值修正：** 将唯一一条超过满分上限的 `Exam_Score`（值为 101）修正回 100，使该条记录恢复逻辑有效性，同时得以保留于数据集中。此外，对数值类字段添加了非负数保护，因为本数据集中不存在负分的实际含义。

2. **缺失值处理：** 对含有缺失值的三个字段（`Teacher_Quality`、`Parental_Education_Level`、`Distance_from_Home`），统一以占位类别 `"Unknown"` 进行填补。选用此方案的理由如下：
   - 各字段缺失数量较少（每列 67–90 条，均不超过总行数的 1.4%），若直接删除行会造成不必要的有效信息损失。
   - 以 `"Unknown"` 填补可完整保留这些记录，使其继续参与分析，避免数据损耗。
   - 在后续的编码与建模步骤中，`"Unknown"` 作为独立的类别分组对待，比直接丢弃更具信息价值。

清洗后的数据集完整保留了原始规模 **(6,607 行 × 20 列)**，未删除任何行。

---

*Table 1: Summary of Missing Values Handled (已处理的缺失值总结)*

| Column (列名) | Missing Count (缺失数量) | % of Total (占比) | Handling Strategy (处理策略) |
| :--- | :--- | :--- | :--- |
| Teacher_Quality | 78 | 1.18% | Replaced with "Unknown" |
| Parental_Education_Level | 90 | 1.36% | Replaced with "Unknown" |
| Distance_from_Home | 67 | 1.01% | Replaced with "Unknown" |
| Exam_Score > 100 | 1 | 0.02% | Clipped to 100 (value correction) |
