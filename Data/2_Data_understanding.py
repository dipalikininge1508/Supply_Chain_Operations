import pandas as pd
import gdown
import os

file_id = "1WIncON4DKmSUIqdttb-MD0vAhvfQutbM"
csv_path = "data/APL_Logistics.csv"

os.makedirs("data", exist_ok=True)

if not os.path.exists(csv_path):
    url = f"https://drive.google.com/uc?id={file_id}"
    gdown.download(url, csv_path, quiet=False)

df = pd.read_csv(csv_path, encoding="latin1")

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
