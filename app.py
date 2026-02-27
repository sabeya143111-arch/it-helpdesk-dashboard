# ================================================================
#   IT HELPDESK ANALYTICS — ULTRA PREMIUM v21.1 (FIXED)
#   Arabic + English + Accurate Columns + Excel Download Fixed
# ================================================================

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import io, os, requests
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import (SimpleDocTemplate, Table, TableStyle,
                                Paragraph, Spacer, PageBreak, Image, HRFlowable)
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

try:
    from arabic_reshaper import reshape
    from bidi.algorithm import get_display
    ARABIC_SUPPORT = True
except ImportError:
    ARABIC_SUPPORT = False
    def reshape(t): return str(t)
    def get_display(t): return str(t)

st.set_page_config(page_title="IT Helpdesk Analytics", page_icon="🖥️",
                   layout="wide", initial_sidebar_state="expanded")

# ── ARABIC FONT LOADER ───────────────────────────────────────────
@st.cache_resource
def load_arabic_fonts():
    fonts_loaded = {}
    font_urls = {
        'Amiri-Regular': [
            "https://github.com/aliftype/amiri/raw/main/Amiri-Regular.ttf",
            "https://fonts.gstatic.com/s/amiri/v27/J7aRnpd8CGxBHqUpvrIw74NL.ttf",
        ],
        'Amiri-Bold': [
            "https://github.com/aliftype/amiri/raw/main/Amiri-Bold.ttf",
            "https://fonts.gstatic.com/s/amiri/v27/J7acnpd8CGxBHqUpvrIGJBEoRdI.ttf",
        ],
    }
    for font_name, urls in font_urls.items():
        path = f"/tmp/{font_name}.ttf"
        if not os.path.exists(path):
            for url in urls:
                try:
                    r = requests.get(url, timeout=20)
                    if r.status_code == 200:
                        with open(path, 'wb') as f:
                            f.write(r.content)
                        break
                except:
                    continue
        try:
            if os.path.exists(path):
                pdfmetrics.registerFont(TTFont(font_name, path))
                fonts_loaded[font_name] = True
        except:
            fonts_loaded[font_name] = False
    return fonts_loaded

FONTS = load_arabic_fonts()
FONT_OK = FONTS.get('Amiri-Regular', False)
AR_FONT = 'Amiri-Regular' if FONT_OK else 'Helvetica'
AR_FONT_BOLD = 'Amiri-Bold' if FONTS.get('Amiri-Bold', False) else 'Helvetica-Bold'

def ar(text, max_len=None):
    t = str(text).strip()
    if not t or t in ['nan', '', 'None']:
        return ''
    if max_len and len(t) > max_len:
        t = t[:max_len-2] + '..'
    if ARABIC_SUPPORT and any('\u0600' <= c <= '\u06FF' for c in t):
        try:
            reshaped = reshape(t)
            return get_display(reshaped)
        except:
            return t
    return t

