import streamlit as st
import pandas as pd
import plotly.express as px


st.markdown("""
    <style>
    html, body, [class*="css"]  {
        font-size: 14px;
    }
    </style>
""", unsafe_allow_html=True)
# -------------------------------
# PAGE CONFIG (IMPORTANT)
# -------------------------------
st.set_page_config(layout="wide")

# -------------------------------
# TITLE
# -------------------------------
st.title("📦 Logistics Performance Dashboard")

# -------------------------------
# LOAD DATA
# -------------------------------
df = pd.read_csv("APL_Logistics.csv", encoding='latin1')

df.columns = df.columns.str.replace(" ", "_")

# -------------------------------
# FEATURES
# -------------------------------
df['Delay_Gap'] = df['Days_for_shipping_(real)'] - df['Days_for_shipment_(scheduled)']
df['Delivery_Status'] = df['Delay_Gap'].apply(lambda x: 'Delayed' if x > 0 else 'On-Time')

# -------------------------------
# SIDEBAR FILTER
# -------------------------------
st.sidebar.header("🔍 Filters")

mode = st.sidebar.selectbox("Shipping Mode", df['Shipping_Mode'].unique())
region = st.sidebar.selectbox("Region", df['Order_Region'].unique())

df = df[(df['Shipping_Mode'] == mode) & (df['Order_Region'] == region)]

# -------------------------------
# KPI CALCULATIONS
# -------------------------------
total_orders = len(df)
on_time_pct = (df['Delivery_Status'] == 'On-Time').mean() * 100
delayed_pct = (df['Delivery_Status'] == 'Delayed').mean() * 100
avg_delay = df['Delay_Gap'].mean()
total_profit = df['Order_Profit_Per_Order'].sum()
avg_sales = df['Sales'].mean()

# -------------------------------
# KPI CARDS (ROW 1)
# -------------------------------
st.subheader("📊 Key Metrics")

col1, col2, col3, col4, col5 = st.columns(5)

col1.metric("📦 Orders", total_orders)
col2.metric("✅ On-Time %", f"{round(on_time_pct,2)}%")
col3.metric("⚠ Delayed %", f"{round(delayed_pct,2)}%")
col4.metric("⏱ Avg Delay", f"{round(avg_delay,2)} days")
col5.metric("💰 Profit", f"${round(total_profit,2)}")

# -------------------------------
# KPI CARDS (ROW 2)
# -------------------------------
col6, col7 = st.columns(2)

col6.metric("📊 Avg Sales", f"${round(avg_sales,2)}")
col7.metric("🚚 Shipping Mode", mode)

# -------------------------------
# 1. DELAY RISK
# -------------------------------
st.markdown("---")
st.subheader("📉 Delay Risk Analysis")

fig1 = px.histogram(
    df,
    x='Delay_Gap',
    color='Delivery_Status'
)

st.plotly_chart(fig1, use_container_width=True)

# -------------------------------
# 2. SHIPPING MODE COMPARISON
# -------------------------------
st.markdown("---")
st.subheader("🚚 Shipping Mode Comparison")

mode_data = df.groupby('Shipping_Mode')['Delay_Gap'].mean().reset_index()

fig2 = px.bar(
    mode_data,
    x='Shipping_Mode',
    y='Delay_Gap',
    color='Shipping_Mode'
)

st.plotly_chart(fig2, use_container_width=True)

# -------------------------------
# 3. REGION ANALYSIS
# -------------------------------
st.markdown("---")
st.subheader("🌍 Regional Analysis")

region_data = df.groupby('Order_Region')['Delay_Gap'].mean().reset_index()

fig3 = px.bar(
    region_data,
    x='Order_Region',
    y='Delay_Gap',
    color='Delay_Gap'
)

st.plotly_chart(fig3, use_container_width=True)

# -------------------------------
# 4. HEATMAP
# -------------------------------
st.markdown("---")
st.subheader("🗺 Delivery Heatmap")

fig4 = px.scatter_geo(
    df.sample(2000),
    lat='Latitude',
    lon='Longitude',
    color='Delay_Gap'
)

st.plotly_chart(fig4, use_container_width=True)

# -------------------------------
# DATA TABLE
# -------------------------------
st.markdown("---")
st.subheader("📄 Data Preview")

st.dataframe(df.head())
