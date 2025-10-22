# Version 1: Create Folder & Clean data
## Define base
import os
import re
import pandas as pd
os.chdir(r'D:\Bi\Mini Project\Project 22_Start Date 22.10.25_Manufacturing Efficiency Analysis\Version 1')

## Create Folder to store cleaned data
os.makedirs('Cleaned_Data', exist_ok=True)

## Find & Load Raw Data
for file in os.listdir('Raw'):
    if file.endswith('.csv'):
        raw_path = os.path.join('Raw', file)
        print(f'Found Raw Data: {file}')
        break

df = pd.read_csv(raw_path)
print('Loaded Raw Data')

## Basic Cleaning
for col in df.columns:
    if pd.api.types.is_numeric_dtype(df[col]):
        df[col] = df[col].fillna(df[col].median())
    elif pd.api.types.is_datetime64_any_dtype(df[col]):
        median_date = df[col].median()
        df[col] = df[col].fillna(median_date)
    else:
        df[col] = df[col]

for col in df.select_dtypes(include= ['number']).columns:
    q1 = df[col].quantile(0.25)
    q3 = df[col].quantile(0.75)
    iqr = q3 - q1
    lower = q1 - 1.5 * iqr
    upper = q3 + 1.5 * iqr
    outlier_row_count = df[(df[col] < lower) | (df[col] > upper)].shape[0]
    print(f'Outlier detected: {col} : {outlier_row_count}')
    df[col] = df[col].clip(lower, upper)

clean_name = re.sub(r'\.csv$', '_cleaned.csv', file)
df.to_csv(os.path.join('Cleaned_Data', clean_name), index = False)
print(f'Cleaned Data Saved: {clean_name}')




