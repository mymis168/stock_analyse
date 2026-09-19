import streamlit as st
import yfinance as yf
import pandas as pd


st.set_page_config(
    page_title="PCSchool｜公司基本面",
    page_icon="▣",
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
        --amber: #c47d18;
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
    .lede { color: var(--muted); font-size: 1rem; line-height: 1.8; max-width: 680px; }
    .hero { border-bottom: 1px solid var(--line); padding: .6rem 0 2.2rem; margin-bottom: 1.5rem; }
    .hero-tag { display: inline-block; background: var(--teal-soft); color: var(--teal); padding: .35rem .6rem; border-radius: 4px; font-size: .75rem; font-weight: 700; }
    .section-label { border-left: 3px solid var(--teal); padding-left: .7rem; margin: 2.2rem 0 1rem; }
    .section-label h3 { margin: 0; font-size: 1.05rem; }
    .section-label p { color: var(--muted); margin: .25rem 0 0; font-size: .82rem; }
    .panel { background: var(--panel); border: 1px solid var(--line); border-radius: 6px; padding: 1.2rem 1.3rem; }
    .panel-title { font-size: .92rem; font-weight: 700; margin-bottom: .8rem; }
    .metric-card { background: var(--panel); border: 1px solid var(--line); border-radius: 6px; padding: 1rem 1.15rem; min-height: 100px; }
    .metric-title { color: var(--muted); font-size: .78rem; }
    .metric-value { color: var(--ink); font-size: 1.45rem; font-weight: 700; margin: .35rem 0; }
    .metric-delta { color: var(--teal); font-size: .78rem; font-weight: 700; }
    .metric-delta.down { color: var(--red); }
    .company-name { font-size: 1.5rem; font-weight: 700; margin-bottom: .3rem; }
    .company-meta { color: var(--muted); font-size: .82rem; }
    .footnote { color: var(--muted); font-size: .74rem; margin-top: 1.2rem; }
    @media (max-width: 900px) { .block-container { padding: 1.5rem 1.15rem 3rem; } }
    </style>
    """,
    unsafe_allow_html=True,
)


def format_value(value, suffix="", decimals=2):
    if value is None or pd.isna(value):
        return "—"
    if isinstance(value, (int, float)):
        return f"{value:,.{decimals}f}{suffix}"
    return str(value)


def statement_value(statement, row_names):
    for row_name in row_names:
        if row_name in statement.index:
            values = statement.loc[row_name].dropna()
            if not values.empty:
                return values.iloc[0]
    return None


with st.sidebar:
    st.markdown('<div class="brand">巨匠電腦專題</div>', unsafe_allow_html=True)
    st.markdown("## 股票分析工作台")
    st.markdown('<p class="sidebar-note">從財務數據理解企業體質與長期競爭力。</p>', unsafe_allow_html=True)
    st.divider()
    st.markdown("**公司基本面**")
    selected_ticker = st.selectbox(
        "選擇股票代號",
        ["0050.TW","0056.TW","2330.TW", "2317.TW","2345.TW","2059.TW","2382.TW","2454.TW","3008.TW","3017.TW","3711.TW","5274.TWO",],
        index=None,
        placeholder="選擇一檔股票",
    )
    st.divider()
    st.caption("資料來源")
    st.markdown("🟢 Yahoo Finance")


st.markdown(
    '<div class="hero"><span class="hero-tag">Fundamental Research</span><div class="eyebrow" style="margin-top:1.3rem">Business quality</div><h1>公司基本面<br><span style="color:#087f8c">看見企業的底氣。</span></h1><p class="lede">以公司概況、估值、獲利能力與財務結構，建立一個可比較、可追蹤的企業研究框架。</p></div>',
    unsafe_allow_html=True,
)

st.markdown('<div class="section-label"><h3>公司查詢</h3><p>選擇股票後載入最新公司基本面資料</p></div>', unsafe_allow_html=True)

if selected_ticker is None:
    st.info("請從左側選擇股票代號，開始查看公司基本面。")
else:
    ticker = yf.Ticker(selected_ticker)
    try:
        info = ticker.info
        income_statement = ticker.income_stmt
        balance_sheet = ticker.balance_sheet
        cash_flow = ticker.cashflow
    except Exception as error:
        st.error(f"暫時無法取得 {selected_ticker} 的公司資料：{error}")
        st.stop()

    if not info:
        st.warning("目前沒有可顯示的公司基本面資料，請稍後再試。")
        st.stop()

    company_name = info.get("longName") or info.get("shortName") or selected_ticker
    industry = info.get("industry") or "產業資料未提供"
    sector = info.get("sector") or "產業分類未提供"
    summary = info.get("longBusinessSummary") or "目前沒有公司營運摘要。"

    st.markdown('<div class="section-label"><h3>公司概況</h3><p>企業識別與市場定位</p></div>', unsafe_allow_html=True)
    overview_column, profile_column = st.columns([1, 1.5], gap="large")
    with overview_column:
        st.markdown(
            f'<div class="panel"><div class="company-name">{company_name}</div><div class="company-meta">{selected_ticker}　·　{sector}</div><div class="company-meta" style="margin-top:.45rem">主要產業：{industry}</div></div>',
            unsafe_allow_html=True,
        )
    with profile_column:
        st.markdown(f'<div class="panel"><div class="panel-title">營運摘要</div><p style="color:#6f7c87;font-size:.84rem;line-height:1.75;margin:0">{summary}</p></div>', unsafe_allow_html=True)

    market_cap = info.get("marketCap")
    market_cap_display = format_value(market_cap / 1e8, " 億", 1) if market_cap else "—"
    metrics = [
        ("市值", market_cap_display, "市場規模"),
        ("本益比", format_value(info.get("trailingPE"), "x"), "歷史本益比"),
        ("股價淨值比", format_value(info.get("priceToBook"), "x"), "估值指標"),
        ("股息殖利率", format_value(info.get("dividendYield"), "%"), "年化殖利率"),
    ]
    metric_columns = st.columns(4)
    for column, (title, value, caption) in zip(metric_columns, metrics):
        with column:
            st.markdown(f'<div class="metric-card"><div class="metric-title">{title}</div><div class="metric-value">{value}</div><div class="metric-delta">{caption}</div></div>', unsafe_allow_html=True)

    st.markdown('<div class="section-label"><h3>獲利能力</h3><p>觀察營收規模與利潤品質</p></div>', unsafe_allow_html=True)
    profit_columns = st.columns(4)
    profit_metrics = [
        ("營收", info.get("totalRevenue"), "元", 1e8),
        ("毛利率", info.get("grossMargins"), "%", 100),
        ("營業利益率", info.get("operatingMargins"), "%", 100),
        ("淨利率", info.get("profitMargins"), "%", 100),
    ]
    for column, (title, value, suffix, multiplier) in zip(profit_columns, profit_metrics):
        with column:
            display = format_value(value / multiplier, suffix, 1) if value is not None else "—"
            st.markdown(f'<div class="metric-card"><div class="metric-title">{title}</div><div class="metric-value">{display}</div><div class="metric-delta">最新資料</div></div>', unsafe_allow_html=True)

    st.markdown('<div class="section-label"><h3>財務健康</h3><p>檢視資本結構與現金流狀況</p></div>', unsafe_allow_html=True)
    balance_columns = st.columns([1, 1], gap="large")
    total_debt = statement_value(balance_sheet, ["Total Debt", "Long Term Debt And Capital Lease Obligation"])
    cash = statement_value(balance_sheet, ["Cash Cash Equivalents And Short Term Investments", "Cash And Cash Equivalents"])
    operating_cash_flow = statement_value(cash_flow, ["Operating Cash Flow", "Total Cash From Operating Activities"])
    free_cash_flow = statement_value(cash_flow, ["Free Cash Flow"])
    with balance_columns[0]:
        st.markdown('<div class="panel"><div class="panel-title">資產負債</div></div>', unsafe_allow_html=True)
        st.dataframe(
            pd.DataFrame({"指標": ["總負債", "現金與短期投資"], "數值": [format_value(total_debt), format_value(cash)]}),
            hide_index=True,
            use_container_width=True,
        )
    with balance_columns[1]:
        st.markdown('<div class="panel"><div class="panel-title">現金流</div></div>', unsafe_allow_html=True)
        st.dataframe(
            pd.DataFrame({"指標": ["營業現金流", "自由現金流"], "數值": [format_value(operating_cash_flow), format_value(free_cash_flow)]}),
            hide_index=True,
            use_container_width=True,
        )

    st.markdown('<div class="section-label"><h3>財務報表</h3><p>展開查看 yfinance 回傳的原始年度資料</p></div>', unsafe_allow_html=True)
    statement_tabs = st.tabs(["損益表", "資產負債表", "現金流量表"])
    statements = [income_statement, balance_sheet, cash_flow]
    for tab, statement in zip(statement_tabs, statements):
        with tab:
            if statement.empty:
                st.info("目前沒有可顯示的報表資料。")
            else:
                st.dataframe(statement, use_container_width=True, height=390)

    st.markdown('<p class="footnote">資料來源：Yahoo Finance。財務資料可能有延遲或缺漏，僅供研究參考，非投資建議。</p>', unsafe_allow_html=True)
