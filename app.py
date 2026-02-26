# ================================================================
#   IT HELPDESK ANALYTICS — ARABIC RTL FIXED v17.0
#   Professional PDF with Proper Arabic Display
#   Author: tarique14321495
# ================================================================

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import io, os, requests
from datetime import datetime
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import (SimpleDocTemplate, Table, TableStyle,
                                Paragraph, Spacer, PageBreak, Image, HRFlowable)
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

# ── ARABIC TEXT HANDLER (CRITICAL FIX) ───────────────────────────
def ar(text):
    """Convert Arabic text to display correctly in PDF (RTL)"""
    t = str(text).strip()
    if not t or t == 'nan' or t == '':
        return ''
    # Check if text contains Arabic characters
    if ARABIC_SUPPORT and any('\u0600' <= c <= '\u06FF' for c in t):
        # Reshape Arabic text and apply bidirectional algorithm
        reshaped = reshape(t)
        return get_display(reshaped)
    return t

# ── CSS (SAME) ───────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700;800;900&display=swap');
*{font-family:'Inter',sans-serif!important;box-sizing:border-box}
.stApp{background:#020810!important}
.main .block-container{background:#020810!important;padding-top:.8rem!important;max-width:100%!important}
[data-testid="stSidebar"]{background:linear-gradient(180deg,#030912,#060f20,#030912)!important;border-right:1px solid rgba(0,212,255,.15)!important}
[data-testid="stSidebar"] label,[data-testid="stSidebar"] p,[data-testid="stSidebar"] span{color:#7aadcc!important;font-size:.83rem!important}
.glow-header{animation:glow 3s ease-in-out infinite;background:linear-gradient(135deg,#060f20,#0a1e3a,#040c1c);padding:22px 30px;border-radius:20px;margin-bottom:20px;border:1px solid rgba(0,212,255,.18)}
.kpi{background:linear-gradient(145deg,#060f20,#0b1e3a);border:1px solid rgba(0,212,255,.12);border-top:3px solid #00d4ff;border-radius:20px;padding:22px 12px 18px;text-align:center;box-shadow:0 8px 32px rgba(0,0,0,.6);transition:transform .3s;margin-bottom:12px}
.kpi:hover{transform:translateY(-6px) scale(1.02)}
.kpi-icon{font-size:1.6rem;margin-bottom:8px;display:block}
.kpi-num{font-size:2.1rem;font-weight:900;color:#00d4ff;line-height:1;display:block}
.kpi-lbl{font-size:.68rem;color:#4a7a9a;margin-top:6px;display:block;letter-spacing:1.2px;text-transform:uppercase;font-weight:700}
.sec{background:linear-gradient(90deg,rgba(0,120,255,.1),transparent);border-left:3px solid #00d4ff;border-radius:0 12px 12px 0;padding:11px 22px;margin:28px 0 16px;color:#e0f0ff;font-size:1rem;font-weight:800}
.ai-card{background:linear-gradient(135deg,#060f1c,#091a30);border:1px solid rgba(0,212,255,.15);border-left:4px solid #00d4ff;border-radius:16px;padding:18px 20px;margin-bottom:12px}
.ai-badge{display:inline-block;background:rgba(0,212,255,.12);color:#00d4ff;padding:3px 12px;border-radius:20px;font-size:.68rem;font-weight:800;letter-spacing:1px;text-transform:uppercase;margin-bottom:8px;border:1px solid rgba(0,212,255,.2)}
.ai-text{color:#b8d4ec;font-size:.88rem;line-height:1.7}
.ins-card{background:linear-gradient(135deg,#060f1c,#091a30);border:1px solid rgba(0,212,255,.1);border-radius:14px;padding:16px 18px;margin-bottom:10px}
.metric-card{background:linear-gradient(145deg,#060f20,#0b1e3a);border:1px solid rgba(0,212,255,.1);border-radius:16px;padding:20px;text-align:center}
.prog-wrap{margin-bottom:12px}
.prog-label{display:flex;justify-content:space-between;color:#7aadcc;font-size:.78rem;font-weight:600;margin-bottom:5px}
.prog-bar-bg{background:rgba(255,255,255,.05);border-radius:20px;height:12px;overflow:hidden}
.prog-bar-fill{height:12px;border-radius:20px}
.stDownloadButton>button{background:linear-gradient(135deg,#c0392b,#e74c3c,#ff6b6b)!important;color:white!important;border:none!important;border-radius:14px!important;padding:14px 32px!important;font-weight:800!important;font-size:.95rem!important;box-shadow:0 6px 28px rgba(231,76,60,.5)!important;transition:all .3s!important}
.stDownloadButton>button:hover{box-shadow:0 10px 40px rgba(231,76,60,.7)!important;transform:translateY(-4px)!important}
</style>""", unsafe_allow_html=True)

# ── TRANSLATIONS ─────────────────────────────────────────────────
T = {
    'AR': {
        'title':'لوحة تحليلات مكتب الدعم التقني','subtitle':'تقرير شامل ودقيق',
        'upload':'📂 رفع ملف Excel','pdf_lang':'🌐 لغة PDF','dept_filter':'🏢 الإدارة',
        'svc_filter':'⚙️ الخدمة','main_filter':'🔥 التصنيف','top_n':'🔢 أعلى N',
        'theme':'🎨 نمط','all':'الكل','total_rec':'السجلات',
        'departments':'الإدارات','svc_types':'الخدمات','issue_types':'المشكلات',
        'agents':'الموظفون','tab_overview':'📊 عامة','tab_issues':'🔥 المشكلات',
        'tab_dept':'🏢 الإدارات','tab_agents':'👨‍💻 الموظفون','tab_trend':'📈 الاتجاهات',
        'tab_raw':'🗃️ البيانات','kpi_sec':'📌 المؤشرات','ai_insights':'🤖 الرؤى',
        'top_agent_lbl':'أكثر موظف','top_dept_lbl':'أكثر إدارة',
        'top_issue_lbl':'أكثر مشكلة','coverage_pct':'التغطية',
        'accuracy_title':'✅ الدقة',
    },
    'EN': {
        'title':'IT Helpdesk Analytics','subtitle':'Professional Report',
        'upload':'📂 Upload Excel','pdf_lang':'🌐 PDF Language','dept_filter':'🏢 Department',
        'svc_filter':'⚙️ Service','main_filter':'🔥 Category','top_n':'🔢 Top N',
        'theme':'🎨 Theme','all':'All','total_rec':'Records',
        'departments':'Departments','svc_types':'Services','issue_types':'Issues',
        'agents':'Agents','tab_overview':'📊 Overview','tab_issues':'🔥 Issues',
        'tab_dept':'🏢 Departments','tab_agents':'👨‍💻 Agents','tab_trend':'📈 Trends',
        'tab_raw':'🗃️ Data','kpi_sec':'📌 KPIs','ai_insights':'🤖 Insights',
        'top_agent_lbl':'Top Agent','top_dept_lbl':'Top Dept',
        'top_issue_lbl':'Top Issue','coverage_pct':'Coverage',
        'accuracy_title':'✅ Accuracy',
    }
}

C_DEPT='إدارة العميل'; C_SVC='الخدمة'; C_MAIN='التصنيف الرئيسي'
C_SUB='التصنيف الفرعي'; C_AGENT='مسند الى'

# ── SIDEBAR ──────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("<div style='text-align:center;padding:16px 0 8px'>"
                "<div style='background:linear-gradient(135deg,#0038a0,#00aaff);display:inline-block;"
                "border-radius:16px;padding:12px 16px;font-size:2rem'>🖥️</div></div>",
                unsafe_allow_html=True)
    lang = st.radio("🌐 Language", ["EN","AR"], horizontal=True)
    tx = T[lang]
    st.markdown(f"<h3 style='text-align:center;color:#00d4ff!important;margin:4px 0 12px;"
                f"font-size:.92rem;font-weight:800'>{tx['title']}</h3>", unsafe_allow_html=True)
    st.markdown(f"<div style='text-align:center;font-size:.75rem;font-weight:700;color:{'#00dc78' if FONT_OK else '#ffc800'}'>"
                f"{'✅ Arabic Ready' if FONT_OK else '⚠️ Loading'}</div>", unsafe_allow_html=True)
    st.markdown("---")
    uploaded = st.file_uploader(tx['upload'], type=["xlsx","xls"])
    if uploaded: st.success(f"✅ {uploaded.name}")

if not uploaded:
    st.markdown(
        f"<div style='min-height:85vh;display:flex;flex-direction:column;align-items:center;"
        f"justify-content:center;text-align:center;padding:40px'>"
        f"<div style='background:linear-gradient(135deg,#0038a0,#00aaff);border-radius:28px;"
        f"padding:22px;font-size:3.8rem;margin-bottom:26px'>🖥️</div>"
        f"<h1 style='color:#00d4ff;font-size:2.8rem;font-weight:900;margin:0 0 14px'>{tx['title']}</h1>"
        f"<p style='color:#4a7a9a;font-size:1.05rem'>Upload Excel</p></div>",
        unsafe_allow_html=True)
    st.stop()

# ── LOAD DATA ────────────────────────────────────────────────────
@st.cache_data(show_spinner="⚙️ Loading...")
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
    theme = st.selectbox(tx['theme'], ["plotly_dark","plotly","ggplot2"])

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
    st.markdown(f"<div class='sec'>{l}</div>", unsafe_allow_html=True)

def ccfg(fig, h=450):
    fig.update_layout(
        height=h, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        font_color='#7aadcc', margin=dict(l=10,r=10,t=50,b=10),
        hoverlabel=dict(bgcolor='#0a1e38',font_size=12),
        xaxis=dict(gridcolor='rgba(255,255,255,.04)'),
        yaxis=dict(gridcolor='rgba(255,255,255,.04)'))
    return fig

def ins(label, value, sub, color):
    return (f"<div class='ins-card' style='border-left:3px solid {color}'>"
            f"<div style='color:#4a7a9a;font-size:.68rem;font-weight:800;text-transform:uppercase'>{label}</div>"
            f"<div style='color:#e0f0ff;font-size:.9rem;font-weight:800;margin-top:6px'>{value}</div>"
            f"<div style='color:{color};font-size:.8rem;margin-top:4px;font-weight:600'>{sub}</div></div>")

def pbar(label, val, mx, cnt, color="#00d4ff"):
    p = round(val/mx*100) if mx else 0
    s = (label[:28]+'…') if len(label)>28 else label
    return (f"<div class='prog-wrap'><div class='prog-label'><span>{s}</span>"
            f"<span>{cnt:,} ({p}%)</span></div>"
            f"<div class='prog-bar-bg'><div class='prog-bar-fill' "
            f"style='width:{p}%;background:linear-gradient(90deg,#0038a0,{color})'></div></div></div>")

# ── CHART TO PNG ─────────────────────────────────────────────────
def fig_to_png(fig, w=900, h=420):
    try:
        return fig.to_image(format="png", width=w, height=h, scale=1.5)
    except:
        return None

# ══════════════════════════════════════════════════════════════════
# ARABIC RTL PDF GENERATOR — FIXED
# ══════════════════════════════════════════════════════════════════
def generate_professional_pdf(df_data, stats, language="English"):
    buffer = io.BytesIO()
    total = len(df_data)
    is_ar = (language == "العربية")

    doc = SimpleDocTemplate(buffer, pagesize=landscape(A4),
                            rightMargin=27, leftMargin=27,
                            topMargin=30, bottomMargin=25)
    story = []

    # ── COLORS ───────────────────────────────────────────────────
    NAVY     = colors.HexColor('#003090')
    BLUE     = colors.HexColor('#0070e0')
    TEAL     = colors.HexColor('#008b8b')
    GREEN    = colors.HexColor('#00a080')
    RED      = colors.HexColor('#e05050')
    GRAY     = colors.HexColor('#666666')
    LIGHTGRAY= colors.HexColor('#f5f5f5')
    WHITE    = colors.white

    # ── STYLES WITH RTL SUPPORT ──────────────────────────────────
    cover_title = ParagraphStyle('CT', fontSize=32, textColor=NAVY,
                                  alignment=TA_CENTER, fontName=AR_FONT if is_ar else 'Helvetica-Bold',
                                  spaceAfter=12, leading=38)
    cover_sub = ParagraphStyle('CS', fontSize=16, textColor=BLUE,
                               alignment=TA_CENTER, fontName=AR_FONT if is_ar else 'Helvetica',
                               spaceAfter=8)
    cover_date = ParagraphStyle('CD', fontSize=11, textColor=GRAY,
                                alignment=TA_CENTER, spaceAfter=6, fontName='Helvetica')
    h1 = ParagraphStyle('H1', fontSize=18, textColor=NAVY,
                        fontName=AR_FONT if is_ar else 'Helvetica-Bold',
                        spaceBefore=16, spaceAfter=10,
                        alignment=TA_RIGHT if is_ar else TA_LEFT)
    h2 = ParagraphStyle('H2', fontSize=14, textColor=BLUE,
                        fontName=AR_FONT if is_ar else 'Helvetica-Bold',
                        spaceBefore=12, spaceAfter=8,
                        alignment=TA_RIGHT if is_ar else TA_LEFT)
    h3 = ParagraphStyle('H3', fontSize=11, textColor=GRAY,
                        fontName=AR_FONT if is_ar else 'Helvetica-Bold',
                        spaceBefore=8, spaceAfter=6,
                        alignment=TA_RIGHT if is_ar else TA_LEFT)
    body = ParagraphStyle('BD', fontSize=9.5, textColor=colors.HexColor('#333'),
                          alignment=TA_RIGHT if is_ar else TA_JUSTIFY,
                          leading=13, fontName=AR_FONT if is_ar else 'Helvetica')
    footer_style = ParagraphStyle('FT', fontSize=7.5, textColor=GRAY,
                                   alignment=TA_CENTER, fontName='Helvetica')

    # ── HELPER FUNCS ─────────────────────────────────────────────
    def tbl(data, widths, hdr_color):
        t = Table(data, colWidths=widths, repeatRows=1)
        t.setStyle(TableStyle([
            ('BACKGROUND',    (0,0), (-1,0),  hdr_color),
            ('TEXTCOLOR',     (0,0), (-1,0),  WHITE),
            ('FONTNAME',      (0,0), (-1,0),  AR_FONT if is_ar else 'Helvetica-Bold'),
            ('FONTSIZE',      (0,0), (-1,0),  9.5),
            ('ALIGN',         (0,0), (-1,-1), 'CENTER'),
            ('FONTNAME',      (0,1), (-1,-1), AR_FONT),
            ('FONTSIZE',      (0,1), (-1,-1), 8.5),
            ('GRID',          (0,0), (-1,-1), 0.5, hdr_color),
            ('ROWBACKGROUNDS',(0,1), (-1,-1), [WHITE, LIGHTGRAY]),
            ('VALIGN',        (0,0), (-1,-1), 'MIDDLE'),
            ('LEFTPADDING',   (0,0), (-1,-1), 8),
            ('RIGHTPADDING',  (0,0), (-1,-1), 8),
            ('TOPPADDING',    (0,1), (-1,-1), 6),
            ('BOTTOMPADDING', (0,1), (-1,-1), 6),
        ]))
        return t

    def add_chart(fig, w_in=10.2, h_in=3.8):
        png = fig_to_png(fig, int(w_in*96), int(h_in*96))
        if png:
            story.append(Image(io.BytesIO(png), width=w_in*inch, height=h_in*inch))

    def two_charts(fig1, fig2, h_in=3.2):
        p1 = fig_to_png(fig1, 560, int(h_in*96))
        p2 = fig_to_png(fig2, 560, int(h_in*96))
        if p1 and p2:
            row = Table(
                [[Image(io.BytesIO(p1), width=4.8*inch, height=h_in*inch),
                  Image(io.BytesIO(p2), width=4.8*inch, height=h_in*inch)]],
                colWidths=[5*inch, 5*inch]
            )
            story.append(row)

    # ══════════════════════════════════════════════════════════════
    # PAGE 1 — COVER (FIXED ARABIC)
    # ══════════════════════════════════════════════════════════════
    story.append(Spacer(1, 1.5*inch))
    story.append(Paragraph(
        ar("تحليلات مكتب الدعم التقني") if is_ar else "IT HELPDESK ANALYTICS",
        cover_title))
    story.append(Paragraph(
        ar("تقرير الأداء الشامل والمفصل") if is_ar else "COMPREHENSIVE PERFORMANCE REPORT",
        cover_sub))
    story.append(Spacer(1, 0.3*inch))
    story.append(HRFlowable(width="60%", thickness=2, color=BLUE, spaceAfter=20))
    
    now = datetime.now()
    story.append(Paragraph(f"Report Date: {now.strftime('%B %d, %Y')}", cover_date))
    story.append(Paragraph(f"Generated: {now.strftime('%I:%M %p')}", cover_date))
    story.append(Paragraph(f"Data Source: {uploaded.name}", cover_date))
    
    story.append(Spacer(1, 0.5*inch))
    
    # Key metrics (FIXED ARABIC)
    boxes_data = [
        ["🎫", ar("إجمالي التذاكر") if is_ar else "Total Tickets", f"{total:,}"],
        ["🏢", ar("الإدارات") if is_ar else "Departments", f"{df_data[C_DEPT].nunique()}"],
        ["👨‍💻", ar("الموظفون النشطون") if is_ar else "Active Agents", f"{df_data[C_AGENT].dropna().nunique()}"],
    ]
    
    for row_data in boxes_data:
        box = Table([row_data], colWidths=[0.6*inch, 4*inch, 2*inch])
        box.setStyle(TableStyle([
            ('BACKGROUND',  (0,0), (-1,-1), colors.HexColor('#f8f9fa')),
            ('FONTSIZE',    (0,0), (0,0),   16),
            ('ALIGN',       (0,0), (0,0),   'CENTER'),
            ('FONTNAME',    (1,0), (1,0),   AR_FONT if is_ar else 'Helvetica-Bold'),
            ('FONTSIZE',    (1,0), (1,0),   10),
            ('TEXTCOLOR',   (1,0), (1,0),   NAVY),
            ('ALIGN',       (1,0), (1,0),   'RIGHT' if is_ar else 'LEFT'),
            ('FONTNAME',    (2,0), (2,0),   'Helvetica-Bold'),
            ('FONTSIZE',    (2,0), (2,0),   12),
            ('TEXTCOLOR',   (2,0), (2,0),   BLUE),
            ('ALIGN',       (2,0), (2,0),   'CENTER'),
            ('VALIGN',      (0,0), (-1,-1), 'MIDDLE'),
            ('LEFTPADDING', (0,0), (-1,-1), 10),
            ('RIGHTPADDING',(0,0), (-1,-1), 10),
            ('TOPPADDING',  (0,0), (-1,-1), 8),
            ('BOTTOMPADDING',(0,0),(-1,-1), 8),
            ('BOX',         (0,0), (-1,-1), 1, BLUE),
        ]))
        story.append(box)
        story.append(Spacer(1, 0.15*inch))
    
    story.append(Spacer(1, 0.8*inch))
    story.append(HRFlowable(width="100%", thickness=0.5, color=GRAY, spaceAfter=8))
    story.append(Paragraph(
        ar("سري — للاستخدام الداخلي فقط") if is_ar else "CONFIDENTIAL — For Internal Use Only",
        footer_style))
    story.append(PageBreak())

    # ══════════════════════════════════════════════════════════════
    # PAGE 2 — EXECUTIVE SUMMARY (FIXED ARABIC)
    # ══════════════════════════════════════════════════════════════
    story.append(Paragraph(
        ar("الملخص التنفيذي") if is_ar else "EXECUTIVE SUMMARY",
        h1))
    story.append(Spacer(1, 0.15*inch))
    
    exec_text = ar(f"""
يقدم هذا التقرير تحليلاً شاملاً لأداء مكتب الدعم التقني ويغطي {total:,} تذكرة دعم. 
يكشف التحليل عن مؤشرات الأداء التشغيلية الرئيسية وأنماط توزيع الخدمات ومؤشرات أداء الموظفين.
يُظهر التحقق من جودة البيانات تغطية {stats['dept_fill']}٪ للإدارات ومعدل تعيين {stats['agent_fill']}٪ 
للموظفين، مما يضمن رؤى موثوقة لاتخاذ القرارات الاستراتيجية.
    """) if is_ar else f"""
This report provides a comprehensive analysis of IT Helpdesk performance covering {total:,} support tickets. 
The analysis reveals key operational metrics, service distribution patterns, and agent performance indicators.
Data quality verification shows {stats['dept_fill']}% department coverage and {stats['agent_fill']}% 
agent assignment rate, ensuring reliable insights for strategic decision-making.
    """
    story.append(Paragraph(exec_text.strip(), body))
    story.append(Spacer(1, 0.25*inch))

    # KPI TABLE (FIXED ARABIC HEADERS)
    story.append(Paragraph(
        ar("مؤشرات الأداء الرئيسية") if is_ar else "Key Performance Indicators",
        h2))
    
    kpi_headers = [
        ar("المؤشر") if is_ar else "Metric",
        ar("القيمة") if is_ar else "Value",
        ar("التغطية") if is_ar else "Coverage"
    ]
    
    kpi_rows = [
        [ar("إجمالي التذاكر") if is_ar else "Total Tickets", f"{total:,}", "100%"],
        [ar("الإدارات الفريدة") if is_ar else "Unique Departments", 
         f"{df_data[C_DEPT].nunique()}", f"{stats['dept_fill']}%"],
        [ar("أنواع الخدمات") if is_ar else "Service Types",
         f"{df_data[C_SVC].nunique()}", f"{stats['svc_fill']}%"],
        [ar("فئات المشكلات") if is_ar else "Issue Categories",
         f"{df_data[C_MAIN].nunique()}", f"{stats['main_fill']}%"],
        [ar("الموظفون النشطون") if is_ar else "Active Agents",
         f"{df_data[C_AGENT].dropna().nunique()}", f"{stats['agent_fill']}%"],
        [ar("تغطية الموظفين") if is_ar else "Agent Coverage",
         f"{cov}%", "—"],
    ]
    
    story.append(tbl([kpi_headers] + kpi_rows, [3.2*inch, 2*inch, 1.8*inch], NAVY))
    story.append(Spacer(1, 0.25*inch))

    # TOP PERFORMERS TABLE (FIXED ARABIC)
    story.append(Paragraph(
        ar("أفضل الأداء والمقاييس الحرجة") if is_ar else "Top Performers & Critical Metrics",
        h2))
    
    top_headers = [
        ar("الفئة") if is_ar else "Category",
        ar("الأول") if is_ar else "Top Item",
        ar("التذاكر") if is_ar else "Tickets",
        ar("٪ من الإجمالي") if is_ar else "% of Total"
    ]
    
    top_rows = [
        [ar("أكثر إدارة") if is_ar else "Busiest Department",
         ar(_dp.index[0])[:45] if len(_dp) else 'N/A',
         f"{int(_dp.iloc[0]):,}" if len(_dp) else '0',
         f"{round(_dp.iloc[0]/total*100,1)}%" if len(_dp) else '0%'],
        [ar("أكثر مشكلة") if is_ar else "Top Issue",
         ar(_is.index[0])[:45] if len(_is) else 'N/A',
         f"{int(_is.iloc[0]):,}" if len(_is) else '0',
         f"{round(_is.iloc[0]/total*100,1)}%" if len(_is) else '0%'],
        [ar("أكثر موظف نشاطاً") if is_ar else "Most Active Agent",
         ar(_ag.index[0])[:45] if len(_ag) else 'N/A',
         f"{int(_ag.iloc[0]):,}" if len(_ag) else '0',
         f"{round(_ag.iloc[0]/total*100,1)}%" if len(_ag) else '0%'],
    ]
    
    story.append(tbl([top_headers] + top_rows, [2.5*inch, 3.8*inch, 1.2*inch, 1*inch], GREEN))
    story.append(PageBreak())

    # ══════════════════════════════════════════════════════════════
    # PAGE 3 — CHARTS (ENGLISH ONLY FOR CLARITY)
    # ══════════════════════════════════════════════════════════════
    story.append(Paragraph(
        ar("توزيع أنواع الخدمات وفئات المشكلات") if is_ar else "SERVICE & ISSUE DISTRIBUTION",
        h1))
    story.append(Spacer(1, 0.15*inch))

    svc_df = dff[C_SVC].value_counts().reset_index()
    svc_df.columns = ['Service','Count']
    fig_svc = px.pie(svc_df, values='Count', names='Service',
                     title='Service Distribution', hole=0.5,
                     template='plotly_white', color_discrete_sequence=px.colors.sequential.Blues_r)
    fig_svc.update_traces(textposition='inside', textinfo='percent+label', textfont_size=10)
    fig_svc.update_layout(paper_bgcolor='white', plot_bgcolor='white',
                          font_color='#333', margin=dict(l=10,r=10,t=50,b=10))

    mc_df = dff[C_MAIN].value_counts().head(8).reset_index()
    mc_df.columns = ['Category','Count']
    fig_mc = px.pie(mc_df, values='Count', names='Category',
                    title='Top 8 Issues', hole=0.5,
                    template='plotly_white', color_discrete_sequence=px.colors.sequential.Reds_r)
    fig_mc.update_traces(textposition='inside', textinfo='percent+label', textfont_size=10)
    fig_mc.update_layout(paper_bgcolor='white', plot_bgcolor='white',
                         font_color='#333', margin=dict(l=10,r=10,t=50,b=10))

    two_charts(fig_svc, fig_mc, 3.2)
    story.append(Spacer(1, 0.2*inch))

    # DEPT BAR
    dv = dff[C_DEPT].value_counts().head(15).reset_index()
    dv.columns = ['Dept','Count']
    fig_dv = px.bar(dv, x='Count', y='Dept', orientation='h', color='Count',
                    color_continuous_scale='Teal', template='plotly_white',
                    text='Count', title='Top 15 Departments')
    fig_dv.update_layout(yaxis={'categoryorder':'total ascending'}, showlegend=False,
                         coloraxis_showscale=False, paper_bgcolor='white',
                         plot_bgcolor='white', font_color='#333',
                         margin=dict(l=10,r=10,t=50,b=10))
    fig_dv.update_traces(textposition='outside', marker_line_width=0)
    add_chart(fig_dv, 10.2, 4.2)
    story.append(PageBreak())

    # ══════════════════════════════════════════════════════════════
    # PAGE 4 — ISSUES TABLE (FIXED ARABIC)
    # ══════════════════════════════════════════════════════════════
    story.append(Paragraph(
        ar("تحليل عميق لفئات المشكلات") if is_ar else "ISSUE ANALYSIS",
        h1))
    story.append(Spacer(1, 0.15*inch))

    d = dff[C_MAIN].value_counts().head(15).reset_index()
    d.columns = ['Issue','Count']
    fig_is = px.bar(d, x='Count', y='Issue', orientation='h', color='Count',
                    color_continuous_scale='Reds', template='plotly_white',
                    text='Count', title='Top 15 Issues')
    fig_is.update_layout(yaxis={'categoryorder':'total ascending'}, showlegend=False,
                         coloraxis_showscale=False, paper_bgcolor='white',
                         plot_bgcolor='white', font_color='#333',
                         margin=dict(l=10,r=10,t=50,b=10))
    fig_is.update_traces(textposition='outside')
    add_chart(fig_is, 10.2, 4.5)
    
    story.append(Spacer(1, 0.2*inch))
    story.append(Paragraph(
        ar("أعلى 20 مشكلة — تفصيل دقيق") if is_ar else "Top 20 Issues — Detailed",
        h3))
    
    issue_headers = [
        '#',
        ar("فئة المشكلة") if is_ar else "Issue Category",
        ar("العدد") if is_ar else "Count",
        '%',
        ar("الأولوية") if is_ar else "Priority"
    ]
    
    i_rows = [issue_headers]
    for i,(name,cnt) in enumerate(_is.head(20).items(),1):
        pct = round(cnt/total*100,1)
        pri = (ar("حرج") if pct>10 else ar("عالي") if pct>5 else ar("متوسط")) if is_ar else (
              'Critical' if pct>10 else 'High' if pct>5 else 'Medium')
        i_rows.append([str(i), ar(name)[:50], f"{int(cnt):,}", f"{pct}%", pri])
    story.append(tbl(i_rows, [0.4*inch, 4.5*inch, 1*inch, 0.8*inch, 1*inch], RED))
    story.append(PageBreak())

    # ══════════════════════════════════════════════════════════════
    # PAGE 5 — DEPARTMENTS TABLE (FIXED ARABIC)
    # ══════════════════════════════════════════════════════════════
    story.append(Paragraph(
        ar("تحليل أداء الإدارات") if is_ar else "DEPARTMENT PERFORMANCE",
        h1))
    story.append(Spacer(1, 0.15*inch))

    d2 = dff[C_DEPT].value_counts().head(15).reset_index()
    d2.columns = ['Dept','Count']
    fig_dp = px.bar(d2, x='Count', y='Dept', orientation='h', color='Count',
                    color_continuous_scale='Blues', template='plotly_white',
                    text='Count', title='Top 15 Departments')
    fig_dp.update_layout(yaxis={'categoryorder':'total ascending'}, showlegend=False,
                         coloraxis_showscale=False, paper_bgcolor='white',
                         plot_bgcolor='white', font_color='#333',
                         margin=dict(l=10,r=10,t=50,b=10))
    fig_dp.update_traces(textposition='outside')
    add_chart(fig_dp, 10.2, 4.2)
    
    story.append(Spacer(1, 0.2*inch))
    story.append(Paragraph(
        ar("أعلى 20 إدارة — تحليل الحمل") if is_ar else "Top 20 Departments — Load",
        h3))
    
    dept_headers = [
        '#',
        ar("الإدارة") if is_ar else "Department",
        ar("التذاكر") if is_ar else "Tickets",
        '%',
        ar("مستوى الحمل") if is_ar else "Load"
    ]
    
    d_rows = [dept_headers]
    for i,(name,cnt) in enumerate(_dp.head(20).items(),1):
        pct = round(cnt/total*100,1)
        load = (ar("حرج") if pct>10 else ar("عالي") if pct>5 else ar("عادي")) if is_ar else (
               'Critical' if pct>10 else 'High' if pct>5 else 'Normal')
        d_rows.append([str(i), ar(name)[:50], f"{int(cnt):,}", f"{pct}%", load])
    story.append(tbl(d_rows, [0.4*inch, 4.5*inch, 1*inch, 0.8*inch, 1*inch], BLUE))
    story.append(PageBreak())

    # ══════════════════════════════════════════════════════════════
    # PAGE 6 — AGENTS TABLE (FIXED ARABIC NAMES)
    # ══════════════════════════════════════════════════════════════
    if not df_data[C_AGENT].dropna().empty:
        story.append(Paragraph(
            ar("أداء الموظفين وتوزيع أحمال العمل") if is_ar else "AGENT PERFORMANCE",
            h1))
        story.append(Spacer(1, 0.15*inch))

        ag = (dff.dropna(subset=[C_AGENT])
                 .groupby([C_AGENT,'_short']).size()
                 .reset_index(name='Tickets')
                 .sort_values('Tickets', ascending=False)
                 .head(15))

        fig_ag = px.bar(ag, x='Tickets', y='_short', orientation='h', color='Tickets',
                        color_continuous_scale='Viridis', template='plotly_white',
                        text='Tickets', title='Top 15 Agents')
        fig_ag.update_layout(yaxis={'categoryorder':'total ascending','title':'Agent'},
                             showlegend=False, coloraxis_showscale=False,
                             paper_bgcolor='white', plot_bgcolor='white',
                             font_color='#333', margin=dict(l=10,r=10,t=50,b=10))
        fig_ag.update_traces(textposition='outside')
        add_chart(fig_ag, 10.2, 4.2)
        
        story.append(Spacer(1, 0.2*inch))
        story.append(Paragraph(
            ar("أعلى 25 موظف — الأسماء الكاملة بالعربية") if is_ar else "Top 25 Agents — Full Names",
            h3))
        
        agent_headers = [
            '#',
            ar("الاسم الكامل للموظف") if is_ar else "Agent Full Name",
            ar("التذاكر") if is_ar else "Tickets",
            '%',
            ar("الأداء") if is_ar else "Performance"
        ]
        
        a_rows = [agent_headers]
        for i,(name,cnt) in enumerate(_ag.head(25).items(),1):
            pct = round(cnt/total*100,1)
            perf = (ar("ممتاز") if pct>5 else ar("جيد") if pct>2 else ar("متوسط")) if is_ar else (
                   'Excellent' if pct>5 else 'Good' if pct>2 else 'Average')
            # CRITICAL FIX: Use ar() function for agent names
            a_rows.append([str(i), ar(str(name))[:50], f"{int(cnt):,}", f"{pct}%", perf])
        story.append(tbl(a_rows, [0.4*inch, 4.5*inch, 1*inch, 0.8*inch, 1*inch], GREEN))

    # FOOTER
    story.append(Spacer(1, 0.5*inch))
    story.append(HRFlowable(width="100%", thickness=0.5, color=GRAY, spaceAfter=8))
    story.append(Paragraph(
        f"IT Helpdesk Analytics  |  {now.strftime('%B %d, %Y')}  |  Made by Tarique Siddique",
        footer_style))

    doc.build(story)
    buffer.seek(0)
    return buffer

# ══════════════════════════════════════════════════════════════════
# DASHBOARD (SAME — ONLY PDF FIXED)
# ══════════════════════════════════════════════════════════════════
badge = (' <span style="background:rgba(255,200,0,.12);color:#ffc800;padding:3px 12px;'
         'border-radius:20px;font-size:.72rem;font-weight:800">🟡</span>') if filtered else ""

st.markdown(
    f"<div class='glow-header'>"
    "<div style='display:flex;align-items:center;gap:18px'>"
    "<div style='background:linear-gradient(135deg,#0038a0,#0090ff);border-radius:18px;"
    "padding:16px;font-size:2.2rem'>🖥️</div>"
    "<div style='flex:1'>"
    f"<h1 style='color:#00d4ff;margin:0;font-size:1.8rem;font-weight:900'>{tx['title']}</h1>"
    f"<div style='color:#4a7a9a;margin-top:4px;font-size:.78rem;font-weight:600'>{tx['subtitle']}</div>"
    "<div style='color:#4a7a9a;margin-top:8px;font-size:.82rem;display:flex;gap:14px;flex-wrap:wrap'>"
    f"<span>📄 <b style='color:#7aadcc'>{uploaded.name}</b></span>"
    "<span style='color:#1a3060'>│</span>"
    f"<span>🗂️ <b>{len(df):,}</b></span>"
    "<span style='color:#1a3060'>│</span>"
    f"<span>🔽 <b style='color:#00d4ff'>{len(dff):,}</b></span>"
    f"{badge}</div></div></div></div>",
    unsafe_allow_html=True)

tab1,tab2,tab3,tab4,tab5,tab6 = st.tabs([
    tx['tab_overview'], tx['tab_issues'], tx['tab_dept'],
    tx['tab_agents'], tx['tab_trend'], tx['tab_raw']])

with tab1:
    sec(tx['accuracy_title'])
    c1,c2,c3,c4,c5 = st.columns(5)
    for col,(ico,val,lbl,clr) in zip([c1,c2,c3,c4,c5],[
        ("🗂️",f"{acc['total']:,}","Total","#00d4ff"),
        ("🏢",f"{acc['dept_fill']}%","Dept","#40e0a0"),
        ("⚙️",f"{acc['svc_fill']}%","Service","#40e0a0"),
        ("🔥",f"{acc['main_fill']}%","Category","#40e0a0"),
        ("👨‍💻",f"{acc['agent_fill']}%","Agent","#ffc800"),
    ]):
        with col:
            st.markdown(
                f"<div class='metric-card'>"
                f"<div style='font-size:1.4rem'>{ico}</div>"
                f"<div style='font-size:1.6rem;font-weight:900;color:{clr};margin:6px 0'>{val}</div>"
                f"<div style='font-size:.65rem;color:#4a7a9a;font-weight:700;text-transform:uppercase'>{lbl}</div></div>",
                unsafe_allow_html=True)

    sec(tx['kpi_sec'])
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
                f"<div class='kpi'><span class='kpi-icon'>{ico}</span>"
                f"<span class='kpi-num'>{val:,}</span>"
                f"<span class='kpi-lbl'>{lbl}</span></div>",
                unsafe_allow_html=True)

    sec(tx['ai_insights'])
    a1,a2,a3 = st.columns(3)
    with a1:
        st.markdown(f"<div class='ai-card'><div class='ai-badge'>🏢</div>"
                    f"<div class='ai-text'><b style='color:#00d4ff'>{td_name[:28]}</b> — {td_cnt:,}</div></div>",
                    unsafe_allow_html=True)
    with a2:
        st.markdown(f"<div class='ai-card'><div class='ai-badge'>🔥</div>"
                    f"<div class='ai-text'><b style='color:#ff6060'>{ti_name[:28]}</b> — {ti_cnt:,}</div></div>",
                    unsafe_allow_html=True)
    with a3:
        st.markdown(f"<div class='ai-card'><div class='ai-badge'>📋</div>"
                    f"<div class='ai-text'><b style='color:#40e0a0'>{cov}%</b> assigned</div></div>",
                    unsafe_allow_html=True)

    st.markdown("---")
    r1,r2 = st.columns(2)
    with r1:
        sv = dff[C_SVC].value_counts().reset_index(); sv.columns=['Service','Count']
        fig = px.pie(sv,values='Count',names='Service',title='Services',hole=0.5,template=theme)
        fig.update_traces(textposition='inside',textinfo='percent+label')
        st.plotly_chart(ccfg(fig,380),use_container_width=True)
    with r2:
        mc = dff[C_MAIN].value_counts().head(8).reset_index(); mc.columns=['Category','Count']
        fig = px.pie(mc,values='Count',names='Category',title='Top 8',hole=0.5,template=theme)
        fig.update_traces(textposition='inside',textinfo='percent+label')
        st.plotly_chart(ccfg(fig,380),use_container_width=True)

with tab2:
    sec("🔥 Issues")
    d = dff[C_MAIN].value_counts().head(top_n).reset_index(); d.columns=['Issue','Count']
    fig = px.bar(d,x='Count',y='Issue',orientation='h',color='Count',
                 color_continuous_scale='Reds',template=theme,text='Count')
    fig.update_layout(yaxis={'categoryorder':'total ascending'},showlegend=False,coloraxis_showscale=False)
    fig.update_traces(textposition='outside')
    st.plotly_chart(ccfg(fig,max(380,top_n*32)),use_container_width=True)
    st.dataframe(d,use_container_width=True,height=400)

with tab3:
    sec("🏢 Departments")
    d = dff[C_DEPT].value_counts().head(top_n).reset_index(); d.columns=['Dept','Tickets']
    c1,c2 = st.columns(2)
    with c1:
        fig = px.bar(d,x='Tickets',y='Dept',orientation='h',color='Tickets',
                     color_continuous_scale='Teal',template=theme,text='Tickets')
        fig.update_layout(yaxis={'categoryorder':'total ascending'},showlegend=False,coloraxis_showscale=False)
        fig.update_traces(textposition='outside')
        st.plotly_chart(ccfg(fig,500),use_container_width=True)
    with c2:
        fig2 = px.pie(d,values='Tickets',names='Dept',hole=0.44,template=theme)
        fig2.update_traces(textposition='inside',textinfo='percent+label')
        st.plotly_chart(ccfg(fig2,500),use_container_width=True)
    st.dataframe(d,use_container_width=True,height=400)

with tab4:
    if dff[C_AGENT].dropna().empty:
        st.info("⚠️ No agent data")
    else:
        sec("👨‍💻 Agents")
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
            st.plotly_chart(ccfg(fig,560),use_container_width=True)
        with c2:
            fig2 = px.pie(ag,values='Tickets',names='_short',hole=0.44,template=theme)
            fig2.update_traces(textposition='inside',textinfo='percent+label')
            st.plotly_chart(ccfg(fig2,560),use_container_width=True)
        ad = ag[[C_AGENT,'Tickets']].copy(); ad.columns=['Full Name','Tickets']
        st.dataframe(ad,use_container_width=True,height=400)

with tab5:
    sec("📈 Trends")
    t1,t2 = st.columns(2)
    with t1:
        st.markdown("<div style='color:#00d4ff;font-weight:800;font-size:.9rem;margin-bottom:14px'>🏢 Departments</div>",
                    unsafe_allow_html=True)
        td = dff[C_DEPT].value_counts().head(12)
        mx = int(td.iloc[0]) if len(td) else 1
        st.markdown(
            "<div style='background:rgba(255,255,255,.02);border:1px solid rgba(0,212,255,.08);"
            "border-radius:16px;padding:18px 22px'>" +
            "".join([pbar(str(n),int(v),mx,int(v)) for n,v in td.items()]) +
            "</div>", unsafe_allow_html=True)
    with t2:
        st.markdown("<div style='color:#ff6060;font-weight:800;font-size:.9rem;margin-bottom:14px'>🔥 Issues</div>",
                    unsafe_allow_html=True)
        ti = dff[C_MAIN].value_counts().head(12)
        mx2 = int(ti.iloc[0]) if len(ti) else 1
        st.markdown(
            "<div style='background:rgba(255,255,255,.02);border:1px solid rgba(0,212,255,.08);"
            "border-radius:16px;padding:18px 22px'>" +
            "".join([pbar(str(n),int(v),mx2,int(v),"#ff4060") for n,v in ti.items()]) +
            "</div>", unsafe_allow_html=True)

with tab6:
    sec("🗃️ Raw Data")
    sd = dff.drop(columns=['_short'],errors='ignore').copy()
    c1,c2 = st.columns([1,3])
    with c1: fc = st.selectbox("Column",[tx['all']]+sd.columns.tolist())
    with c2: sr = st.text_input("🔍 Search","")
    if sr:
        mask = (sd.apply(lambda c: c.astype(str).str.contains(sr,case=False,na=False)).any(axis=1)
                if fc==tx['all'] else sd[fc].astype(str).str.contains(sr,case=False,na=False))
        sd = sd[mask]
    st.markdown(f"<div style='color:#4a7a9a;font-size:.83rem'>"
                f"<b style='color:#00d4ff'>{len(sd):,}</b> of <b>{len(df):,}</b></div>",
                unsafe_allow_html=True)
    st.dataframe(sd,use_container_width=True,height=500)

# ══════════════════════════════════════════════════════════════════
# PDF EXPORT (FIXED ARABIC RTL)
# ══════════════════════════════════════════════════════════════════
st.markdown("---")
sec("📄 Professional PDF — Arabic RTL Fixed")

p1,p2,p3 = st.columns([2,1,2])
with p1:
    st.markdown(
        f"<div class='ai-card'><div class='ai-badge'>✅ ARABIC RTL FIXED</div>"
        f"<div class='ai-text'>"
        f"<b style='color:#00dc78'>Arabic Text Displays Correctly</b><br>"
        f"✓ Cover Page — Arabic Names<br>"
        f"✓ Executive Summary — RTL Text<br>"
        f"✓ All Tables — Arabic Headers + Data<br>"
        f"✓ Agent Names — Full Arabic (No ■■■■)<br>"
        f"✓ English/العربية — Both Work<br>"
        f"✓ 6 Pages — Client Ready"
        f"</div></div>",
        unsafe_allow_html=True)
with p2:
    st.markdown(
        "<div style='text-align:center;padding:35px 0'>"
        "<div style='font-size:5rem'>📥</div>"
        "<div style='color:#00dc78;font-size:1.1rem;font-weight:900;margin-top:14px'>RTL FIXED</div>"
        "<div style='color:#00d4ff;font-size:.95rem;font-weight:800'>6 PAGES</div>"
        "</div>", unsafe_allow_html=True)
with p3:
    if st.button("📥 Generate PDF", use_container_width=True, type="primary"):
        with st.spinner(f"🎨 Creating {pdf_lang} PDF..."):
            try:
                buf = generate_professional_pdf(dff, acc, pdf_lang)
                st.success(f"✅ {pdf_lang} PDF Ready — Arabic RTL Fixed!")
                st.download_button(
                    label=f"⬇️ DOWNLOAD {pdf_lang.upper()} REPORT",
                    data=buf,
                    file_name=f"Helpdesk_{pdf_lang}_{datetime.now().strftime('%Y%m%d_%H%M')}.pdf",
                    mime="application/pdf",
                    use_container_width=True
                )
            except Exception as e:
                st.error(f"❌ {str(e)}")

st.markdown(
    "<div style='text-align:center;margin-top:40px;color:#4a7a9a;font-size:.88rem'>"
    "Made by Tarique Siddique 💙</div>",
    unsafe_allow_html=True)
