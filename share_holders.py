import streamlit as st
import yfinance as yf
import pandas as pd


st.set_page_config(page_title="PCSchool｜持股分析", page_icon="◈", layout="wide")

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Noto+Sans+TC:wght@400;500;700;900&display=swap');
    :root { --ink:#17212b; --muted:#6f7c87; --line:#dfe5e8; --paper:#f5f7f8; --panel:#fff; --teal:#087f8c; --soft:#e4f4f3; --red:#c75a5a; }
    html, body, [class*="css"] { font-family:'DM Sans','Noto Sans TC',sans-serif; }
    .stApp { background:var(--paper); color:var(--ink); }
    [data-testid="stHeader"] { background:rgba(245,247,248,.88); }
    [data-testid="stSidebar"] { background:#17212b; border-right:0; }
    [data-testid="stSidebar"] * { color:#eef5f5; }
    [data-testid="stSidebar"] hr { border-color:rgba(255,255,255,.14); }
    .block-container { max-width:1440px; padding:2.5rem 4rem 4rem; }
    .brand { letter-spacing:.16em; font-size:.72rem; font-weight:700; color:#7ed7d1; }
    .sidebar-note { color:#a9bbc0; font-size:.77rem; line-height:1.7; }
    .eyebrow { color:var(--teal); letter-spacing:.12em; font-size:.74rem; font-weight:700; text-transform:uppercase; }
    h1 { font-size:clamp(2rem,3.3vw,3.25rem)!important; letter-spacing:-.04em; line-height:1.1!important; margin:.35rem 0 .75rem!important; }
    .lede { color:var(--muted); font-size:1rem; line-height:1.8; max-width:680px; }
    .hero { border-bottom:1px solid var(--line); padding:.6rem 0 2.2rem; margin-bottom:1.5rem; }
    .hero-tag { display:inline-block; background:var(--soft); color:var(--teal); padding:.35rem .6rem; border-radius:4px; font-size:.75rem; font-weight:700; }
    .section-label { border-left:3px solid var(--teal); padding-left:.7rem; margin:2.2rem 0 1rem; }
    .section-label h3 { margin:0; font-size:1.05rem; }
    .section-label p { color:var(--muted); margin:.25rem 0 0; font-size:.82rem; }
    .panel, .metric-card { background:var(--panel); border:1px solid var(--line); border-radius:6px; }
    .panel { padding:1.2rem 1.3rem; }
    .panel-title { font-size:.92rem; font-weight:700; margin-bottom:.8rem; }
    .metric-card { padding:1rem 1.15rem; min-height:100px; }
    .metric-title { color:var(--muted); font-size:.78rem; }
    .metric-value { color:var(--ink); font-size:1.45rem; font-weight:700; margin:.35rem 0; }
    .metric-delta { color:var(--teal); font-size:.78rem; font-weight:700; }
    .metric-delta.down { color:var(--red); }
    .footnote { color:var(--muted); font-size:.74rem; margin-top:1.2rem; }
    @media (max-width:900px) { .block-container { padding:1.5rem 1.15rem 3rem; } }
    </style>
    """,
    unsafe_allow_html=True,
)


def format_percent(value):
    if value is None or pd.isna(value):
        return "—"
    return f"{float(value) * 100:.1f}%"


def format_number(value):
    if value is None or pd.isna(value):
        return "—"
    return f"{float(value):,.0f}"


with st.sidebar:
    st.markdown('<div class="brand">EQUITYLENS</div>', unsafe_allow_html=True)
    st.markdown("## 股票分析工作台")
    st.markdown('<p class="sidebar-note">拆解法人、基金與內部人動向，理解資金的選擇。</p>', unsafe_allow_html=True)
    st.divider()
    st.markdown("**持股分析**")
    selected_ticker = st.selectbox("選擇股票代號", ["2330.TW", "2317.TW", "2454.TW"], index=None, placeholder="選擇一檔股票")
    st.divider()
    st.caption("資料來源")
    st.markdown("🟢 Yahoo Finance")


st.markdown(
    '<div class="hero"><span class="hero-tag">Ownership Research</span><div class="eyebrow" style="margin-top:1.3rem">Capital movement</div><h1>持股分析<br><span style="color:#087f8c">看見資金的方向。</span></h1><p class="lede">從主要股東、機構投資人到內部人交易，整理股權結構與資金動向，補足價格之外的市場訊號。</p></div>',
    unsafe_allow_html=True,
)

st.markdown('<div class="section-label"><h3>標的查詢</h3><p>選擇股票後載入持股結構與股東資料</p></div>', unsafe_allow_html=True)

if selected_ticker is None:
    st.info("請從左側選擇股票代號，開始查看持股資料。")
else:
    ticker = yf.Ticker(selected_ticker)
    try:
        info = ticker.info
        major_holders = ticker.major_holders
        institutional_holders = ticker.institutional_holders
        mutualfund_holders = ticker.mutualfund_holders
        insider_transactions = ticker.insider_transactions
    except Exception as error:
        st.error(f"暫時無法取得 {selected_ticker} 的持股資料：{error}")
        st.stop()

    company_name = info.get("longName") or info.get("shortName") or selected_ticker
    held_by_insiders = info.get("heldPercentInsiders")
    held_by_institutions = info.get("heldPercentInstitutions")
    shares_outstanding = info.get("sharesOutstanding")
    float_shares = info.get("floatShares")

    st.markdown('<div class="section-label"><h3>持股結構</h3><p>股權集中度與市場流通概況</p></div>', unsafe_allow_html=True)
    metric_columns = st.columns(4)
    metrics = [
        ("內部人持股", format_percent(held_by_insiders), "管理層與關係人"),
        ("機構持股", format_percent(held_by_institutions), "法人與基金"),
        ("流通股數", format_number(float_shares), "可交易股數"),
        ("已發行股數", format_number(shares_outstanding), "公司總股本"),
    ]
    for column, (title, value, caption) in zip(metric_columns, metrics):
        with column:
            st.markdown(f'<div class="metric-card"><div class="metric-title">{title}</div><div class="metric-value">{value}</div><div class="metric-delta">{caption}</div></div>', unsafe_allow_html=True)

    structure_column, signal_column = st.columns([1.25, 1], gap="large")
    with structure_column:
        st.markdown('<div class="panel"><div class="panel-title">持股比例視圖</div></div>', unsafe_allow_html=True)
        ownership_data = pd.DataFrame({"持股類別": ["機構持股", "內部人持股"], "比例": [held_by_institutions or 0, held_by_insiders or 0]})
        st.bar_chart(ownership_data.set_index("持股類別"), color="#087f8c", height=250)
    with signal_column:
        st.markdown(f'<div class="panel"><div class="panel-title">{company_name}｜持股觀察</div><p style="color:#6f7c87;font-size:.84rem;line-height:1.75">機構持股與內部人持股可協助判斷籌碼結構，但實際比例會因揭露時間與資料來源而有所落差。</p><div style="border-top:1px solid #dfe5e8;padding-top:.75rem;color:#087f8c;font-size:.8rem;font-weight:700">資料狀態：已取得公開揭露資料</div></div>', unsafe_allow_html=True)

    st.markdown('<div class="section-label"><h3>主要股東與機構持股</h3><p>查看最新揭露的法人與基金持股名單</p></div>', unsafe_allow_html=True)
    holder_tabs = st.tabs(["主要持股摘要", "機構投資人", "共同基金"])
    holder_data = [major_holders, institutional_holders, mutualfund_holders]
    for tab, holders in zip(holder_tabs, holder_data):
        with tab:
            if holders is None or holders.empty:
                st.info("目前沒有可顯示的持股資料。")
            else:
                st.dataframe(holders, use_container_width=True, height=330)

    st.markdown('<div class="section-label"><h3>內部人交易</h3><p>追蹤董事、高階主管與關係人的近期交易揭露</p></div>', unsafe_allow_html=True)
    if insider_transactions is None or insider_transactions.empty:
        st.info("目前沒有可顯示的內部人交易資料。")
    else:
        st.dataframe(insider_transactions, use_container_width=True, height=350)

    st.markdown('<p class="footnote">資料來源：Yahoo Finance。持股揭露可能有時間差，僅供研究參考，非投資建議。</p>', unsafe_allow_html=True)
