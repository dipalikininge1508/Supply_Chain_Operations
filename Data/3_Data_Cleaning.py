import streamlit as st
import pandas as pd
import gdown
import os
FILE_ID = "1WIncON4DKmSUIqdttb-MD0vAhvfQutbM"
CSV_PATH = "data/APL_Logistics.csv"
@st.cache_data
def load_data():
    os.makedirs("data", exist_ok=True)
    if not os.path.exists(CSV_PATH):
        url = f"https://drive.google.com/uc?id={FILE_ID}"
        gdown.download(
            url,
            CSV_PATH,
            quiet=False
        )
    return pd.read_csv(CSV_PATH, encoding="latin1")
    
df = load_data()

# Missing values
missing_values = df.isnull().sum()

print("Missing Values:")
print(missing_values)

# Missing percentage
missing_percentage = (df.isnull().sum() / len(df)) * 100

print("\nMissing Percentage:")
print(missing_percentage)

#----------------------------------------
# Check duplicate rows
duplicates = df.duplicated().sum()

print("\nNumber of duplicate rows:")
print(duplicates)

df = df.drop_duplicates()

print("\nShape after removing duplicates:")
print(df.shape)

#----------------------------------------
print("\nActual Shipping Days:")
print(df["Days for shipping (real)"].describe())

print("\nScheduled Shipping Days:")
print(df["Days for shipment (scheduled)"].describe())

print("\nActual shipping days <= 0:")
print((df["Days for shipping (real)"] <= 0).sum())

print("\nScheduled shipping days <= 0:")
print((df["Days for shipment (scheduled)"] <= 0).sum())

#----------------------------------------
df["Delay_Gap"] = (
    df["Days for shipping (real)"]
    - df["Days for shipment (scheduled)"]
)

print(df[
    [
        "Days for shipping (real)",
        "Days for shipment (scheduled)",
        "Delay_Gap"
    ]
].head(10))

#----------------------------------------
def classify_delivery(delay):
    if delay > 0:
        return "Delayed"
    elif delay == 0:
        return "On-Time"
    else:
        return "Early"


df["Delivery_Category"] = df["Delay_Gap"].apply(classify_delivery)

print("\nDelivery Category:")
print(df["Delivery_Category"].value_counts())

#----------------------------------------
print("\nLate Delivery Risk:")
print(df["Late_delivery_risk"].value_counts())

print("\nLate Delivery Risk Percentage:")
print(
    df["Late_delivery_risk"]
    .value_counts(normalize=True) * 100
)





