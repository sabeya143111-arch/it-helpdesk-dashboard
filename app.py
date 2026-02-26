# ================================================================
#   IT HELPDESK ANALYTICS — PREMIUM USA CLIENT EDITION v18.0
#   McKinsey-Level Professional Report with Advanced Insights
#   Author: tarique14321495
# ================================================================

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import io, os, requests
from datetime import datetime
from reportlab.lib.pagesizes import A4, landscape, letter
from reportlab.lib.units import inch, cm
from reportlab.lib import colors
from reportlab.platypus import (SimpleDocTemplate, Table, TableStyle,
                                Paragraph, Spacer, PageBreak, Image, HRFlowable,
                                KeepTogether, FrameBreak)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
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

# ── AUTO ARABIC FONT ─────────────────────────────────────────────
@st.cache_resource
def load_font():
    path = "/tmp/Amiri-Regular.ttf"
    if not os.path.exists(path):
        for url in [
            "https://fonts.gstatic.com/s/amiri/v27/J7aRnpd8CGxBHqUpvrIw74NL.ttf",
            "https://cdn.jsdelivr.net/gh/google/fonts@main/ofl/amiri/Amiri-Regular.ttf",
        ]:
            try:
                r = requests.get(url, timeout=20)
                if r.status_code == 200:
                    open(path, 'wb').write(r.content)
                    break
            except:
                continue
    try:
        pdfmetrics.registerFont(TTFont('Amiri', path))
        return True
    except:
        return False

FONT_OK = load_font()
AR_FONT = 'Amiri' if FONT_OK else 'Helvetica'

def ar(text):
    """Convert Arabic text to display correctly (RTL)"""
    t = str(text).strip()
    if not t or t == 'nan' or t == '':
        return ''
    if ARABIC_SUPPORT and any('\u0600' <= c <= '\u06FF' for c in t):
        return get_display(reshape(t))
    return t

