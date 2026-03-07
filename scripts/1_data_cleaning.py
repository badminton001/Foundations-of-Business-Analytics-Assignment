import pandas as pd
import numpy as np
import os

base_dir = r"C:\Users\Y\Desktop\Foundations-of-Business-Analytics-Assignment"
raw_file = os.path.join(base_dir, "StudentPerformanceFactors.csv")
data_dir = os.path.join(base_dir, "data")
os.makedirs(data_dir, exist_ok=True)
clean_file = os.path.join(data_dir, "StudentPerformanceFactors_cleaned.csv")

print("Stage 1: Loading Data...")
df = pd.read_csv(raw_file)
initial_shape = df.shape

print("Stage 2: scientific anomaly handling...")
# Fix anomalies: Exam_Score > 100 is logically impossible for standard percentages
if 'Exam_Score' in df.columns:
    outliers = df[df['Exam_Score'] > 100]
    print(f"  Found {len(outliers)} rows with Exam_Score > 100. Clipping back to 100.")
    df.loc[df['Exam_Score'] > 100, 'Exam_Score'] = 100

# Fix anomalies: Ensure no negative values for numerical variables 
num_cols = df.select_dtypes(include=[np.number]).columns
for col in num_cols:
    negatives = df[df[col] < 0]
    if len(negatives) > 0:
        print(f"  Found {len(negatives)} rows with negative values in {col}. Clipping to 0.")
        df.loc[df[col] < 0, col] = 0

print("Stage 3: Scientific Missing Value Handling (Avoiding Data Leakage)...")
# According to data science rigor, imputing using mean/mode over the entire dataset 
# prior to train/test split causes data leakage.
# Since missing values are purely in categorical columns (Teacher_Quality, Parental_Education_Level, Distance_from_Home),
# we replace nulls with a dedicated constant 'Unknown'. This safely neutralizes the missingness without leakage.
cat_cols = df.select_dtypes(include=['object']).columns
df[cat_cols] = df[cat_cols].fillna('Unknown')

# For any numerical missing values (none found originally, but just in case), drop them to avoid target/feature leakage.
df.dropna(inplace=True)

final_shape = df.shape

print("Stage 4: Saving Cleaned Data...")
df.to_csv(clean_file, index=False)

print(f"Data Cleaning Completed Successfully.\nInitial Shape: {initial_shape}\nFinal Shape: {final_shape}")
print(f"Remaining Missing Values: {df.isnull().sum().sum()}")
