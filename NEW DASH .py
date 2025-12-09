import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import networkx as nx
from datetime import datetime, timedelta
import random
import time

# ────────────────────────────────
# Aman Payment Security – Live Dashboard 2025 (Dark) - FIXED
# ────────────────────────────────

st.set_page_config(page_title="Aman Payment Security", layout="wide", page_icon="🛡️")

# Sidebar settings
st.sidebar.title("⚙️ إعدادات العرض")
auto_refresh = st.sidebar.checkbox("🔄 تحديث تلقائي كل 60 ثانية (وضع لايف)", value=True)

# Custom CSS (always safe)
st.markdown("""
<style>
    .reportview-container, .main {background: linear-gradient(180deg,#0b1220 0%, #071026 100%); color: #e6eef8;}
    .big-title {font-size:46px !important; font-weight:900; color:#34d399; text-align:center; padding:10px 0;}
    .kpi {font-size:38px; font-weight:800; color:#e6eef8;}
    .kpi-small {font-size:15px; color:#a6b4c6; font-weight:600;}
    .card {background: linear-gradient(180deg, rgba(255,255,255,0.04), rgba(255,255,255,0.01));
           padding:18px; border-radius:14px; box-shadow: 0 8px 32px rgba(0,10,40,0.8);
           border:1px solid rgba(52,211,153,0.15);}
    .danger {color:#f87171 !important;}
    .safe {color:#34d399 !important;}
    .yellow {color:#fbbf24 !important;}
    .alert-banner {background:#7f1d1d; padding:16px; border-radius:12px; border-left:6px solid #ef4444;
                   font-size:18px; font-weight:700; color:#fca5a5; animation: pulse 3s infinite;}
    @keyframes pulse {0%,100% {opacity:0.9;} 50% {opacity:1;}}
</style>
""", unsafe_allow_html=True)

# Conditional meta refresh (only when auto_refresh checked)
if auto_refresh:
    st.markdown('<meta http-equiv="refresh" content="60">', unsafe_allow_html=True)

# Header
st.markdown(f'''
<div style="display:flex; align-items:center; gap:20px; padding:10px 0;">
    <img src="https://i.imgur.com/5vM8o7J.png" width="90">
    <div>
        <p class="big-title">🛡️ Aman Payment Security – Live Fraud Shield 2025</p>
        <p style="color:#94a3b8; margin:0; font-size:16px;">
            نظام الكشف الذكي عن الاحتيال • آخر تحديث: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
        </p>
    </div>
</div>
''', unsafe_allow_html=True)

# Live Alert Banner (rotate alerts every ~25 seconds)
alerts = [
    "🚨 هجوم Card Testing عالي السرعة على فودافون كاش (٨٧ محاولة/دقيقة)",
    "⚡ تم اكتشاف وإيقاف تكتل Account Takeover من الإسكندرية (١٢ حساب)",
    "✅ تم تفعيل نموذج الذكاء الاصطناعي الجديد v4.1 – دقة +٥.٨٪",
    "🔥 ارتفاع ملحوظ في Friendly Fraud على Noon (+٢١٠٪ عن الأساس)",
    "🛑 تم حظر شبكة بوتات من القليوبية (٢٨ عنوان IP)"
]
alert = alerts[int(time.time() / 25) % len(alerts)]
st.markdown(f'<div class="alert-banner">🚨 تنبيه فوري • {alert}</div>', unsafe_allow_html=True)

# Data generator + caching (keeps data in session_state, cache for 60s)
@st.cache_data(ttl=60)
def get_data_cached():
    # Use session_state to keep historical live feed and append new transactions
    if 'df' not in st.session_state:
        st.session_state.df = pd.DataFrame()

    now = datetime.now()
    new_txs = random.randint(15, 45)
    cities = ["القاهرة","الجيزة","الإسكندرية","الدقهلية","الشرقية","القليوبية","البحيرة","المنوفية","أسيوط","سوهاج"]
    merchants = ["Amazon","Noon","Talabat","Uber","Careem","Vodafone Cash","Fawry","InstaPay","Booking.com","Souq"]
    types = ["Card Testing","Account Takeover","Friendly Fraud","Bot Attack","Merchant Compromise"]

    new_rows = []
    for _ in range(new_txs):
        row = {
            "transaction_id": f"TX{random.randint(1000000,9999999)}",
            "account_id": f"AC{random.randint(20000,99999)}",
            "merchant": random.choice(merchants),
            "city": random.choice(cities),
            "amount": random.randint(80, 28000),
            "risk_score": random.choices([random.randint(500,750), random.randint(820,1000)], [0.68, 0.32])[0],
            "fraud_type": random.choices(types, [0.28,0.18,0.22,0.20,0.12])[0],
            "status": random.choices(["BLOCKED","REVIEW","APPROVED"], [0.24,0.26,0.50])[0],
            "timestamp": now - timedelta(seconds=random.randint(0, 1800))
        }
        new_rows.append(row)

    new_df = pd.DataFrame(new_rows)
    # ensure timestamp is datetime
    new_df["timestamp"] = pd.to_datetime(new_df["timestamp"])
    st.session_state.df = pd.concat([st.session_state.df, new_df], ignore_index=True)
    # keep only last 24 hours
    cutoff = now - timedelta(hours=24)
    live_df = st.session_state.df[st.session_state.df["timestamp"] >= cutoff].copy()
    return live_df.tail(10000)

