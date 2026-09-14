import streamlit as st
import pandas as pd
import numpy as np
import gdown
import os


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="APL Logistics Delivery Analytics",
    page_icon="🚚",
    layout="wide"
)


# ============================================================
# TITLE
# ============================================================

st.title("🚚 APL Logistics")
st.subheader(
    "Delivery Performance, Delay Risk & Logistics Efficiency Analysis"
)

st.markdown(
    "Interactive dashboard for analyzing delivery performance, "
    "shipping modes, regions, markets and customer segments."
)


# ============================================================
# LOAD DATA
# ============================================================
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

    return pd.read_csv(CSV_PATH)

    df["Delay_Gap"] = (
        df["Days for shipping (real)"]
        - df["Days for shipment (scheduled)"]
    )

    def classify_delivery(delay):

        if delay > 0:
            return "Delayed"

        elif delay == 0:
            return "On-Time"

        else:
            return "Early"

    df["Delivery_Category"] = (
        df["Delay_Gap"].apply(classify_delivery)
    )

    return df


df = load_data()


# ============================================================
# SIDEBAR FILTERS
# ============================================================

st.sidebar.header("🔎 Filters")


# Shipping Mode

shipping_modes = sorted(
    df["Shipping Mode"].dropna().unique()
)

selected_shipping = st.sidebar.multiselect(
    "Shipping Mode",
    shipping_modes,
    default=shipping_modes
)


# Market

markets = sorted(
    df["Market"].dropna().unique()
)

selected_market = st.sidebar.multiselect(
    "Market",
    markets,
    default=markets
)


# Region

regions = sorted(
    df["Order Region"].dropna().unique()
)

selected_region = st.sidebar.multiselect(
    "Order Region",
    regions,
    default=regions
)


# Customer Segment

segments = sorted(
    df["Customer Segment"].dropna().unique()
)

selected_segment = st.sidebar.multiselect(
    "Customer Segment",
    segments,
    default=segments
)


# ============================================================
# APPLY FILTERS
# ============================================================

filtered_df = df[
    (df["Shipping Mode"].isin(selected_shipping)) &
    (df["Market"].isin(selected_market)) &
    (df["Order Region"].isin(selected_region)) &
    (df["Customer Segment"].isin(selected_segment))
].copy()


# ============================================================
# KPI CALCULATIONS
# ============================================================

total_orders = len(filtered_df)

on_time_orders = (
    filtered_df["Delay_Gap"] <= 0
).sum()

delayed_orders = (
    filtered_df["Delay_Gap"] > 0
).sum()


if total_orders > 0:

    on_time_rate = (
        on_time_orders / total_orders
    ) * 100

    late_risk_rate = (
        filtered_df["Late_delivery_risk"].mean()
    ) * 100

    average_delay = (
        filtered_df["Delay_Gap"].mean()
    )

else:

    on_time_rate = 0
    late_risk_rate = 0
    average_delay = 0


# ============================================================
# KPI DISPLAY
# ============================================================

st.header("📊 Delivery Performance Overview")


col1, col2, col3, col4 = st.columns(4)


col1.metric(
    "Total Orders",
    f"{total_orders:,}"
)


col2.metric(
    "On-Time Delivery",
    f"{on_time_rate:.2f}%"
)


col3.metric(
    "Average Delay",
    f"{average_delay:.2f} days"
)


col4.metric(
    "Late Delivery Risk",
    f"{late_risk_rate:.2f}%"
)


# ============================================================
# DELIVERY CATEGORY
# ============================================================

st.header("📦 Delivery Performance")


delivery_counts = (
    filtered_df["Delivery_Category"]
    .value_counts()
)


col1, col2 = st.columns(2)


with col1:

    st.subheader("Delivery Category")

    st.bar_chart(
        delivery_counts
    )


with col2:

    st.subheader("Delay Gap Distribution")

    st.bar_chart(
        filtered_df["Delay_Gap"]
        .value_counts()
        .sort_index()
    )


# ============================================================
# SHIPPING MODE ANALYSIS
# ============================================================

st.header("🚢 Shipping Mode Analysis")


