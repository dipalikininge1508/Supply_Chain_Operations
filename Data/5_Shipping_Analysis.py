import pandas as pd
import matplotlib.pyplot as plt
import gdown
import os

file_id = "1WIncON4DKmSUIqdttb-MD0vAhvfQutbM"
csv_path = "data/APL_Logistics.csv"

os.makedirs("data", exist_ok=True)

if not os.path.exists(csv_path):
    url = f"https://drive.google.com/uc?id={file_id}"
    gdown.download(url, csv_path, quiet=False)

df = pd.read_csv(csv_path, encoding="latin1")

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