df = get_data_cached()

# -- KPIs
total = len(df)
blocked_count = len(df[df["status"] == "BLOCKED"])
loss_saved = int(df[df["status"] == "BLOCKED"]["amount"].sum())
detection_rate = round((blocked_count / total) * 100, 2) if total > 0 else 0

prev_blocked = st.session_state.get("prev_blocked", blocked_count)
prev_loss = st.session_state.get("prev_loss", loss_saved)
# store current for next cycle
st.session_state.prev_blocked = blocked_count
st.session_state.prev_loss = loss_saved

c1, c2, c3, c4 = st.columns(4)
with c1:
    st.markdown(f'<div class="card"><div class="kpi">{total:,}</div><div class="kpi-small">إجمالي المعاملات</div></div>', unsafe_allow_html=True)
with c2:
    st.metric("🚫 تم الحظر", f"{blocked_count:,}", f"{blocked_count - prev_blocked:+}")
with c3:
    st.metric("💰 خسائر مُجنَّبة", f"{loss_saved:,} EGP", f"{loss_saved - prev_loss:+}")
with c4:
    # for display of detection delta vs baseline (example baseline 92.1)
    baseline = 92.1
    st.metric("🎯 معدل الكشف", f"{detection_rate}%", f"{detection_rate - baseline:+.1f}pp")

st.markdown("---")

left, right = st.columns([2, 1])

with left:
    # Map
    st.subheader("📍 توزيع الاحتيال في مصر (آخر 24 ساعة)")
    egypt_coords = {
        "القاهرة": [30.0444,31.2357], "الجيزة":[30.0131,31.2089], "الإسكندرية":[31.2001,29.9187],
        "الدقهلية":[31.0467,31.3785], "الشرقية":[30.5972,31.5021], "القليوبية":[30.3292,31.2089],
        "البحيرة":[31.0333,30.4667], "المنوفية":[30.5972,30.9876], "أسيوط":[27.1810,31.1837], "سوهاج":[26.5591,31.6957]
    }
    map_df = df[df["status"]=="BLOCKED"].groupby("city").size().reset_index(name="count")
    if not map_df.empty:
        map_df["lat"] = map_df["city"].map({k: v[0] for k, v in egypt_coords.items()})
        map_df["lon"] = map_df["city"].map({k: v[1] for k, v in egypt_coords.items()})
        # drop rows with missing coords
        map_df = map_df.dropna(subset=["lat","lon"])
        if map_df.empty:
            st.info("لا توجد معاملات محظورة بها إحداثيات قابلة للعرض على الخريطة الآن.")
        else:
            fig_map = px.scatter_mapbox(
                map_df, lat="lat", lon="lon", size="count", color="count",
                size_max=50, zoom=5.3, color_continuous_scale="OrRd",
                mapbox_style="carto-positron", hover_name="city", template="plotly_dark"
            )
            fig_map.update_layout(margin=dict(l=0,r=0,t=0,b=0), height=480)
            st.plotly_chart(fig_map, use_container_width=True)
    else:
        st.info("لا توجد حالات BLOCKED لعرضها على الخريطة حالياً.")

    # Trend
    trend = df.copy()
    if not trend.empty:
        trend["hour"] = trend["timestamp"].dt.floor("H")
        hourly = trend.groupby("hour").size().reset_index(name="count")
        fig_trend = px.area(hourly, x="hour", y="count", template="plotly_dark")
        fig_trend.update_layout(title="محاولات الاحتيال بالساعة", xaxis_title="", yaxis_title="عدد المعاملات", height=300)
        st.plotly_chart(fig_trend, use_container_width=True)
    else:
        st.info("لا توجد بيانات للاتجاه الزمني الآن.")

    # Network Graph
    st.markdown("### 🌐 شبكات الاحتيال المكتشفة")
    high_risk_df = df[df["risk_score"] >= 850]
    if not high_risk_df.empty:
        high_risk = high_risk_df.sample(min(50, len(high_risk_df)), random_state=42)
        G = nx.Graph()
        for _, row in high_risk.iterrows():
            G.add_edge(row["account_id"], row["merchant"], weight=row["risk_score"])
        try:
            pos = nx.spring_layout(G, k=1, iterations=50, seed=42)
            edge_traces = []
            for edge in G.edges():
                x0, y0 = pos[edge[0]]
                x1, y1 = pos[edge[1]]
                edge_traces.append(go.Scatter(x=[x0,x1,None], y=[y0,y1,None], mode="lines", line=dict(color="#888", width=1), hoverinfo="none"))
            node_x, node_y, node_text, node_color = [], [], [], []
            for node in G.nodes():
                x, y = pos[node]
                node_x.append(x); node_y.append(y); node_text.append(node)
                node_color.append("#34d399" if str(node).startswith("AC") else "#fb7185")
            node_trace = go.Scatter(x=node_x, y=node_y, mode="markers+text", marker=dict(size=16, color=node_color),
                                    text=node_text, textposition="top center", hoverinfo="text")
            fig_net = go.Figure(data=edge_traces + [node_trace])
            fig_net.update_layout(template="plotly_dark", showlegend=False, height=420, margin=dict(l=0,r=0,t=20,b=0))
            st.plotly_chart(fig_net, use_container_width=True)
        except Exception as e:
            st.error(f"حدث خطأ أثناء رسم شبكة الاحتيال: {e}")
    else:
        st.info("لا توجد معاملات عالية الخطورة كافية لرسم شبكة الآن.")

