import streamlit as st
import pandas as pd
import requests
import smtplib

# Function to fetch real-time data with error handling
def get_bond_yield(symbol):
    url = f"https://api.example.com/bond/{symbol}"  # Replace with actual API
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        return response.json().get("yield", "N/A")
    except requests.exceptions.RequestException:
        return "N/A"

def get_nfp_data():
    url = "https://api.example.com/nfp"  # Replace with actual API
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException:
        return {"jobs_added": "N/A", "unemployment_rate": "N/A"}

def get_vix():
    url = "https://api.example.com/vix"  # Replace with actual API
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        return response.json().get("vix_value", "N/A")
    except requests.exceptions.RequestException:
        return "N/A"

# Function to send email alert
def send_email_alert(subject, message):
    sender_email = "your_email@example.com"
    receiver_email = "recipient@example.com"
    password = "your_email_password"
    
    with smtplib.SMTP("smtp.example.com", 587) as server:
        server.starttls()
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, f"Subject: {subject}\n\n{message}")

# Fetch Data
us10y_yield = get_bond_yield("US10Y")
jp10y_yield = get_bond_yield("JP10Y")
nfp_data = get_nfp_data()
vix_value = get_vix()

# Set Alert Levels
us10y_alert = 4.00  # Example threshold
jp10y_alert = 1.00
vix_alert = 20

# Determine Bullish or Bearish Trend
def determine_trend():
    daily_trend = "Bullish" if float(us10y_yield) > us10y_alert else "Bearish"
    weekly_trend = "Bullish" if float(jp10y_yield) < jp10y_alert else "Bearish"
    monthly_trend = "Bullish" if float(vix_value) < vix_alert else "Bearish"
    return daily_trend, weekly_trend, monthly_trend

daily_trend, weekly_trend, monthly_trend = determine_trend()

# Check and send alerts
if float(us10y_yield) < us10y_alert:
    message = f"ALERT: US10Y Yield dropped below {us10y_alert}%. Current: {us10y_yield}%"
    send_email_alert("US10Y Alert", message)

if float(jp10y_yield) > jp10y_alert:
    message = f"ALERT: JP10Y Yield rose above {jp10y_alert}%. Current: {jp10y_yield}%"
    send_email_alert("JP10Y Alert", message)

if float(vix_value) > vix_alert:
    message = f"ALERT: VIX Index is above {vix_alert}. Current: {vix_value}"
    send_email_alert("VIX Alert", message)

# Dashboard Layout
st.title("USD/JPY Real-Time Data Dashboard")

st.subheader("📉 U.S. 10-Year Treasury Yield")
st.metric(label="US10Y Yield", value=f"{us10y_yield}%", delta=f"{'⚠️ Lower' if float(us10y_yield) < us10y_alert else 'Stable'}")

st.subheader("📈 Japan 10-Year Government Bond Yield")
st.metric(label="JP10Y Yield", value=f"{jp10y_yield}%", delta=f"{'🚀 Higher' if float(jp10y_yield) > jp10y_alert else 'Stable'}")

st.subheader("📊 U.S. Non-Farm Payrolls (NFP)")
st.write(f"Employment Change: {nfp_data.get('jobs_added', 'N/A')} jobs")
st.write(f"Unemployment Rate: {nfp_data.get('unemployment_rate', 'N/A')}%")

st.subheader("⚠️ VIX (Volatility Index)")
st.metric(label="VIX Index", value=vix_value, delta=f"{'🆘 High Fear' if float(vix_value) > vix_alert else 'Calm Markets'}")

st.subheader("📈 USD/JPY Trend Signals")
st.write(f"**Daily Trend:** {daily_trend}")
st.write(f"**Weekly Trend:** {weekly_trend}")
st.write(f"**Monthly Trend:** {monthly_trend}")

st.write("*Data updated in real-time*")
