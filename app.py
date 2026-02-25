# ================================================================
#   IT HELPDESK ANALYTICS DASHBOARD  — PREMIUM v5.0
#   Author  : tarique14321495
#   Data    : 2,494 records | Arabic Excel | 5 Columns
#   Features: Bilingual AR/EN | Filters | KPIs | 18 Charts
#   Run     : streamlit run app.py
# ================================================================

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import io

# ── PAGE CONFIG ──────────────────────────────────────────────
st.set_page_config(
    page_title="IT Helpdesk Analytics",
    page_icon="🖥️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── PREMIUM CSS ──────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

*, *::before, *::after { font-family: 'Inter', sans-serif !important; box-sizing: border-box; }

/* ── App background ── */
.stApp { background: #050c1a !important; }
.main .block-container { background: #050c1a !important; padding-top: .8rem !important; max-width: 100% !important; }

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg,#040b18 0%,#071328 60%,#040b18 100%) !important;
    border-right: 1px solid rgba(0,212,255,.12) !important;
}
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] span { color: #8ab4d4 !important; font-size: .83rem !important; }
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3  { color: #00d4ff !important; }

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] {
    background: rgba(255,255,255,.03);
    border: 1px solid rgba(0,212,255,.1);
    border-radius: 14px;
    padding: 5px 7px;
    gap: 4px;
}
.stTabs [data-baseweb="tab"] {
    border-radius: 10px;
    padding: 8px 22px;
    font-size: .87rem;
    font-weight: 600;
    color: #5a8aaa !important;
    background: transparent;
    transition: all .25s ease;
    border: none !important;
}
.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg,#0b3080,#0a4a9e) !important;
    color: #00d4ff !important;
    box-shadow: 0 2px 16px rgba(0,120,255,.3), 0 0 0 1px rgba(0,212,255,.2);
}

/* ── KPI Card ── */
.kpi {
    background: linear-gradient(145deg,#081628,#0d2040);
    border: 1px solid rgba(0,212,255,.12);
    border-top: 3px solid #00d4ff;
    border-radius: 18px;
    padding: 20px 10px 16px;
    text-align: center;
    box-shadow: 0 8px 32px rgba(0,0,0,.5);
    transition: transform .25s ease, box-shadow .25s ease;
    margin-bottom: 10px;
    position: relative;
    overflow: hidden;
}
.kpi::after {
    content: '';
    position: absolute;
    top: -40px; right: -40px;
    width: 100px; height: 100px;
    background: radial-gradient(circle, rgba(0,212,255,.07), transparent 70%);
    border-radius: 50%;
}
.kpi:hover { transform: translateY(-4px); box-shadow: 0 12px 40px rgba(0,80,200,.35); }
.kpi-icon  { font-size: 1.5rem; margin-bottom: 6px; display: block; }
.kpi-num   { font-size: 2rem; font-weight: 800; color: #00d4ff; line-height: 1; display: block; }
.kpi-lbl   { font-size: .7rem; color: #5a8aaa; margin-top: 5px; display: block;
             letter-spacing: 1px; text-transform: uppercase; font-weight: 600; }

/* ── Section header ── */
.sec {
    display: flex;
    align-items: center;
    gap: 10px;
    background: linear-gradient(90deg, rgba(0,120,255,.08) 0%, transparent 80%);
    border-left: 3px solid #00d4ff;
    border-radius: 0 10px 10px 0;
    padding: 10px 20px;
    margin: 26px 0 14px;
    color: #e0f0ff;
    font-size: 1rem;
    font-weight: 700;
    letter-spacing: .2px;
}

/* ── Divider ── */
hr { border: none; border-top: 1px solid rgba(0,212,255,.08) !important; margin: 14px 0 !important; }

/* ── Dataframe ── */
[data-testid="stDataFrame"] {
    border: 1px solid rgba(0,212,255,.1) !important;
    border-radius: 14px !important;
    overflow: hidden !important;
}

/* ── Inputs ── */
[data-testid="stSelectbox"] > div > div,
[data-testid="stTextInput"] > div > div > input {
    background: #081628 !important;
    border: 1px solid rgba(0,212,255,.15) !important;
    border-radius: 10px !important;
    color: #c0d8f0 !important;
}

/* ── Download button ── */
.stDownloadButton > button {
    background: linear-gradient(135deg,#0050c8,#0080ff) !important;
    color: white !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 11px 28px !important;
    font-weight: 700 !important;
    font-size: .88rem !important;
    letter-spacing: .3px !important;
    box-shadow: 0 4px 20px rgba(0,100,255,.35) !important;
    transition: all .25s ease !important;
}
.stDownloadButton > button:hover {
    box-shadow: 0 6px 28px rgba(0,100,255,.55) !important;
    transform: translateY(-2px) !important;
}

/* ── Slider ── */
[data-testid="stSlider"] [role="slider"] { background: #00d4ff !important; }
[data-testid="stSlider"] [data-testid="stSliderTrack"] div:first-child {
    background: linear-gradient(90deg,#0050c8,#00d4ff) !important;
}

/* ── Radio buttons ── */
[data-testid="stRadio"] label { color: #8ab4d4 !important; }
[data-testid="stRadio"] [aria-checked="true"] + div { color: #00d4ff !important; }

/* ── Success message ── */
[data-testid="stAlert"] { border-radius: 12px !important; }

/* ── Expander ── */
[data-testid="stExpander"] {
    background: rgba(255,255,255,.02) !important;
    border: 1px solid rgba(0,212,255,.1) !important;
    border-radius: 12px !important;
}

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 5px; height: 5px; }
::-webkit-scrollbar-track { background: #081628; }
::-webkit-scrollbar-thumb { background: #1a4080; border-radius: 10px; }
::-webkit-scrollbar-thumb:hover { background: #00d4ff; }
</style>
""", unsafe_allow_html=True)

# ── TRANSLATIONS ─────────────────────────────────────────────
T = {
    'AR': {
        'title'         : 'لوحة تحليلات مكتب الدعم التقني',
        'upload'        : '📂 رفع ملف Excel',
        'filters'       : '🔽 الفلاتر',
        'dept_filter'   : '🏢 الإدارة',
        'svc_filter'    : '⚙️ الخدمة',
        'main_filter'   : '🔥 التصنيف الرئيسي',
        'top_n'         : '🔢 أعلى N نتيجة',
        'theme'         : '🎨 نمط الرسم البياني',
        'all'           : 'الكل',
        'total_rec'     : 'إجمالي السجلات',
        'departments'   : 'الإدارات',
        'svc_types'     : 'أنواع الخدمات',
        'issue_types'   : 'أنواع المشكلات',
        'agents'        : 'الموظفون',
        'tab_overview'  : '📊 نظرة عامة',
        'tab_issues'    : '🔥 المشكلات',
        'tab_dept'      : '🏢 الإدارات',
        'tab_agents'    : '👨‍💻 الموظفون',
        'tab_raw'       : '🗃️ البيانات الخام',
        'kpi_sec'       : '📌 مؤشرات الأداء الرئيسية',
        'overview_dist' : '📊 توزيع نوع الخدمة',
        'top8_issues'   : '🔥 أعلى 8 تصنيفات رئيسية',
        'top_dept_vol'  : '🏢 أعلى الإدارات بعدد الطلبات',
        'svc_x_issue'   : '🧩 الخدمة × التصنيف الرئيسي',
        'top_main'      : '🔥 أعلى التصنيفات الرئيسية',
        'top_sub'       : '📂 أعلى التصنيفات الفرعية',
        'treemap'       : '🔗 شجرة تسلسل التصنيفات',
        'heatmap_svc'   : '🌡️ خريطة حرارية: الخدمة × التصنيف',
        'dept_vol'      : '🏢 حجم الطلبات لكل إدارة',
        'dept_svc'      : '⚙️ الإدارة × نوع الخدمة',
        'dept_issue'    : '🔥 الإدارة × التصنيف الرئيسي',
        'sunburst'      : '☀️ الإدارة ← الخدمة (Sunburst)',
        'agent_wl'      : '👨‍💻 أداء الموظفين',
        'agent_svc'     : '⚙️ الموظف × نوع الخدمة',
        'agent_issue'   : '🔥 الموظف × التصنيف الرئيسي',
        'agent_hm'      : '🌡️ خريطة: الموظف × الإدارة',
        'raw_title'     : '🗃️ مستكشف البيانات الخام',
        'filter_col'    : 'تصفية العمود',
        'search_ph'     : '🔍 ابحث هنا...',
        'showing'       : 'عرض',
        'of'            : 'من',
        'rows'          : 'سجل',
        'download'      : '⬇️ تنزيل كملف Excel',
        'col_stats'     : '📈 إحصائيات الأعمدة',
        'unique'        : 'قيم فريدة',
        'filtered_lbl'  : '🟡 التصفية نشطة',
        'welcome_h'     : 'لوحة تحليلات مكتب الدعم التقني',
        'welcome_p'     : 'ارفع ملف Excel من القائمة الجانبية وسيتم إنشاء لوحة التحليلات تلقائياً',
        'dept_share'    : 'نسبة الإدارات',
        'agent_share'   : 'حصة الموظفين',
        'top_agent_lbl' : '🏆 أكثر موظف نشاطاً',
        'top_dept_lbl'  : '🏅 أكثر إدارة طلباً',
        'top_issue_lbl' : '🔥 أكثر مشكلة تكراراً',
        'coverage_pct'  : '📋 نسبة التغطية',
    },
    'EN': {
        'title'         : 'IT Helpdesk Analytics Dashboard',
        'upload'        : '📂 Upload Excel File',
        'filters'       : '🔽 Filters',
        'dept_filter'   : '🏢 Department',
        'svc_filter'    : '⚙️ Service Type',
        'main_filter'   : '🔥 Main Category',
        'top_n'         : '🔢 Top N Items',
        'theme'         : '🎨 Chart Theme',
        'all'           : 'All',
        'total_rec'     : 'Total Records',
        'departments'   : 'Departments',
        'svc_types'     : 'Service Types',
        'issue_types'   : 'Issue Types',
        'agents'        : 'Agents',
        'tab_overview'  : '📊 Overview',
        'tab_issues'    : '🔥 Issues',
        'tab_dept'      : '🏢 Departments',
        'tab_agents'    : '👨‍💻 Agents',
        'tab_raw'       : '🗃️ Raw Data',
        'kpi_sec'       : '📌 Key Performance Indicators',
        'overview_dist' : '📊 Service Type Distribution',
        'top8_issues'   : '🔥 Top 8 Issue Categories',
        'top_dept_vol'  : '🏢 Top Departments by Ticket Volume',
        'svc_x_issue'   : '🧩 Service Type × Issue Category',
        'top_main'      : '🔥 Top Main Categories',
        'top_sub'       : '📂 Top Sub Categories',
        'treemap'       : '🔗 Issue Hierarchy Treemap',
        'heatmap_svc'   : '🌡️ Service × Issue Heatmap',
        'dept_vol'      : '🏢 Department Ticket Volume',
        'dept_svc'      : '⚙️ Department × Service Type',
        'dept_issue'    : '🔥 Department × Issue Category',
        'sunburst'      : '☀️ Department → Service Sunburst',
        'agent_wl'      : '👨‍💻 Agent Performance',
        'agent_svc'     : '⚙️ Agent × Service Type',
        'agent_issue'   : '🔥 Agent × Issue Category',
        'agent_hm'      : '🌡️ Agent × Department Heatmap',
        'raw_title'     : '🗃️ Raw Data Explorer',
        'filter_col'    : 'Filter Column',
        'search_ph'     : '🔍 Search here...',
        'showing'       : 'Showing',
        'of'            : 'of',
        'rows'          : 'rows',
        'download'      : '⬇️ Download as Excel',
        'col_stats'     : '📈 Column Statistics',
        'unique'        : 'unique values',
        'filtered_lbl'  : '🟡 Filter Active',
        'welcome_h'     : 'IT Helpdesk Analytics Dashboard',
        'welcome_p'     : 'Upload your Excel file from the sidebar and the full dashboard will build automatically',
        'dept_share'    : 'Department Share',
        'agent_share'   : 'Agent Workload Share',
        'top_agent_lbl' : '🏆 Most Active Agent',
        'top_dept_lbl'  : '🏅 Busiest Department',
        'top_issue_lbl' : '🔥 Top Issue',
        'coverage_pct'  : '📋 Agent Coverage',
    }
}

# ── COLUMN KEYS ───────────────────────────────────────────────
C_DEPT  = 'إدارة العميل'
C_SVC   = 'الخدمة'
C_MAIN  = 'التصنيف الرئيسي'
C_SUB   = 'التصنيف الفرعي'
C_AGENT = 'مسند الى'

# ── SIDEBAR ───────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='text-align:center;padding:16px 0 8px;'>
      <div style='background:linear-gradient(135deg,#0048b3,#00aaff);
                  display:inline-block;border-radius:14px;
                  padding:10px 14px;font-size:1.8rem;
                  box-shadow:0 4px 16px rgba(0,140,255,.35);'>🖥️</div>
    </div>""", unsafe_allow_html=True)

    lang = st.radio("🌐 Language / اللغة", ["EN", "AR"],
                    horizontal=True, index=0)
    tx   = T[lang]

    st.markdown(f"<h3 style='text-align:center;color:#00d4ff !important;"
                f"margin:4px 0 12px;font-size:.95rem;'>{tx['title']}</h3>",
                unsafe_allow_html=True)
    st.markdown("---")
    uploaded = st.file_uploader(tx['upload'], type=["xlsx","xls"])
    if uploaded:
        st.success(f"✅ {uploaded.name}", icon="✅")

# ── WELCOME ───────────────────────────────────────────────────
if not uploaded:
    st.markdown(f"""
    <div style='min-height:85vh;display:flex;flex-direction:column;
                align-items:center;justify-content:center;text-align:center;
                padding:40px 20px;'>
      <div style='background:linear-gradient(135deg,#0048b3,#00aaff);
                  border-radius:24px;padding:20px 26px;
                  font-size:3.5rem;margin-bottom:24px;
                  box-shadow:0 12px 40px rgba(0,150,255,.4),
                             0 0 80px rgba(0,212,255,.12);'>🖥️</div>
      <h1 style='color:#00d4ff;font-size:2.6rem;font-weight:800;
                 margin:0 0 14px;letter-spacing:-.5px;'>{tx["welcome_h"]}</h1>
      <p style='color:#5a8aaa;font-size:1.05rem;max-width:480px;
                line-height:1.7;margin:0 auto 40px;'>{tx["welcome_p"]}</p>
      <div style='display:flex;justify-content:center;gap:14px;flex-wrap:wrap;'>
        {"".join([
            f"<div style='background:linear-gradient(145deg,#081628,#0d2040);"
            f"border:1px solid rgba(0,212,255,.12);"
            f"border-top:3px solid #00d4ff;"
            f"border-radius:16px;padding:26px 20px;width:150px;"
            f"box-shadow:0 8px 24px rgba(0,0,0,.4);'>"
            f"<div style='font-size:2.4rem'>{ic}</div>"
            f"<div style='color:#8ab4d4;margin-top:10px;font-size:.85rem;"
            f"font-weight:600;'>{lb}</div></div>"
            for ic,lb in [('📊',tx['tab_overview']),('🔥',tx['tab_issues']),
                           ('🏢',tx['tab_dept']),('👨‍💻',tx['tab_agents'])]
        ])}
      </div>
    </div>""", unsafe_allow_html=True)
    st.stop()

# ── LOAD DATA ────────────────────────────────────────────────
@st.cache_data(show_spinner="⚙️ Processing data...")
def load_data(raw_bytes: bytes) -> pd.DataFrame:
    df = pd.read_excel(io.BytesIO(raw_bytes), sheet_name=0, header=2)
    if C_DEPT in df.columns:
        df = df[df[C_DEPT] != 'Grand Total']
    keep = [c for c in [C_DEPT, C_SVC, C_MAIN, C_SUB, C_AGENT] if c in df.columns]
    df   = df[keep].copy()
    for c in [C_DEPT, C_SVC, C_MAIN, C_SUB]:
        if c in df.columns:
            df[c] = df[c].replace('', pd.NA).ffill()
    if C_AGENT in df.columns:
        df[C_AGENT] = df[C_AGENT].astype(str).str.strip()
        df[C_AGENT] = df[C_AGENT].replace({'nan':pd.NA,'Agent':pd.NA,'':pd.NA})
    df.dropna(how='all', inplace=True)
    df.reset_index(drop=True, inplace=True)
    df['_agent_short'] = df[C_AGENT]\
        .str.replace('−متعاقد','',regex=False)\
        .str.replace('-متعاقد','',regex=False).str.strip()
    return df

try:
    raw_bytes = uploaded.read()
    df        = load_data(raw_bytes)
except Exception as e:
    st.error(f"❌ Load error: {e}")
    st.stop()

if df.empty:
    st.error("❌ No data found."); st.stop()

# ── SIDEBAR FILTERS ───────────────────────────────────────────
with st.sidebar:
    st.markdown("---")
    st.markdown(f"<p style='color:#00d4ff !important;font-weight:700;margin-bottom:4px;'>"
                f"{tx['filters']}</p>", unsafe_allow_html=True)

    ALL   = tx['all']
    s_dep = st.selectbox(tx['dept_filter'],
                         [ALL]+sorted(df[C_DEPT].dropna().unique().tolist()))
    s_svc = st.selectbox(tx['svc_filter'],
                         [ALL]+sorted(df[C_SVC].dropna().unique().tolist()))
    s_mn  = st.selectbox(tx['main_filter'],
                         [ALL]+sorted(df[C_MAIN].dropna().unique().tolist()))
    st.markdown("---")
    top_n  = st.slider(tx['top_n'], 5, 30, 15)
    theme  = st.selectbox(tx['theme'],
                          ["plotly_dark","plotly","ggplot2"])
    st.markdown("---")
    st.markdown(f"<div style='text-align:center;"
                f"color:#5a8aaa !important;font-size:.78rem;'>"
                f"📊 Total: <b style='color:#00d4ff'>{len(df):,}</b> records"
                f"</div>", unsafe_allow_html=True)

# ── APPLY FILTERS ────────────────────────────────────────────
dff = df.copy()
if s_dep != ALL: dff = dff[dff[C_DEPT] == s_dep]
if s_svc != ALL: dff = dff[dff[C_SVC]  == s_svc]
if s_mn  != ALL: dff = dff[dff[C_MAIN] == s_mn]
filtered = len(dff) < len(df)

# ── QUICK INSIGHTS (pre-compute) ─────────────────────────────
top_agent = dff[C_AGENT].dropna().value_counts()
top_dept  = dff[C_DEPT].dropna().value_counts()
top_issue = dff[C_MAIN].dropna().value_counts()

top_agent_name  = str(top_agent.index[0]).replace('−متعاقد','').replace('-متعاقد','').strip() if len(top_agent) else '—'
top_agent_count = int(top_agent.iloc[0]) if len(top_agent) else 0
top_dept_name   = str(top_dept.index[0]) if len(top_dept) else '—'
top_dept_count  = int(top_dept.iloc[0])  if len(top_dept) else 0
top_issue_name  = str(top_issue.index[0]) if len(top_issue) else '—'
top_issue_count = int(top_issue.iloc[0]) if len(top_issue) else 0
agent_cov_pct   = round(dff[C_AGENT].notna().sum() / len(dff) * 100, 1) if len(dff) else 0

# ── HEADER ───────────────────────────────────────────────────
filter_badge = (
    f'<span style="background:rgba(255,200,0,.12);color:#ffc800;'
    f'padding:3px 12px;border-radius:20px;font-size:.75rem;font-weight:700;'
    f'border:1px solid rgba(255,200,0,.25);">{tx["filtered_lbl"]}</span>'
) if filtered else ""

st.markdown(f"""
<div style='background:linear-gradient(135deg,#081628 0%,#0a1e38 50%,#060d1f 100%);
            padding:20px 28px;border-radius:18px;margin-bottom:18px;
            border:1px solid rgba(0,212,255,.1);
            box-shadow:0 10px 40px rgba(0,0,0,.5),
                       inset 0 1px 0 rgba(255,255,255,.04);
            position:relative;overflow:hidden;'>
  <div style='position:absolute;top:-50px;right:-50px;width:200px;height:200px;
              background:radial-gradient(circle,rgba(0,212,255,.06),transparent 70%);
              border-radius:50%;pointer-events:none;'></div>
  <div style='position:absolute;bottom:-60px;left:20%;width:160px;height:160px;
              background:radial-gradient(circle,rgba(0,80,255,.05),transparent 70%);
              border-radius:50%;pointer-events:none;'></div>
  <div style='display:flex;align-items:center;gap:16px;position:relative;z-index:1;'>
    <div style='background:linear-gradient(135deg,#0048b3,#0090ff);
                border-radius:16px;padding:14px 16px;font-size:2rem;line-height:1;
                box-shadow:0 4px 20px rgba(0,140,255,.4);flex-shrink:0;'>🖥️</div>
    <div style='flex:1;'>
      <h1 style='color:#00d4ff;margin:0;font-size:1.75rem;font-weight:800;
                 letter-spacing:-.4px;line-height:1.2;'>{tx["title"]}</h1>
      <div style='color:#5a8aaa;margin-top:6px;font-size:.83rem;
                  display:flex;gap:14px;flex-wrap:wrap;align-items:center;'>
        <span>📄 <b style='color:#8ab4d4'>{uploaded.name}</b></span>
        <span style='color:#1a3050'>│</span>
        <span>🗂️ Total: <b style='color:#c0d8f0'>{len(df):,}</b></span>
        <span style='color:#1a3050'>│</span>
        <span>🔽 Shown: <b style='color:#00d4ff'>{len(dff):,}</b></span>
        {"<span style='color:#1a3050'>│</span>" + filter_badge if filtered else ""}
      </div>
    </div>
  </div>
</div>""", unsafe_allow_html=True)

# ── HELPER ───────────────────────────────────────────────────
def sec(label):
    st.markdown(f'<div class="sec">{label}</div>', unsafe_allow_html=True)

def chart_cfg(fig, h=450):
    fig.update_layout(
        height=h,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font_color='#8ab4d4',
        margin=dict(l=10, r=10, t=50, b=10),
        hoverlabel=dict(
            bgcolor='#0d2040',
            font_size=12,
            bordercolor='#00d4ff'
        ),
        xaxis=dict(gridcolor='rgba(255,255,255,.05)',
                   linecolor='rgba(255,255,255,.08)'),
        yaxis=dict(gridcolor='rgba(255,255,255,.05)',
                   linecolor='rgba(255,255,255,.08)'),
    )
    return fig

# ── TABS ─────────────────────────────────────────────────────
tab1,tab2,tab3,tab4,tab5 = st.tabs([
    tx['tab_overview'], tx['tab_issues'],
    tx['tab_dept'],     tx['tab_agents'],
    tx['tab_raw'],
])

# ════════════════════════════════════════════
#  TAB 1 ── OVERVIEW
# ════════════════════════════════════════════
with tab1:

    # ── Row 1: KPI cards ──
    sec(tx['kpi_sec'])
    k1,k2,k3,k4,k5 = st.columns(5)
    kpis = [
        ("🎫", len(dff),                             tx['total_rec']),
        ("🏢", dff[C_DEPT].nunique(),                tx['departments']),
        ("⚙️", dff[C_SVC].nunique(),                 tx['svc_types']),
        ("🔥", dff[C_MAIN].nunique(),                tx['issue_types']),
        ("👨‍💻", dff[C_AGENT].dropna().nunique(),      tx['agents']),
    ]
    for c,(ico,v,lbl) in zip([k1,k2,k3,k4,k5], kpis):
        with c:
            st.markdown(f"""<div class="kpi">
              <span class="kpi-icon">{ico}</span>
              <span class="kpi-num">{v:,}</span>
              <span class="kpi-lbl">{lbl}</span>
            </div>""", unsafe_allow_html=True)

    # ── Row 2: Insight strip ──
    st.markdown("<div style='height:6px'></div>", unsafe_allow_html=True)
    i1,i2,i3,i4 = st.columns(4)
    insight_style = ("background:linear-gradient(135deg,#081628,#091e3a);"
                     "border:1px solid rgba(0,212,255,.1);border-left:3px solid;"
                     "border-radius:12px;padding:14px 16px;margin-bottom:10px;")
    with i1:
        st.markdown(f"<div style='{insight_style}border-left-color:#00d4ff;'>"
                    f"<div style='color:#5a8aaa;font-size:.72rem;font-weight:700;"
                    f"letter-spacing:.8px;text-transform:uppercase;'>"
                    f"{tx['top_agent_lbl']}</div>"
                    f"<div style='color:#e0f0ff;font-size:.88rem;font-weight:700;"
                    f"margin-top:5px;'>{top_agent_name}</div>"
                    f"<div style='color:#00d4ff;font-size:.8rem;'>{top_agent_count:,} tickets</div>"
                    f"</div>", unsafe_allow_html=True)
    with i2:
        st.markdown(f"<div style='{insight_style}border-left-color:#f0a020;'>"
                    f"<div style='color:#5a8aaa;font-size:.72rem;font-weight:700;"
                    f"letter-spacing:.8px;text-transform:uppercase;'>"
                    f"{tx['top_dept_lbl']}</div>"
                    f"<div style='color:#e0f0ff;font-size:.85rem;font-weight:700;"
                    f"margin-top:5px;line-height:1.3;'>{top_dept_name[:30]}…</div>"
                    f"<div style='color:#f0a020;font-size:.8rem;'>{top_dept_count:,} tickets</div>"
                    f"</div>", unsafe_allow_html=True)
    with i3:
        st.markdown(f"<div style='{insight_style}border-left-color:#ff4060;'>"
                    f"<div style='color:#5a8aaa;font-size:.72rem;font-weight:700;"
                    f"letter-spacing:.8px;text-transform:uppercase;'>"
                    f"{tx['top_issue_lbl']}</div>"
                    f"<div style='color:#e0f0ff;font-size:.85rem;font-weight:700;"
                    f"margin-top:5px;line-height:1.3;'>{top_issue_name[:30]}</div>"
                    f"<div style='color:#ff4060;font-size:.8rem;'>{top_issue_count:,} tickets</div>"
                    f"</div>", unsafe_allow_html=True)
    with i4:
        st.markdown(f"<div style='{insight_style}border-left-color:#40e0a0;'>"
                    f"<div style='color:#5a8aaa;font-size:.72rem;font-weight:700;"
                    f"letter-spacing:.8px;text-transform:uppercase;'>"
                    f"{tx['coverage_pct']}</div>"
                    f"<div style='color:#40e0a0;font-size:1.6rem;font-weight:800;"
                    f"margin-top:5px;'>{agent_cov_pct}%</div>"
                    f"<div style='color:#5a8aaa;font-size:.78rem;'>of tickets assigned</div>"
                    f"</div>", unsafe_allow_html=True)

    st.markdown("---")

    # ── Row 3: 2 pies ──
    r1,r2 = st.columns(2)
    with r1:
        svc = dff[C_SVC].value_counts().reset_index()
        svc.columns = ['Service','Count']
        fig = px.pie(svc, values='Count', names='Service',
                     title=tx['overview_dist'], hole=0.48, template=theme)
        fig.update_traces(textposition='inside', textinfo='percent+label',
                          textfont_size=11)
        fig.update_layout(showlegend=True, legend=dict(
            orientation='v', x=1.01, y=0.5, font_size=11))
        st.plotly_chart(chart_cfg(fig,380), use_container_width=True)
    with r2:
        mc = dff[C_MAIN].value_counts().head(8).reset_index()
        mc.columns = ['Category','Count']
        fig = px.pie(mc, values='Count', names='Category',
                     title=tx['top8_issues'], hole=0.48, template=theme)
        fig.update_traces(textposition='inside', textinfo='percent+label',
                          textfont_size=11)
        fig.update_layout(showlegend=True, legend=dict(
            orientation='v', x=1.01, y=0.5, font_size=11))
        st.plotly_chart(chart_cfg(fig,380), use_container_width=True)

    # ── Top Depts horizontal bar ──
    sec(tx['top_dept_vol'])
    dv = dff[C_DEPT].value_counts().head(15).reset_index()
    dv.columns = ['Dept','Count']
    fig = px.bar(dv, x='Count', y='Dept', orientation='h',
                 color='Count', color_continuous_scale='Blues',
                 template=theme, text='Count')
    fig.update_layout(yaxis={'categoryorder':'total ascending'},
                      showlegend=False, coloraxis_showscale=False)
    fig.update_traces(textposition='outside',
                      marker_line_width=0)
    st.plotly_chart(chart_cfg(fig,520), use_container_width=True)

    # ── Service × Main category stacked ──
    sec(tx['svc_x_issue'])
    top_m = dff[C_MAIN].value_counts().head(8).index.tolist()
    sm = dff[dff[C_MAIN].isin(top_m)]\
         .groupby([C_SVC, C_MAIN]).size().reset_index(name='Count')
    fig = px.bar(sm, x=C_SVC, y='Count', color=C_MAIN,
                 barmode='stack', template=theme, text='Count')
    fig.update_layout(xaxis_tickangle=-25,
                      legend=dict(orientation='h', yanchor='bottom', y=1.01))
    fig.update_traces(textposition='inside', marker_line_width=0)
    st.plotly_chart(chart_cfg(fig,450), use_container_width=True)

# ════════════════════════════════════════════
#  TAB 2 ── ISSUES
# ════════════════════════════════════════════
with tab2:
    sec(tx['top_main'])
    d = dff[C_MAIN].value_counts().head(top_n).reset_index()
    d.columns = ['Issue','Count']
    fig = px.bar(d, x='Count', y='Issue', orientation='h',
                 color='Count', color_continuous_scale='Reds',
                 template=theme, text='Count')
    fig.update_layout(yaxis={'categoryorder':'total ascending'},
                      showlegend=False, coloraxis_showscale=False)
    fig.update_traces(textposition='outside', marker_line_width=0)
    st.plotly_chart(chart_cfg(fig, max(380, top_n*32)), use_container_width=True)

    sec(tx['top_sub'])
    d2 = dff[C_SUB].dropna().value_counts().head(top_n).reset_index()
    d2.columns = ['Sub','Count']
    fig2 = px.bar(d2, x='Count', y='Sub', orientation='h',
                  color='Count', color_continuous_scale='Oranges',
                  template=theme, text='Count')
    fig2.update_layout(yaxis={'categoryorder':'total ascending'},
                       showlegend=False, coloraxis_showscale=False)
    fig2.update_traces(textposition='outside', marker_line_width=0)
    st.plotly_chart(chart_cfg(fig2, max(380, top_n*32)), use_container_width=True)

    # Treemap
    sec(tx['treemap'])
    tree = dff.dropna(subset=[C_MAIN, C_SUB])\
              .groupby([C_MAIN, C_SUB]).size().reset_index(name='Count')
    fig3 = px.treemap(tree, path=[C_MAIN, C_SUB], values='Count',
                      template=theme, color='Count',
                      color_continuous_scale='Blues')
    fig3.update_traces(textinfo='label+value+percent root',
                       marker_line_width=1,
                       marker_line_color='rgba(0,0,0,.3)')
    st.plotly_chart(chart_cfg(fig3, 650), use_container_width=True)

    # Heatmap: Service × Main
    sec(tx['heatmap_svc'])
    h_svcs = dff[C_SVC].value_counts().head(8).index.tolist()
    h_main = dff[C_MAIN].value_counts().head(12).index.tolist()
    heat   = dff[dff[C_SVC].isin(h_svcs) & dff[C_MAIN].isin(h_main)]\
             .groupby([C_SVC, C_MAIN]).size().reset_index(name='Count')
    piv    = heat.pivot(index=C_SVC, columns=C_MAIN, values='Count').fillna(0)
    fig4   = go.Figure(go.Heatmap(
        z=piv.values, x=piv.columns.tolist(), y=piv.index.tolist(),
        colorscale='YlOrRd',
        text=piv.values.astype(int), texttemplate='%{text}',
        hoverongaps=False,
        hovertemplate='Service: %{y}<br>Issue: %{x}<br>Count: %{z}<extra></extra>'
    ))
    fig4.update_layout(xaxis_tickangle=-35)
    st.plotly_chart(chart_cfg(fig4, 420), use_container_width=True)

# ════════════════════════════════════════════
#  TAB 3 ── DEPARTMENTS
# ════════════════════════════════════════════
with tab3:
    sec(tx['dept_vol'])
    d = dff[C_DEPT].value_counts().head(top_n).reset_index()
    d.columns = ['Dept','Tickets']

    c1,c2 = st.columns(2)
    with c1:
        fig = px.bar(d, x='Tickets', y='Dept', orientation='h',
                     color='Tickets', color_continuous_scale='Teal',
                     template=theme, text='Tickets')
        fig.update_layout(yaxis={'categoryorder':'total ascending'},
                          showlegend=False, coloraxis_showscale=False)
        fig.update_traces(textposition='outside', marker_line_width=0)
        st.plotly_chart(chart_cfg(fig,500), use_container_width=True)
    with c2:
        fig2 = px.pie(d, values='Tickets', names='Dept',
                      hole=0.42, template=theme)
        fig2.update_traces(textposition='inside', textinfo='percent+label',
                           textfont_size=10)
        st.plotly_chart(chart_cfg(fig2,500), use_container_width=True)

    # Dept × Service
    sec(tx['dept_svc'])
    top_d = d['Dept'].head(12).tolist()
    ds = dff[dff[C_DEPT].isin(top_d)]\
         .groupby([C_DEPT, C_SVC]).size().reset_index(name='Count')
    fig3 = px.bar(ds, x=C_DEPT, y='Count', color=C_SVC,
                  barmode='stack', template=theme)
    fig3.update_layout(xaxis_tickangle=-30,
                       legend=dict(orientation='h', yanchor='bottom', y=1.01))
    fig3.update_traces(marker_line_width=0)
    st.plotly_chart(chart_cfg(fig3,500), use_container_width=True)

    # Dept × Main Category
    sec(tx['dept_issue'])
    top_m = dff[C_MAIN].value_counts().head(8).index.tolist()
    cr = dff[dff[C_DEPT].isin(top_d) & dff[C_MAIN].isin(top_m)]\
         .groupby([C_DEPT, C_MAIN]).size().reset_index(name='Count')
    fig4 = px.bar(cr, x=C_DEPT, y='Count', color=C_MAIN,
                  barmode='stack', template=theme)
    fig4.update_layout(xaxis_tickangle=-30,
                       legend=dict(orientation='h', yanchor='bottom', y=1.01))
    fig4.update_traces(marker_line_width=0)
    st.plotly_chart(chart_cfg(fig4,530), use_container_width=True)

    # Sunburst
    sec(tx['sunburst'])
    sun = dff[dff[C_DEPT].isin(top_d)]\
          .groupby([C_DEPT, C_SVC]).size().reset_index(name='Count')
    fig5 = px.sunburst(sun, path=[C_DEPT, C_SVC], values='Count',
                       template=theme, color='Count',
                       color_continuous_scale='Blues')
    fig5.update_traces(textinfo='label+percent root')
    st.plotly_chart(chart_cfg(fig5,620), use_container_width=True)

# ════════════════════════════════════════════
#  TAB 4 ── AGENTS
# ════════════════════════════════════════════
with tab4:
    if dff[C_AGENT].dropna().empty:
        st.info("⚠️ No agent data available.")
    else:
        sec(tx['agent_wl'])
        ag = dff.dropna(subset=[C_AGENT])\
                .groupby([C_AGENT,'_agent_short'])\
                .size().reset_index(name='Tickets')\
                .sort_values('Tickets',ascending=False)\
                .head(top_n)

        c1,c2 = st.columns(2)
        with c1:
            fig = px.bar(ag, x='Tickets', y='_agent_short',
                         orientation='h',
                         color='Tickets', color_continuous_scale='Viridis',
                         template=theme, text='Tickets')
            fig.update_layout(yaxis={'categoryorder':'total ascending',
                                     'title':''},
                              showlegend=False, coloraxis_showscale=False)
            fig.update_traces(textposition='outside', marker_line_width=0)
            st.plotly_chart(chart_cfg(fig,560), use_container_width=True)
        with c2:
            fig2 = px.pie(ag, values='Tickets', names='_agent_short',
                          hole=0.42, template=theme)
            fig2.update_traces(textposition='inside',
                               textinfo='percent+label', textfont_size=10)
            st.plotly_chart(chart_cfg(fig2,560), use_container_width=True)

        top_ag_keys = ag[C_AGENT].tolist()

        # Agent × Service Type
        sec(tx['agent_svc'])
        agv = dff[dff[C_AGENT].isin(top_ag_keys)]\
              .groupby(['_agent_short', C_SVC])\
              .size().reset_index(name='Count')
        fig3 = px.bar(agv, x='_agent_short', y='Count',
                      color=C_SVC, barmode='stack', template=theme)
        fig3.update_layout(xaxis_tickangle=-30, xaxis_title='Agent',
                           legend=dict(orientation='h', yanchor='bottom', y=1.01))
        fig3.update_traces(marker_line_width=0)
        st.plotly_chart(chart_cfg(fig3,480), use_container_width=True)

        # Agent × Main Category
        sec(tx['agent_issue'])
        top_m = dff[C_MAIN].value_counts().head(8).index.tolist()
        agi = dff[dff[C_AGENT].isin(top_ag_keys) &
                  dff[C_MAIN].isin(top_m)]\
              .groupby(['_agent_short', C_MAIN])\
              .size().reset_index(name='Count')
        fig4 = px.bar(agi, x='_agent_short', y='Count',
                      color=C_MAIN, barmode='stack', template=theme)
        fig4.update_layout(xaxis_tickangle=-30, xaxis_title='Agent',
                           legend=dict(orientation='h', yanchor='bottom', y=1.01))
        fig4.update_traces(marker_line_width=0)
        st.plotly_chart(chart_cfg(fig4,480), use_container_width=True)

        # Agent × Department Heatmap
        sec(tx['agent_hm'])
        top_d2 = dff[C_DEPT].value_counts().head(12).index.tolist()
        cov = dff[dff[C_AGENT].isin(top_ag_keys) &
                  dff[C_DEPT].isin(top_d2)]\
              .groupby(['_agent_short', C_DEPT])\
              .size().reset_index(name='Count')
        piv2 = cov.pivot(index='_agent_short',
                         columns=C_DEPT,
                         values='Count').fillna(0)
        fig5 = go.Figure(go.Heatmap(
            z=piv2.values,
            x=piv2.columns.tolist(),
            y=piv2.index.tolist(),
            colorscale='Teal',
            text=piv2.values.astype(int),
            texttemplate='%{text}',
            hoverongaps=False,
            hovertemplate='Agent: %{y}<br>Dept: %{x}<br>Tickets: %{z}<extra></extra>'
        ))
        fig5.update_layout(xaxis_tickangle=-35)
        st.plotly_chart(chart_cfg(fig5,520), use_container_width=True)

# ════════════════════════════════════════════
#  TAB 5 ── RAW DATA
# ════════════════════════════════════════════
with tab5:
    sec(tx['raw_title'])

    show_df = dff.drop(columns=['_agent_short'], errors='ignore').copy()

    sc1,sc2 = st.columns([1,3])
    with sc1:
        fcol = st.selectbox(tx['filter_col'],
                            [tx['all']] + show_df.columns.tolist())
    with sc2:
        srch = st.text_input(tx['search_ph'], "")

    if srch:
        if fcol == tx['all']:
            mask = show_df.apply(lambda c: c.astype(str)
                                  .str.contains(srch, case=False, na=False))\
                          .any(axis=1)
        else:
            mask = show_df[fcol].astype(str)\
                         .str.contains(srch, case=False, na=False)
        show_df = show_df[mask]

    st.markdown(
        f"<div style='color:#5a8aaa;font-size:.83rem;margin-bottom:6px;'>"
        f"<b style='color:#00d4ff'>{len(show_df):,}</b> {tx['of']} "
        f"<b style='color:#8ab4d4'>{len(df):,}</b> {tx['rows']}</div>",
        unsafe_allow_html=True
    )
    st.dataframe(show_df, use_container_width=True, height=500)

    # Column statistics
    with st.expander(tx['col_stats']):
        cols_stat = st.columns(min(len(show_df.columns), 3))
        for i, col in enumerate(show_df.columns):
            with cols_stat[i % len(cols_stat)]:
                vc = show_df[col].dropna().value_counts()
                st.markdown(
                    f"<div style='color:#00d4ff;font-weight:700;"
                    f"font-size:.85rem;margin-bottom:4px;'>{col}</div>"
                    f"<div style='color:#5a8aaa;font-size:.75rem;"
                    f"margin-bottom:6px;'>{len(vc):,} {tx['unique']}</div>",
                    unsafe_allow_html=True
                )
                st.dataframe(
                    vc.head(8).rename('Count').reset_index(),
                    use_container_width=True,
                    hide_index=True, height=220
                )

    # Download
    st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)
    out = io.BytesIO()
    with pd.ExcelWriter(out, engine='openpyxl') as w:
        show_df.to_excel(w, index=False, sheet_name='HelpDesk_Data')
    st.download_button(
        label=tx['download'],
        data=out.getvalue(),
        file_name="helpdesk_export.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        use_container_width=False
    )