with right:
    st.subheader("🔥 أخطر 10 معاملات الآن")
    if not df.empty:
        top10 = df.nlargest(10, "risk_score")[["transaction_id","amount","merchant","city","risk_score","fraud_type","status"]].copy()
        top10["amount"] = top10["amount"].astype(int)
        # Use st.write to render styled dataframe (Streamlit supports Styler via st.write)
        st.write(top10.style.background_gradient(subset=["risk_score"], cmap="Reds"))
    else:
        st.info("لا توجد بيانات لعرضها في قائمة الأخطر الآن.")

    st.subheader("🏷️ التجار الأكثر استهدافاً")
    if not df.empty:
        merch = df.groupby("merchant").agg({"transaction_id":"count","amount":"sum","risk_score":"mean"}).round(0)
        merch = merch.rename(columns={"transaction_id":"عدد المعاملات","amount":"إجمالي المبالغ"}).sort_values("risk_score", ascending=False)
        fig_merch = px.bar(merch.head(8), y=merch.head(8).index, x="عدد المعاملات", color="risk_score",
                           color_continuous_scale="Reds", orientation="h", template="plotly_dark")
        st.plotly_chart(fig_merch, use_container_width=True)
    else:
        st.info("لا توجد بيانات للتجار الآن.")

    st.subheader("📊 توزيع درجات الخطر")
    if not df.empty:
        fig_hist = px.histogram(df, x="risk_score", nbins=25, template="plotly_dark")
        st.plotly_chart(fig_hist, use_container_width=True)
    else:
        st.info("لا توجد بيانات لعرض التوزيع الآن.")

# Filters
st.markdown("---")
st.subheader("🔎 فلترة وتحليل متقدم")
f1, f2, f3, f4 = st.columns(4)
with f1:
    city_f = st.selectbox("المحافظة", ["الكل"] + sorted(df["city"].dropna().unique()))
with f2:
    merch_f = st.selectbox("التاجر", ["الكل"] + sorted(df["merchant"].dropna().unique()))
with f3:
    status_f = st.selectbox("الحالة", ["الكل","BLOCKED","REVIEW","APPROVED"])
with f4:
    score_f = st.slider("الحد الأدنى لدرجة الخطر", 500, 1000, 700)

filtered = df.copy()
if city_f != "الكل" and city_f:
    filtered = filtered[filtered["city"] == city_f]
if merch_f != "الكل" and merch_f:
    filtered = filtered[filtered["merchant"] == merch_f]
if status_f != "الكل":
    filtered = filtered[filtered["status"] == status_f]
filtered = filtered[filtered["risk_score"] >= score_f]

st.markdown(f"**عرض {len(filtered):,} معاملة مُفلترة** • آخر تحديث: {datetime.now().strftime('%H:%M:%S')}")
if not filtered.empty:
    st.dataframe(filtered.sort_values("timestamp", ascending=False).head(300), use_container_width=True, height=500)
else:
    st.info("لا توجد معاملات بعد تطبيق الفلاتر.")

# Footer
st.markdown("""
<div style="text-align:center; margin-top:50px; padding:20px; color:#64748b; font-size:14px;">
    <strong style="color:#34d399; font-size:18px;">Aman Payment Security © 2025</strong><br>
    Enterprise Fraud Shield • بنك مصر - فوري - فودافون كاش - البنك الأهلي
</div>
""", unsafe_allow_html=True)
