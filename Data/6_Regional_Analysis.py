import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("../Data/APL_Logistics.csv", encoding="latin1")

df["Delay_Gap"] = (
    df["Days for shipping (real)"]
    - df["Days for shipment (scheduled)"]
)

regional_analysis = df.groupby("Order Region").agg(
    Total_Orders=("Order Region", "count"),
    Average_Delay=("Delay_Gap", "mean"),
    Late_Risk=("Late_delivery_risk", "mean")
).reset_index()

regional_analysis["Late_Risk"] = (
    regional_analysis["Late_Risk"] * 100
)

regional_analysis = regional_analysis.sort_values(
    "Late_Risk",
    ascending=False
)

print(regional_analysis)

#------------------------------------------
top_regions = regional_analysis.head(10)

print("\nTop 10 High-Risk Regions:")
print(top_regions)

#------------------------------------------
plt.figure(figsize=(10, 6))

plt.barh(
    top_regions["Order Region"],
    top_regions["Late_Risk"]
)

plt.title("Top High-Risk Regions")
plt.xlabel("Late Delivery Risk (%)")
plt.ylabel("Order Region")

plt.gca().invert_yaxis()

plt.tight_layout()
plt.show()

#--------------------------------------------
market_analysis = df.groupby("Market").agg(
    Total_Orders=("Market", "count"),
    Average_Delay=("Delay_Gap", "mean"),
    Late_Risk=("Late_delivery_risk", "mean")
).reset_index()

market_analysis["Late_Risk"] *= 100

print("\nMarket Analysis:")
print(market_analysis)