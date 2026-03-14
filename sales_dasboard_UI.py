import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# -------------------------------------------------
# Page Config
# -------------------------------------------------
st.set_page_config(page_title="Sales Dashboard", layout="wide")
st.title("📊 Sales Data Dashboard")

plt.style.use("ggplot")
np.random.seed(42)

# -------------------------------------------------
# Generate Data
# -------------------------------------------------
dates = pd.date_range(start="2024-01-01", end="2024-12-31", freq="D")

data = pd.DataFrame({
    "order_id": range(1, 1001),
    "date": np.random.choice(dates, 1000),
    "region": np.random.choice(["North", "East", "West", "South"], 1000),
    "product": np.random.choice(["Laptop", "Phones", "Tablet", "Headphones"], 1000),
    "quantity": np.random.randint(1, 5, 1000),
    "price": np.random.randint(500, 5000, 1000)
})

category_map = {
    "Laptop": "Electronics",
    "Phones": "Electronics",
    "Tablet": "Electronics",
    "Headphones": "Accessories"
}

data["category"] = data["product"].map(category_map)
data["revenue"] = data["quantity"] * data["price"]
data["month"] = data["date"].dt.to_period("M")

# -------------------------------------------------
# Sidebar Filters
# -------------------------------------------------
st.sidebar.header("🔎 Filters")

selected_region = st.sidebar.selectbox(
    "Select Region",
    ["All"] + list(data["region"].unique())
)

selected_category = st.sidebar.selectbox(
    "Select Category",
    ["All"] + list(data["category"].unique())
)

filtered_data = data.copy()

if selected_region != "All":
    filtered_data = filtered_data[filtered_data["region"] == selected_region]

if selected_category != "All":
    filtered_data = filtered_data[filtered_data["category"] == selected_category]

# -------------------------------------------------
# KPIs
# -------------------------------------------------
total_revenue = filtered_data["revenue"].sum()
total_orders = filtered_data["order_id"].nunique()
top_product = filtered_data.groupby("product")["revenue"].sum().idxmax()

col1, col2, col3 = st.columns(3)

col1.metric("💰 Total Revenue", f"{total_revenue:,.0f}")
col2.metric("📦 Total Orders", total_orders)
col3.metric("🏆 Top Product", top_product)

st.divider()

# -------------------------------------------------
# Monthly Revenue Trend (Smaller)
# -------------------------------------------------
st.subheader("📈 Monthly Revenue Trend")

monthly_sales = filtered_data.groupby("month")["revenue"].sum()

fig1, ax1 = plt.subplots(figsize=(7, 3))
monthly_sales.plot(ax=ax1)
ax1.set_xlabel("Month")
ax1.set_ylabel("Revenue")
plt.tight_layout()
st.pyplot(fig1)

st.divider()

# -------------------------------------------------
# Side-by-Side Charts
# -------------------------------------------------
colA, colB = st.columns(2)

# Region-wise Sales
with colA:
    st.subheader("🌍 Region-wise Sales")
    regional_sales = filtered_data.groupby("region")["revenue"].sum()
    fig2, ax2 = plt.subplots(figsize=(5, 3))
    sns.barplot(x=regional_sales.index, y=regional_sales.values, ax=ax2)
    ax2.set_ylabel("Revenue")
    plt.tight_layout()
    st.pyplot(fig2)

# Category Distribution
with colB:
    st.subheader("🥧 Category Distribution")
    category_sales = filtered_data.groupby("category")["revenue"].sum()
    fig3, ax3 = plt.subplots(figsize=(5, 3))
    ax3.pie(category_sales, labels=category_sales.index, autopct="%1.1f%%")
    plt.tight_layout()
    st.pyplot(fig3)