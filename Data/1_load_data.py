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

print("Dataset loaded successfully!")

print("\nShape of dataset:")
print(df.shape)

print("\nFirst 5 rows:")
print(df.head())

print("\nColumn names:")
print(df.columns.tolist())
