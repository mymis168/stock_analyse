import streamlit as st
import pandas as pd


st.set_page_config(
	page_title="PCSchool｜股票分析工作台",
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
		--amber: #c47d18;
		--red: #c75a5a;
	}

	html, body, [class*="css"] { font-family: 'DM Sans', 'Noto Sans TC', sans-serif; }
	.stApp { background: var(--paper); color: var(--ink); }
	[data-testid="stHeader"] { background: rgba(245, 247, 248, 0.88); }
	[data-testid="stSidebar"] { background: #17212b; border-right: 0; }
	[data-testid="stSidebar"] * { color: #eef5f5; }
	[data-testid="stSidebar"] .stRadio label { padding: 0.45rem 0.5rem; border-radius: 6px; }
	[data-testid="stSidebar"] .stRadio label:hover { background: rgba(255,255,255,.08); }
	[data-testid="stSidebar"] hr { border-color: rgba(255,255,255,.14); }
	.block-container { max-width: 1440px; padding: 2.5rem 4rem 4rem; }
	.brand { letter-spacing: .016em; font-size: .62rem; font-weight: 700; color: #7ed7d1; }
	.sidebar-note { color: #a9bbc0; font-size: .77rem; line-height: 1.7; }
	.eyebrow { color: var(--teal); letter-spacing: .12em; font-size: .74rem; font-weight: 700; text-transform: uppercase; }
	h1 { font-size: clamp(2rem, 3.3vw, 3.25rem) !important; letter-spacing: -.04em; line-height: 1.1 !important; margin: .35rem 0 .75rem !important; }
	h2 { letter-spacing: -.025em; }
	.lede { color: var(--muted); font-size: 1rem; line-height: 1.8; max-width: 620px; }
	.hero { border-bottom: 1px solid var(--line); padding: .6rem 0 2.2rem; margin-bottom: 1.5rem; }
	.hero-tag { display: inline-block; background: var(--teal-soft); color: var(--teal); padding: .35rem .6rem; border-radius: 4px; font-size: .75rem; font-weight: 700; }
	.section-label { border-left: 3px solid var(--teal); padding-left: .7rem; margin: 2.2rem 0 1rem; }
	.section-label h3 { margin: 0; font-size: 1.05rem; }
	.section-label p { color: var(--muted); margin: .25rem 0 0; font-size: .82rem; }
	.metric-card { background: var(--panel); border: 1px solid var(--line); border-radius: 6px; padding: 1rem 1.15rem; min-height: 105px; }
	.metric-title { color: var(--muted); font-size: .78rem; }
	.metric-value { color: var(--ink); font-size: 1.55rem; font-weight: 700; margin: .35rem 0; }
	.metric-delta { color: var(--teal); font-size: .78rem; font-weight: 700; }
	.metric-delta.down { color: var(--red); }
	.panel { background: var(--panel); border: 1px solid var(--line); border-radius: 6px; padding: 1.2rem 1.3rem; }
	.panel-title { font-size: .92rem; font-weight: 700; margin-bottom: .8rem; }
	.ticker { display: flex; align-items: baseline; gap: .65rem; }
	.ticker strong { font-size: 1.9rem; letter-spacing: -.04em; }
	.ticker span { color: var(--teal); font-size: .9rem; font-weight: 700; }
	.signal { display: flex; justify-content: space-between; padding: .7rem 0; border-bottom: 1px solid var(--line); font-size: .85rem; }
	.signal:last-child { border-bottom: 0; }
	.signal b { color: var(--teal); }
	.footnote { color: var(--muted); font-size: .74rem; margin-top: 1.2rem; }
	@media (max-width: 900px) { .block-container { padding: 1.5rem 1.15rem 3rem; } }
	</style>
	""",
	unsafe_allow_html=True,
)


with st.sidebar:
	st.markdown('<div class="brand">巨匠職訓專班</div>', unsafe_allow_html=True)
	st.markdown("## 股票分析工作台")
	st.markdown('<p class="sidebar-note">以數據整理投資決策，快速掌握市場、企業與持股的關鍵脈絡。</p>', unsafe_allow_html=True)
	st.divider()
	st.markdown("**分析模組**")
	st.radio("分析模組", ["總覽 Dashboard", "股價行情", "公司基本面", "持股分析", "公司盈餘"], label_visibility="collapsed")
	st.divider()
	st.caption("資料狀態")
	st.markdown("🟢 研究資料庫已更新")
	st.caption("最後同步：2026 / 09 / 03  16:00")


st.markdown(
	'<div class="hero"><span class="hero-tag">投資研究工具</span><div class="eyebrow" style="margin-top:1.3rem">Research, refined</div><h1>把市場雜訊，整理成<br><span style="color:#087f8c">可讀的投資洞察。</span></h1><p class="lede">EquityLens 是一套專為投資研究設計的股分析軟體，整合股價、公司基本面、持股結構與公司盈餘，讓你從市場表現一路看到企業價值。</p></div>',
	unsafe_allow_html=True,
)


st.markdown('<div class="section-label"><h3>市場快照</h3><p>今日市場核心指標與研究範圍</p></div>', unsafe_allow_html=True)
metric_columns = st.columns(4)
metrics = [
	("追蹤標的", "1,284", "涵蓋台股與美股"),
	("市場情緒", "偏多", "較昨日 +6.4%"),
	("研究清單", "18", "3 項今日更新"),
	("資料完整度", "98.7%", "即時同步中"),
]
for column, (title, value, delta) in zip(metric_columns, metrics):
	with column:
		st.markdown(f'<div class="metric-card"><div class="metric-title">{title}</div><div class="metric-value">{value}</div><div class="metric-delta">{delta}</div></div>', unsafe_allow_html=True)


st.markdown('<div class="section-label"><h3>研究總覽</h3><p>從價格趨勢到企業體質，一頁掌握重要訊號</p></div>', unsafe_allow_html=True)
chart_column, insight_column = st.columns([1.65, 1], gap="large")
with chart_column:
	st.markdown('<div class="panel"><div class="panel-title">市場基準指數｜近 12 個月</div><div class="ticker"><strong>22,418.67</strong><span>▲ 1.24%</span></div></div>', unsafe_allow_html=True)
	chart_data = pd.DataFrame(
		{"台股加權指數": [18420, 18860, 19120, 18980, 19640, 20180, 19940, 20760, 21120, 21580, 21870, 22418]},
		index=["09月", "10月", "11月", "12月", "01月", "02月", "03月", "04月", "05月", "06月", "07月", "08月"],
	)
	st.line_chart(chart_data, color="#087f8c", height=290)

with insight_column:
	st.markdown('<div class="panel"><div class="panel-title">今日研究訊號</div><div class="signal"><span>大型股動能</span><b>強勢</b></div><div class="signal"><span>獲利預期修正</span><b>正向</b></div><div class="signal"><span>法人持股變化</span><b>淨流入</b></div><div class="signal"><span>估值分位</span><b>中性</b></div><div class="signal"><span>波動風險</span><b style="color:#c47d18">可控</b></div></div>', unsafe_allow_html=True)
	st.markdown('<p class="footnote">訊號由價格、財務與籌碼資料綜合計算，僅供研究參考。</p>', unsafe_allow_html=True)


st.markdown('<div class="section-label"><h3>核心分析模組</h3><p>四個面向，建立完整的公司研究視角</p></div>', unsafe_allow_html=True)
module_columns = st.columns(4, gap="medium")
modules = [
	("01", "股價行情", "掌握即時價格、報酬率與趨勢強弱，辨識市場正在交易的故事。", "價格 · 趨勢 · 風險"),
	("02", "公司基本面", "從營收、毛利率到資產負債，快速建立企業經營體質的全貌。", "財務 · 競爭力 · 估值"),
	("03", "持股分析", "拆解機構與主要股東動向，理解籌碼集中度與資金流向。", "法人 · 股東 · 籌碼"),
	("04", "公司盈餘", "追蹤季度盈餘、預期差與成長品質，找出獲利加速或轉折。", "盈餘 · 預期 · 成長"),
]
for column, (number, title, description, tags) in zip(module_columns, modules):
	with column:
		st.markdown(f'<div class="panel" style="min-height:205px"><div class="eyebrow">{number}</div><h3 style="margin:.55rem 0 .7rem">{title}</h3><p style="color:#6f7c87;font-size:.83rem;line-height:1.7;min-height:82px">{description}</p><div style="color:#087f8c;font-size:.72rem;font-weight:700">{tags}</div></div>', unsafe_allow_html=True)


st.markdown('<div class="section-label"><h3>工作方式</h3><p>為研究者保留清晰、可追溯的判斷路徑</p></div>', unsafe_allow_html=True)
workflow_columns = st.columns(3)
for column, title, text in zip(
	workflow_columns,
	["搜尋標的", "交叉驗證", "形成觀點"],
	["輸入股票代號，快速定位關注的公司與市場資料。", "將價格、基本面、持股與盈餘放在同一個脈絡檢視。", "以一致的資料結構整理訊號，支援更有紀律的投資判斷。"],
):
	with column:
		st.markdown(f'<div style="border-top:2px solid #17212b;padding-top:.85rem"><b>{title}</b><p style="color:#6f7c87;font-size:.82rem;line-height:1.65;margin-top:.45rem">{text}</p></div>', unsafe_allow_html=True)

st.markdown('<p class="footnote">EquityLens · 專業投資研究介面 · 本頁展示資料為產品介面示意，非投資建議。</p>', unsafe_allow_html=True)