# ── PREMIUM CSS ──────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700;800;900&display=swap');
*{font-family:'Inter',sans-serif!important;box-sizing:border-box}
.stApp{background:linear-gradient(135deg,#0a0e27 0%,#1a1f3a 50%,#0a0e27 100%)!important}
.main .block-container{background:transparent!important;padding-top:.8rem!important;max-width:100%!important}
[data-testid="stSidebar"]{background:linear-gradient(180deg,#0d1117,#161b22,#0d1117)!important;
border-right:2px solid rgba(88,166,255,.2)!important;box-shadow:4px 0 20px rgba(0,0,0,.5)}
[data-testid="stSidebar"] label,[data-testid="stSidebar"] p,[data-testid="stSidebar"] span{
color:#8ab4f8!important;font-size:.84rem!important;font-weight:500}
@keyframes premium-glow{0%,100%{box-shadow:0 8px 32px rgba(88,166,255,.15),
inset 0 1px 0 rgba(255,255,255,.1)}50%{box-shadow:0 12px 48px rgba(88,166,255,.25),
inset 0 1px 0 rgba(255,255,255,.15)}}
@keyframes slide-up{from{opacity:0;transform:translateY(30px)}to{opacity:1;transform:translateY(0)}}
.premium-header{animation:premium-glow 4s ease-in-out infinite,slide-up .8s ease;
background:linear-gradient(135deg,#1a1f3a,#2d3561,#1a1f3a);padding:28px 36px;border-radius:24px;
margin-bottom:24px;border:2px solid rgba(88,166,255,.25);position:relative;overflow:hidden}
.premium-header::before{content:'';position:absolute;top:-50%;left:-50%;width:200%;height:200%;
background:radial-gradient(circle,rgba(88,166,255,.08) 0%,transparent 70%);
animation:rotate 20s linear infinite}
@keyframes rotate{from{transform:rotate(0deg)}to{transform:rotate(360deg)}}
.kpi-premium{background:linear-gradient(145deg,#1a1f3a,#2d3561);border:2px solid rgba(88,166,255,.2);
border-top:4px solid #58a6ff;border-radius:20px;padding:24px 14px 20px;text-align:center;
box-shadow:0 8px 32px rgba(0,0,0,.4),inset 0 1px 0 rgba(255,255,255,.05);
transition:all .4s cubic-bezier(.175,.885,.32,1.275);margin-bottom:14px;position:relative;overflow:hidden}
.kpi-premium::before{content:'';position:absolute;top:0;left:-100%;width:100%;height:100%;
background:linear-gradient(90deg,transparent,rgba(88,166,255,.1),transparent);transition:left .6s}
.kpi-premium:hover{transform:translateY(-8px) scale(1.03);
box-shadow:0 16px 48px rgba(88,166,255,.3),inset 0 2px 0 rgba(255,255,255,.1);border-top-color:#79c0ff}
.kpi-premium:hover::before{left:100%}
.kpi-icon{font-size:1.8rem;margin-bottom:10px;display:block;filter:drop-shadow(0 2px 8px rgba(88,166,255,.4))}
.kpi-num{font-size:2.4rem;font-weight:900;color:#58a6ff;line-height:1;display:block;
text-shadow:0 0 20px rgba(88,166,255,.5);letter-spacing:-1px}
.kpi-lbl{font-size:.7rem;color:#7d8590;margin-top:8px;display:block;letter-spacing:1.5px;
text-transform:uppercase;font-weight:800}
.sec-premium{background:linear-gradient(90deg,rgba(88,166,255,.15),transparent);
border-left:4px solid #58a6ff;border-radius:0 16px 16px 0;padding:14px 28px;margin:32px 0 20px;
color:#c9d1d9;font-size:1.1rem;font-weight:900;box-shadow:0 4px 16px rgba(88,166,255,.1)}
.insight-card{background:linear-gradient(135deg,#161b22,#1c2128);border:2px solid rgba(88,166,255,.2);
border-left:5px solid #58a6ff;border-radius:18px;padding:20px 24px;margin-bottom:14px;
transition:all .3s ease;box-shadow:0 4px 16px rgba(0,0,0,.3)}
.insight-card:hover{border-left-color:#79c0ff;box-shadow:0 8px 32px rgba(88,166,255,.2);
transform:translateX(4px)}
.insight-badge{display:inline-block;background:rgba(88,166,255,.15);color:#58a6ff;padding:4px 14px;
border-radius:24px;font-size:.7rem;font-weight:900;letter-spacing:1.2px;text-transform:uppercase;
margin-bottom:10px;border:1px solid rgba(88,166,255,.3)}
.insight-text{color:#c9d1d9;font-size:.92rem;line-height:1.8;font-weight:400}
.metric-premium{background:linear-gradient(145deg,#1a1f3a,#2d3561);
border:2px solid rgba(88,166,255,.15);border-radius:18px;padding:22px;text-align:center;
box-shadow:0 4px 16px rgba(0,0,0,.3)}
.stDownloadButton>button{background:linear-gradient(135deg,#1f6feb,#388bfd,#58a6ff)!important;
color:white!important;border:none!important;border-radius:16px!important;padding:16px 38px!important;
font-weight:900!important;font-size:1rem!important;box-shadow:0 8px 32px rgba(31,111,235,.4)!important;
transition:all .4s!important;letter-spacing:.5px;text-transform:uppercase}
.stDownloadButton>button:hover{box-shadow:0 12px 48px rgba(31,111,235,.6)!important;
transform:translateY(-4px) scale(1.05)!important;
background:linear-gradient(135deg,#1f6feb,#58a6ff,#79c0ff)!important}
</style>
""", unsafe_allow_html=True)

# ── COLUMN MAPPING ───────────────────────────────────────────────
COLUMN_MAP = {
    'إدارة العميل': 'Department',
    'الخدمة': 'Service',
    'التصنيف الرئيسي': 'Main Category',
    'التصنيف الفرعي': 'Sub Category',
    'مسند الى': 'Assigned To'
}

C_DEPT_AR = 'إدارة العميل'
C_SVC_AR  = 'الخدمة'
C_MAIN_AR = 'التصنيف الرئيسي'
C_SUB_AR  = 'التصنيف الفرعي'
C_AGENT_AR= 'مسند الى'

C_DEPT = 'Department'
C_SVC  = 'Service'
C_MAIN = 'Main Category'
C_SUB  = 'Sub Category'
C_AGENT= 'Assigned To'

# ── TRANSLATIONS ─────────────────────────────────────────────────
T = {
    'AR': {
        'title':'لوحة تحليلات مكتب الدعم التقني','subtitle':'تقرير احترافي متقدم',
        'upload':'📂 رفع الملف','pdf_lang':'🌐 اللغة','dept_filter':'🏢 الإدارة',
        'svc_filter':'⚙️ الخدمة','main_filter':'🔥 الفئة','top_n':'🔢 أعلى',
        'theme':'🎨 النمط','all':'الكل','total_rec':'السجلات',
        'departments':'الإدارات','svc_types':'الخدمات','issue_types':'المشكلات',
        'agents':'الموظفون','tab_overview':'📊 عامة','tab_issues':'🔥 المشكلات',
        'tab_dept':'🏢 الإدارات','tab_agents':'👨‍💻 الموظفون','tab_trend':'📈 التوجهات',
        'tab_raw':'🗃️ البيانات','kpi_sec':'📌 المؤشرات','ai_insights':'🤖 الرؤى',
        'tab_heatmap':'🧊 Heatmap','tab_quality':'✅ الجودة'
    },
    'EN': {
        'title':'IT Helpdesk Analytics','subtitle':'Premium Enterprise Report',
        'upload':'📂 Upload Data','pdf_lang':'🌐 Language','dept_filter':'🏢 Department',
        'svc_filter':'⚙️ Service','main_filter':'🔥 Category','top_n':'🔢 Top N',
        'theme':'🎨 Theme','all':'All','total_rec':'Records',
        'departments':'Departments','svc_types':'Services','issue_types':'Issues',
        'agents':'Agents','tab_overview':'📊 Overview','tab_issues':'🔥 Issues',
        'tab_dept':'🏢 Departments','tab_agents':'👨‍💻 Agents','tab_trend':'📈 Trends',
        'tab_raw':'🗃️ Data','kpi_sec':'📌 KPIs','ai_insights':'🤖 Insights',
        'tab_heatmap':'🧊 Heatmap','tab_quality':'✅ Quality'
    }
}

# ── SIDEBAR (UPLOAD + LANGUAGE) ─────────────────────────────────
with st.sidebar:
    st.markdown(
        "<div style='text-align:center;padding:20px 0 12px'>"
        "<div style='background:linear-gradient(135deg,#1f6feb,#58a6ff);display:inline-block;"
        "border-radius:20px;padding:16px 20px;font-size:2.4rem;box-shadow:0 8px 32px rgba(31,111,235,.4)'>🖥️</div>"
        "</div>", unsafe_allow_html=True)
    lang = st.radio("🌐 Language", ["EN","AR"], horizontal=True)
    tx = T[lang]
    st.markdown(
        f"<h3 style='text-align:center;color:#58a6ff!important;margin:6px 0 14px;"
        f"font-size:1rem;font-weight:900;letter-spacing:1px'>{tx['title']}</h3>",
        unsafe_allow_html=True)
    st.markdown(
        f"<div style='text-align:center;font-size:.78rem;font-weight:700;"
        f"color:{'#3fb950' if FONT_OK else '#d29922'}'>"
        f"{'✅ Arabic Font Ready' if FONT_OK else '⚠️ Loading Font'}</div>",
        unsafe_allow_html=True)
    st.markdown("---")
    uploaded = st.file_uploader(tx['upload'], type=["xlsx","xls"])
    if uploaded: st.success(f"✅ {uploaded.name}")

if not uploaded:
    st.markdown(
        f"<div style='min-height:88vh;display:flex;flex-direction:column;align-items:center;"
        f"justify-content:center;text-align:center;padding:48px'>"
        f"<div style='background:linear-gradient(135deg,#1f6feb,#58a6ff);border-radius:32px;"
        f"padding:28px;font-size:4.2rem;margin-bottom:32px;box-shadow:0 20px 60px rgba(31,111,235,.4)'>🖥️</div>"
        f"<h1 style='color:#58a6ff;font-size:3rem;font-weight:900;margin:0 0 16px;letter-spacing:-1px'>{tx['title']}</h1>"
        f"<p style='color:#7d8590;font-size:1.1rem;font-weight:500'>Upload Excel to begin analysis</p></div>",
        unsafe_allow_html=True)
    st.stop()

# ── DATA LOAD (FIXED: SAARE COLUMNS RAKHNA) ─────────────────────
@st.cache_data(show_spinner="⚙️ Processing data...")
def load_data(rb):
    # header row detect
    bh = 0
    for h in [0,1,2,3]:
        try:
            t = pd.read_excel(io.BytesIO(rb), sheet_name=0, header=h)
            if C_DEPT_AR in t.columns:
                bh = h
                break
        except:
            pass

    df = pd.read_excel(io.BytesIO(rb), sheet_name=0, header=bh)

    # total rows hatao (Grand Total, المجموع)
    if C_DEPT_AR in df.columns:
        df = df[~df[C_DEPT_AR].astype(str).str.contains('Grand Total|المجموع', na=False)]

    # forward-fill only high level columns
    for c in [C_DEPT_AR, C_SVC_AR, C_MAIN_AR, C_SUB_AR]:
        if c in df.columns:
            df[c] = df[c].replace('', pd.NA).ffill()

    # agent cleaning
    if C_AGENT_AR in df.columns:
        df[C_AGENT_AR] = df[C_AGENT_AR].astype(str).str.strip()
        df[C_AGENT_AR] = df[C_AGENT_AR].replace(
            {'nan':pd.NA,'Agent':pd.NA,'مسند الى':pd.NA,'':pd.NA}
        )

    # drop full blank rows
    df.dropna(how='all', inplace=True)
    df.reset_index(drop=True, inplace=True)

    # short agent
    if C_AGENT_AR in df.columns:
        df['_short'] = (df[C_AGENT_AR].str.replace('−متعاقد','',regex=False)
                        .str.replace('-متعاقد','',regex=False).str.strip())
    else:
        df['_short'] = pd.NA

    # rename mapping only for known columns, baaki original arabic hi rahenge
    df = df.rename(columns=COLUMN_MAP)

    # dates ko datetime
    for col in ['تاريخ الإنشاء','تاريخ حل البلاغ','تاريخ ووقت الاغلاق']:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors='coerce')

    # accuracy stats
    acc = {
        'total': len(df),
        'dept_fill':  round(df[C_DEPT].notna().sum()/len(df)*100,1)  if C_DEPT  in df.columns else 0,
        'svc_fill':   round(df[C_SVC].notna().sum()/len(df)*100,1)   if C_SVC   in df.columns else 0,
        'main_fill':  round(df[C_MAIN].notna().sum()/len(df)*100,1)  if C_MAIN  in df.columns else 0,
        'agent_fill': round(df[C_AGENT].notna().sum()/len(df)*100,1) if C_AGENT in df.columns else 0,
    }
    return df, acc

try:
    rb = uploaded.read()
    df, acc = load_data(rb)
except Exception as e:
    st.error(f"❌ {e}")
    st.stop()

if df.empty:
    st.error("❌ No data")
    st.stop()

# ── EXTRA COLUMNS: RESOLUTION / SLA FLAGS ───────────────────────
df_work = df.copy()

if 'تاريخ الإنشاء' in df_work.columns and 'تاريخ حل البلاغ' in df_work.columns:
    df_work['Resolution_Days'] = (df_work['تاريخ حل البلاغ'] - df_work['تاريخ الإنشاء']).dt.total_seconds() / (24*3600)
else:
    df_work['Resolution_Days'] = pd.NA

if 'تم خرق اتفاقية الاستجابة' in df_work.columns:
    df_work['SLA_Breach_Response'] = df_work['تم خرق اتفاقية الاستجابة'].astype(str)
else:
    df_work['SLA_Breach_Response'] = pd.NA

if 'تم خرق اتفاقية الحل' in df_work.columns:
    df_work['SLA_Breach_Resolution'] = df_work['تم خرق اتفاقية الحل'].astype(str)
else:
    df_work['SLA_Breach_Resolution'] = pd.NA

# ── HELPER: DATAFRAME → EXCEL BYTES (DOWNLOAD FIX) ───────────────
def df_to_excel_bytes(d):
    out = io.BytesIO()
    with pd.ExcelWriter(out, engine="xlsxwriter") as writer:
        d.to_excel(writer, index=False, sheet_name="Data")
    out.seek(0)
    return out.getvalue()

# ── SIDE FILTERS + PRESET ────────────────────────────────────────
with st.sidebar:
    st.markdown("---")
    pdf_lang = st.radio(tx['pdf_lang'], ["English","العربية"], horizontal=True)

    st.markdown("### 🎯 View Preset")
    preset = st.selectbox(
        "Preset",
        ["Management View","Operations View","SLA View"]
    )

    st.markdown("### 🧠 Smart Filters")
    ALL = tx['all']
    s_dep = st.multiselect(
        tx['dept_filter'],
        sorted(df_work[C_DEPT].dropna().unique().tolist()),
        default=[]
    )
    s_svc = st.multiselect(
        tx['svc_filter'],
        sorted(df_work[C_SVC].dropna().unique().tolist()),
        default=[]
    )
    s_mn = st.multiselect(
        tx['main_filter'],
        sorted(df_work[C_MAIN].dropna().unique().tolist()),
        default=[]
    )

    if 'تاريخ الإنشاء' in df_work.columns:
        st.markdown("📅 Date Range (Creation)")
        min_date = df_work['تاريخ الإنشاء'].min()
        max_date = df_work['تاريخ الإنشاء'].max()
        if pd.isna(min_date) or pd.isna(max_date):
            date_from, date_to = None, None
        else:
            date_from, date_to = st.date_input(
                "From / To",
                value=(min_date.date(), max_date.date())
            )
    else:
        date_from, date_to = None, None

    st.markdown("---")
    top_n = st.slider(tx['top_n'], 5, 30, 15)
    theme = st.selectbox(tx['theme'], ["plotly_dark","plotly_white","ggplot2"])

# filter apply
dff = df_work.copy()
if s_dep:
    dff = dff[dff[C_DEPT].isin(s_dep)]
if s_svc:
    dff = dff[dff[C_SVC].isin(s_svc)]
if s_mn:
    dff = dff[dff[C_MAIN].isin(s_mn)]
if date_from and date_to and 'تاريخ الإنشاء' in dff.columns:
    dff = dff[
        (dff['تاريخ الإنشاء'] >= pd.to_datetime(date_from)) &
        (dff['تاريخ الإنشاء'] <= pd.to_datetime(date_to))
    ]

filtered = len(dff) < len(df_work)

_ag = dff[C_AGENT].dropna().value_counts()
_dp = dff[C_DEPT].dropna().value_counts()
_is = dff[C_MAIN].dropna().value_counts()
_sv = dff[C_SVC].dropna().value_counts()

ta_name = str(_ag.index[0]).replace('−متعاقد','').replace('-متعاقد','').strip() if len(_ag) else '—'
ta_cnt  = int(_ag.iloc[0]) if len(_ag) else 0
td_name = str(_dp.index[0]) if len(_dp) else '—'
td_cnt  = int(_dp.iloc[0]) if len(_dp) else 0
ti_name = str(_is.index[0]) if len(_is) else '—'
ti_cnt  = int(_is.iloc[0]) if len(_is) else 0
cov     = round(dff[C_AGENT].notna().sum()/max(len(dff),1)*100,1)

def sec(l):
    st.markdown(f"<div class='sec-premium'>{l}</div>", unsafe_allow_html=True)

def ccfg(fig, h=450):
    fig.update_layout(
        height=h, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        font=dict(family='Inter, sans-serif', size=12, color='#c9d1d9'),
        margin=dict(l=10,r=10,t=50,b=10),
        hoverlabel=dict(bgcolor='#161b22',font_size=12,font_color='#c9d1d9'),
        xaxis=dict(gridcolor='rgba(125,133,144,.1)',showgrid=True),
        yaxis=dict(gridcolor='rgba(125,133,144,.1)',showgrid=True))
    return fig

def fig_to_png(fig, w=900, h=420):
    try:
        return fig.to_image(format="png", width=w, height=h, scale=2)
    except:
        return None

# ── QUALITY SCORE ────────────────────────────────────────────────
def compute_data_quality(dfq):
    total = len(dfq)
    if total == 0:
        return 0, {}
    issues = {}
    for col, key in [(C_DEPT,'dept_missing'),(C_SVC,'svc_missing'),
                     (C_MAIN,'main_missing'),(C_AGENT,'agent_missing')]:
        if col in dfq.columns:
            miss = dfq[col].isna().sum()
            if miss > 0:
                issues[key] = miss

    if 'Resolution_Days' in dfq.columns:
        neg = dfq['Resolution_Days'].dropna()
        neg = (neg < 0).sum()
        if neg > 0:
            issues['negative_resolution'] = neg

    if 'الحالة' in dfq.columns and 'تاريخ حل البلاغ' in dfq.columns:
        mask = (dfq['الحالة'].astype(str).str.contains('Closed', case=False, na=False)) & \
               (dfq['تاريخ حل البلاغ'].isna())
        cnt = mask.sum()
        if cnt > 0:
            issues['closed_no_res_date'] = cnt

    score = 100
    for _, v in issues.items():
        score -= min(20, int((v/total)*100))
    score = max(score, 0)
    return score, issues

quality_score, quality_issues = compute_data_quality(df_work)

# ── PDF GENERATOR (same as pehle, thoda short) ───────────────────
def generate_premium_pdf(df_data, stats, language="English"):
    buffer = io.BytesIO()
    total = len(df_data)
    is_ar = (language == "العربية")

    doc = SimpleDocTemplate(buffer, pagesize=letter,
                            rightMargin=0.75*inch, leftMargin=0.75*inch,
                            topMargin=0.75*inch, bottomMargin=0.6*inch)
    story = []

    PRIMARY   = colors.HexColor('#1f6feb')
    ACCENT    = colors.HexColor('#58a6ff')
    SUCCESS   = colors.HexColor('#3fb950')
    WARNING   = colors.HexColor('#d29922')
    DANGER    = colors.HexColor('#f85149')
    BG        = colors.HexColor('#f6f8fa')
    WHITE     = colors.white

    base_font = AR_FONT if is_ar else 'Helvetica'
    bold_font = AR_FONT_BOLD if is_ar else 'Helvetica-Bold'
    ar_mult   = 1.8 if is_ar else 1.3

    cover_title = ParagraphStyle('CT',
        fontSize=32, textColor=PRIMARY, alignment=TA_CENTER, fontName=bold_font,
        spaceAfter=18, leading=32*ar_mult)
    cover_sub = ParagraphStyle('CS',
        fontSize=16, textColor=ACCENT, alignment=TA_CENTER, fontName=base_font,
        spaceAfter=12, leading=16*ar_mult)
    cover_meta = ParagraphStyle('CM',
        fontSize=9, textColor=colors.HexColor('#6e7681'),
        alignment=TA_CENTER, spaceAfter=6, fontName='Helvetica', leading=12)

    h1 = ParagraphStyle('H1',
        fontSize=18, textColor=PRIMARY, fontName=bold_font,
        spaceBefore=20, spaceAfter=14, leading=18*ar_mult,
        alignment=TA_RIGHT if is_ar else TA_LEFT)
    h2 = ParagraphStyle('H2',
        fontSize=14, textColor=ACCENT, fontName=bold_font,
        spaceBefore=16, spaceAfter=12, leading=14*ar_mult,
        alignment=TA_RIGHT if is_ar else TA_LEFT)
    body = ParagraphStyle('BD',
        fontSize=10, textColor=colors.HexColor('#24292f'),
        alignment=TA_RIGHT if is_ar else TA_JUSTIFY,
        leading=10*ar_mult, fontName=base_font,
        spaceBefore=8, spaceAfter=8)
    footer = ParagraphStyle('FT',
        fontSize=8, textColor=colors.HexColor('#6e7681'),
        alignment=TA_CENTER, fontName='Helvetica', leading=11)

    def tbl(data, widths, hdr_color, stripe=True):
        processed = []
        for ri,row in enumerate(data):
            out = []
            for cell in row:
                s = str(cell)
                if ri == 0:
                    out.append(s)
                else:
                    if is_ar and any('\u0600' <= c <= '\u06FF' for c in s):
                        out.append(ar(s, max_len=50))
                    else:
                        out.append(s[:50])
            processed.append(out)
        t = Table(processed, colWidths=widths, repeatRows=1)
        v_pad = 10 if is_ar else 7
        styles = [
            ('BACKGROUND',(0,0),(-1,0),hdr_color),
            ('TEXTCOLOR',(0,0),(-1,0),WHITE),
            ('FONTNAME',(0,0),(-1,0),'Helvetica-Bold'),
            ('FONTSIZE',(0,0),(-1,0),9),
            ('ALIGN',(0,0),(-1,-1),'CENTER'),
            ('FONTNAME',(0,1),(-1,-1),base_font),
            ('FONTSIZE',(0,1),(-1,-1),8.5),
            ('GRID',(0,0),(-1,-1),0.5,colors.HexColor('#d0d7de')),
            ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
            ('LEFTPADDING',(0,0),(-1,-1),8),
            ('RIGHTPADDING',(0,0),(-1,-1),8),
            ('TOPPADDING',(0,0),(-1,0),12),
            ('BOTTOMPADDING',(0,0),(-1,0),12),
            ('TOPPADDING',(0,1),(-1,-1),v_pad),
            ('BOTTOMPADDING',(0,1),(-1,-1),v_pad),
        ]
        if stripe:
            styles.append(('ROWBACKGROUNDS',(0,1),(-1,-1),[WHITE,BG]))
        t.setStyle(TableStyle(styles))
        return t

    def add_chart(fig, w_in=7.5, h_in=3.5):
        png = fig_to_png(fig, int(w_in*96), int(h_in*96))
        if png:
            story.append(Image(io.BytesIO(png), width=w_in*inch, height=h_in*inch))

    # cover
    story.append(Spacer(1,1.2*inch))
    story.append(Paragraph(
        ar("تحليلات مكتب الدعم التقني") if is_ar else "IT HELPDESK ANALYTICS",
        cover_title))
    story.append(Paragraph(
        ar("تقرير الأداء الشامل والاحترافي") if is_ar else "COMPREHENSIVE PERFORMANCE REPORT",
        cover_sub))
    story.append(Spacer(1,0.3*inch))
    story.append(HRFlowable(width="50%", thickness=3, color=PRIMARY,
                            spaceBefore=10, spaceAfter=20))

    now = datetime.now()
    story.append(Paragraph(f"<b>Report Date:</b> {now.strftime('%B %d, %Y')}", cover_meta))
    story.append(Paragraph(f"<b>Generated:</b> {now.strftime('%I:%M %p')}", cover_meta))
    story.append(Paragraph(f"<b>Data Source:</b> {uploaded.name}", cover_meta))
    story.append(Paragraph(f"<b>Total Records:</b> {total:,} tickets", cover_meta))
    story.append(Spacer(1,0.5*inch))

    story.append(Spacer(1,0.8*inch))
    story.append(HRFlowable(width="100%", thickness=0.5,
                            color=colors.HexColor('#d0d7de'), spaceAfter=10))
    story.append(Paragraph(
        ar("سري — للاستخدام الداخلي فقط") if is_ar else "CONFIDENTIAL — Internal Use Only",
        footer))
    story.append(PageBreak())

    # summary
    story.append(Paragraph(
        ar("الملخص التنفيذي") if is_ar else "EXECUTIVE SUMMARY", h1))
    story.append(Spacer(1,0.15*inch))

    exec_text = ar(f"""
يقدم هذا التقرير تحليلا شاملا ومتقدما لأداء مكتب الدعم التقني ويغطي {total:,} تذكرة دعم تم معالجتها 
تظهر نتائج التحقق من جودة البيانات تغطية بنسبة {stats['dept_fill']}٪ للإدارات ومعدل تعيين بنسبة {stats['agent_fill']}٪ 
    """) if is_ar else f"""
This report covers {total:,} support tickets with department coverage {stats['dept_fill']}% 
and agent assignment rate {stats['agent_fill']}%.
    """
    story.append(Paragraph(exec_text.strip(), body))
    story.append(Spacer(1,0.2*inch))

    kpi_data = [
        ["Metric","Value","Coverage","Status"],
        ["Total Tickets",f"{total:,}","100%","✓"],
        ["Unique Departments",f"{df_data[C_DEPT].nunique()}",
         f"{stats['dept_fill']}%","✓" if stats['dept_fill']>90 else "⚠"],
        ["Service Categories",f"{df_data[C_SVC].nunique()}",
         f"{stats['svc_fill']}%","✓" if stats['svc_fill']>90 else "⚠"],
        ["Issue Categories",f"{df_data[C_MAIN].nunique()}",
         f"{stats['main_fill']}%","✓" if stats['main_fill']>90 else "⚠"],
        ["Active Agents",f"{df_data[C_AGENT].dropna().nunique()}",
         f"{stats['agent_fill']}%","✓" if stats['agent_fill']>80 else "⚠"],
    ]
    story.append(tbl(kpi_data,[2.2*inch,1.3*inch,1.1*inch,0.7*inch],PRIMARY))
    story.append(PageBreak())

    doc.build(story)
    buffer.seek(0)
    return buffer

# ── HEADER ───────────────────────────────────────────────────────
badge = (
    " <span style=\"background:rgba(210,153,34,.15);color:#d29922;padding:4px 14px;"
    "border-radius:20px;font-size:.72rem;font-weight:900;border:1px solid rgba(210,153,34,.3)\">"
    "🔽 FILTERED</span>"
) if filtered else ""

st.markdown(
    f"<div class='premium-header'>"
    "<div style='display:flex;align-items:center;gap:22px;position:relative;z-index:1'>"
    "<div style='background:linear-gradient(135deg,#1f6feb,#58a6ff);border-radius:22px;"
    "padding:18px 22px;font-size:2.6rem;box-shadow:0 8px 32px rgba(31,111,235,.4)'>🖥️</div>"
    "<div style='flex:1'>"
    f"<h1 style='color:#58a6ff;margin:0;font-size:2rem;font-weight:900;"
    f"letter-spacing:1px;text-shadow:0 2px 12px rgba(88,166,255,.3)'>{tx['title']}</h1>"
    f"<div style='color:#7d8590;margin-top:6px;font-size:.82rem;font-weight:600;letter-spacing:.3px'>"
    f"{tx['subtitle']}</div>"
    "<div style='color:#7d8590;margin-top:10px;font-size:.84rem;display:flex;gap:16px;flex-wrap:wrap'>"
    f"<span>📄 <b style='color:#c9d1d9'>{uploaded.name}</b></span>"
    "<span style='color:#30363d'>│</span>"
    f"<span>🗂️ <b style='color:#c9d1d9'>{len(df_work):,}</b> total</span>"
    "<span style='color:#30363d'>│</span>"
    f"<span>🔽 <b style='color:#58a6ff'>{len(dff):,}</b> shown</span>"
    f"{badge}</div></div></div></div>",
    unsafe_allow_html=True
)

# ── TABS ─────────────────────────────────────────────────────────
tab1,tab2,tab3,tab4,tab5,tab6,tab7,tab8 = st.tabs([
    tx['tab_overview'], tx['tab_issues'], tx['tab_dept'],
    tx['tab_agents'], tx['tab_trend'], tx['tab_raw'],
    tx['tab_heatmap'], tx['tab_quality']
])

# OVERVIEW
with tab1:
    sec("📌 KEY PERFORMANCE INDICATORS")
    k1,k2,k3,k4,k5 = st.columns(5)
    for col,(ico,val,lbl) in zip(
        [k1,k2,k3,k4,k5],
        [
            ("🎫",len(dff),tx['total_rec']),
            ("🏢",dff[C_DEPT].nunique(),tx['departments']),
            ("⚙️",dff[C_SVC].nunique(),tx['svc_types']),
            ("🔥",dff[C_MAIN].nunique(),tx['issue_types']),
            ("👨‍💻",dff[C_AGENT].dropna().nunique(),tx['agents']),
        ]
    ):
        with col:
            st.markdown(
                f"<div class='kpi-premium'><span class='kpi-icon'>{ico}</span>"
                f"<span class='kpi-num'>{val:,}</span>"
                f"<span class='kpi-lbl'>{lbl}</span></div>",
                unsafe_allow_html=True)

    sec("⏱️ ADVANCED KPI RIBBON")
    c1,c2,c3,c4 = st.columns(4)
    with c1:
        avg_res = dff['Resolution_Days'].dropna().mean() if 'Resolution_Days' in dff.columns else None
        txt = f"{avg_res:.1f} days" if avg_res is not None else "—"
        st.markdown(
            f"<div class='metric-premium'><div style='color:#58a6ff;font-weight:800;font-size:.8rem'>"
            f"AVG RESOLUTION</div><div style='font-size:1.8rem;color:#c9d1d9;font-weight:900'>{txt}</div></div>",
            unsafe_allow_html=True)
    with c2:
        if 'SLA_Breach_Resolution' in dff.columns:
            m = dff['SLA_Breach_Resolution'].astype(str).str.upper()
            if len(m.dropna())>0:
                breach = (m.eq('TRUE')).mean()*100
                txt = f"{breach:.1f}%"
            else:
                txt = "—"
        else:
            txt = "—"
        st.markdown(
            f"<div class='metric-premium'><div style='color:#f85149;font-weight:800;font-size:.8rem'>"
            f"SLA BREACH (RES)</div><div style='font-size:1.8rem;color:#c9d1d9;font-weight:900'>{txt}</div></div>",
            unsafe_allow_html=True)
    with c3:
        if 'في إنتظار جهة خارجية' in dff.columns:
            m = dff['في إنتظار جهة خارجية'].astype(str).str.upper()
            if len(m.dropna())>0:
                ext = (m.eq('TRUE')).mean()*100
                txt = f"{ext:.1f}%"
            else:
                txt = "—"
        else:
            txt = "—"
        st.markdown(
            f"<div class='metric-premium'><div style='color:#d29922;font-weight:800;font-size:.8rem'>"
            f"WAITING EXTERNAL</div><div style='font-size:1.8rem;color:#c9d1d9;font-weight:900'>{txt}</div></div>",
            unsafe_allow_html=True)
    with c4:
        st.markdown(
            f"<div class='metric-premium'><div style='color:#3fb950;font-weight:800;font-size:.8rem'>"
            f"DATA QUALITY SCORE</div><div style='font-size:1.8rem;color:#c9d1d9;font-weight:900'>{quality_score}</div></div>",
            unsafe_allow_html=True)

    sec("🤖 INTELLIGENT INSIGHTS")
    i1,i2,i3 = st.columns(3)
    with i1:
        st.markdown(
            f"<div class='insight-card'><div class='insight-badge'>TOP DEPARTMENT</div>"
            f"<div class='insight-text'><b style='color:#58a6ff'>{td_name[:30]}</b><br>"
            f"{td_cnt:,} tickets • {round(td_cnt/max(len(dff),1)*100,1)}%</div></div>",
            unsafe_allow_html=True)
    with i2:
        st.markdown(
            f"<div class='insight-card'><div class='insight-badge'>TOP ISSUE</div>"
            f"<div class='insight-text'><b style='color:#f85149'>{ti_name[:30]}</b><br>"
            f"{ti_cnt:,} occurrences • {round(ti_cnt/max(len(dff),1)*100,1)}%</div></div>",
            unsafe_allow_html=True)
    with i3:
        st.markdown(
            f"<div class='insight-card'><div class='insight-badge'>COVERAGE</div>"
            f"<div class='insight-text'><b style='color:#3fb950'>{cov}%</b> Assignment<br>"
            f"Agent: <b>{ta_name[:25]}</b> • {ta_cnt:,} tickets</div></div>",
            unsafe_allow_html=True)

# ISSUES
with tab2:
    sec("🔥 ISSUE CATEGORY ANALYSIS")
    d = dff[C_MAIN].value_counts().head(top_n).reset_index()
    d.columns=['Issue','Count']
    fig = px.bar(d,x='Count',y='Issue',orientation='h',color='Count',
                 color_continuous_scale='Reds',template=theme,text='Count')
    fig.update_layout(yaxis={'categoryorder':'total ascending'},
                      showlegend=False,coloraxis_showscale=False)
    st.plotly_chart(ccfg(fig,max(400,top_n*35)),use_container_width=True)
    st.dataframe(d,use_container_width=True,height=450)

# DEPARTMENTS
with tab3:
    sec("🏢 DEPARTMENT PERFORMANCE")
    d = dff[C_DEPT].value_counts().head(top_n).reset_index()
    d.columns=['Dept','Tickets']
    fig = px.bar(d,x='Tickets',y='Dept',orientation='h',color='Tickets',
                 color_continuous_scale='Teal',template=theme,text='Tickets')
    fig.update_layout(yaxis={'categoryorder':'total ascending'},
                      showlegend=False,coloraxis_showscale=False)
    st.plotly_chart(ccfg(fig,520),use_container_width=True)
    st.dataframe(d,use_container_width=True,height=450)

# AGENTS
with tab4:
    if dff[C_AGENT].dropna().empty:
        st.info("⚠️ No agent data available")
    else:
        sec("👨‍💻 AGENT WORKLOAD")
        ag = (dff.dropna(subset=[C_AGENT])
                 .groupby([C_AGENT,'_short']).size()
                 .reset_index(name='Tickets')
                 .sort_values('Tickets',ascending=False)
                 .head(top_n))
        fig = px.bar(ag,x='Tickets',y='_short',orientation='h',color='Tickets',
                     color_continuous_scale='Viridis',template=theme,text='Tickets')
        fig.update_layout(yaxis={'categoryorder':'total ascending','title':'Agent'},
                          showlegend=False,coloraxis_showscale=False)
        st.plotly_chart(ccfg(fig,580),use_container_width=True)
        st.dataframe(ag[[C_AGENT,'Tickets']],use_container_width=True,height=450)

# SIMPLE TOP LISTS
with tab5:
    sec("📈 TREND SNAPSHOTS")
    t1,t2 = st.columns(2)
    with t1:
        st.markdown(
            "<div style='color:#58a6ff;font-weight:900;margin-bottom:16px'>🏢 Departments</div>",
            unsafe_allow_html=True)
        td_data = dff[C_DEPT].value_counts().head(10)
        fig_td = go.Figure(go.Bar(x=td_data.values,y=td_data.index,orientation='h',
            marker=dict(color=td_data.values,colorscale='Teal'),
            text=td_data.values,textposition='outside'))
        fig_td.update_layout(yaxis={'categoryorder':'total ascending'},showlegend=False,height=450,
                             paper_bgcolor='rgba(0,0,0,0)',
                             plot_bgcolor='rgba(0,0,0,0)',font_color='#c9d1d9')
        st.plotly_chart(fig_td,use_container_width=True)
    with t2:
        st.markdown(
            "<div style='color:#f85149;font-weight:900;margin-bottom:16px'>🔥 Issues</div>",
            unsafe_allow_html=True)
        ti_data = dff[C_MAIN].value_counts().head(10)
        fig_ti = go.Figure(go.Bar(x=ti_data.values,y=ti_data.index,orientation='h',
            marker=dict(color=ti_data.values,colorscale='Reds'),
            text=ti_data.values,textposition='outside'))
        fig_ti.update_layout(yaxis={'categoryorder':'total ascending'},showlegend=False,height=450,
                             paper_bgcolor='rgba(0,0,0,0)',
                             plot_bgcolor='rgba(0,0,0,0)',font_color='#c9d1d9')
        st.plotly_chart(fig_ti,use_container_width=True)

# RAW DATA + DOWNLOAD (FIXED)
with tab6:
    sec("🗃️ RAW DATA EXPLORER")
    sd = dff.drop(columns=['_short'],errors='ignore').copy()
    c1,c2 = st.columns([1,3])
    with c1:
        fc = st.selectbox("Column",[tx['all']]+sd.columns.tolist())
    with c2:
        sr = st.text_input("🔍 Search","")
    if sr:
        if fc == tx['all']:
            mask = sd.apply(lambda c: c.astype(str).str.contains(sr,case=False,na=False)).any(axis=1)
        else:
            mask = sd[fc].astype(str).str.contains(sr,case=False,na=False)
        sd = sd[mask]
    st.markdown(
        f"<div style='color:#7d8590;margin-bottom:8px'>"
        f"<b style='color:#58a6ff'>{len(sd):,}</b> of {len(df_work):,} records</div>",
        unsafe_allow_html=True)
    st.dataframe(sd,use_container_width=True,height=550)

    excel_bytes = df_to_excel_bytes(sd)
    st.download_button(
        "⬇️ Download Filtered Excel",
        data=excel_bytes,
        file_name="filtered_tickets.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        use_container_width=True
    )

# HEATMAP + DRILL
with tab7:
    sec("🧊 DEPARTMENT × ISSUE HEATMAP")
    if C_DEPT in dff.columns and C_MAIN in dff.columns:
        pivot = pd.crosstab(dff[C_DEPT], dff[C_MAIN])
        fig_hm = px.imshow(
            pivot,
            color_continuous_scale="Blues",
            aspect="auto",
            labels=dict(x="Issue Category", y="Department", color="Tickets")
        )
        fig_hm.update_layout(
            height=600,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font_color='#c9d1d9'
        )
        st.plotly_chart(fig_hm, use_container_width=True)
    else:
        st.info("Heatmap needs Department and Main Category columns.")

# QUALITY
with tab8:
    sec("✅ DATA QUALITY & AUDIT")
    q1,q2 = st.columns([1,2])
    with q1:
        st.markdown(
            f"<div class='metric-premium'>"
            f"<div style='color:#3fb950;font-weight:800;font-size:.8rem'>QUALITY SCORE</div>"
            f"<div style='font-size:2.4rem;color:#c9d1d9;font-weight:900'>{quality_score}</div>"
            f"</div>", unsafe_allow_html=True)
    with q2:
        st.markdown(
            "<div class='insight-card'><div class='insight-badge'>QUALITY CHECKS</div>"
            "<div class='insight-text'>"
            "• Missing key fields (Department, Service, Category, Agent)<br>"
            "• Negative or invalid resolution days<br>"
            "• Closed tickets without resolution date<br>"
            "Fix these records for 100% clean analytics."
            "</div></div>", unsafe_allow_html=True)

    if not quality_issues:
        st.success("✅ No major data issues detected.")
    else:
        st.warning("⚠️ Some data quality issues detected:")
        for k,v in quality_issues.items():
            st.write(f"- **{k}** → {v} records")

# PDF EXPORT
st.markdown("---")
sec("📄 PERFECT PDF — ENGLISH HEADERS + ARABIC DATA")

p1,p2 = st.columns([3,2])
with p1:
    st.markdown(
        f"<div class='insight-card' style='border-left:5px solid #1f6feb'>"
        f"<div class='insight-badge'>✅ 100% ACCURATE DATA</div>"
        f"<div class='insight-text'>"
        f"<b style='color:#3fb950'>English Headers • Arabic Content • Perfect RTL</b><br>"
        f"✓ Table Headers: Metric, Value, Coverage, Status<br>"
        f"✓ Data Cells: Arabic RTL safe<br>"
        f"✓ Auto Arabic→English mapping for key columns<br>"
        f"</div></div>",
        unsafe_allow_html=True)
with p2:
    if st.button("📥 Generate Perfect PDF", use_container_width=True, type="primary"):
        with st.spinner(f"🎨 Creating perfect {pdf_lang} PDF..."):
            try:
                buf = generate_premium_pdf(dff, acc, pdf_lang)
                st.success(f"✅ Perfect {pdf_lang} PDF Generated!")
                st.download_button(
                    label=f"⬇️ DOWNLOAD PERFECT {pdf_lang.upper()} PDF",
                    data=buf,
                    file_name=f"IT_Helpdesk_{pdf_lang}_{datetime.now().strftime('%Y%m%d_%H%M')}.pdf",
                    mime="application/pdf",
                    use_container_width=True
                )
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")

st.markdown(
    "<div style='text-align:center;margin-top:48px;padding-top:24px;"
    "border-top:1px solid rgba(88,166,255,.1)'>"
    "<div style='color:#7d8590;font-size:.92rem;font-weight:600'>Perfect English + Arabic Analytics</div>"
    "<div style='color:#58a6ff;font-size:.82rem;margin-top:6px;font-weight:500'>Crafted by Tarique Siddique 💙</div>"
    "</div>",
    unsafe_allow_html=True)