mode_analysis = (
    filtered_df
    .groupby("Shipping Mode")
    .agg(
        Total_Orders=(
            "Shipping Mode",
            "count"
        ),

        Average_Delay=(
            "Delay_Gap",
            "mean"
        ),

        Late_Risk=(
            "Late_delivery_risk",
            "mean"
        )
    )
    .reset_index()
)


mode_analysis["Late_Risk"] = (
    mode_analysis["Late_Risk"] * 100
)


st.dataframe(
    mode_analysis,
    use_container_width=True
)


st.subheader(
    "Average Delay by Shipping Mode"
)

st.bar_chart(
    mode_analysis.set_index(
        "Shipping Mode"
    )["Average_Delay"]
)


# ============================================================
# REGIONAL ANALYSIS
# ============================================================

st.header("🌍 Regional Analysis")


regional_analysis = (
    filtered_df
    .groupby("Order Region")
    .agg(
        Total_Orders=(
            "Order Region",
            "count"
        ),

        Average_Delay=(
            "Delay_Gap",
            "mean"
        ),

        Late_Risk=(
            "Late_delivery_risk",
            "mean"
        )
    )
    .reset_index()
)


regional_analysis["Late_Risk"] = (
    regional_analysis["Late_Risk"] * 100
)


regional_analysis = regional_analysis.sort_values(
    "Late_Risk",
    ascending=False
)


st.dataframe(
    regional_analysis,
    use_container_width=True
)


st.subheader(
    "Late Delivery Risk by Region"
)


st.bar_chart(
    regional_analysis.set_index(
        "Order Region"
    )["Late_Risk"]
)


# ============================================================
# MARKET ANALYSIS
# ============================================================

st.header("📈 Market Analysis")


market_analysis = (
    filtered_df
    .groupby("Market")
    .agg(
        Total_Orders=(
            "Market",
            "count"
        ),

        Average_Delay=(
            "Delay_Gap",
            "mean"
        ),

        Late_Risk=(
            "Late_delivery_risk",
            "mean"
        )
    )
    .reset_index()
)


market_analysis["Late_Risk"] = (
    market_analysis["Late_Risk"] * 100
)


st.dataframe(
    market_analysis,
    use_container_width=True
)


# ============================================================
# CUSTOMER SEGMENT ANALYSIS
# ============================================================

st.header("👥 Customer Segment Analysis")


segment_analysis = (
    filtered_df
    .groupby("Customer Segment")
    .agg(
        Total_Orders=(
            "Customer Segment",
            "count"
        ),

        Average_Delay=(
            "Delay_Gap",
            "mean"
        ),

        Late_Risk=(
            "Late_delivery_risk",
            "mean"
        ),

        Average_Sales=(
            "Sales",
            "mean"
        )
    )
    .reset_index()
)


segment_analysis["Late_Risk"] = (
    segment_analysis["Late_Risk"] * 100
)


st.dataframe(
    segment_analysis,
    use_container_width=True
)


# ============================================================
# HIGH RISK REGIONS
# ============================================================

st.header("⚠️ High-Risk Regions")


top_risk_regions = regional_analysis.head(10)


st.dataframe(
    top_risk_regions,
    use_container_width=True
)


# ============================================================
# BUSINESS INSIGHTS
# ============================================================

st.header("💡 Key Business Insights")


if len(filtered_df) > 0:

    highest_risk_region = (
        regional_analysis.iloc[0]["Order Region"]
    )

    highest_risk_value = (
        regional_analysis.iloc[0]["Late_Risk"]
    )

    highest_delay_mode = (
        mode_analysis.sort_values(
            "Average_Delay",
            ascending=False
        ).iloc[0]["Shipping Mode"]
    )

    st.write(
        f"• **Highest-risk region:** "
        f"{highest_risk_region} "
        f"({highest_risk_value:.2f}% late risk)"
    )

    st.write(
        f"• **Shipping mode with highest average delay:** "
        f"{highest_delay_mode}"
    )

    st.write(
        f"• **Overall on-time delivery rate:** "
        f"{on_time_rate:.2f}%"
    )

    st.write(
        f"• **Average delivery delay:** "
        f"{average_delay:.2f} days"
    )

else:

    st.warning(
        "No data available for the selected filters."
    )


# ============================================================
# FOOTER
# ============================================================

st.markdown("---")

st.caption(
    "APL Logistics — Delivery Performance & Delay Risk Analysis"
)