# ── PREMIUM CSS ──────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700;800;900&display=swap');
*{font-family:'Inter',sans-serif!important;box-sizing:border-box}
.stApp{background:linear-gradient(135deg,#0a0e27 0%,#1a1f3a 50%,#0a0e27 100%)!important}
.main .block-container{background:transparent!important;padding-top:.8rem!important;max-width:100%!important}
[data-testid="stSidebar"]{background:linear-gradient(180deg,#0d1117,#161b22,#0d1117)!important;border-right:2px solid rgba(88,166,255,.2)!important;box-shadow:4px 0 20px rgba(0,0,0,.5)}
[data-testid="stSidebar"] label,[data-testid="stSidebar"] p,[data-testid="stSidebar"] span{color:#8ab4f8!important;font-size:.84rem!important;font-weight:500}
@keyframes premium-glow{0%,100%{box-shadow:0 8px 32px rgba(88,166,255,.15),inset 0 1px 0 rgba(255,255,255,.1)}50%{box-shadow:0 12px 48px rgba(88,166,255,.25),inset 0 1px 0 rgba(255,255,255,.15)}}
@keyframes slide-up{from{opacity:0;transform:translateY(30px)}to{opacity:1;transform:translateY(0)}}
.premium-header{animation:premium-glow 4s ease-in-out infinite,slide-up .8s ease;background:linear-gradient(135deg,#1a1f3a,#2d3561,#1a1f3a);padding:28px 36px;border-radius:24px;margin-bottom:24px;border:2px solid rgba(88,166,255,.25);position:relative;overflow:hidden}
.premium-header::before{content:'';position:absolute;top:-50%;left:-50%;width:200%;height:200%;background:radial-gradient(circle,rgba(88,166,255,.08) 0%,transparent 70%);animation:rotate 20s linear infinite}
@keyframes rotate{from{transform:rotate(0deg)}to{transform:rotate(360deg)}}
.kpi-premium{background:linear-gradient(145deg,#1a1f3a,#2d3561);border:2px solid rgba(88,166,255,.2);border-top:4px solid #58a6ff;border-radius:20px;padding:24px 14px 20px;text-align:center;box-shadow:0 8px 32px rgba(0,0,0,.4),inset 0 1px 0 rgba(255,255,255,.05);transition:all .4s cubic-bezier(.175,.885,.32,1.275);margin-bottom:14px;position:relative;overflow:hidden}
.kpi-premium::before{content:'';position:absolute;top:0;left:-100%;width:100%;height:100%;background:linear-gradient(90deg,transparent,rgba(88,166,255,.1),transparent);transition:left .6s}
.kpi-premium:hover{transform:translateY(-8px) scale(1.03);box-shadow:0 16px 48px rgba(88,166,255,.3),inset 0 2px 0 rgba(255,255,255,.1);border-top-color:#79c0ff}
.kpi-premium:hover::before{left:100%}
.kpi-icon{font-size:1.8rem;margin-bottom:10px;display:block;filter:drop-shadow(0 2px 8px rgba(88,166,255,.4))}
.kpi-num{font-size:2.4rem;font-weight:900;color:#58a6ff;line-height:1;display:block;text-shadow:0 0 20px rgba(88,166,255,.5);letter-spacing:-1px}
.kpi-lbl{font-size:.7rem;color:#7d8590;margin-top:8px;display:block;letter-spacing:1.5px;text-transform:uppercase;font-weight:800}
.sec-premium{background:linear-gradient(90deg,rgba(88,166,255,.15),transparent);border-left:4px solid #58a6ff;border-radius:0 16px 16px 0;padding:14px 28px;margin:32px 0 20px;color:#c9d1d9;font-size:1.1rem;font-weight:900;box-shadow:0 4px 16px rgba(88,166,255,.1)}
.insight-card{background:linear-gradient(135deg,#161b22,#1c2128);border:2px solid rgba(88,166,255,.2);border-left:5px solid #58a6ff;border-radius:18px;padding:20px 24px;margin-bottom:14px;transition:all .3s ease;box-shadow:0 4px 16px rgba(0,0,0,.3)}
.insight-card:hover{border-left-color:#79c0ff;box-shadow:0 8px 32px rgba(88,166,255,.2);transform:translateX(4px)}
.insight-badge{display:inline-block;background:rgba(88,166,255,.15);color:#58a6ff;padding:4px 14px;border-radius:24px;font-size:.7rem;font-weight:900;letter-spacing:1.2px;text-transform:uppercase;margin-bottom:10px;border:1px solid rgba(88,166,255,.3)}
.insight-text{color:#c9d1d9;font-size:.92rem;line-height:1.8;font-weight:400}
.metric-premium{background:linear-gradient(145deg,#1a1f3a,#2d3561);border:2px solid rgba(88,166,255,.15);border-radius:18px;padding:22px;text-align:center;box-shadow:0 4px 16px rgba(0,0,0,.3)}
.stDownloadButton>button{background:linear-gradient(135deg,#1f6feb,#388bfd,#58a6ff)!important;color:white!important;border:none!important;border-radius:16px!important;padding:16px 38px!important;font-weight:900!important;font-size:1rem!important;box-shadow:0 8px 32px rgba(31,111,235,.4)!important;transition:all .4s!important;letter-spacing:.5px;text-transform:uppercase}
.stDownloadButton>button:hover{box-shadow:0 12px 48px rgba(31,111,235,.6)!important;transform:translateY(-4px) scale(1.05)!important;background:linear-gradient(135deg,#1f6feb,#58a6ff,#79c0ff)!important}
</style>""", unsafe_allow_html=True)

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
    }
}

C_DEPT='إدارة العميل'; C_SVC='الخدمة'; C_MAIN='التصنيف الرئيسي'
C_SUB='التصنيف الفرعي'; C_AGENT='مسند الى'

# ── SIDEBAR ──────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("<div style='text-align:center;padding:20px 0 12px'>"
                "<div style='background:linear-gradient(135deg,#1f6feb,#58a6ff);display:inline-block;"
                "border-radius:20px;padding:16px 20px;font-size:2.4rem;box-shadow:0 8px 32px rgba(31,111,235,.4)'>🖥️</div>"
                "</div>", unsafe_allow_html=True)
    lang = st.radio("🌐 Language", ["EN","AR"], horizontal=True)
    tx = T[lang]
    st.markdown(f"<h3 style='text-align:center;color:#58a6ff!important;margin:6px 0 14px;"
                f"font-size:1rem;font-weight:900;letter-spacing:1px'>{tx['title']}</h3>", unsafe_allow_html=True)
    st.markdown(f"<div style='text-align:center;font-size:.78rem;font-weight:700;color:{'#3fb950' if FONT_OK else '#d29922'}'>"
                f"{'✅ Ready' if FONT_OK else '⚠️ Loading'}</div>", unsafe_allow_html=True)
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

# ── LOAD DATA ────────────────────────────────────────────────────
@st.cache_data(show_spinner="⚙️ Processing data...")
def load_data(rb):
    bh = 2
    for h in [0,1,2,3]:
        try:
            t = pd.read_excel(io.BytesIO(rb), sheet_name=0, header=h)
            if C_DEPT in t.columns: bh=h; break
        except: pass
    df = pd.read_excel(io.BytesIO(rb), sheet_name=0, header=bh)
    if C_DEPT in df.columns:
        df = df[~df[C_DEPT].astype(str).str.contains('Grand Total|المجموع', na=False)]
    keep = [c for c in [C_DEPT,C_SVC,C_MAIN,C_SUB,C_AGENT] if c in df.columns]
    df = df[keep].copy()
    for c in [C_DEPT,C_SVC,C_MAIN,C_SUB]:
        if c in df.columns: df[c] = df[c].replace('', pd.NA).ffill()
    if C_AGENT in df.columns:
        df[C_AGENT] = df[C_AGENT].astype(str).str.strip()
        df[C_AGENT] = df[C_AGENT].replace({'nan':pd.NA,'Agent':pd.NA,'مسند الى':pd.NA,'':pd.NA})
    df.dropna(how='all', inplace=True)
    mc = [c for c in [C_DEPT,C_SVC,C_MAIN] if c in df.columns]
    df = df.dropna(subset=mc, how='all')
    df.reset_index(drop=True, inplace=True)
    df['_short'] = (df[C_AGENT].str.replace('−متعاقد','',regex=False)
                    .str.replace('-متعاقد','',regex=False).str.strip()
                    if C_AGENT in df.columns else pd.NA)
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
    st.error(f"❌ {e}"); st.stop()
if df.empty: st.error("❌ No data"); st.stop()

# ── SIDEBAR FILTERS ──────────────────────────────────────────────
with st.sidebar:
    st.markdown("---")
    pdf_lang = st.radio(tx['pdf_lang'], ["English","العربية"], horizontal=True)
    st.markdown("---")
    ALL = tx['all']
    s_dep = st.selectbox(tx['dept_filter'], [ALL]+sorted(df[C_DEPT].dropna().unique().tolist()))
    s_svc = st.selectbox(tx['svc_filter'],  [ALL]+sorted(df[C_SVC].dropna().unique().tolist()))
    s_mn  = st.selectbox(tx['main_filter'], [ALL]+sorted(df[C_MAIN].dropna().unique().tolist()))
    st.markdown("---")
    top_n = st.slider(tx['top_n'], 5, 30, 15)
    theme = st.selectbox(tx['theme'], ["plotly_dark","plotly_white","ggplot2"])

dff = df.copy()
if s_dep != ALL: dff = dff[dff[C_DEPT]==s_dep]
if s_svc != ALL: dff = dff[dff[C_SVC]==s_svc]
if s_mn  != ALL: dff = dff[dff[C_MAIN]==s_mn]
filtered = len(dff) < len(df)

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

# ── CHART TO PNG ─────────────────────────────────────────────────
def fig_to_png(fig, w=900, h=420):
    try:
        return fig.to_image(format="png", width=w, height=h, scale=2)
    except:
        return None

# ══════════════════════════════════════════════════════════════════
# PREMIUM USA CLIENT PDF GENERATOR
# ══════════════════════════════════════════════════════════════════
def generate_premium_pdf(df_data, stats, language="English"):
    buffer = io.BytesIO()
    total = len(df_data)
    is_ar = (language == "العربية")

    doc = SimpleDocTemplate(buffer, pagesize=letter,
                            rightMargin=0.75*inch, leftMargin=0.75*inch,
                            topMargin=0.75*inch, bottomMargin=0.6*inch)
    story = []

    # ── PREMIUM COLORS (USA CORPORATE) ───────────────────────────
    PRIMARY   = colors.HexColor('#1f6feb')  # GitHub Blue
    ACCENT    = colors.HexColor('#58a6ff')  # Light Blue
    SUCCESS   = colors.HexColor('#3fb950')  # Green
    WARNING   = colors.HexColor('#d29922')  # Gold
    DANGER    = colors.HexColor('#f85149')  # Red
    DARK      = colors.HexColor('#0d1117')  # Almost Black
    MEDIUM    = colors.HexColor('#161b22')  # Dark Gray
    LIGHT     = colors.HexColor('#c9d1d9')  # Light Gray
    BG        = colors.HexColor('#f6f8fa')  # Light Background
    WHITE     = colors.white

    # ── PREMIUM STYLES ───────────────────────────────────────────
    cover_title = ParagraphStyle('CT', fontSize=36, textColor=PRIMARY,
                                  alignment=TA_CENTER, fontName=AR_FONT if is_ar else 'Helvetica-Bold',
                                  spaceAfter=14, leading=42, letterSpacing=1)
    cover_sub = ParagraphStyle('CS', fontSize=18, textColor=ACCENT,
                               alignment=TA_CENTER, fontName=AR_FONT if is_ar else 'Helvetica',
                               spaceAfter=10, letterSpacing=2)
    cover_meta = ParagraphStyle('CM', fontSize=10, textColor=colors.HexColor('#6e7681'),
                                alignment=TA_CENTER, spaceAfter=4, fontName='Helvetica')
    h1 = ParagraphStyle('H1', fontSize=20, textColor=PRIMARY,
                        fontName=AR_FONT if is_ar else 'Helvetica-Bold',
                        spaceBefore=18, spaceAfter=12, leading=24,
                        alignment=TA_RIGHT if is_ar else TA_LEFT, letterSpacing=0.5)
    h2 = ParagraphStyle('H2', fontSize=16, textColor=ACCENT,
                        fontName=AR_FONT if is_ar else 'Helvetica-Bold',
                        spaceBefore=14, spaceAfter=10, leading=20,
                        alignment=TA_RIGHT if is_ar else TA_LEFT)
    h3 = ParagraphStyle('H3', fontSize=13, textColor=colors.HexColor('#6e7681'),
                        fontName=AR_FONT if is_ar else 'Helvetica-Bold',
                        spaceBefore=10, spaceAfter=8,
                        alignment=TA_RIGHT if is_ar else TA_LEFT)
    body = ParagraphStyle('BD', fontSize=10.5, textColor=colors.HexColor('#24292f'),
                          alignment=TA_RIGHT if is_ar else TA_JUSTIFY,
                          leading=15, fontName=AR_FONT if is_ar else 'Helvetica',
                          spaceBefore=6, spaceAfter=6)
    footer = ParagraphStyle('FT', fontSize=8, textColor=colors.HexColor('#6e7681'),
                           alignment=TA_CENTER, fontName='Helvetica')
    bullet_style = ParagraphStyle('BL', fontSize=10.5, textColor=colors.HexColor('#24292f'),
                                   leftIndent=20, bulletIndent=10, fontName=AR_FONT if is_ar else 'Helvetica',
                                   leading=16, spaceBefore=4, spaceAfter=4,
                                   alignment=TA_RIGHT if is_ar else TA_LEFT)

    # ── HELPER FUNCTIONS ─────────────────────────────────────────
    def tbl(data, widths, hdr_color, stripe=True):
        t = Table(data, colWidths=widths, repeatRows=1)
        styles = [
            ('BACKGROUND',    (0,0), (-1,0),  hdr_color),
            ('TEXTCOLOR',     (0,0), (-1,0),  WHITE),
            ('FONTNAME',      (0,0), (-1,0),  AR_FONT if is_ar else 'Helvetica-Bold'),
            ('FONTSIZE',      (0,0), (-1,0),  10),
            ('ALIGN',         (0,0), (-1,-1), 'CENTER'),
            ('FONTNAME',      (0,1), (-1,-1), AR_FONT),
            ('FONTSIZE',      (0,1), (-1,-1), 9),
            ('GRID',          (0,0), (-1,-1), 0.5, colors.HexColor('#d0d7de')),
            ('VALIGN',        (0,0), (-1,-1), 'MIDDLE'),
            ('LEFTPADDING',   (0,0), (-1,-1), 10),
            ('RIGHTPADDING',  (0,0), (-1,-1), 10),
            ('TOPPADDING',    (0,0), (-1,0),  10),
            ('BOTTOMPADDING', (0,0), (-1,0),  10),
            ('TOPPADDING',    (0,1), (-1,-1), 7),
            ('BOTTOMPADDING', (0,1), (-1,-1), 7),
        ]
        if stripe:
            styles.append(('ROWBACKGROUNDS',(0,1), (-1,-1), [WHITE, BG]))
        t.setStyle(TableStyle(styles))
        return t

    def add_chart(fig, w_in=7.5, h_in=3.5):
        png = fig_to_png(fig, int(w_in*96), int(h_in*96))
        if png:
            story.append(Image(io.BytesIO(png), width=w_in*inch, height=h_in*inch))

    def metric_box(icon, label, value, color=PRIMARY):
        data = [[icon, label, value]]
        t = Table(data, colWidths=[0.5*inch, 3.5*inch, 2*inch])
        t.setStyle(TableStyle([
            ('BACKGROUND',  (0,0), (1,0), BG),
            ('BACKGROUND',  (2,0), (2,0), WHITE),
            ('FONTSIZE',    (0,0), (0,0), 18),
            ('ALIGN',       (0,0), (0,0), 'CENTER'),
            ('FONTNAME',    (1,0), (1,0), AR_FONT if is_ar else 'Helvetica-Bold'),
            ('FONTSIZE',    (1,0), (1,0), 11),
            ('TEXTCOLOR',   (1,0), (1,0), PRIMARY),
            ('ALIGN',       (1,0), (1,0), 'RIGHT' if is_ar else 'LEFT'),
            ('FONTNAME',    (2,0), (2,0), 'Helvetica-Bold'),
            ('FONTSIZE',    (2,0), (2,0), 14),
            ('TEXTCOLOR',   (2,0), (2,0), color),
            ('ALIGN',       (2,0), (2,0), 'CENTER'),
            ('VALIGN',      (0,0), (-1,-1), 'MIDDLE'),
            ('LEFTPADDING', (0,0), (-1,-1), 12),
            ('RIGHTPADDING',(0,0), (-1,-1), 12),
            ('TOPPADDING',  (0,0), (-1,-1), 10),
            ('BOTTOMPADDING',(0,0),(-1,-1), 10),
            ('BOX',         (0,0), (-1,-1), 1.5, color),
            ('ROUNDEDCORNERS', [12,12,12,12]),
        ]))
        return t

    # ══════════════════════════════════════════════════════════════
    # COVER PAGE (PREMIUM DESIGN)
    # ══════════════════════════════════════════════════════════════
    story.append(Spacer(1, 1.2*inch))
    story.append(Paragraph(
        ar("تحليلات مكتب الدعم التقني") if is_ar else "IT HELPDESK ANALYTICS",
        cover_title))
    story.append(Paragraph(
        ar("تقرير الأداء الشامل والاحترافي") if is_ar else "COMPREHENSIVE PERFORMANCE REPORT",
        cover_sub))
    story.append(Spacer(1, 0.3*inch))
    story.append(HRFlowable(width="50%", thickness=3, color=PRIMARY, spaceBefore=10, spaceAfter=20))
    
    now = datetime.now()
    story.append(Paragraph(f"<b>Report Date:</b> {now.strftime('%B %d, %Y')}", cover_meta))
    story.append(Paragraph(f"<b>Generated:</b> {now.strftime('%I:%M %p %Z')}", cover_meta))
    story.append(Paragraph(f"<b>Data Source:</b> {uploaded.name}", cover_meta))
    story.append(Paragraph(f"<b>Total Records:</b> {total:,} tickets analyzed", cover_meta))
    
    story.append(Spacer(1, 0.6*inch))
    
    # Executive Metrics
    metrics = [
        ("🎫", ar("إجمالي التذاكر") if is_ar else "Total Support Tickets", f"{total:,}", ACCENT),
        ("🏢", ar("الإدارات") if is_ar else "Departments Analyzed", f"{df_data[C_DEPT].nunique()}", SUCCESS),
        ("👨‍💻", ar("الموظفون") if is_ar else "Active Support Agents", f"{df_data[C_AGENT].dropna().nunique()}", PRIMARY),
    ]
    
    for icon, label, val, clr in metrics:
        story.append(metric_box(icon, label, val, clr))
        story.append(Spacer(1, 0.12*inch))
    
    story.append(Spacer(1, 1*inch))
    story.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor('#d0d7de'), spaceAfter=10))
    story.append(Paragraph(
        ar("سري — للاستخدام الداخلي فقط") if is_ar else "CONFIDENTIAL — For Internal Use Only",
        footer))
    story.append(PageBreak())

    # ══════════════════════════════════════════════════════════════
    # EXECUTIVE SUMMARY
    # ══════════════════════════════════════════════════════════════
    story.append(Paragraph(
        ar("الملخص التنفيذي") if is_ar else "EXECUTIVE SUMMARY",
        h1))
    story.append(Spacer(1, 0.15*inch))
    
    exec_text = ar(f"""
يقدم هذا التقرير تحليلاً شاملاً ومتقدماً لأداء مكتب الدعم التقني، ويغطي {total:,} تذكرة دعم تم معالجتها. 
يكشف التحليل عن مؤشرات الأداء التشغيلية الرئيسية، وأنماط توزيع الخدمات، ومؤشرات أداء الموظفين بدقة عالية.
تُظهر نتائج التحقق من جودة البيانات تغطية بنسبة {stats['dept_fill']}٪ للإدارات ومعدل تعيين بنسبة {stats['agent_fill']}٪ 
للموظفين، مما يضمن رؤى موثوقة وقابلة للتنفيذ لاتخاذ القرارات الاستراتيجية على مستوى المؤسسة.
    """) if is_ar else f"""
This comprehensive report provides an advanced analytical assessment of IT Helpdesk operations, 
covering {total:,} support tickets processed during the analysis period. The analysis reveals critical 
operational performance indicators, service distribution patterns, and agent performance metrics with 
precision. Data quality verification demonstrates {stats['dept_fill']}% department coverage and 
{stats['agent_fill']}% agent assignment rate, ensuring actionable insights for strategic decision-making.
    """
    story.append(Paragraph(exec_text.strip(), body))
    story.append(Spacer(1, 0.25*inch))

    # KEY PERFORMANCE INDICATORS
    story.append(Paragraph(
        ar("مؤشرات الأداء الرئيسية") if is_ar else "KEY PERFORMANCE INDICATORS",
        h2))
    story.append(Spacer(1, 0.1*inch))
    
    kpi_data = [
        [ar("المؤشر") if is_ar else "Metric",
         ar("القيمة") if is_ar else "Value",
         ar("التغطية") if is_ar else "Coverage",
         ar("الحالة") if is_ar else "Status"],
        [ar("إجمالي التذاكر") if is_ar else "Total Tickets",
         f"{total:,}", "100%", "✓"],
        [ar("الإدارات الفريدة") if is_ar else "Unique Departments",
         f"{df_data[C_DEPT].nunique()}", f"{stats['dept_fill']}%",
         "✓" if stats['dept_fill']>90 else "⚠"],
        [ar("أنواع الخدمات") if is_ar else "Service Categories",
         f"{df_data[C_SVC].nunique()}", f"{stats['svc_fill']}%",
         "✓" if stats['svc_fill']>90 else "⚠"],
        [ar("فئات المشكلات") if is_ar else "Issue Categories",
         f"{df_data[C_MAIN].nunique()}", f"{stats['main_fill']}%",
         "✓" if stats['main_fill']>90 else "⚠"],
        [ar("الموظفون النشطون") if is_ar else "Active Agents",
         f"{df_data[C_AGENT].dropna().nunique()}", f"{stats['agent_fill']}%",
         "✓" if stats['agent_fill']>80 else "⚠"],
        [ar("معدل التعيين") if is_ar else "Assignment Rate",
         f"{cov}%", "—",
         "✓" if cov>85 else "⚠"],
    ]
    
    story.append(tbl(kpi_data, [2.5*inch, 1.5*inch, 1.2*inch, 0.8*inch], PRIMARY))
    story.append(Spacer(1, 0.25*inch))

    # TOP PERFORMERS
    story.append(Paragraph(
        ar("أفضل الأداء والمقاييس الحرجة") if is_ar else "TOP PERFORMERS & CRITICAL METRICS",
        h2))
    story.append(Spacer(1, 0.1*inch))
    
    top_data = [
        [ar("الفئة") if is_ar else "Category",
         ar("العنصر الأول") if is_ar else "Top Item",
         ar("التذاكر") if is_ar else "Volume",
         ar("النسبة") if is_ar else "% Share"],
        [ar("أكثر إدارة") if is_ar else "Busiest Department",
         ar(_dp.index[0])[:40] if len(_dp) else 'N/A',
         f"{int(_dp.iloc[0]):,}" if len(_dp) else '0',
         f"{round(_dp.iloc[0]/total*100,1)}%" if len(_dp) else '0%'],
        [ar("أكثر مشكلة") if is_ar else "Top Issue Category",
         ar(_is.index[0])[:40] if len(_is) else 'N/A',
         f"{int(_is.iloc[0]):,}" if len(_is) else '0',
         f"{round(_is.iloc[0]/total*100,1)}%" if len(_is) else '0%'],
        [ar("أنشط موظف") if is_ar else "Most Active Agent",
         ar(_ag.index[0])[:40] if len(_ag) else 'N/A',
         f"{int(_ag.iloc[0]):,}" if len(_ag) else '0',
         f"{round(_ag.iloc[0]/total*100,1)}%" if len(_ag) else '0%'],
        [ar("أكثر خدمة") if is_ar else "Top Service Type",
         ar(_sv.index[0])[:40] if len(_sv) else 'N/A',
         f"{int(_sv.iloc[0]):,}" if len(_sv) else '0',
         f"{round(_sv.iloc[0]/total*100,1)}%" if len(_sv) else '0%'],
    ]
    
    story.append(tbl(top_data, [2.2*inch, 2.8*inch, 1*inch, 1*inch], SUCCESS))
    story.append(PageBreak())

    # ══════════════════════════════════════════════════════════════
    # VISUAL ANALYTICS (CHARTS)
    # ══════════════════════════════════════════════════════════════
    story.append(Paragraph(
        ar("التحليلات المرئية — توزيع الخدمات والمشكلات") if is_ar else "VISUAL ANALYTICS — SERVICE & ISSUE DISTRIBUTION",
        h1))
    story.append(Spacer(1, 0.15*inch))

    # Service Distribution Pie
    svc_df = dff[C_SVC].value_counts().reset_index()
    svc_df.columns = ['Service','Count']
    fig_svc = px.pie(svc_df, values='Count', names='Service',
                     title='Service Type Distribution', hole=0.45,
                     template='plotly_white',
                     color_discrete_sequence=px.colors.sequential.Blues_r)
    fig_svc.update_traces(textposition='inside', textinfo='percent+label',
                          textfont_size=11, marker=dict(line=dict(color='white', width=2)))
    fig_svc.update_layout(paper_bgcolor='white', plot_bgcolor='white',
                          font_color='#24292f', margin=dict(l=10,r=10,t=50,b=10),
                          title_font_size=14, title_font_color='#1f6feb')
    add_chart(fig_svc, 7.5, 3.2)
    story.append(Spacer(1, 0.2*inch))

    # Department Bar Chart
    dv = dff[C_DEPT].value_counts().head(12).reset_index()
    dv.columns = ['Department','Tickets']
    fig_dept = px.bar(dv, x='Tickets', y='Department', orientation='h',
                      text='Tickets', color='Tickets',
                      color_continuous_scale='Teal',
                      template='plotly_white',
                      title='Top 12 Departments by Ticket Volume')
    fig_dept.update_layout(yaxis={'categoryorder':'total ascending'},
                           showlegend=False, coloraxis_showscale=False,
                           paper_bgcolor='white', plot_bgcolor='white',
                           font_color='#24292f',
                           margin=dict(l=10,r=10,t=50,b=10),
                           title_font_size=14, title_font_color='#1f6feb')
    fig_dept.update_traces(textposition='outside', marker_line_width=0)
    add_chart(fig_dept, 7.5, 3.8)
    story.append(Spacer(1, 0.15*inch))

    # Key Insights Bullets
    story.append(Paragraph(
        ar("الرؤى الرئيسية") if is_ar else "KEY INSIGHTS",
        h3))
    
    insights = [
        f"• Top department '{td_name[:30]}' handles {round(td_cnt/total*100,1)}% of total ticket volume",
        f"• Service distribution spans {df_data[C_SVC].nunique()} distinct service categories",
        f"• Top 3 issue categories account for {round(dff[C_MAIN].value_counts().head(3).sum()/total*100,1)}% of all tickets",
        f"• Agent coverage rate of {cov}% indicates {'strong' if cov>85 else 'moderate'} assignment efficiency",
    ] if not is_ar else [
        f"• أكثر إدارة '{td_name[:30]}' تتعامل مع {round(td_cnt/total*100,1)}٪ من إجمالي التذاكر",
        f"• توزيع الخدمات يشمل {df_data[C_SVC].nunique()} فئة خدمة مميزة",
        f"• أعلى 3 فئات مشكلات تمثل {round(dff[C_MAIN].value_counts().head(3).sum()/total*100,1)}٪ من جميع التذاكر",
        f"• معدل تغطية الموظفين {cov}٪ يشير إلى كفاءة تعيين {'قوية' if cov>85 else 'متوسطة'}",
    ]
    
    for insight in insights:
        story.append(Paragraph(insight, bullet_style))
    
    story.append(PageBreak())

    # ══════════════════════════════════════════════════════════════
    # DETAILED TABLES
    # ══════════════════════════════════════════════════════════════
    story.append(Paragraph(
        ar("التحليل التفصيلي — أعلى المشكلات") if is_ar else "DETAILED ANALYSIS — TOP ISSUES",
        h1))
    story.append(Spacer(1, 0.15*inch))

    # Issues Table
    issue_headers = [
        '#',
        ar("فئة المشكلة") if is_ar else "Issue Category",
        ar("العدد") if is_ar else "Count",
        '%',
        ar("الأولوية") if is_ar else "Priority"
    ]
    
    issue_rows = [issue_headers]
    for i,(name,cnt) in enumerate(_is.head(15).items(),1):
        pct = round(cnt/total*100,1)
        pri = (ar("حرج") if pct>10 else ar("عالي") if pct>5 else ar("متوسط")) if is_ar else (
              'Critical' if pct>10 else 'High' if pct>5 else 'Medium')
        issue_rows.append([str(i), ar(name)[:45], f"{int(cnt):,}", f"{pct}%", pri])
    
    story.append(tbl(issue_rows, [0.35*inch, 3.5*inch, 0.9*inch, 0.7*inch, 0.8*inch], DANGER))
    story.append(Spacer(1, 0.25*inch))

    # Departments Table
    story.append(Paragraph(
        ar("الإدارات — تحليل الحمل") if is_ar else "DEPARTMENTS — WORKLOAD ANALYSIS",
        h2))
    story.append(Spacer(1, 0.1*inch))
    
    dept_headers = [
        '#',
        ar("الإدارة") if is_ar else "Department",
        ar("التذاكر") if is_ar else "Tickets",
        '%',
        ar("الحمل") if is_ar else "Load"
    ]
    
    dept_rows = [dept_headers]
    for i,(name,cnt) in enumerate(_dp.head(15).items(),1):
        pct = round(cnt/total*100,1)
        load = (ar("حرج") if pct>10 else ar("عالي") if pct>5 else ar("عادي")) if is_ar else (
               'Critical' if pct>10 else 'High' if pct>5 else 'Normal')
        dept_rows.append([str(i), ar(name)[:45], f"{int(cnt):,}", f"{pct}%", load])
    
    story.append(tbl(dept_rows, [0.35*inch, 3.5*inch, 0.9*inch, 0.7*inch, 0.8*inch], ACCENT))
    story.append(PageBreak())

    # ══════════════════════════════════════════════════════════════
    # AGENT PERFORMANCE
    # ══════════════════════════════════════════════════════════════
    if not df_data[C_AGENT].dropna().empty:
        story.append(Paragraph(
            ar("أداء الموظفين وتوزيع أحمال العمل") if is_ar else "AGENT PERFORMANCE & WORKLOAD DISTRIBUTION",
            h1))
        story.append(Spacer(1, 0.15*inch))

        agent_headers = [
            '#',
            ar("اسم الموظف الكامل") if is_ar else "Agent Full Name",
            ar("التذاكر") if is_ar else "Tickets",
            '%',
            ar("التقييم") if is_ar else "Rating"
        ]
        
        agent_rows = [agent_headers]
        for i,(name,cnt) in enumerate(_ag.head(20).items(),1):
            pct = round(cnt/total*100,1)
            rating = (ar("ممتاز") if pct>5 else ar("جيد") if pct>2 else ar("متوسط")) if is_ar else (
                     'Excellent' if pct>5 else 'Good' if pct>2 else 'Average')
            agent_rows.append([str(i), ar(str(name))[:45], f"{int(cnt):,}", f"{pct}%", rating])
        
        story.append(tbl(agent_rows, [0.35*inch, 3.5*inch, 0.9*inch, 0.7*inch, 0.8*inch], SUCCESS))
        story.append(Spacer(1, 0.25*inch))

    # ══════════════════════════════════════════════════════════════
    # STRATEGIC RECOMMENDATIONS
    # ══════════════════════════════════════════════════════════════
    story.append(Paragraph(
        ar("التوصيات الاستراتيجية") if is_ar else "STRATEGIC RECOMMENDATIONS",
        h1))
    story.append(Spacer(1, 0.15*inch))

    recommendations = [
        ("Resource Optimization",
         f"Redistribute workload from high-volume department ({td_name[:25]}) to optimize resource utilization and prevent agent burnout."),
        ("Capacity Planning",
         f"Review top-performing agents' capacity to ensure sustainable productivity levels while maintaining service quality standards."),
        ("Issue Prevention",
         f"Implement root cause analysis for top 3 recurring issues to reduce future ticket volume by an estimated 15-20%."),
        ("Training Investment",
         "Deploy targeted training programs for departments with lower resolution rates to improve first-contact resolution metrics."),
        ("Process Automation",
         "Automate handling of common issue categories using AI-powered chatbots to reduce average response time by 30-40%."),
        ("Performance Metrics",
         "Establish real-time dashboards for monitoring KPIs and implement predictive analytics for proactive issue management."),
    ] if not is_ar else [
        ("تحسين الموارد",
         f"إعادة توزيع العمل من الإدارة ذات الحجم الأكبر ({td_name[:25]}) لتحسين استخدام الموارد ومنع إرهاق الموظفين."),
        ("تخطيط القدرات",
         f"مراجعة قدرة الموظفين ذوي الأداء الأعلى لضمان مستويات إنتاجية مستدامة مع الحفاظ على معايير الجودة."),
        ("منع المشكلات",
         f"تنفيذ تحليل السبب الجذري لأعلى 3 مشكلات متكررة لتقليل حجم التذاكر المستقبلية بنسبة 15-20٪."),
        ("الاستثمار في التدريب",
         "نشر برامج تدريب مستهدفة للإدارات ذات معدلات الحل المنخفضة لتحسين مقاييس الحل من الاتصال الأول."),
        ("أتمتة العمليات",
         "أتمتة معالجة فئات المشكلات الشائعة باستخدام روبوتات الدردشة المدعومة بالذكاء الاصطناعي لتقليل وقت الاستجابة بنسبة 30-40٪."),
        ("مقاييس الأداء",
         "إنشاء لوحات معلومات في الوقت الفعلي لمراقبة مؤشرات الأداء وتنفيذ التحليلات التنبؤية للإدارة الاستباقية للمشكلات."),
    ]

    for i, (title, desc) in enumerate(recommendations, 1):
        rec_data = [[f"{i}.", title, desc]]
        rec_table = Table(rec_data, colWidths=[0.35*inch, 1.8*inch, 4.15*inch])
        rec_table.setStyle(TableStyle([
            ('BACKGROUND',  (0,0), (1,0), BG),
            ('BACKGROUND',  (2,0), (2,0), WHITE),
            ('FONTNAME',    (0,0), (0,0), 'Helvetica-Bold'),
            ('FONTNAME',    (1,0), (1,0), AR_FONT if is_ar else 'Helvetica-Bold'),
            ('FONTNAME',    (2,0), (2,0), AR_FONT if is_ar else 'Helvetica'),
            ('FONTSIZE',    (0,0), (2,0), 10),
            ('TEXTCOLOR',   (0,0), (1,0), PRIMARY),
            ('TEXTCOLOR',   (2,0), (2,0), colors.HexColor('#24292f')),
            ('ALIGN',       (0,0), (0,0), 'CENTER'),
            ('ALIGN',       (1,0), (1,0), 'RIGHT' if is_ar else 'LEFT'),
            ('ALIGN',       (2,0), (2,0), 'RIGHT' if is_ar else 'LEFT'),
            ('VALIGN',      (0,0), (-1,-1), 'MIDDLE'),
            ('LEFTPADDING', (0,0), (-1,-1), 12),
            ('RIGHTPADDING',(0,0), (-1,-1), 12),
            ('TOPPADDING',  (0,0), (-1,-1), 10),
            ('BOTTOMPADDING',(0,0),(-1,-1), 10),
            ('BOX',         (0,0), (-1,-1), 1.5, ACCENT),
            ('ROUNDEDCORNERS', [8,8,8,8]),
        ]))
        story.append(rec_table)
        story.append(Spacer(1, 0.12*inch))

    # FOOTER
    story.append(Spacer(1, 0.5*inch))
    story.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor('#d0d7de'), spaceAfter=10))
    story.append(Paragraph(
        f"IT Helpdesk Analytics Report  |  {now.strftime('%B %d, %Y')}  |  Prepared by Tarique Siddique",
        footer))

    doc.build(story)
    buffer.seek(0)
    return buffer

# ══════════════════════════════════════════════════════════════════
# DASHBOARD (PREMIUM UI)
# ══════════════════════════════════════════════════════════════════
badge = (' <span style="background:rgba(210,153,34,.15);color:#d29922;padding:4px 14px;'
         'border-radius:20px;font-size:.72rem;font-weight:900;border:1px solid rgba(210,153,34,.3)">🔽 FILTERED</span>') if filtered else ""

st.markdown(
    f"<div class='premium-header'>"
    "<div style='display:flex;align-items:center;gap:22px;position:relative;z-index:1'>"
    "<div style='background:linear-gradient(135deg,#1f6feb,#58a6ff);border-radius:22px;"
    "padding:18px 22px;font-size:2.6rem;box-shadow:0 8px 32px rgba(31,111,235,.4)'>🖥️</div>"
    "<div style='flex:1'>"
    f"<h1 style='color:#58a6ff;margin:0;font-size:2rem;font-weight:900;"
    f"letter-spacing:1px;text-shadow:0 2px 12px rgba(88,166,255,.3)'>{tx['title']}</h1>"
    f"<div style='color:#7d8590;margin-top:6px;font-size:.82rem;font-weight:600;letter-spacing:.3px'>{tx['subtitle']}</div>"
    "<div style='color:#7d8590;margin-top:10px;font-size:.84rem;display:flex;gap:16px;flex-wrap:wrap'>"
    f"<span>📄 <b style='color:#c9d1d9'>{uploaded.name}</b></span>"
    "<span style='color:#30363d'>│</span>"
    f"<span>🗂️ <b style='color:#c9d1d9'>{len(df):,}</b> total</span>"
    "<span style='color:#30363d'>│</span>"
    f"<span>🔽 <b style='color:#58a6ff'>{len(dff):,}</b> shown</span>"
    f"{badge}</div></div></div></div>",
    unsafe_allow_html=True)

tab1,tab2,tab3,tab4,tab5,tab6 = st.tabs([
    tx['tab_overview'], tx['tab_issues'], tx['tab_dept'],
    tx['tab_agents'], tx['tab_trend'], tx['tab_raw']])

with tab1:
    sec("📊 DATA QUALITY METRICS")
    c1,c2,c3,c4,c5 = st.columns(5)
    for col,(ico,val,lbl,clr) in zip([c1,c2,c3,c4,c5],[
        ("🗂️",f"{acc['total']:,}","Total","#58a6ff"),
        ("🏢",f"{acc['dept_fill']}%","Dept","#3fb950"),
        ("⚙️",f"{acc['svc_fill']}%","Service","#3fb950"),
        ("🔥",f"{acc['main_fill']}%","Category","#3fb950"),
        ("👨‍💻",f"{acc['agent_fill']}%","Agent","#d29922"),
    ]):
        with col:
            st.markdown(
                f"<div class='metric-premium'>"
                f"<div style='font-size:1.6rem;filter:drop-shadow(0 2px 8px {clr}66)'>{ico}</div>"
                f"<div style='font-size:1.8rem;font-weight:900;color:{clr};margin:8px 0;letter-spacing:-1px'>{val}</div>"
                f"<div style='font-size:.68rem;color:#7d8590;font-weight:800;text-transform:uppercase;letter-spacing:1.5px'>{lbl}</div></div>",
                unsafe_allow_html=True)

    sec("📌 KEY PERFORMANCE INDICATORS")
    k1,k2,k3,k4,k5 = st.columns(5)
    for col,(ico,val,lbl) in zip([k1,k2,k3,k4,k5],[
        ("🎫",len(dff),tx['total_rec']),
        ("🏢",dff[C_DEPT].nunique(),tx['departments']),
        ("⚙️",dff[C_SVC].nunique(),tx['svc_types']),
        ("🔥",dff[C_MAIN].nunique(),tx['issue_types']),
        ("👨‍💻",dff[C_AGENT].dropna().nunique(),tx['agents']),
    ]):
        with col:
            st.markdown(
                f"<div class='kpi-premium'><span class='kpi-icon'>{ico}</span>"
                f"<span class='kpi-num'>{val:,}</span>"
                f"<span class='kpi-lbl'>{lbl}</span></div>",
                unsafe_allow_html=True)

    sec("🤖 INTELLIGENT INSIGHTS")
    i1,i2,i3 = st.columns(3)
    with i1:
        st.markdown(f"<div class='insight-card'><div class='insight-badge'>TOP DEPARTMENT</div>"
                    f"<div class='insight-text'><b style='color:#58a6ff'>{td_name[:30]}</b><br>"
                    f"{td_cnt:,} tickets • {round(td_cnt/len(dff)*100,1)}% of total</div></div>",
                    unsafe_allow_html=True)
    with i2:
        st.markdown(f"<div class='insight-card'><div class='insight-badge'>TOP ISSUE</div>"
                    f"<div class='insight-text'><b style='color:#f85149'>{ti_name[:30]}</b><br>"
                    f"{ti_cnt:,} occurrences • {round(ti_cnt/len(dff)*100,1)}% share</div></div>",
                    unsafe_allow_html=True)
    with i3:
        st.markdown(f"<div class='insight-card'><div class='insight-badge'>COVERAGE</div>"
                    f"<div class='insight-text'><b style='color:#3fb950'>{cov}%</b> Assignment Rate<br>"
                    f"Agent: <b>{ta_name[:25]}</b> • {ta_cnt:,} tickets</div></div>",
                    unsafe_allow_html=True)

    st.markdown("---")
    r1,r2 = st.columns(2)
    with r1:
        sv = dff[C_SVC].value_counts().reset_index(); sv.columns=['Service','Count']
        fig = px.pie(sv,values='Count',names='Service',title='Service Distribution',
                     hole=0.45,template=theme,color_discrete_sequence=px.colors.sequential.Blues_r)
        fig.update_traces(textposition='inside',textinfo='percent+label')
        st.plotly_chart(ccfg(fig,400),use_container_width=True)
    with r2:
        mc = dff[C_MAIN].value_counts().head(8).reset_index(); mc.columns=['Category','Count']
        fig = px.pie(mc,values='Count',names='Category',title='Top 8 Issues',
                     hole=0.45,template=theme,color_discrete_sequence=px.colors.sequential.Reds_r)
        fig.update_traces(textposition='inside',textinfo='percent+label')
        st.plotly_chart(ccfg(fig,400),use_container_width=True)

with tab2:
    sec("🔥 ISSUE CATEGORY ANALYSIS")
    d = dff[C_MAIN].value_counts().head(top_n).reset_index(); d.columns=['Issue','Count']
    fig = px.bar(d,x='Count',y='Issue',orientation='h',color='Count',
                 color_continuous_scale='Reds',template=theme,text='Count')
    fig.update_layout(yaxis={'categoryorder':'total ascending'},showlegend=False,coloraxis_showscale=False)
    fig.update_traces(textposition='outside')
    st.plotly_chart(ccfg(fig,max(400,top_n*35)),use_container_width=True)
    st.dataframe(d,use_container_width=True,height=450)

with tab3:
    sec("🏢 DEPARTMENT PERFORMANCE")
    d = dff[C_DEPT].value_counts().head(top_n).reset_index(); d.columns=['Dept','Tickets']
    c1,c2 = st.columns(2)
    with c1:
        fig = px.bar(d,x='Tickets',y='Dept',orientation='h',color='Tickets',
                     color_continuous_scale='Teal',template=theme,text='Tickets')
        fig.update_layout(yaxis={'categoryorder':'total ascending'},showlegend=False,coloraxis_showscale=False)
        fig.update_traces(textposition='outside')
        st.plotly_chart(ccfg(fig,520),use_container_width=True)
    with c2:
        fig2 = px.pie(d,values='Tickets',names='Dept',hole=0.45,template=theme)
        fig2.update_traces(textposition='inside',textinfo='percent+label')
        st.plotly_chart(ccfg(fig2,520),use_container_width=True)
    st.dataframe(d,use_container_width=True,height=450)

with tab4:
    if dff[C_AGENT].dropna().empty:
        st.info("⚠️ No agent data available")
    else:
        sec("👨‍💻 AGENT WORKLOAD DISTRIBUTION")
        ag = (dff.dropna(subset=[C_AGENT])
                 .groupby([C_AGENT,'_short']).size()
                 .reset_index(name='Tickets')
                 .sort_values('Tickets',ascending=False)
                 .head(top_n))
        c1,c2 = st.columns(2)
        with c1:
            fig = px.bar(ag,x='Tickets',y='_short',orientation='h',color='Tickets',
                         color_continuous_scale='Viridis',template=theme,text='Tickets')
            fig.update_layout(yaxis={'categoryorder':'total ascending','title':'Agent'},
                              showlegend=False,coloraxis_showscale=False)
            fig.update_traces(textposition='outside')
            st.plotly_chart(ccfg(fig,580),use_container_width=True)
        with c2:
            fig2 = px.pie(ag,values='Tickets',names='_short',hole=0.45,template=theme)
            fig2.update_traces(textposition='inside',textinfo='percent+label')
            st.plotly_chart(ccfg(fig2,580),use_container_width=True)
        ad = ag[[C_AGENT,'Tickets']].copy(); ad.columns=['Full Name','Tickets']
        st.dataframe(ad,use_container_width=True,height=450)

with tab5:
    sec("📈 TREND ANALYSIS")
    t1,t2 = st.columns(2)
    with t1:
        st.markdown("<div style='color:#58a6ff;font-weight:900;font-size:1rem;margin-bottom:16px'>🏢 Department Trends</div>",
                    unsafe_allow_html=True)
        td_data = dff[C_DEPT].value_counts().head(10)
        fig_td = go.Figure(go.Bar(
            x=td_data.values,
            y=td_data.index,
            orientation='h',
            marker=dict(color=td_data.values,colorscale='Teal'),
            text=td_data.values,
            textposition='outside'
        ))
        fig_td.update_layout(yaxis={'categoryorder':'total ascending'},
                             showlegend=False,height=450,
                             paper_bgcolor='rgba(0,0,0,0)',
                             plot_bgcolor='rgba(0,0,0,0)',
                             font_color='#c9d1d9')
        st.plotly_chart(fig_td,use_container_width=True)
    with t2:
        st.markdown("<div style='color:#f85149;font-weight:900;font-size:1rem;margin-bottom:16px'>🔥 Issue Trends</div>",
                    unsafe_allow_html=True)
        ti_data = dff[C_MAIN].value_counts().head(10)
        fig_ti = go.Figure(go.Bar(
            x=ti_data.values,
            y=ti_data.index,
            orientation='h',
            marker=dict(color=ti_data.values,colorscale='Reds'),
            text=ti_data.values,
            textposition='outside'
        ))
        fig_ti.update_layout(yaxis={'categoryorder':'total ascending'},
                             showlegend=False,height=450,
                             paper_bgcolor='rgba(0,0,0,0)',
                             plot_bgcolor='rgba(0,0,0,0)',
                             font_color='#c9d1d9')
        st.plotly_chart(fig_ti,use_container_width=True)

with tab6:
    sec("🗃️ RAW DATA EXPLORER")
    sd = dff.drop(columns=['_short'],errors='ignore').copy()
    c1,c2 = st.columns([1,3])
    with c1: fc = st.selectbox("Column",[tx['all']]+sd.columns.tolist())
    with c2: sr = st.text_input("🔍 Search","")
    if sr:
        mask = (sd.apply(lambda c: c.astype(str).str.contains(sr,case=False,na=False)).any(axis=1)
                if fc==tx['all'] else sd[fc].astype(str).str.contains(sr,case=False,na=False))
        sd = sd[mask]
    st.markdown(f"<div style='color:#7d8590;font-size:.88rem;margin-bottom:8px'>"
                f"<b style='color:#58a6ff'>{len(sd):,}</b> of <b>{len(df):,}</b> records</div>",
                unsafe_allow_html=True)
    st.dataframe(sd,use_container_width=True,height=550)

# ══════════════════════════════════════════════════════════════════
# PREMIUM PDF EXPORT
# ══════════════════════════════════════════════════════════════════
st.markdown("---")
sec("📄 PREMIUM USA CLIENT PDF REPORT")

p1,p2,p3 = st.columns([2,1,2])
with p1:
    st.markdown(
        f"<div class='insight-card' style='border-left:5px solid #1f6feb'>"
        f"<div class='insight-badge'>🇺🇸 USA CLIENT EDITION</div>"
        f"<div class='insight-text'>"
        f"<b style='color:#3fb950'>McKinsey-Level Professional Report</b><br>"
        f"✓ Premium Cover Page — Corporate Design<br>"
        f"✓ Executive Summary — Strategic Insights<br>"
        f"✓ Visual Analytics — High-Res Charts<br>"
        f"✓ Detailed Tables — Top 15-20 Items<br>"
        f"✓ Strategic Recommendations — Actionable<br>"
        f"✓ English/العربية — Full RTL Support<br>"
        f"✓ Letter Size (8.5×11) — USA Standard<br>"
        f"✓ {'✅ Arabic Font Ready' if FONT_OK else '⚠️ Loading Font'}"
        f"</div></div>",
        unsafe_allow_html=True)
with p2:
    st.markdown(
        "<div style='text-align:center;padding:40px 0'>"
        "<div style='font-size:5.5rem;filter:drop-shadow(0 4px 16px rgba(31,111,235,.4))'>📥</div>"
        "<div style='color:#1f6feb;font-size:1.2rem;font-weight:900;margin-top:16px;letter-spacing:1px'>PREMIUM</div>"
        "<div style='color:#58a6ff;font-size:1rem;font-weight:800;margin-top:4px'>CLIENT PDF</div>"
        "</div>", unsafe_allow_html=True)
with p3:
    if st.button("📥 Generate Premium Report", use_container_width=True, type="primary"):
        with st.spinner(f"🎨 Creating premium {pdf_lang} PDF..."):
            try:
                buf = generate_premium_pdf(dff, acc, pdf_lang)
                st.success(f"✅ Premium {pdf_lang} PDF Generated!")
                st.download_button(
                    label=f"⬇️ DOWNLOAD {pdf_lang.upper()} REPORT",
                    data=buf,
                    file_name=f"IT_Helpdesk_Premium_{pdf_lang}_{datetime.now().strftime('%Y%m%d_%H%M')}.pdf",
                    mime="application/pdf",
                    use_container_width=True
                )
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")

st.markdown(
    "<div style='text-align:center;margin-top:48px;padding-top:24px;border-top:1px solid rgba(88,166,255,.1)'>"
    "<div style='color:#7d8590;font-size:.92rem;font-weight:600'>Premium Analytics Platform</div>"
    "<div style='color:#58a6ff;font-size:.82rem;margin-top:6px;font-weight:500'>Crafted by Tarique Siddique 💙</div>"
    "</div>",
    unsafe_allow_html=True)
