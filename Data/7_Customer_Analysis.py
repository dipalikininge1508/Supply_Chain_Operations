import matplotlib.pyplot as plt
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

df["Delay_Gap"] = (
    df["Days for shipping (real)"]
    - df["Days for shipment (scheduled)"]
)

segment_analysis = df.groupby("Customer Segment").agg(
    Total_Orders=("Customer Segment", "count"),
    Average_Delay=("Delay_Gap", "mean"),
    Late_Risk=("Late_delivery_risk", "mean"),
    Average_Sales=("Sales", "mean")
).reset_index()

segment_analysis["Late_Risk"] *= 100

print(segment_analysis)

#---------------------------------------------------
country_analysis = df.groupby("Order Country").agg(
    Total_Orders=("Order Country", "count"),
    Average_Delay=("Delay_Gap", "mean"),
    Late_Risk=("Late_delivery_risk", "mean")
).reset_index()

country_analysis["Late_Risk"] *= 100

country_analysis = country_analysis.sort_values(
    "Late_Risk",
    ascending=False
)

print("\nTop 15 High-Risk Countries:")
print(country_analysis.head(15))

#--------------------------------------------------
numeric_columns = [
    "Days for shipping (real)",
    "Days for shipment (scheduled)",
    "Benefit per order",
    "Sales per customer",
    "Order Item Discount",
    "Order Item Discount Rate",
    "Order Item Product Price",
    "Order Item Profit Ratio",
    "Order Item Quantity",
    "Sales",
    "Order Item Total",
    "Order Profit Per Order",
    "Product Price",
    "Late_delivery_risk",
    "Delay_Gap"
]

correlation = df[numeric_columns].corr()

print(correlation["Delay_Gap"].sort_values(ascending=False))

#----------------------------------------------
df.to_csv(
    "../Outputs/APL_Logistics_Cleaned.csv",
    index=False
)

print("Cleaned dataset saved successfully!")
