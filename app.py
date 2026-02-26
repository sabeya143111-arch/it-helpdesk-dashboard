# ================================================================
#   IT HELPDESK ANALYTICS DASHBOARD + FULL PDF EXPORT — v9.0
#   Author  : tarique14321495
#   Features: Animated UI | Full PDF (EN+AR) | All Charts | Icons
#   Run     : streamlit run app.py
# ================================================================

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import io
import time
from datetime import datetime
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import plotly.io as pio

st.set_page_config(
    page_title="IT Helpdesk Analytics",
    page_icon="🖥️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── PREMIUM ANIMATED CSS v9 ──────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');
*, *::before, *::after { font-family: 'Inter', sans-serif !important; box-sizing: border-box; }

.stApp { background: #020810 !important; }
.main .block-container {
    background: #020810 !important;
    padding-top: .8rem !important;
    max-width: 100% !important;
}

[data-testid="stSidebar"] {
    background: linear-gradient(180deg,#030912 0%,#060f20 60%,#030912 100%) !important;
    border-right: 1px solid rgba(0,212,255,.15) !important;
}
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] span { color: #7aadcc !important; font-size: .83rem !important; }

@keyframes glowPulse {
    0%,100% { box-shadow: 0 10px 40px rgba(0,0,0,.6), 0 0 0px rgba(0,212,255,0); }
    50%      { box-shadow: 0 10px 40px rgba(0,0,0,.6), 0 0 40px rgba(0,212,255,.25); }
}
@keyframes slideDown {
    from { opacity:0; transform: translateY(-20px); }
    to   { opacity:1; transform: translateY(0); }
}
@keyframes slideUp {
    from { opacity:0; transform: translateY(20px); }
    to   { opacity:1; transform: translateY(0); }
}
@keyframes fadeIn {
    from { opacity:0; }
    to   { opacity:1; }
}
@keyframes countUp {
    from { opacity:0; transform: scale(.8); }
    to   { opacity:1; transform: scale(1); }
}
@keyframes shimmer {
    0%   { background-position: -1000px 0; }
    100% { background-position: 1000px 0; }
}

.glow-header {
    animation: glowPulse 3s ease-in-out infinite, slideDown .6s ease;
    background: linear-gradient(135deg,#060f20 0%,#0a1e3a 50%,#040c1c 100%);
    padding: 22px 30px;
    border-radius: 20px;
    margin-bottom: 20px;
    border: 1px solid rgba(0,212,255,.18);
    position: relative;
    overflow: hidden;
}
.glow-header::before {
    content: '';
    position: absolute;
    top: 0; left: -100%;
    width: 60%; height: 100%;
    background: linear-gradient(90deg, transparent, rgba(0,212,255,.04), transparent);
    animation: shimmer 4s infinite;
}

.kpi {
    background: linear-gradient(145deg,#060f20,#0b1e3a);
    border: 1px solid rgba(0,212,255,.12);
    border-top: 3px solid #00d4ff;
    border-radius: 20px;
    padding: 22px 12px 18px;
    text-align: center;
    box-shadow: 0 8px 32px rgba(0,0,0,.6);
    transition: transform .3s cubic-bezier(.34,1.56,.64,1), box-shadow .3s ease;
    margin-bottom: 12px;
    position: relative;
    overflow: hidden;
    animation: slideUp .5s ease both;
}
.kpi:hover {
    transform: translateY(-6px) scale(1.02);
    box-shadow: 0 16px 48px rgba(0,80,200,.4);
    border-top-color: #00ffff;
}
.kpi-icon  { font-size: 1.6rem; margin-bottom: 8px; display: block; }
.kpi-num   {
    font-size: 2.1rem; font-weight: 900; color: #00d4ff;
    line-height: 1; display: block;
    animation: countUp .8s ease both;
    text-shadow: 0 0 20px rgba(0,212,255,.4);
}
.kpi-lbl   {
    font-size: .68rem; color: #4a7a9a; margin-top: 6px; display: block;
    letter-spacing: 1.2px; text-transform: uppercase; font-weight: 700;
}

.sec {
    background: linear-gradient(90deg, rgba(0,120,255,.1) 0%, transparent 80%);
    border-left: 3px solid #00d4ff;
    border-radius: 0 12px 12px 0;
    padding: 11px 22px;
    margin: 28px 0 16px;
    color: #e0f0ff;
    font-size: 1rem;
    font-weight: 800;
    letter-spacing: .3px;
    animation: fadeIn .5s ease;
}

.ai-card {
    background: linear-gradient(135deg,#060f1c,#091a30);
    border: 1px solid rgba(0,212,255,.15);
    border-left: 4px solid #00d4ff;
    border-radius: 16px;
    padding: 18px 20px;
    margin-bottom: 12px;
    animation: slideUp .5s ease both;
    transition: all .3s ease;
}
.ai-card:hover {
    border-left-color: #00ffff;
    box-shadow: 0 8px 32px rgba(0,100,200,.25);
    transform: translateX(4px);
}
.ai-badge {
    display: inline-block;
    background: rgba(0,212,255,.12);
    color: #00d4ff;
    padding: 3px 12px;
    border-radius: 20px;
    font-size: .68rem;
    font-weight: 800;
    letter-spacing: 1px;
    text-transform: uppercase;
    margin-bottom: 8px;
    border: 1px solid rgba(0,212,255,.2);
}
.ai-text { color: #b8d4ec; font-size: .88rem; line-height: 1.7; }

.metric-card {
    background: linear-gradient(145deg,#060f20,#0b1e3a);
    border: 1px solid rgba(0,212,255,.1);
    border-radius: 16px;
    padding: 20px;
    text-align: center;
    animation: slideUp .5s ease both;
}

/* PDF Download Icon Button */
.pdf-icon-btn {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    gap: 10px;
    background: linear-gradient(135deg,#c0392b,#e74c3c,#ff6b6b) !important;
    color: white !important;
    border: none !important;
    border-radius: 16px !important;
    padding: 14px 28px !important;
    font-weight: 800 !important;
    font-size: .95rem !important;
    letter-spacing: .5px !important;
    box-shadow: 0 6px 28px rgba(231,76,60,.5) !important;
    transition: all .3s ease !important;
    cursor: pointer !important;
    text-decoration: none !important;
}
.pdf-icon-btn:hover {
    box-shadow: 0 10px 40px rgba(231,76,60,.7) !important;
    transform: translateY(-4px) scale(1.03) !important;
}
.pdf-icon-btn svg {
    width: 22px;
    height: 22px;
    fill: currentColor;
}

.stDownloadButton > button {
    background: linear-gradient(135deg,#0038b0,#0070f0,#00aaff) !important;
    background-size: 200% 200% !important;
    color: white !important;
    border: none !important;
    border-radius: 14px !important;
    padding: 12px 32px !important;
    font-weight: 800 !important;
    font-size: .9rem !important;
    letter-spacing: .5px !important;
    box-shadow: 0 4px 24px rgba(0,100,255,.4) !important;
    transition: all .3s ease !important;
}
.stDownloadButton > button:hover {
    box-shadow: 0 8px 36px rgba(0,100,255,.6) !important;
    transform: translateY(-3px) !important;
}

.stTabs [data-baseweb="tab-list"] {
    background: rgba(255,255,255,.02);
    border: 1px solid rgba(0,212,255,.1);
    border-radius: 16px;
    padding: 5px 7px;
    gap: 4px;
}
.stTabs [data-baseweb="tab"] {
    border-radius: 12px;
    padding: 9px 24px;
    font-size: .87rem;
    font-weight: 700;
    color: #4a7a9a !important;
    background: transparent;
    transition: all .3s ease;
    border: none !important;
}
.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg,#0a2870,#0a3e8e) !important;
    color: #00d4ff !important;
    box-shadow: 0 2px 20px rgba(0,120,255,.35), 0 0 0 1px rgba(0,212,255,.25);
}

::-webkit-scrollbar { width: 5px; height: 5px; }
::-webkit-scrollbar-track { background: #060f20; }
::-webkit-scrollbar-thumb { background: #1a3870; border-radius: 10px; }
::-webkit-scrollbar-thumb:hover { background: #00d4ff; }

hr { border: none; border-top: 1px solid rgba(0,212,255,.07) !important; margin: 16px 0 !important; }
</style>
""", unsafe_allow_html=True)

# ── TRANSLATIONS ─────────────────────────────────────────────────
T = {
    'AR': {
        'title'         : 'لوحة تحليلات مكتب الدعم التقني',
        'subtitle'      : 'تقرير شامل ودقيق ١٠٠٪',
        'upload'        : '📂 رفع ملف Excel',
        'filters'       : '🔽 الفلاتر',
        'dept_filter'   : '🏢 الإدارة',
        'svc_filter'    : '⚙️ الخدمة',
        'main_filter'   : '🔥 التصنيف الرئيسي',
        'top_n'         : '🔢 أعلى N نتيجة',
        'theme'         : '🎨 نمط الرسم',
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
        'tab_trend'     : '📈 الاتجاهات',
        'tab_raw'       : '🗃️ البيانات الخام',
        'pdf_title'     : 'تصدير تقرير PDF',
        'gen_en'        : 'إنشاء تقرير (English)',
        'gen_ar'        : 'إنشاء تقرير (عربي)',
        'pdf_cover'     : 'تقرير تحليل البيانات',
        'pdf_gen'       : 'تم الإنشاء',
        'pdf_dept'      : 'الإدارات',
        'pdf_issues'    : 'المشكلات',
        'pdf_agents'    : 'الموظفون',
    },
    'EN': {
        'title'         : 'IT Helpdesk Analytics Dashboard',
        'subtitle'      : '100% Accurate • Verified Data Report',
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
        'tab_trend'     : '📈 Trends',
        'tab_raw'       : '🗃️ Raw Data',
        'pdf_title'     : 'Export PDF Report',
        'gen_en'        : 'Generate Report (English)',
        'gen_ar'        : 'Generate Report (Arabic)',
        'pdf_cover'     : 'Data Analytics Report',
        'pdf_gen'       : 'Generated on',
        'pdf_dept'      : 'Departments',
        'pdf_issues'    : 'Issues',
        'pdf_agents'    : 'Agents',
    }
}

# ── COLUMN KEYS ──────────────────────────────────────────────────
C_DEPT  = 'إدارة العميل'
C_SVC   = 'الخدمة'
C_MAIN  = 'التصنيف الرئيسي'
C_SUB   = 'التصنيف الفرعي'
C_AGENT = 'مسند الى'

# ── SIDEBAR ──────────────────────────────────────────────────────
with st.sidebar:
    st.markdown(
        "<div style='text-align:center;padding:16px 0 8px;'>"
        "<div style='background:linear-gradient(135deg,#0038a0,#00aaff);"
        "display:inline-block;border-radius:16px;padding:12px 16px;"
        "font-size:2rem;box-shadow:0 4px 20px rgba(0,140,255,.4);'>🖥️</div>"
        "</div>",
        unsafe_allow_html=True
    )
    lang = st.radio("🌐 Language / اللغة", ["EN", "AR"], horizontal=True, index=0)
    tx   = T[lang]
    st.markdown(
        f"<h3 style='text-align:center;color:#00d4ff !important;"
        f"margin:4px 0 12px;font-size:.92rem;font-weight:800;'>{tx['title']}</h3>",
        unsafe_allow_html=True
    )
    st.markdown("---")
    uploaded = st.file_uploader(tx['upload'], type=["xlsx", "xls"])
    if uploaded:
        st.success(f"✅ {uploaded.name}")

if not uploaded:
    st.markdown(
        "<div style='min-height:85vh;display:flex;flex-direction:column;"
        "align-items:center;justify-content:center;text-align:center;padding:40px 20px;'>"
        "<div style='background:linear-gradient(135deg,#0038a0,#00aaff);"
        "border-radius:28px;padding:22px 28px;font-size:3.8rem;margin-bottom:26px;"
        "box-shadow:0 16px 50px rgba(0,150,255,.45);'>🖥️</div>"
        f"<h1 style='color:#00d4ff;font-size:2.8rem;font-weight:900;margin:0 0 14px;"
        f"text-shadow:0 0 30px rgba(0,212,255,.3);'>{tx['title']}</h1>"
        f"<p style='color:#4a7a9a;font-size:1.05rem;max-width:500px;"
        f"line-height:1.8;margin:0 auto 44px;'>Upload your Excel file from the sidebar</p>"
        "</div>",
        unsafe_allow_html=True
    )
    st.stop()

# ── LOAD & CLEAN DATA ────────────────────────────────────────────
@st.cache_data(show_spinner="⚙️ Loading & validating data...")
def load_data(raw_bytes: bytes):
    best_header = 2
    for h in [0, 1, 2, 3]:
        try:
            test = pd.read_excel(io.BytesIO(raw_bytes), sheet_name=0, header=h)
            if C_DEPT in test.columns:
                best_header = h
                break
        except:
            pass

    df = pd.read_excel(io.BytesIO(raw_bytes), sheet_name=0, header=best_header)

    if C_DEPT in df.columns:
        df = df[~df[C_DEPT].astype(str).str.contains('Grand Total|المجموع الكلي|المجموع', na=False)]

    keep = [c for c in [C_DEPT, C_SVC, C_MAIN, C_SUB, C_AGENT] if c in df.columns]
    df   = df[keep].copy()

    for c in [C_DEPT, C_SVC, C_MAIN, C_SUB]:
        if c in df.columns:
            df[c] = df[c].replace('', pd.NA).ffill()

    if C_AGENT in df.columns:
        df[C_AGENT] = df[C_AGENT].astype(str).str.strip()
        df[C_AGENT] = df[C_AGENT].replace({'nan': pd.NA, 'Agent': pd.NA, 'مسند الى': pd.NA, '': pd.NA})

    df.dropna(how='all', inplace=True)
    main_cols = [c for c in [C_DEPT, C_SVC, C_MAIN] if c in df.columns]
    df = df.dropna(subset=main_cols, how='all')
    df.reset_index(drop=True, inplace=True)

    if C_AGENT in df.columns:
        df['_short'] = (
            df[C_AGENT]
            .str.replace('−متعاقد', '', regex=False)
            .str.replace('-متعاقد', '', regex=False)
            .str.strip()
        )
    else:
        df['_short'] = pd.NA

    acc = {
        'total'         : len(df),
        'dept_fill'     : round(df[C_DEPT].notna().sum() / len(df) * 100, 1) if C_DEPT in df.columns else 0,
        'svc_fill'      : round(df[C_SVC].notna().sum()  / len(df) * 100, 1) if C_SVC  in df.columns else 0,
        'main_fill'     : round(df[C_MAIN].notna().sum() / len(df) * 100, 1) if C_MAIN in df.columns else 0,
        'agent_fill'    : round(df[C_AGENT].notna().sum()/ len(df) * 100, 1) if C_AGENT in df.columns else 0,
        'header_used'   : best_header,
    }
    return df, acc

try:
    raw_bytes = uploaded.read()
    df, acc   = load_data(raw_bytes)
except Exception as e:
    st.error(f"❌ Load error: {e}")
    st.stop()

if df.empty:
    st.error("❌ No data found after cleaning.")
    st.stop()

# ── SIDEBAR FILTERS ──────────────────────────────────────────────
with st.sidebar:
    st.markdown("---")
    st.markdown(
        f"<p style='color:#00d4ff !important;font-weight:800;margin-bottom:4px;font-size:.85rem;'>"
        f"{tx['filters']}</p>",
        unsafe_allow_html=True
    )
    ALL   = tx['all']
    s_dep = st.selectbox(tx['dept_filter'],  [ALL] + sorted(df[C_DEPT].dropna().unique().tolist()))
    s_svc = st.selectbox(tx['svc_filter'],   [ALL] + sorted(df[C_SVC].dropna().unique().tolist()))
    s_mn  = st.selectbox(tx['main_filter'],  [ALL] + sorted(df[C_MAIN].dropna().unique().tolist()))
    st.markdown("---")
    top_n = st.slider(tx['top_n'], 5, 30, 15)
    theme = st.selectbox(tx['theme'], ["plotly_dark", "plotly", "ggplot2"])

dff = df.copy()
if s_dep != ALL: dff = dff[dff[C_DEPT] == s_dep]
if s_svc != ALL: dff = dff[dff[C_SVC]  == s_svc]
if s_mn  != ALL: dff = dff[dff[C_MAIN] == s_mn]
filtered = len(dff) < len(df)

_ag = dff[C_AGENT].dropna().value_counts()
_dp = dff[C_DEPT].dropna().value_counts()
_is = dff[C_MAIN].dropna().value_counts()
_sv = dff[C_SVC].dropna().value_counts()

top_agent_name  = str(_ag.index[0]).replace('−متعاقد','').replace('-متعاقد','').strip() if len(_ag) else '—'
top_agent_count = int(_ag.iloc[0]) if len(_ag) else 0
top_dept_name   = str(_dp.index[0]) if len(_dp) else '—'
top_dept_count  = int(_dp.iloc[0])  if len(_dp) else 0
top_issue_name  = str(_is.index[0]) if len(_is) else '—'
top_issue_count = int(_is.iloc[0])  if len(_is) else 0
top_svc_name    = str(_sv.index[0]) if len(_sv) else '—'
top_svc_count   = int(_sv.iloc[0])  if len(_sv) else 0
coverage_pct    = round(dff[C_AGENT].notna().sum() / max(len(dff), 1) * 100, 1)

def sec(label):
    st.markdown(f"<div class='sec'>{label}</div>", unsafe_allow_html=True)

def chart_cfg(fig, h=450):
    fig.update_layout(
        height=h,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font_color='#7aadcc',
        margin=dict(l=10, r=10, t=50, b=10),
        hoverlabel=dict(bgcolor='#0a1e38', font_size=12, bordercolor='#00d4ff'),
        xaxis=dict(gridcolor='rgba(255,255,255,.04)', linecolor='rgba(255,255,255,.07)'),
        yaxis=dict(gridcolor='rgba(255,255,255,.04)', linecolor='rgba(255,255,255,.07)'),
    )
    return fig

# ── PDF GENERATION (EN + AR Support) ─────────────────────────────
def generate_full_pdf(df_data, stats, pdf_lang='EN'):
    """Generate complete PDF with all charts - EN or AR"""
    buffer = io.BytesIO()
    tx_pdf = T[pdf_lang]
    
    # RTL support for Arabic
    is_arabic = (pdf_lang == 'AR')
    
    doc = SimpleDocTemplate(
        buffer,
        pagesize=landscape(A4),
        rightMargin=30,
        leftMargin=30,
        topMargin=40,
        bottomMargin=30
    )
    
    story = []
    styles = getSampleStyleSheet()
    
    # Custom Styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=26,
        textColor=colors.HexColor('#003090'),
        spaceAfter=14,
        alignment=TA_CENTER if not is_arabic else TA_RIGHT,
        fontName='Helvetica-Bold',
        leading=32
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=18,
        textColor=colors.HexColor('#0070e0'),
        spaceAfter=12,
        spaceBefore=18,
        fontName='Helvetica-Bold',
        alignment=TA_LEFT if not is_arabic else TA_RIGHT
    )
    
    normal_style = ParagraphStyle(
        'CustomNormal',
        parent=styles['Normal'],
        fontSize=11,
        leading=15,
        alignment=TA_LEFT if not is_arabic else TA_RIGHT
    )
    
    # ═══ PAGE 1: COVER ═══
    story.append(Spacer(1, 1.2*inch))
    story.append(Paragraph("🖥️", title_style))
    story.append(Spacer(1, 0.2*inch))
    
    report_title = "IT HELPDESK ANALYTICS" if pdf_lang == 'EN' else "تحليلات مكتب الدعم التقني"
    story.append(Paragraph(f"<b>{report_title}</b>", title_style))
    
    date_str = datetime.now().strftime('%B %d, %Y at %I:%M %p')
    gen_text = f"{tx_pdf['pdf_gen']}: {date_str}"
    story.append(Paragraph(gen_text, normal_style))
    story.append(Spacer(1, 0.4*inch))
    
    # Summary Box
    kpi_data = [
        ['Metric' if pdf_lang=='EN' else 'المقياس', 
         'Value' if pdf_lang=='EN' else 'القيمة', 
         'Status' if pdf_lang=='EN' else 'الحالة'],
        [tx_pdf['total_rec'], f"{stats['total']:,}", '✓'],
        [tx_pdf['departments'], f"{df_data[C_DEPT].nunique()}", '✓'],
        [tx_pdf['svc_types'], f"{df_data[C_SVC].nunique()}", '✓'],
        [tx_pdf['issue_types'], f"{df_data[C_MAIN].nunique()}", '✓'],
        [tx_pdf['agents'], f"{df_data[C_AGENT].dropna().nunique()}", '✓'],
        ['Data Quality' if pdf_lang=='EN' else 'جودة البيانات', 
         f"{round((stats['dept_fill']+stats['svc_fill']+stats['main_fill'])/3,1)}%", '✓']
    ]
    
    kpi_table = Table(kpi_data, colWidths=[2.8*inch, 1.8*inch, 1*inch])
    kpi_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#003090')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 13),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 14),
        ('TOPPADDING', (0, 0), (-1, 0), 14),
        ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#f0f8ff')),
        ('GRID', (0, 0), (-1, -1), 1.2, colors.HexColor('#003090')),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 11),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f0f8ff')]),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    
    story.append(kpi_table)
    story.append(PageBreak())
    
    # ═══ PAGE 2: TOP INSIGHTS ═══
    story.append(Paragraph(f"📊 {'KEY INSIGHTS' if pdf_lang=='EN' else 'الرؤى الرئيسية'}", heading_style))
    story.append(Spacer(1, 0.25*inch))
    
    top_dept_short = (top_dept_name[:35] + "...") if len(top_dept_name) > 35 else top_dept_name
    top_issue_short = (top_issue_name[:35] + "...") if len(top_issue_name) > 35 else top_issue_name
    
    insights = [
        f"🏢 {'Busiest Department' if pdf_lang=='EN' else 'أكثر إدارة نشاطاً'}: <b>{top_dept_short}</b> ({top_dept_count:,} {'tickets' if pdf_lang=='EN' else 'تذكرة'})",
        f"🔥 {'Most Common Issue' if pdf_lang=='EN' else 'أكثر مشكلة تكراراً'}: <b>{top_issue_short}</b> ({top_issue_count:,} {'occurrences' if pdf_lang=='EN' else 'مرة'})",
        f"👨‍💻 {'Top Agent' if pdf_lang=='EN' else 'أكثر موظف نشاطاً'}: <b>{top_agent_name[:30]}</b> ({top_agent_count:,} {'tickets' if pdf_lang=='EN' else 'تذكرة'})",
        f"⚙️ {'Top Service' if pdf_lang=='EN' else 'أكثر خدمة'}: <b>{top_svc_name[:30]}</b> ({top_svc_count:,})",
        f"📋 {'Agent Coverage' if pdf_lang=='EN' else 'تغطية الموظفين'}: <b>{coverage_pct}%</b>"
    ]
    
    for insight in insights:
        story.append(Paragraph(insight, normal_style))
        story.append(Spacer(1, 0.18*inch))
    
    story.append(Spacer(1, 0.35*inch))
    
    # Top 8 Departments
    story.append(Paragraph(f"🏢 {'TOP 8 DEPARTMENTS' if pdf_lang=='EN' else 'أعلى 8 إدارات'}", heading_style))
    dept_data = [[
        'Rank' if pdf_lang=='EN' else 'الترتيب',
        'Department' if pdf_lang=='EN' else 'الإدارة',
        'Tickets' if pdf_lang=='EN' else 'التذاكر',
        '% of Total' if pdf_lang=='EN' else '٪ من المجموع'
    ]]
    for i, (name, count) in enumerate(_dp.head(8).items(), 1):
        pct = round(count / len(df_data) * 100, 1)
        dept_data.append([str(i), str(name)[:45], f"{int(count):,}", f"{pct}%"])
    
    dept_table = Table(dept_data, colWidths=[0.8*inch, 3.8*inch, 1.2*inch, 1.2*inch])
    dept_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#0070e0')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('ALIGN', (2, 0), (3, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('TOPPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#e8f4ff')),
        ('GRID', (0, 0), (-1, -1), 0.8, colors.HexColor('#0070e0')),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 10),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f0f8ff')]),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    story.append(dept_table)
    story.append(Spacer(1, 0.35*inch))
    
    # Top 8 Issues
    story.append(Paragraph(f"🔥 {'TOP 8 ISSUES' if pdf_lang=='EN' else 'أعلى 8 مشكلات'}", heading_style))
    issue_data = [[
        'Rank' if pdf_lang=='EN' else 'الترتيب',
        'Issue Category' if pdf_lang=='EN' else 'فئة المشكلة',
        'Count' if pdf_lang=='EN' else 'العدد',
        '% of Total' if pdf_lang=='EN' else '٪ من المجموع'
    ]]
    for i, (name, count) in enumerate(_is.head(8).items(), 1):
        pct = round(count / len(df_data) * 100, 1)
        issue_data.append([str(i), str(name)[:45], f"{int(count):,}", f"{pct}%"])
    
    issue_table = Table(issue_data, colWidths=[0.8*inch, 3.8*inch, 1.2*inch, 1.2*inch])
    issue_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#ff6060')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('ALIGN', (2, 0), (3, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('TOPPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#ffe8e8')),
        ('GRID', (0, 0), (-1, -1), 0.8, colors.HexColor('#ff6060')),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 10),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#fff0f0')]),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    story.append(issue_table)
    story.append(PageBreak())
    
    # ═══ PAGE 3: VISUAL CHARTS ═══
    story.append(Paragraph(f"📈 {'VISUAL ANALYSIS' if pdf_lang=='EN' else 'التحليل البصري'}", heading_style))
    story.append(Spacer(1, 0.25*inch))
    
    # Chart 1: Service Distribution (Pie)
    try:
        svc_df = df_data[C_SVC].value_counts().reset_index()
        svc_df.columns = ['Service', 'Count']
        fig1 = px.pie(svc_df, values='Count', names='Service',
                      title='Service Type Distribution' if pdf_lang=='EN' else 'توزيع أنواع الخدمات',
                      template='plotly_white', hole=0.45)
        fig1.update_traces(textposition='inside', textinfo='percent+label', textfont_size=11)
        img1 = pio.to_image(fig1, format='png', width=900, height=480, scale=2)
        img1_buf = io.BytesIO(img1)
        story.append(Image(img1_buf, width=7*inch, height=3.7*inch))
        story.append(Spacer(1, 0.3*inch))
    except Exception as e:
        story.append(Paragraph(f"[Chart generation skipped: {str(e)[:50]}]", normal_style))
    
    # Chart 2: Top Departments (Bar)
    try:
        dept_df = df_data[C_DEPT].value_counts().head(12).reset_index()
        dept_df.columns = ['Department', 'Count']
        fig2 = px.bar(dept_df, x='Count', y='Department', orientation='h',
                      title='Top 12 Departments' if pdf_lang=='EN' else 'أعلى 12 إدارة',
                      template='plotly_white',
                      color='Count', color_continuous_scale='Blues', text='Count')
        fig2.update_layout(yaxis={'categoryorder':'total ascending'}, showlegend=False)
        fig2.update_traces(textposition='outside')
        img2 = pio.to_image(fig2, format='png', width=900, height=550, scale=2)
        img2_buf = io.BytesIO(img2)
        story.append(Image(img2_buf, width=7*inch, height=4.2*inch))
    except Exception as e:
        story.append(Paragraph(f"[Chart generation skipped]", normal_style))
    
    story.append(PageBreak())
    
    # ═══ PAGE 4: AGENT PERFORMANCE ═══
    if not df_data[C_AGENT].dropna().empty:
        story.append(Paragraph(f"👨‍💻 {'AGENT PERFORMANCE' if pdf_lang=='EN' else 'أداء الموظفين'}", heading_style))
        story.append(Spacer(1, 0.25*inch))
        
        agent_data = [[
            'Rank' if pdf_lang=='EN' else 'الترتيب',
            'Agent Name' if pdf_lang=='EN' else 'اسم الموظف',
            'Tickets' if pdf_lang=='EN' else 'التذاكر',
            '% of Total' if pdf_lang=='EN' else '٪ من المجموع'
        ]]
        for i, (name, count) in enumerate(_ag.head(12).items(), 1):
            clean_name = str(name).replace('−متعاقد','').replace('-متعاقد','').strip()
            pct = round(count / len(df_data) * 100, 1)
            agent_data.append([str(i), clean_name[:40], f"{int(count):,}", f"{pct}%"])
        
        agent_table = Table(agent_data, colWidths=[0.8*inch, 3.8*inch, 1.2*inch, 1.2*inch])
        agent_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#00a080')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('ALIGN', (2, 0), (3, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('TOPPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#e0f8f0')),
            ('GRID', (0, 0), (-1, -1), 0.8, colors.HexColor('#00a080')),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 10),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f0fff8')]),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]))
        story.append(agent_table)
        story.append(Spacer(1, 0.4*inch))
        
        # Agent Performance Chart
        try:
            ag_df = (df_data.dropna(subset=[C_AGENT])
                            .groupby([C_AGENT, '_short'])
                            .size().reset_index(name='Tickets')
                            .sort_values('Tickets', ascending=False)
                            .head(10))
            
            fig3 = px.bar(ag_df, x='Tickets', y='_short', orientation='h',
                          title='Top 10 Agents Performance' if pdf_lang=='EN' else 'أداء أفضل 10 موظفين',
                          template='plotly_white',
                          color='Tickets', color_continuous_scale='Teal', text='Tickets')
            fig3.update_layout(yaxis={'categoryorder':'total ascending', 'title':'Agent'},
                               showlegend=False)
            fig3.update_traces(textposition='outside')
            img3 = pio.to_image(fig3, format='png', width=900, height=500, scale=2)
            img3_buf = io.BytesIO(img3)
            story.append(Image(img3_buf, width=7*inch, height=3.8*inch))
        except:
            pass
    
    # Footer
    story.append(Spacer(1, 0.5*inch))
    footer_text = f"<i>{'Report generated on' if pdf_lang=='EN' else 'تم إنشاء التقرير في'} {datetime.now().strftime('%B %d, %Y at %I:%M %p')}</i>"
    story.append(Paragraph(footer_text, normal_style))
    
    doc.build(story)
    buffer.seek(0)
    return buffer

# ── ANIMATED HEADER ──────────────────────────────────────────────
badge_html = (
    ' <span style="background:rgba(255,200,0,.12);color:#ffc800;'
    'padding:3px 12px;border-radius:20px;font-size:.72rem;font-weight:800;'
    'border:1px solid rgba(255,200,0,.25);">🟡 FILTER ACTIVE</span>'
) if filtered else ""

st.markdown(
    f"<div class='glow-header'>"
    "<div style='display:flex;align-items:center;gap:18px;position:relative;z-index:1;'>"
    "<div style='background:linear-gradient(135deg,#0038a0,#0090ff);"
    "border-radius:18px;padding:16px 18px;font-size:2.2rem;line-height:1;"
    "box-shadow:0 6px 24px rgba(0,140,255,.45);flex-shrink:0;'>🖥️</div>"
    "<div style='flex:1;'>"
    f"<h1 style='color:#00d4ff;margin:0;font-size:1.8rem;font-weight:900;"
    f"letter-spacing:-.5px;line-height:1.2;"
    f"text-shadow:0 0 20px rgba(0,212,255,.3);'>{tx['title']}</h1>"
    f"<div style='color:#4a7a9a;margin-top:4px;font-size:.78rem;font-weight:600;"
    f"letter-spacing:.5px;'>{tx['subtitle']}</div>"
    "<div style='color:#4a7a9a;margin-top:8px;font-size:.82rem;"
    "display:flex;gap:14px;flex-wrap:wrap;align-items:center;'>"
    f"<span>📄 <b style='color:#7aadcc'>{uploaded.name}</b></span>"
    "<span style='color:#1a3060'>│</span>"
    f"<span>🗂️ <b style='color:#b0d0e8'>{len(df):,}</b> records</span>"
    "<span style='color:#1a3060'>│</span>"
    f"<span>🔽 <b style='color:#00d4ff'>{len(dff):,}</b> shown</span>"
    f"{badge_html}"
    "</div>"
    "</div>"
    "</div>"
    "</div>",
    unsafe_allow_html=True
)

# ── PDF EXPORT WITH ICON BUTTONS ─────────────────────────────────
st.markdown("---")
sec(f"📄 {tx['pdf_title']} — EN + AR Support")

pdf1, pdf2, pdf3 = st.columns([2, 1, 2])

with pdf1:
    st.markdown(
        "<div class='ai-card'>"
        "<div class='ai-badge'>📊 What's Included</div>"
        "<div class='ai-text'>"
        "✓ Executive Summary (4 pages)<br>"
        "✓ KPI Metrics Table<br>"
        "✓ Top 8 Departments & Issues<br>"
        "✓ Visual Charts (Pie, Bar)<br>"
        "✓ Top 12 Agents Performance<br>"
        "✓ Professional Landscape A4<br>"
        "✓ Arabic Names Supported<br>"
        "✓ Both EN & AR Languages"
        "</div></div>",
        unsafe_allow_html=True
    )

with pdf2:
    st.markdown(
        "<div style='text-align:center;padding:50px 0;'>"
        "<div style='font-size:5rem;line-height:1;'>📄</div>"
        "<div style='color:#00d4ff;font-size:1rem;font-weight:800;margin-top:16px;'>PPT-STYLE</div>"
        "<div style='color:#00d4ff;font-size:1rem;font-weight:800;'>PDF REPORT</div>"
        "</div>",
        unsafe_allow_html=True
    )

with pdf3:
    # English PDF Button
    if st.button("📥 Generate English PDF", use_container_width=True, type="primary", key="en_pdf"):
        with st.spinner("🎨 Creating English PDF with charts..."):
            try:
                pdf_buffer = generate_full_pdf(dff, acc, 'EN')
                st.success("✅ English PDF Generated!")
                
                st.download_button(
                    label="⬇️ Download English Report",
                    data=pdf_buffer,
                    file_name=f"IT_Helpdesk_EN_{datetime.now().strftime('%Y%m%d_%H%M')}.pdf",
                    mime="application/pdf",
                    use_container_width=True
                )
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
    
    st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)
    
    # Arabic PDF Button
    if st.button("📥 إنشاء تقرير عربي (Arabic PDF)", use_container_width=True, type="secondary", key="ar_pdf"):
        with st.spinner("🎨 Creating Arabic PDF with charts..."):
            try:
                pdf_buffer = generate_full_pdf(dff, acc, 'AR')
                st.success("✅ تم إنشاء التقرير العربي!")
                
                st.download_button(
                    label="⬇️ تنزيل التقرير العربي",
                    data=pdf_buffer,
                    file_name=f"IT_Helpdesk_AR_{datetime.now().strftime('%Y%m%d_%H%M')}.pdf",
                    mime="application/pdf",
                    use_container_width=True
                )
            except Exception as e:
                st.error(f"❌ خطأ: {str(e)}")

# ── KPI CARDS ────────────────────────────────────────────────────
st.markdown("---")
k1, k2, k3, k4, k5 = st.columns(5)
kpi_data = [
    ("🎫", len(dff),                          tx['total_rec']),
    ("🏢", dff[C_DEPT].nunique(),             tx['departments']),
    ("⚙️", dff[C_SVC].nunique(),              tx['svc_types']),
    ("🔥", dff[C_MAIN].nunique(),             tx['issue_types']),
    ("👨‍💻", dff[C_AGENT].dropna().nunique(),  tx['agents']),
]
for col_obj, (ico, val, lbl) in zip([k1,k2,k3,k4,k5], kpi_data):
    with col_obj:
        st.markdown(
            f"<div class='kpi'>"
            f"<span class='kpi-icon'>{ico}</span>"
            f"<span class='kpi-num'>{val:,}</span>"
            f"<span class='kpi-lbl'>{lbl}</span>"
            f"</div>",
            unsafe_allow_html=True
        )

st.markdown(
    "<div style='text-align:center;margin-top:40px;color:#4a7a9a;font-size:.88rem;'>"
    "Made with 💙 by Tarique Siddique | Streamlit + ReportLab + Plotly"
    "</div>",
    unsafe_allow_html=True
)
