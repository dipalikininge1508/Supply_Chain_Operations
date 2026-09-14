import pandas as pd
import matplotlib.pyplot as plt

# Load dataset
df = pd.read_csv("../Data/APL_Logistics.csv", encoding="latin1")

# Calculate delay gap
df["Delay_Gap"] = (
    df["Days for shipping (real)"]
    - df["Days for shipment (scheduled)"]
)

# Delivery classification
def classify_delivery(delay):
    if delay > 0:
        return "Delayed"
    elif delay == 0:
        return "On-Time"
    else:
        return "Early"


df["Delivery_Category"] = df["Delay_Gap"].apply(classify_delivery)

# Total orders
total_orders = len(df)

# On-time orders
on_time_orders = (df["Delay_Gap"] <= 0).sum()

# Delayed orders
delayed_orders = (df["Delay_Gap"] > 0).sum()

# On-time delivery rate
on_time_rate = (on_time_orders / total_orders) * 100

# Average delay
average_delay = df["Delay_Gap"].mean()

# Late delivery risk
late_risk_rate = df["Late_delivery_risk"].mean() * 100

print("Total Orders:", total_orders)
print("On-Time Orders:", on_time_orders)
print("Delayed Orders:", delayed_orders)

print("\nOn-Time Delivery Rate:")
print(round(on_time_rate, 2), "%")

print("\nAverage Delivery Delay:")
print(round(average_delay, 2), "days")

print("\nLate Delivery Risk Ratio:")
print(round(late_risk_rate, 2), "%")

#-------------------------------------------------
delivery_counts = df["Delivery_Category"].value_counts()

plt.figure(figsize=(8, 5))

plt.bar(
    delivery_counts.index,
    delivery_counts.values
)

plt.title("Delivery Performance")
plt.xlabel("Delivery Category")
plt.ylabel("Number of Orders")

plt.tight_layout()
plt.show()

#-------------------------------------------------
plt.figure(figsize=(8, 5))

plt.hist(df["Delay_Gap"], bins=20)

plt.title("Distribution of Delivery Delay Gap")
plt.xlabel("Delay Gap (Days)")
plt.ylabel("Number of Orders")

plt.tight_layout()
plt.show()
