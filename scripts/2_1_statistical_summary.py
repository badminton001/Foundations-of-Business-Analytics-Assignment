import pandas as pd
import numpy as np
import os

base_dir = r"C:\Users\Y\Desktop\Foundations-of-Business-Analytics-Assignment"
data_path = os.path.join(base_dir, "data", "StudentPerformanceFactors_cleaned.csv")

# Load Cleaned Data
df = pd.read_csv(data_path)

# Extract Numerical Columns
num_cols = df.select_dtypes(include=[np.number]).columns.tolist()

results = []

for col in num_cols:
    mean_val = df[col].mean()
    median_val = df[col].median()
    mode_val = df[col].mode()[0] if not df[col].mode().empty else np.nan
    std_val = df[col].std()
    skewness_val = df[col].skew()
    
    results.append({
        'Variable': col,
        'Mean': round(mean_val, 2),
        'Median': round(median_val, 2),
        'Mode': round(mode_val, 2),
        'Std_Dev': round(std_val, 2),
        'Skewness': round(skewness_val, 2)
    })

stats_df = pd.DataFrame(results)

# Save to CSV
output_path = os.path.join(base_dir, "data", "Numerical_Statistical_Summary.csv")
stats_df.to_csv(output_path, index=False)

print(f"Statistical Summary computed and saved to {output_path}")
print(stats_df)
