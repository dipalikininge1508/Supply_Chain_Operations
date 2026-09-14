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

# Delay Gap
df["Delay_Gap"] = (
    df["Days for shipping (real)"]
    - df["Days for shipment (scheduled)"]
)

# Shipping mode analysis
mode_analysis = df.groupby("Shipping Mode").agg(
    Total_Orders=("Shipping Mode", "count"),
    Average_Delay=("Delay_Gap", "mean"),
    Late_Risk=("Late_delivery_risk", "mean")
).reset_index()

mode_analysis["Late_Risk"] = mode_analysis["Late_Risk"] * 100

print(mode_analysis)

#---------------------------------------------------
plt.figure(figsize=(8, 5))

plt.bar(
    mode_analysis["Shipping Mode"],
    mode_analysis["Average_Delay"]
)

plt.title("Average Delivery Delay by Shipping Mode")
plt.xlabel("Shipping Mode")
plt.ylabel("Average Delay (Days)")

plt.xticks(rotation=30)

plt.tight_layout()
plt.show()
