import pandas as pd

# Load dataset
df = pd.read_csv("../Data/APL_Logistics.csv", encoding="latin1")

print("Dataset loaded successfully!")

print("\nShape of dataset:")
print(df.shape)

print("\nFirst 5 rows:")
print(df.head())

print("\nColumn names:")
print(df.columns.tolist())