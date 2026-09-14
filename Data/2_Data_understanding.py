import pandas as pd

# Load dataset
df = pd.read_csv("../Data/APL_Logistics.csv", encoding="latin1")

# Shape
print("Shape:")
print(df.shape)

# First 5 rows
print("\nFirst 5 rows:")
print(df.head())

# Last 5 rows
print("\nLast 5 rows:")
print(df.tail())

# Column names
print("\nColumns:")
print(df.columns.tolist())

# Data types
print("\nData Types:")
print(df.dtypes)

# Statistical summary
print("\nStatistical Summary:")
print(df.describe())

# Information
print("\nDataset Information:")
print(df.info())