import streamlit as st
import yfinance as yf
import pandas as pd


st.set_page_config(
    page_title="PCSchool｜股價行情",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded",
)


st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Noto+Sans+TC:wght@400;500;700;900&display=swap');

    :root {
        --ink: #17212b;
        --muted: #6f7c87;
        --line: #dfe5e8;
        --paper: #f5f7f8;
        --panel: #ffffff;
        --teal: #087f8c;
        --teal-soft: #e4f4f3;
        --red: #c75a5a;
    }
    html, body, [class*="css"] { font-family: 'DM Sans', 'Noto Sans TC', sans-serif; }
    .stApp { background: var(--paper); color: var(--ink); }
    [data-testid="stHeader"] { background: rgba(245, 247, 248, .88); }
    [data-testid="stSidebar"] { background: #17212b; border-right: 0; }
    [data-testid="stSidebar"] * { color: #eef5f5; }
    [data-testid="stSidebar"] hr { border-color: rgba(255,255,255,.14); }
    .block-container { max-width: 1440px; padding: 2.5rem 4rem 4rem; }
    .brand { letter-spacing: .16em; font-size: .72rem; font-weight: 700; color: #7ed7d1; }
    .sidebar-note { color: #a9bbc0; font-size: .77rem; line-height: 1.7; }
    .eyebrow { color: var(--teal); letter-spacing: .12em; font-size: .74rem; font-weight: 700; text-transform: uppercase; }
    h1 { font-size: clamp(2rem, 3.3vw, 3.25rem) !important; letter-spacing: -.04em; line-height: 1.1 !important; margin: .35rem 0 .75rem !important; }
    .lede { color: var(--muted); font-size: 1rem; line-height: 1.8; max-width: 650px; }
    .hero { border-bottom: 1px solid var(--line); padding: .6rem 0 2.2rem; margin-bottom: 1.5rem; }
    .hero-tag { display: inline-block; background: var(--teal-soft); color: var(--teal); padding: .35rem .6rem; border-radius: 4px; font-size: .75rem; font-weight: 700; }
    .section-label { border-left: 3px solid var(--teal); padding-left: .7rem; margin: 2.2rem 0 1rem; }
    .section-label h3 { margin: 0; font-size: 1.05rem; }
    .section-label p { color: var(--muted); margin: .25rem 0 0; font-size: .82rem; }
    .panel { background: var(--panel); border: 1px solid var(--line); border-radius: 6px; padding: 1.2rem 1.3rem; }
    .panel-title { font-size: .92rem; font-weight: 700; margin-bottom: .8rem; }
    .ticker { display: flex; align-items: baseline; gap: .65rem; }
    .ticker strong { font-size: 1.9rem; letter-spacing: -.04em; }
    .ticker span { color: var(--teal); font-size: .9rem; font-weight: 700; }
    .ticker span.down { color: var(--red); }
    .metric-card { background: var(--panel); border: 1px solid var(--line); border-radius: 6px; padding: 1rem 1.15rem; min-height: 100px; }
    .metric-title { color: var(--muted); font-size: .78rem; }
    .metric-value { color: var(--ink); font-size: 1.45rem; font-weight: 700; margin: .35rem 0; }
    .metric-delta { color: var(--teal); font-size: .78rem; font-weight: 700; }
    .metric-delta.down { color: var(--red); }
    .footnote { color: var(--muted); font-size: .74rem; margin-top: 1.2rem; }
    @media (max-width: 900px) { .block-container { padding: 1.5rem 1.15rem 3rem; } }
    </style>
    """,
    unsafe_allow_html=True,
)

with st.sidebar:    
    st.markdown('<div class="brand">EQUITYLENS</div>', unsafe_allow_html=True)
    st.markdown("## 股票分析工作台")
    st.markdown('<p class="sidebar-note">以價格與交易資料建立清晰的市場觀察。</p>', unsafe_allow_html=True)
    st.divider()
    st.markdown("**股價行情**")
    selected_ticker = st.selectbox(
        "選擇股票代號",
        ["2330.TW", "2317.TW", "2454.TW"],
        index=None,
        placeholder="選擇一檔股票",
    )
    period = st.selectbox("資料期間", ["1mo", "3mo", "6mo", "1y"], index=0)
    st.divider()
    st.caption("資料來源")
    st.markdown("🟢 Yahoo Finance")


st.markdown(
    '<div class="hero"><span class="hero-tag">Market Data</span><div class="eyebrow" style="margin-top:1.3rem">Price intelligence</div><h1>股價行情<br><span style="color:#087f8c">看見價格的脈絡。</span></h1><p class="lede">快速檢視標的的歷史價格、交易量與報酬表現，將短期波動放回更完整的趨勢中理解。</p></div>',
    unsafe_allow_html=True,
)

st.markdown('<div class="section-label"><h3>標的查詢</h3><p>選擇股票後載入最新市場資料</p></div>', unsafe_allow_html=True)

if selected_ticker is None:
    st.info("請從左側選擇股票代號，開始查看股價資料。")
else:
    ticker = yf.Ticker(selected_ticker)
    try:
        data = ticker.history(period=period)
    except Exception as error:
        st.error(f"暫時無法取得 {selected_ticker} 的行情資料：{error}")
        st.stop()

    if data.empty:
        st.warning("目前沒有可顯示的行情資料，請稍後再試。")
        st.stop()

    latest_close = float(data["Close"].iloc[-1])
    previous_close = float(data["Close"].iloc[-2]) if len(data) > 1 else latest_close
    change = latest_close - previous_close
    change_pct = (change / previous_close * 100) if previous_close else 0
    total_return = (latest_close / float(data["Close"].iloc[0]) - 1) * 100
    average_volume = int(data["Volume"].mean())
    high_price = float(data["High"].max())
    change_class = "down" if change < 0 else ""
    change_symbol = "▼" if change < 0 else "▲"

    st.markdown('<div class="section-label"><h3>行情摘要</h3><p>最新交易日與期間表現</p></div>', unsafe_allow_html=True)
    st.markdown(
        f'<div class="panel"><div class="panel-title">{selected_ticker}｜最新收盤價</div><div class="ticker"><strong>{latest_close:,.2f}</strong><span class="{change_class}">{change_symbol} {abs(change_pct):.2f}%</span></div></div>',
        unsafe_allow_html=True,
    )
    metric_columns = st.columns(4)
    metrics = [
        ("期間報酬", f"{total_return:+.2f}%", "依所選期間計算", "down" if total_return < 0 else ""),
        ("期間最高", f"{high_price:,.2f}", "最高收盤區間", ""),
        ("平均成交量", f"{average_volume:,}", "股／交易日", ""),
        ("資料筆數", f"{len(data)}", "個交易日", ""),
    ]
    for column, (title, value, delta, style_class) in zip(metric_columns, metrics):
        with column:
            st.markdown(f'<div class="metric-card"><div class="metric-title">{title}</div><div class="metric-value">{value}</div><div class="metric-delta {style_class}">{delta}</div></div>', unsafe_allow_html=True)

    st.markdown('<div class="section-label"><h3>價格趨勢</h3><p>收盤價與成交量的歷史變化</p></div>', unsafe_allow_html=True)
    chart_column, volume_column = st.columns([1.7, 1], gap="large")
    with chart_column:
        chart_data = data[["Close"]].rename(columns={"Close": "收盤價"})
        st.markdown('<div class="panel"><div class="panel-title">收盤價走勢</div></div>', unsafe_allow_html=True)
        st.line_chart(chart_data, color="#087f8c", height=300)
    with volume_column:
        volume_data = data[["Volume"]].rename(columns={"Volume": "成交量"})
        st.markdown('<div class="panel"><div class="panel-title">成交量</div></div>', unsafe_allow_html=True)
        st.bar_chart(volume_data, color="#8bc9c6", height=300)

    st.markdown('<div class="section-label"><h3>歷史行情</h3><p>可展開檢視原始交易資料</p></div>', unsafe_allow_html=True)
    display_data = data.copy()
    display_data.index = pd.to_datetime(display_data.index).strftime("%Y-%m-%d")
    st.dataframe(display_data, use_container_width=True, height=360)
    st.markdown('<p class="footnote">資料來源：Yahoo Finance。行情資料僅供研究參考，非投資建議。</p>', unsafe_allow_html=True)
