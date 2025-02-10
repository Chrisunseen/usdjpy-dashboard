import streamlit as st
import pandas as pd
import requests
import smtplib

# Function to fetch real-time data with error handling
def get_bond_yield(symbol):
    st.write(f"Fetching data for: {symbol}")
    url = f"https://api.example.com/bond/{symbol}"  # Replace with actual API
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        return response.json().get("yield", "N/A")
    except requests.exceptions.RequestException:
        return "N/A"

def get_market_index(symbol):
    st.write(f"Fetching data for: {symbol}")
    url = f"https://api.example.com/index/{symbol}"  # Replace with actual API
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        return response.json().get("value", "N/A")
    except requests.exceptions.RequestException:
        return "N/A"

# Fetch Data
us10y_yield = get_bond_yield("US10Y")
jp10y_yield = get_bond_yield("JP10Y")
dxy_value = get_market_index("DXY")
nikkei_value = get_market_index("Nikkei225")
vix_value = get_market_index("VIX")
spx_value = get_market_index("SPX")

# Dashboard Layout
st.title("USD/JPY Real-Time Data Dashboard")

st.subheader("📉 U.S. 10-Year Treasury Yield")
st.metric(label="US10Y Yield", value=f"{us10y_yield if us10y_yield != 'N/A' else 'Data Unavailable'}%", delta=f"{'⚠️ Lower' if us10y_yield != 'N/A' and float(us10y_yield) < 4.00 else 'Stable'}")

st.subheader("📈 Japan 10-Year Government Bond Yield")
st.metric(label="JP10Y Yield", value=f"{jp10y_yield if jp10y_yield != 'N/A' else 'Data Unavailable'}%", delta=f"{'🚀 Higher' if jp10y_yield != 'N/A' and float(jp10y_yield) > 1.00 else 'Stable'}")

st.subheader("💲 U.S. Dollar Index (DXY)")
st.metric(label="DXY Index", value=f"{dxy_value if dxy_value != 'N/A' else 'Data Unavailable'}", delta=f"{'📈 USD Strengthening' if dxy_value != 'N/A' and float(dxy_value) > 100 else '📉 USD Weakening'}")

st.subheader("🏯 Nikkei 225 (Japan Stock Index)")
st.metric(label="Nikkei 225", value=f"{nikkei_value if nikkei_value != 'N/A' else 'Data Unavailable'}", delta=f"{'📈 Risk-On (JPY Weakens)' if nikkei_value != 'N/A' and float(nikkei_value) > 28000 else '📉 Risk-Off (JPY Strengthens)'}")

st.subheader("⚠️ VIX (Volatility Index)")
st.metric(label="VIX Index", value=f"{vix_value if vix_value != 'N/A' else 'Data Unavailable'}", delta=f"{'🆘 High Fear (JPY Strengthens)' if vix_value != 'N/A' and float(vix_value) > 20 else 'Calm Markets (JPY Weakens)'}")

st.subheader("📊 S&P 500 Index (SPX)")
st.metric(label="S&P 500", value=f"{spx_value if spx_value != 'N/A' else 'Data Unavailable'}", delta=f"{'📈 Risk-On (JPY Weakens)' if spx_value != 'N/A' and float(spx_value) > 4000 else '📉 Risk-Off (JPY Strengthens)'}")

st.write("*Data updated in real-time*")
