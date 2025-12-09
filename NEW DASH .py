# app.py - Aman Payment Security 2025 - FINAL GLOBAL EDITION
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import networkx as nx
from datetime import datetime, timedelta
import random
import time

st.set_page_config(page_title="Aman Fraud Shield 2025", layout="wide", page_icon="🛡️")

# === CSS السحري اللي هيخلي الداشبورد يجنن ===
st.markdown("""
<style>
    .main {background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%); color: #e2e8f0;}
    .big-title {font-size: 48px !important; font-weight: 900; color: #34d399; text-align: center; text-shadow: 0 0 20px rgba(52,211,153,0.5);}
    .card {background: rgba(255,255,255,0.05); backdrop-filter: blur(10px); border-radius: 16px; 
           padding: 20px; border: 1px solid rgba(52,211,153,0.2); box-shadow: 0 8px 32px rgba(0,0,0,0.3);}
    .alert {background: linear-gradient(90deg,#7f1d1d,#991b1b); color:#fca5a5; padding:16px; border-radius:12px; 
            border-left:6px solid #ef4444; font-weight:bold; animation: pulse 2s infinite;}
    @keyframes pulse {0%,100%{opacity:0.9} 50%{opacity:1}}
    .stMetric {font-weight: bold !important;}
</style>
""", unsafe_allow_html=True)

# Header + Logo
st.markdown("""
<div style="text-align:center; padding:20px 0;">
    <img src="https://i.imgur.com/5vM8o7J.png" width="100" style="border-radius:50%;">
    <div class="big-title">🛡️ Aman Payment Security</div>
    <p style="color:#94a3b8; font-size:18px;">Live Fraud Detection Shield • Egypt 2025</p>
</div>
""", unsafe_allow_html=True)

# Live Alert
alerts = [
    "Card Testing Attack Detected – Vodafone Cash (89 attempts/min)",
    "Account Takeover Cluster Blocked – Alexandria (12 accounts)",
    "New ML Model v4.2 Deployed – Precision +6.1%",
    "Friendly Fraud Spike on Noon.com (+198%)",
    "Bot Network Neutralized – Qalyubia (31 IPs blocked)"
]
st.markdown(f'<div class="alert">LIVE ALERT • {alerts[int(time.time()/20)%len(alerts)]}</div>', unsafe_allow_html=True)

# Generate Live Data
@st.cache_data(ttl=30)
def get_data():
    if 'data' not in st.session_state:
        st.session_state.data = pd.DataFrame()
    now = datetime.now()
    new = pd.DataFrame([
        {
            "id": f"TX{random.randint(1000000,9999999)}",
            "amount": random.randint(80, 35000),
            "merchant": random.choice(["Noon","Amazon","Talabat","Uber","Fawry","Vodafone Cash","InstaPay"]),
            "city": random.choice(["القاهرة","الجيزة","الإسكندرية","الدقهلية","سوهاج","أسيوط","القليوبية"]),
            "risk": random.choices([random.randint(500,720), random.randint(850,1000)], [0.7,0.3])[0],
            "type": random.choice(["Card Testing","ATO","Friendly Fraud","Bot","Compromise"]),
            "status": random.choices(["BLOCKED","REVIEW","APPROVED"], [0.26,0.24,0.5])[0],
            "time": now - timedelta(seconds=random.randint(0,3600))
        } for _ in range(random.randint(20,50))
    ])
    st.session_state.data = pd.concat([st.session_state.data, new], ignore_index=True)
    cutoff = now - timedelta(hours=24)
    df = st.session_state.data[st.session_state.data["time"] >= cutoff].copy()
    return df.tail(8000)

df = get_data()

# KPIs
blocked = len(df[df.status=="BLOCKED"])
total = len(df)
saved = df[df.status=="BLOCKED"].amount.sum()
rate = round(blocked/total*100, 2) if total>0 else 0

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown(f'<div class="card"><h2>{total:,}</h2><p>Total Transactions</p></div>', unsafe_allow_html=True)
with col2:
    st.markdown(f'<div class="card" style="border-color:#ef4444;"><h2 style="color:#f87171">{blocked:,}</h2><p>Blocked Fraud</p></div>', unsafe_allow_html=True)
with col3:
    st.markdown(f'<div class="card" style="border-color:#10b981;"><h2 style="color:#34d399">{saved:,} EGP</h2><p>Losses Prevented</p></div>', unsafe_allow_html=True)
with col4:
    st.markdown(f'<div class="card"><h2 style="color:#fbbf24">{rate}%</h2><p>Detection Rate</p></div>', unsafe_allow_html=True)

st.markdown("---")

left, right = st.columns([2.2, 1])

with left:
    st.subheader("Fraud Map – Egypt (Last 24h)")
    cities = {"القاهرة":[30.04,31.24],"الإسكندرية":[31.20,29.92],"الجيزة":[30.01,31.21],
              "الدقهلية":[31.05,31.38],"سوهاج":[26.56,31.70],"أسيوط":[27.18,31.18],"القليوبية":[30.33,31.21]}
    map_df = df[df.status=="BLOCKED"].groupby("city").size().reset_index(name="count")
    map_df["lat"] = map_df.city.map(lambda x: cities.get(x,[0,0])[0])
    map_df["lon"] = map_df.city.map(lambda x: cities.get(x,[0,0])[1])
    fig = px.scatter_mapbox(map_df, lat="lat", lon="lon", size="count", color="count", zoom=5.5,
                            mapbox_style="carto-darkmatter", height=500,
                            color_continuous_scale="OrRd", hover_name="city")
    fig.update_layout(margin=dict(l=0,r=0,t=0,b=0), paper_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Fraud Trend (Hourly)")
    trend = df.set_index("time").resample("1H").size().reset_index(name="count")
    fig2 = px.area(trend, x="time", y="count", template="plotly_dark", color_discrete_sequence=["#f87171"])
    st.plotly_chart(fig2, use_container_width=True)

with right:
    st.subheader("Top 10 Riskiest Transactions")
    top10 = df.nlargest(10, "risk")[["id","amount","merchant","city","risk","type","status"]]
    st.dataframe(top10, use_container_width=True, hide_index=True)

    st.subheader("Most Targeted Merchants")
    merch = df.merchant.value_counts().head(7)
    fig3 = px.bar(y=merch.index, x=merch.values, orientation='h', template="plotly_dark", color=merch.values, color_continuous_scale="Reds")
    st.plotly_chart(fig3, use_container_width=True)

# Auto Refresh
if st.checkbox("Auto Refresh Every 60s", value=True):
    time.sleep(60)
    st.rerun()
