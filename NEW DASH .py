# app.p
# Aman Payment Security – Live Fraud Shield 2025 (Enhanced)
# استيراد المكتبات
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import networkx as nx
from datetime import datetime, timedelta
import random, time, pyperclip, base64

# ─────────── إعدادات الصفحة ───────────
st.set_page_config(
    page_title="Aman Payment Security",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─────────── دالة تحميل CSS ديناميكي ───────────
def load_css(style="dark"):
    css_light = """
    <style>
        body {background:#ffffff; color:#111827;}
        .main {background:#ffffff;}
        .card {background:#f3f4f6; border:1px solid #d1d5db;}
        .kpi {color:#111827;}
        .alert-banner {background:#fef2f2; color:#b91c1c; border-left:6px solid #ef4444;}
    </style>
    """
    css_dark = """
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
        /* إخفاء شريط menu وmade with streamlit */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
    </style>
    """
    if style == "light":
        st.markdown(css_light, unsafe_allow_html=True)
    else:
        st.markdown(css_dark, unsafe_allow_html=True)

# ─────────── Sidebar ───────────
with st.sidebar:
    st.title("⚙️ إعدادات العرض")
    theme = st.radio("الثيم", ["داكن", "فاتح"], horizontal=True, index=0)
    load_css("dark" if theme == "داكن" else "light")
    auto_refresh = st.checkbox("🔄 تحديث تلقائي كل 60 ثانية", value=True)
    sound_alert = st.checkbox("🔊 تنبيه صوتي عند هجوم جديد", value=False)
    if st.button("🗑️ مسح الكاش"):
        st.cache_data.clear()
        st.toast("✅ تم مسح الكاش", icon="🗑️")

# ─────────── مولّد البيانات (cached) ───────────
@st.cache_data(ttl=60, show_spinner="⏳ جاري تحديث البيانات الحية...")
def get_data():
    now = datetime.now()
    new_txs = random.randint(15, 45)
    cities = ["القاهرة","الجيزة","الإسكندرية","الدقهلية","الشرقية","القليوبية","البحيرة","المنوفية","أسيوط","سوهاج"]
    merchants = ["Amazon","Noon","Talabat","Uber","Careem","Vodafone Cash","Fawry","InstaPay","Booking.com","Souq"]
    types = ["Card Testing","Account Takeover","Friendly Fraud","Bot Attack","Merchant Compromise"]
    rows = []
    for _ in range(new_txs):
        rows.append({
            "transaction_id": f"TX{random.randint(1e6,9e6):,.0f}",
            "account_id": f"AC{random.randint(2e4,9e5):,.0f}",
            "merchant": random.choice(merchants),
            "city": random.choice(cities),
            "amount": random.randint(80, 28000),
            "risk_score": random.choices([random.randint(500,750), random.randint(820,1000)], [.68, .32])[0],
            "fraud_type": random.choices(types, [.28,.18,.22,.20,.12])[0],
            "status": random.choices(["BLOCKED","REVIEW","APPROVED"], [.24,.26,.50])[0],
            "timestamp": now - timedelta(seconds=random.randint(0, 1800))
        })
    return pd.DataFrame(rows)

# ─────────── الهيكل العلوي ───────────
df = get_data()
total = len(df)
blocked_count = len(df[df["status"] == "BLOCKED"])
loss_saved = df[df["status"] == "BLOCKED"]["amount"].sum()
detection_rate = (blocked_count / total * 100) if total else 0.0

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

# ─────────── شريط تنبيه متحرك ───────────
alerts = [
    "🚨 هجوم Card Testing عالي السرعة على فودافون كاش (٨٧ محاولة/دقيقة)",
    "⚡ تم اكتشاف وإيقاف تكتل Account Takeover من الإسكندرية (١٢ حساب)",
    "✅ تم تفعيل نموذج الذكاء الاصطناعي الجديد v4.2 – دقة +٦.٢٪",
    "🔥 ارتفاع ملحوظ في Friendly Fraud على Noon (+٢١٠٪ عن الأساس)",
    "🛑 تم حظر شبكة بوتات من القليوبية (٢٨ عنوان IP)"
]
alert = alerts[int(time.time() / 25) % len(alerts)]
st.markdown(f'<div class="alert-banner">🚨 تنبيه فوري • {alert}</div>', unsafe_allow_html=True)

# ─────────── KPIs ───────────
c1, c2, c3, c4 = st.columns(4)
with c1:
    st.markdown(f'<div class="card"><div class="kpi">{total:,}</div><div class="kpi-small">إجمالي المعاملات</div></div>', unsafe_allow_html=True)
with c2:
    delta_blocked = blocked_count - st.session_state.get("prev_blocked", blocked_count)
    st.metric("🚫 تم الحظر", f"{blocked_count:,}", f"{delta_blocked:+}", delta_color="inverse")
with c3:
    delta_loss = int(loss_saved - st.session_state.get("prev_loss", loss_saved))
    st.metric("💰 خسائر مُجنَّبة", f"{int(loss_saved):,} EGP", f"{delta_loss:+}", delta_color="normal")
with c4:
    st.metric("🎯 معدل الكشف", f"{detection_rate:.1f}%", f"{detection_rate-92.1:+.1f}pp")
st.session_state.prev_blocked = blocked_count
st.session_state.prev_loss = loss_saved

st.markdown("---")

# ─────────── التخطيطات الرئيسية ───────────
left, right = st.columns([2, 1])

with left:
    # خريطة مصر
    st.subheader("📍 توزيع الاحتيال في مصر (آخر 24 ساعة)")
    egypt = {"القاهرة":[30.0444,31.2357],"الجيزة":[30.0131,31.2089],"الإسكندرية":[31.2001,29.9187],
             "الدقهلية":[31.0467,31.3785],"الشرقية":[30.5972,31.5021],"القليوبية":[30.3292,31.2089],
             "البحيرة":[31.0333,30.4667],"المنوفية":[30.5972,30.9876],"أسيوط":[27.1810,31.1837],"سوهاج":[26.5591,31.6957]}
    map_df = df[df["status"]=="BLOCKED"].groupby("city").size().reset_index(name="count")
    map_df["lat"] = map_df["city"].map({k:v[0] for k,v in egypt.items()})
    map_df["lon"] = map_df["city"].map({k:v[1] for k,v in egypt.items()})
    fig_map = px.scatter_mapbox(map_df, lat="lat", lon="lon", size="count", color="count",
                                size_max=50, zoom=5.3, color_continuous_scale="OrRd",
                                mapbox_style="carto-positron", hover_name="city", template="plotly_dark")
    fig_map.update_layout(margin=dict(l=0,r=0,t=0,b=0), height=480)
    st.plotly_chart(fig_map, use_container_width=True)

    # الاتجاه الزمني
    trend = df.copy()
    trend["hour"] = trend["timestamp"].dt.floor("H")
    hourly = trend.groupby("hour").size().reset_index(name="count")
    fig_trend = px.area(hourly, x="hour", y="count", template="plotly_dark", color_discrete_sequence=["#f87171"],
                        animation_frame="hour", animation_group="count", range_y=[0, hourly["count"].max()*1.1])
    fig_trend.update_layout(title="محاولات الاحتيال بالساعة", xaxis_title="", yaxis_title="عدد المعاملات", height=300)
    st.plotly_chart(fig_trend, use_container_width=True)

with right:
    # أخطر 10 معاملات
    st.subheader("🔥 أخطر 10 معاملات الآن")
    top10 = df.nlargest(10, "risk_score")[["transaction_id","amount","merchant","city","risk_score","fraud_type","status"]]
    top10["amount"] = top10["amount"].astype(int)
    st.dataframe(top10.style.background_gradient(subset=["risk_score"], cmap="Reds"), use_container_width=True, height=380)

    # التجار الأكثر استهدافاً
    st.subheader("🏷️ التجار الأكثر استهدافاً")
    merch = df.groupby("merchant").agg({"transaction_id":"count","amount":"sum","risk_score":"mean"}).round(0)
    merch = merch.rename(columns={"transaction_id":"عدد المعاملات","amount":"إجمالي المبالغ"}).sort_values("risk_score", ascending=False)
    fig_merch = px.bar(merch.head(8), y=merch.head(8).index, x="عدد المعاملات", color="risk_score",
                       color_continuous_scale="Reds", orientation="h", template="plotly_dark")
    st.plotly_chart(fig_merch, use_container_width=True)

# ─────────── فلترة متقدمة + تصدير ───────────
st.markdown("---")
st.subheader("🔎 فلترة وتحليل متقدم")
f1, f2, f3, f4 = st.columns(4)
with f1: city_f = st.selectbox("المحافظة", ["الكل"] + sorted(df["city"].unique()))
with f2: merch_f = st.selectbox("التاجر", ["الكل"] + sorted(df["merchant"].unique()))
with f3: status_f = st.selectbox("الحالة", ["الكل","BLOCKED","REVIEW","APPROVED"])
with f4: score_f = st.slider("الحد الأدنى لدرجة الخطر", 500, 1000, 700)

filtered = df.copy()
if city_f != "الكل": filtered = filtered[filtered["city"] == city_f]
if merch_f != "الكل": filtered = filtered[filtered["merchant"] == merch_f]
if status_f != "الكل": filtered = filtered[filtered["status"] == status_f]
filtered = filtered[filtered["risk_score"] >= score_f]

st.markdown(f"**عرض {len(filtered):,} معاملة مُفلترة** • آخر تحديث: {datetime.now().strftime('%H:%M:%S')}")

# زر تصدير CSV
csv = filtered.to_csv(index=False)
b64 = base64.b64encode(csv.encode()).decode()
href = f'<a href="data:file/csv;base64,{b64}" download="aman_filtered.csv">📥 تصدير CSV</a>'
st.markdown(href, unsafe_allow_html=True)

st.dataframe(filtered.sort_values("timestamp", ascending=False).head(300), use_container_width=True, height=500)

# ─────────── تذييل ───────────
st.markdown("""
