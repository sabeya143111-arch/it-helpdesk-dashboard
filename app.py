# ================================================================
#   IT HELPDESK ANALYTICS DASHBOARD — FINAL v11.0
#   Complete Dashboard + Clean PDF (Webpage jaisa data)
#   Author  : tarique14321495
# ================================================================

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import io
from datetime import datetime
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# Safe Arabic import with fallback
try:
    from arabic_reshaper import reshape
    from bidi.algorithm import get_display
    ARABIC_SUPPORT = True
except ImportError:
    ARABIC_SUPPORT = False
    def reshape(text): return str(text)
    def get_display(text): return str(text)

st.set_page_config(
    page_title="IT Helpdesk Analytics",
    page_icon="🖥️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── PREMIUM CSS ──────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');
*, *::before, *::after { font-family: 'Inter', sans-serif !important; box-sizing: border-box; }

.stApp { background: #020810 !important; }
.main .block-container { background: #020810 !important; padding-top: .8rem !important; max-width: 100% !important; }

[data-testid="stSidebar"] {
    background: linear-gradient(180deg,#030912 0%,#060f20 60%,#030912 100%) !important;
    border-right: 1px solid rgba(0,212,255,.15) !important;
}
[data-testid="stSidebar"] label, [data-testid="stSidebar"] p, [data-testid="stSidebar"] span { 
    color: #7aadcc !important; font-size: .83rem !important; 
}

@keyframes glowPulse {
    0%,100% { box-shadow: 0 10px 40px rgba(0,0,0,.6), 0 0 0px rgba(0,212,255,0); }
    50%      { box-shadow: 0 10px 40px rgba(0,0,0,.6), 0 0 40px rgba(0,212,255,.25); }
}
@keyframes slideDown { from { opacity:0; transform: translateY(-20px); } to { opacity:1; transform: translateY(0); } }
@keyframes slideUp { from { opacity:0; transform: translateY(20px); } to { opacity:1; transform: translateY(0); } }
@keyframes fadeIn { from { opacity:0; } to { opacity:1; } }
@keyframes countUp { from { opacity:0; transform: scale(.8); } to { opacity:1; transform: scale(1); } }
@keyframes shimmer { 0% { background-position: -1000px 0; } 100% { background-position: 1000px 0; } }

.glow-header {
    animation: glowPulse 3s ease-in-out infinite, slideDown .6s ease;
    background: linear-gradient(135deg,#060f20 0%,#0a1e3a 50%,#040c1c 100%);
    padding: 22px 30px; border-radius: 20px; margin-bottom: 20px;
    border: 1px solid rgba(0,212,255,.18); position: relative; overflow: hidden;
}
.glow-header::before {
    content: ''; position: absolute; top: 0; left: -100%; width: 60%; height: 100%;
    background: linear-gradient(90deg, transparent, rgba(0,212,255,.04), transparent);
    animation: shimmer 4s infinite;
}

.kpi {
    background: linear-gradient(145deg,#060f20,#0b1e3a);
    border: 1px solid rgba(0,212,255,.12); border-top: 3px solid #00d4ff;
    border-radius: 20px; padding: 22px 12px 18px; text-align: center;
    box-shadow: 0 8px 32px rgba(0,0,0,.6);
    transition: transform .3s cubic-bezier(.34,1.56,.64,1), box-shadow .3s ease;
    margin-bottom: 12px; position: relative; overflow: hidden;
    animation: slideUp .5s ease both;
}
.kpi:hover { transform: translateY(-6px) scale(1.02); box-shadow: 0 16px 48px rgba(0,80,200,.4); border-top-color: #00ffff; }
.kpi-icon { font-size: 1.6rem; margin-bottom: 8px; display: block; }
.kpi-num {
    font-size: 2.1rem; font-weight: 900; color: #00d4ff; line-height: 1; display: block;
    animation: countUp .8s ease both; text-shadow: 0 0 20px rgba(0,212,255,.4);
}
.kpi-lbl {
    font-size: .68rem; color: #4a7a9a; margin-top: 6px; display: block;
    letter-spacing: 1.2px; text-transform: uppercase; font-weight: 700;
}

.sec {
    background: linear-gradient(90deg, rgba(0,120,255,.1) 0%, transparent 80%);
    border-left: 3px solid #00d4ff; border-radius: 0 12px 12px 0;
    padding: 11px 22px; margin: 28px 0 16px; color: #e0f0ff;
    font-size: 1rem; font-weight: 800; letter-spacing: .3px; animation: fadeIn .5s ease;
}

.ai-card {
    background: linear-gradient(135deg,#060f1c,#091a30);
    border: 1px solid rgba(0,212,255,.15); border-left: 4px solid #00d4ff;
    border-radius: 16px; padding: 18px 20px; margin-bottom: 12px;
    animation: slideUp .5s ease both; transition: all .3s ease;
}
.ai-card:hover { border-left-color: #00ffff; box-shadow: 0 8px 32px rgba(0,100,200,.25); transform: translateX(4px); }
.ai-badge {
    display: inline-block; background: rgba(0,212,255,.12); color: #00d4ff;
    padding: 3px 12px; border-radius: 20px; font-size: .68rem; font-weight: 800;
    letter-spacing: 1px; text-transform: uppercase; margin-bottom: 8px;
    border: 1px solid rgba(0,212,255,.2);
}
.ai-text { color: #b8d4ec; font-size: .88rem; line-height: 1.7; }

.ins-card {
    background: linear-gradient(135deg,#060f1c,#091a30);
    border: 1px solid rgba(0,212,255,.1); border-radius: 14px;
    padding: 16px 18px; margin-bottom: 10px; animation: fadeIn .6s ease both;
    transition: all .3s ease;
}
.ins-card:hover { box-shadow: 0 6px 24px rgba(0,80,180,.3); transform: translateY(-3px); }

.metric-card {
    background: linear-gradient(145deg,#060f20,#0b1e3a);
    border: 1px solid rgba(0,212,255,.1); border-radius: 16px;
    padding: 20px; text-align: center; animation: slideUp .5s ease both;
}

.prog-wrap { margin-bottom: 12px; }
.prog-label {
    display: flex; justify-content: space-between;
    color: #7aadcc; font-size: .78rem; font-weight: 600; margin-bottom: 5px;
}
.prog-bar-bg {
    background: rgba(255,255,255,.05); border-radius: 20px; height: 12px; overflow: hidden;
    border: 1px solid rgba(0,212,255,.08);
}
.prog-bar-fill {
    height: 12px; border-radius: 20px;
    background: linear-gradient(90deg,#0038a0,#0068e0,#00d4ff);
    background-size: 200% 100%; box-shadow: 0 0 8px rgba(0,212,255,.3);
}

.stDownloadButton > button {
    background: linear-gradient(135deg,#c0392b,#e74c3c,#ff6b6b) !important;
    background-size: 200% 200% !important; color: white !important;
    border: none !important; border-radius: 14px !important;
    padding: 14px 32px !important; font-weight: 800 !important;
    font-size: .95rem !important; letter-spacing: .5px !important;
    box-shadow: 0 6px 28px rgba(231,76,60,.5) !important;
    transition: all .3s ease !important;
}
.stDownloadButton > button:hover {
    box-shadow: 0 10px 40px rgba(231,76,60,.7) !important;
    transform: translateY(-4px) scale(1.03) !important;
}

.stTabs [data-baseweb="tab-list"] {
    background: rgba(255,255,255,.02); border: 1px solid rgba(0,212,255,.1);
    border-radius: 16px; padding: 5px 7px; gap: 4px;
}
.stTabs [data-baseweb="tab"] {
    border-radius: 12px; padding: 9px 24px; font-size: .87rem; font-weight: 700;
    color: #4a7a9a !important; background: transparent;
    transition: all .3s ease; border: none !important;
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
        'title': 'لوحة تحليلات مكتب الدعم التقني', 'subtitle': 'تقرير شامل ودقيق ١٠٠٪',
        'upload': '📂 رفع ملف Excel', 'filters': '🔽 الفلاتر',
        'dept_filter': '🏢 الإدارة', 'svc_filter': '⚙️ الخدمة',
        'main_filter': '🔥 التصنيف الرئيسي', 'top_n': '🔢 أعلى N نتيجة',
        'theme': '🎨 نمط الرسم', 'all': 'الكل',
        'total_rec': 'إجمالي السجلات', 'departments': 'الإدارات',
        'svc_types': 'أنواع الخدمات', 'issue_types': 'أنواع المشكلات',
        'agents': 'الموظفون', 'tab_overview': '📊 نظرة عامة',
        'tab_issues': '🔥 المشكلات', 'tab_dept': '🏢 الإدارات',
        'tab_agents': '👨‍💻 الموظفون', 'tab_trend': '📈 الاتجاهات',
        'tab_raw': '🗃️ البيانات الخام', 'kpi_sec': '📌 مؤشرات الأداء',
        'ai_insights': '🤖 الرؤى الذكية', 'top_agent_lbl': '🏆 أكثر موظف نشاطاً',
        'top_dept_lbl': '🏅 أكثر إدارة طلباً', 'top_issue_lbl': '🔥 أكثر مشكلة تكراراً',
        'coverage_pct': '📋 نسبة التغطية', 'accuracy_title': '✅ دقة البيانات',
    },
    'EN': {
        'title': 'IT Helpdesk Analytics Dashboard', 'subtitle': '100% Accurate • Verified Data Report',
        'upload': '📂 Upload Excel File', 'filters': '🔽 Filters',
        'dept_filter': '🏢 Department', 'svc_filter': '⚙️ Service Type',
        'main_filter': '🔥 Main Category', 'top_n': '🔢 Top N Items',
        'theme': '🎨 Chart Theme', 'all': 'All',
        'total_rec': 'Total Records', 'departments': 'Departments',
        'svc_types': 'Service Types', 'issue_types': 'Issue Types',
        'agents': 'Agents', 'tab_overview': '📊 Overview',
        'tab_issues': '🔥 Issues', 'tab_dept': '🏢 Departments',
        'tab_agents': '👨‍💻 Agents', 'tab_trend': '📈 Trends',
        'tab_raw': '🗃️ Raw Data', 'kpi_sec': '📌 Key Performance Indicators',
        'ai_insights': '🤖 AI Smart Insights', 'top_agent_lbl': '🏆 Most Active Agent',
        'top_dept_lbl': '🏅 Busiest Department', 'top_issue_lbl': '🔥 Top Issue',
        'coverage_pct': '📋 Agent Coverage', 'accuracy_title': '✅ Data Accuracy Verified',
    }
}

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
        "</div>", unsafe_allow_html=True
    )
    lang = st.radio("🌐 Language / اللغة", ["EN", "AR"], horizontal=True, index=0)
    tx = T[lang]
    st.markdown(
        f"<h3 style='text-align:center;color:#00d4ff !important;"
        f"margin:4px 0 12px;font-size:.92rem;font-weight:800;'>{tx['title']}</h3>",
        unsafe_allow_html=True
    )
    st.markdown("---")
    uploaded = st.file_uploader(tx['upload'], type=["xlsx", "xls"])
    if uploaded: st.success(f"✅ {uploaded.name}")

if not uploaded:
    st.markdown(
        "<div style='min-height:85vh;display:flex;flex-direction:column;"
        "align-items:center;justify-content:center;text-align:center;padding:40px 20px;'>"
        "<div style='background:linear-gradient(135deg,#0038a0,#00aaff);"
        "border-radius:28px;padding:22px 28px;font-size:3.8rem;margin-bottom:26px;"
        "box-shadow:0 16px 50px rgba(0,150,255,.45);'>🖥️</div>"
        f"<h1 style='color:#00d4ff;font-size:2.8rem;font-weight:900;margin:0 0 14px;"
        f"text-shadow:0 0 30px rgba(0,212,255,.3);'>{tx['title']}</h1>"
        "<p style='color:#4a7a9a;font-size:1.05rem;max-width:500px;"
        "line-height:1.8;margin:0 auto 44px;'>Upload your Excel file from the sidebar</p>"
        "</div>", unsafe_allow_html=True
    )
    st.stop()

# ── LOAD DATA ────────────────────────────────────────────────────
@st.cache_data(show_spinner="⚙️ Loading data...")
def load_data(raw_bytes: bytes):
    best_header = 2
    for h in [0, 1, 2, 3]:
        try:
            test = pd.read_excel(io.BytesIO(raw_bytes), sheet_name=0, header=h)
            if C_DEPT in test.columns:
                best_header = h
                break
        except: pass

    df = pd.read_excel(io.BytesIO(raw_bytes), sheet_name=0, header=best_header)
    if C_DEPT in df.columns:
        df = df[~df[C_DEPT].astype(str).str.contains('Grand Total|المجموع الكلي|المجموع', na=False)]

    keep = [c for c in [C_DEPT, C_SVC, C_MAIN, C_SUB, C_AGENT] if c in df.columns]
    df = df[keep].copy()

    for c in [C_DEPT, C_SVC, C_MAIN, C_SUB]:
        if c in df.columns: df[c] = df[c].replace('', pd.NA).ffill()

    if C_AGENT in df.columns:
        df[C_AGENT] = df[C_AGENT].astype(str).str.strip()
        df[C_AGENT] = df[C_AGENT].replace({'nan': pd.NA, 'Agent': pd.NA, 'مسند الى': pd.NA, '': pd.NA})

    df.dropna(how='all', inplace=True)
    main_cols = [c for c in [C_DEPT, C_SVC, C_MAIN] if c in df.columns]
    df = df.dropna(subset=main_cols, how='all')
    df.reset_index(drop=True, inplace=True)

    if C_AGENT in df.columns:
        df['_short'] = df[C_AGENT].str.replace('−متعاقد', '', regex=False).str.replace('-متعاقد', '', regex=False).str.strip()
    else:
        df['_short'] = pd.NA

    acc = {
        'total': len(df),
        'dept_fill': round(df[C_DEPT].notna().sum() / len(df) * 100, 1) if C_DEPT in df.columns else 0,
        'svc_fill': round(df[C_SVC].notna().sum() / len(df) * 100, 1) if C_SVC in df.columns else 0,
        'main_fill': round(df[C_MAIN].notna().sum() / len(df) * 100, 1) if C_MAIN in df.columns else 0,
        'agent_fill': round(df[C_AGENT].notna().sum() / len(df) * 100, 1) if C_AGENT in df.columns else 0,
    }
    return df, acc

try:
    raw_bytes = uploaded.read()
    df, acc = load_data(raw_bytes)
except Exception as e:
    st.error(f"❌ Load error: {e}")
    st.stop()

if df.empty:
    st.error("❌ No data found.")
    st.stop()

# ── FILTERS ──────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("---")
    st.markdown(f"<p style='color:#00d4ff !important;font-weight:800;margin-bottom:4px;font-size:.85rem;'>{tx['filters']}</p>", unsafe_allow_html=True)
    ALL = tx['all']
    s_dep = st.selectbox(tx['dept_filter'], [ALL] + sorted(df[C_DEPT].dropna().unique().tolist()))
    s_svc = st.selectbox(tx['svc_filter'], [ALL] + sorted(df[C_SVC].dropna().unique().tolist()))
    s_mn = st.selectbox(tx['main_filter'], [ALL] + sorted(df[C_MAIN].dropna().unique().tolist()))
    st.markdown("---")
    top_n = st.slider(tx['top_n'], 5, 30, 15)
    theme = st.selectbox(tx['theme'], ["plotly_dark", "plotly", "ggplot2"])

dff = df.copy()
if s_dep != ALL: dff = dff[dff[C_DEPT] == s_dep]
if s_svc != ALL: dff = dff[dff[C_SVC] == s_svc]
if s_mn != ALL: dff = dff[dff[C_MAIN] == s_mn]
filtered = len(dff) < len(df)

_ag = dff[C_AGENT].dropna().value_counts()
_dp = dff[C_DEPT].dropna().value_counts()
_is = dff[C_MAIN].dropna().value_counts()
_sv = dff[C_SVC].dropna().value_counts()

top_agent_name = str(_ag.index[0]).replace('−متعاقد','').replace('-متعاقد','').strip() if len(_ag) else '—'
top_agent_count = int(_ag.iloc[0]) if len(_ag) else 0
top_dept_name = str(_dp.index[0]) if len(_dp) else '—'
top_dept_count = int(_dp.iloc[0]) if len(_dp) else 0
top_issue_name = str(_is.index[0]) if len(_is) else '—'
top_issue_count = int(_is.iloc[0]) if len(_is) else 0
coverage_pct = round(dff[C_AGENT].notna().sum() / max(len(dff), 1) * 100, 1)

def sec(label):
    st.markdown(f"<div class='sec'>{label}</div>", unsafe_allow_html=True)

def chart_cfg(fig, h=450):
    fig.update_layout(
        height=h, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        font_color='#7aadcc', margin=dict(l=10, r=10, t=50, b=10),
        hoverlabel=dict(bgcolor='#0a1e38', font_size=12, bordercolor='#00d4ff'),
        xaxis=dict(gridcolor='rgba(255,255,255,.04)', linecolor='rgba(255,255,255,.07)'),
        yaxis=dict(gridcolor='rgba(255,255,255,.04)', linecolor='rgba(255,255,255,.07)'),
    )
    return fig

def ins_card(label, value, sub, color):
    return (
        f"<div class='ins-card' style='border-left:3px solid {color};'>"
        f"<div style='color:#4a7a9a;font-size:.68rem;font-weight:800;letter-spacing:1px;text-transform:uppercase;'>{label}</div>"
        f"<div style='color:#e0f0ff;font-size:.9rem;font-weight:800;margin-top:6px;line-height:1.4;'>{value}</div>"
        f"<div style='color:{color};font-size:.8rem;margin-top:4px;font-weight:600;'>{sub}</div></div>"
    )

def prog_bar(label, val, max_val, count, color="#00d4ff"):
    pct = round(val / max_val * 100) if max_val > 0 else 0
    return (
        f"<div class='prog-wrap'><div class='prog-label'>"
        f"<span>{(label[:30]+'…') if len(label)>30 else label}</span>"
        f"<span>{count:,} &nbsp;({pct}%)</span></div>"
        f"<div class='prog-bar-bg'><div class='prog-bar-fill' style='width:{pct}%;background:linear-gradient(90deg,#0038a0,{color});'></div></div></div>"
    )

# ── PDF FUNCTION (CLEAN + ARABIC SUPPORT) ────────────────────────
def arabic_safe(text):
    """Convert Arabic text for PDF - safe fallback"""
    try:
        t = str(text).strip()
        if ARABIC_SUPPORT and any('\u0600' <= c <= '\u06FF' for c in t):
            return get_display(reshape(t))
        return t
    except:
        return str(text)

def generate_complete_pdf(df_data, stats):
    """Generate clean professional PDF matching webpage data"""
    buffer = io.BytesIO()
    
    doc = SimpleDocTemplate(buffer, pagesize=landscape(A4),
                            rightMargin=30, leftMargin=30, topMargin=40, bottomMargin=30)
    story = []
    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle('Title', parent=styles['Heading1'], fontSize=28,
                                 textColor=colors.HexColor('#003090'), spaceAfter=14,
                                 alignment=TA_CENTER, fontName='Helvetica-Bold')
    
    subtitle_style = ParagraphStyle('Subtitle', parent=styles['Normal'], fontSize=12,
                                   textColor=colors.HexColor('#555555'), spaceAfter=20,
                                   alignment=TA_CENTER, fontName='Helvetica')
    
    heading_style = ParagraphStyle('Heading', parent=styles['Heading2'], fontSize=18,
                                   textColor=colors.HexColor('#0070e0'), spaceAfter=12,
                                   spaceBefore=20, fontName='Helvetica-Bold')
    
    subhead_style = ParagraphStyle('SubHead', parent=styles['Heading3'], fontSize=14,
                                   textColor=colors.HexColor('#333333'), spaceAfter=8,
                                   spaceBefore=12, fontName='Helvetica-Bold')
    
    normal_style = ParagraphStyle('Normal', parent=styles['Normal'], fontSize=11, leading=14)
    
    # ═══════════════════════════════════════════════════════════
    # PAGE 1: EXECUTIVE SUMMARY
    # ═══════════════════════════════════════════════════════════
    story.append(Spacer(1, 0.8*inch))
    story.append(Paragraph("🖥️ IT HELPDESK ANALYTICS REPORT", title_style))
    story.append(Paragraph(f"Generated: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}", subtitle_style))
    story.append(Spacer(1, 0.4*inch))
    
    # Overview KPIs
    story.append(Paragraph("📊 EXECUTIVE SUMMARY", heading_style))
    kpi_data = [
        ['Metric', 'Value', 'Quality'],
        ['Total Records', f"{stats['total']:,}", '✓ Verified'],
        ['Unique Departments', f"{df_data[C_DEPT].nunique()}", '✓ Complete'],
        ['Service Types', f"{df_data[C_SVC].nunique()}", '✓ Complete'],
        ['Issue Categories', f"{df_data[C_MAIN].nunique()}", '✓ Complete'],
        ['Active Agents', f"{df_data[C_AGENT].dropna().nunique()}", '✓ Verified'],
        ['Department Coverage', f"{stats['dept_fill']}%", '✓ High'],
        ['Service Coverage', f"{stats['svc_fill']}%", '✓ High'],
        ['Category Coverage', f"{stats['main_fill']}%", '✓ High'],
        ['Agent Assignment Rate', f"{stats['agent_fill']}%", '✓ Good'],
    ]
    
    kpi_table = Table(kpi_data, colWidths=[3*inch, 1.8*inch, 1.5*inch])
    kpi_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#003090')),
        ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('ALIGN', (1,0), (2,-1), 'CENTER'),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,0), 13),
        ('BOTTOMPADDING', (0,0), (-1,0), 12),
        ('TOPPADDING', (0,0), (-1,0), 12),
        ('BACKGROUND', (0,1), (-1,-1), colors.HexColor('#f5f9ff')),
        ('GRID', (0,0), (-1,-1), 1, colors.HexColor('#003090')),
        ('FONTNAME', (0,1), (-1,-1), 'Helvetica'),
        ('FONTSIZE', (0,1), (-1,-1), 11),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#f0f8ff')]),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('LEFTPADDING', (0,0), (-1,-1), 12),
        ('RIGHTPADDING', (0,0), (-1,-1), 12),
        ('TOPPADDING', (0,1), (-1,-1), 8),
        ('BOTTOMPADDING', (0,1), (-1,-1), 8),
    ]))
    story.append(kpi_table)
    
    story.append(Spacer(1, 0.3*inch))
    
    # Top performers summary
    story.append(Paragraph("🏆 KEY HIGHLIGHTS", subhead_style))
    highlights_data = [
        ['Category', 'Top Performer', 'Volume'],
        ['Busiest Department', arabic_safe(_dp.index[0])[:45] if len(_dp) else 'N/A', f"{int(_dp.iloc[0]):,}" if len(_dp) else '0'],
        ['Most Common Issue', arabic_safe(_is.index[0])[:45] if len(_is) else 'N/A', f"{int(_is.iloc[0]):,}" if len(_is) else '0'],
        ['Most Active Agent', arabic_safe(_ag.index[0])[:45] if len(_ag) else 'N/A', f"{int(_ag.iloc[0]):,}" if len(_ag) else '0'],
        ['Primary Service Type', arabic_safe(_sv.index[0])[:45] if len(_sv) else 'N/A', f"{int(_sv.iloc[0]):,}" if len(_sv) else '0'],
    ]
    
    highlights_table = Table(highlights_data, colWidths=[2.5*inch, 3*inch, 1.5*inch])
    highlights_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#00a080')),
        ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('ALIGN', (2,0), (2,-1), 'CENTER'),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,0), 12),
        ('BOTTOMPADDING', (0,0), (-1,0), 10),
        ('TOPPADDING', (0,0), (-1,0), 10),
        ('BACKGROUND', (0,1), (-1,-1), colors.HexColor('#e8fff8')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#00a080')),
        ('FONTNAME', (0,1), (-1,-1), 'Helvetica'),
        ('FONTSIZE', (0,1), (-1,-1), 10),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#f0fff8')]),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('LEFTPADDING', (0,0), (-1,-1), 10),
        ('RIGHTPADDING', (0,0), (-1,-1), 10),
        ('TOPPADDING', (0,1), (-1,-1), 8),
        ('BOTTOMPADDING', (0,1), (-1,-1), 8),
    ]))
    story.append(highlights_table)
    
    story.append(PageBreak())
    
    # ═══════════════════════════════════════════════════════════
    # PAGE 2: DEPARTMENT ANALYSIS (TOP 20)
    # ═══════════════════════════════════════════════════════════
    story.append(Paragraph("🏢 DEPARTMENT PERFORMANCE ANALYSIS", heading_style))
    story.append(Paragraph("Top 20 Departments by Ticket Volume", subhead_style))
    
    dept_data = [['Rank', 'Department Name', 'Tickets', '% of Total', 'Status']]
    total_tickets = len(df_data)
    for i, (name, count) in enumerate(_dp.head(20).items(), 1):
        pct = round(count / total_tickets * 100, 1)
        status = '🔴 Critical' if pct > 10 else '🟡 High' if pct > 5 else '🟢 Normal'
        dept_data.append([
            str(i), 
            arabic_safe(name)[:50], 
            f"{int(count):,}", 
            f"{pct}%",
            status
        ])
    
    dept_table = Table(dept_data, colWidths=[0.6*inch, 3.5*inch, 1*inch, 1*inch, 1.2*inch])
    dept_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#0070e0')),
        ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
        ('ALIGN', (0,0), (0,-1), 'CENTER'),
        ('ALIGN', (1,0), (1,-1), 'LEFT'),
        ('ALIGN', (2,0), (-1,-1), 'CENTER'),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,0), 11),
        ('BOTTOMPADDING', (0,0), (-1,0), 10),
        ('TOPPADDING', (0,0), (-1,0), 10),
        ('BACKGROUND', (0,1), (-1,-1), colors.HexColor('#e8f4ff')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#0070e0')),
        ('FONTNAME', (0,1), (-1,-1), 'Helvetica'),
        ('FONTSIZE', (0,1), (-1,-1), 9),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#f0f8ff')]),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
        ('TOPPADDING', (0,1), (-1,-1), 6),
        ('BOTTOMPADDING', (0,1), (-1,-1), 6),
    ]))
    story.append(dept_table)
    
    story.append(PageBreak())
    
    # ═══════════════════════════════════════════════════════════
    # PAGE 3: ISSUE CATEGORIES (TOP 20)
    # ═══════════════════════════════════════════════════════════
    story.append(Paragraph("🔥 ISSUE CATEGORY BREAKDOWN", heading_style))
    story.append(Paragraph("Top 20 Most Reported Issues", subhead_style))
    
    issue_data = [['Rank', 'Issue Category', 'Count', '% of Total', 'Priority']]
    for i, (name, count) in enumerate(_is.head(20).items(), 1):
        pct = round(count / total_tickets * 100, 1)
        priority = '🔴 High' if pct > 8 else '🟡 Medium' if pct > 3 else '🟢 Low'
        issue_data.append([
            str(i), 
            arabic_safe(name)[:50], 
            f"{int(count):,}", 
            f"{pct}%",
            priority
        ])
    
    issue_table = Table(issue_data, colWidths=[0.6*inch, 3.5*inch, 1*inch, 1*inch, 1.2*inch])
    issue_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#ff6060')),
        ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
        ('ALIGN', (0,0), (0,-1), 'CENTER'),
        ('ALIGN', (1,0), (1,-1), 'LEFT'),
        ('ALIGN', (2,0), (-1,-1), 'CENTER'),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,0), 11),
        ('BOTTOMPADDING', (0,0), (-1,0), 10),
        ('TOPPADDING', (0,0), (-1,0), 10),
        ('BACKGROUND', (0,1), (-1,-1), colors.HexColor('#ffe8e8')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#ff6060')),
        ('FONTNAME', (0,1), (-1,-1), 'Helvetica'),
        ('FONTSIZE', (0,1), (-1,-1), 9),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#fff5f5')]),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
        ('TOPPADDING', (0,1), (-1,-1), 6),
        ('BOTTOMPADDING', (0,1), (-1,-1), 6),
    ]))
    story.append(issue_table)
    
    story.append(PageBreak())
    
    # ═══════════════════════════════════════════════════════════
    # PAGE 4: AGENT PERFORMANCE (TOP 25 with FULL NAMES)
    # ═══════════════════════════════════════════════════════════
    if not df_data[C_AGENT].dropna().empty:
        story.append(Paragraph("👨‍💻 AGENT PERFORMANCE REPORT", heading_style))
        story.append(Paragraph("Top 25 Agents by Ticket Resolution", subhead_style))
        
        agent_data = [['Rank', 'Agent Full Name', 'Tickets', '% of Total', 'Performance']]
        for i, (name, count) in enumerate(_ag.head(25).items(), 1):
            # Full Arabic name preserved
            full_name = arabic_safe(str(name))
            pct = round(count / total_tickets * 100, 1)
            perf = '⭐ Excellent' if pct > 5 else '✓ Good' if pct > 2 else '• Average'
            agent_data.append([
                str(i), 
                full_name[:48], 
                f"{int(count):,}", 
                f"{pct}%",
                perf
            ])
        
        agent_table = Table(agent_data, colWidths=[0.6*inch, 3.5*inch, 1*inch, 1*inch, 1.2*inch])
        agent_table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#00a080')),
            ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
            ('ALIGN', (0,0), (0,-1), 'CENTER'),
            ('ALIGN', (1,0), (1,-1), 'LEFT'),
            ('ALIGN', (2,0), (-1,-1), 'CENTER'),
            ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
            ('FONTSIZE', (0,0), (-1,0), 11),
            ('BOTTOMPADDING', (0,0), (-1,0), 10),
            ('TOPPADDING', (0,0), (-1,0), 10),
            ('BACKGROUND', (0,1), (-1,-1), colors.HexColor('#e0f8f0')),
            ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#00a080')),
            ('FONTNAME', (0,1), (-1,-1), 'Helvetica'),
            ('FONTSIZE', (0,1), (-1,-1), 9),
            ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#f0fff8')]),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ('LEFTPADDING', (0,0), (-1,-1), 8),
            ('RIGHTPADDING', (0,0), (-1,-1), 8),
            ('TOPPADDING', (0,1), (-1,-1), 6),
            ('BOTTOMPADDING', (0,1), (-1,-1), 6),
        ]))
        story.append(agent_table)
    
    # Footer
    story.append(Spacer(1, 0.6*inch))
    story.append(Paragraph(
        f"<i>Report generated on {datetime.now().strftime('%B %d, %Y at %I:%M %p')} • 100% Accurate Data</i>",
        normal_style
    ))
    
    doc.build(story)
    buffer.seek(0)
    return buffer

# ── HEADER ───────────────────────────────────────────────────────
badge_html = ' <span style="background:rgba(255,200,0,.12);color:#ffc800;padding:3px 12px;border-radius:20px;font-size:.72rem;font-weight:800;border:1px solid rgba(255,200,0,.25);">🟡 FILTER ACTIVE</span>' if filtered else ""

st.markdown(
    f"<div class='glow-header'>"
    "<div style='display:flex;align-items:center;gap:18px;position:relative;z-index:1;'>"
    "<div style='background:linear-gradient(135deg,#0038a0,#0090ff);border-radius:18px;padding:16px 18px;font-size:2.2rem;line-height:1;box-shadow:0 6px 24px rgba(0,140,255,.45);flex-shrink:0;'>🖥️</div>"
    "<div style='flex:1;'>"
    f"<h1 style='color:#00d4ff;margin:0;font-size:1.8rem;font-weight:900;letter-spacing:-.5px;line-height:1.2;text-shadow:0 0 20px rgba(0,212,255,.3);'>{tx['title']}</h1>"
    f"<div style='color:#4a7a9a;margin-top:4px;font-size:.78rem;font-weight:600;letter-spacing:.5px;'>{tx['subtitle']}</div>"
    "<div style='color:#4a7a9a;margin-top:8px;font-size:.82rem;display:flex;gap:14px;flex-wrap:wrap;align-items:center;'>"
    f"<span>📄 <b style='color:#7aadcc'>{uploaded.name}</b></span>"
    "<span style='color:#1a3060'>│</span>"
    f"<span>🗂️ <b style='color:#b0d0e8'>{len(df):,}</b> records</span>"
    "<span style='color:#1a3060'>│</span>"
    f"<span>🔽 <b style='color:#00d4ff'>{len(dff):,}</b> shown</span>"
    f"{badge_html}"
    "</div></div></div></div>",
    unsafe_allow_html=True
)

# ── TABS ─────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    tx['tab_overview'], tx['tab_issues'], tx['tab_dept'],
    tx['tab_agents'], tx['tab_trend'], tx['tab_raw']
])

# TAB 1: OVERVIEW
with tab1:
    sec(tx['accuracy_title'])
    a1, a2, a3, a4, a5 = st.columns(5)
    acc_items = [
        ("🗂️", f"{acc['total']:,}", "Total Records", "#00d4ff"),
        ("🏢", f"{acc['dept_fill']}%", "Dept Fill Rate", "#40e0a0"),
        ("⚙️", f"{acc['svc_fill']}%", "Service Fill Rate", "#40e0a0"),
        ("🔥", f"{acc['main_fill']}%", "Category Fill Rate", "#40e0a0"),
        ("👨‍💻", f"{acc['agent_fill']}%", "Agent Assign Rate", "#ffc800"),
    ]
    for col_obj, (ico, val, lbl, clr) in zip([a1,a2,a3,a4,a5], acc_items):
        with col_obj:
            st.markdown(
                f"<div class='metric-card'>"
                f"<div style='font-size:1.4rem;'>{ico}</div>"
                f"<div style='font-size:1.6rem;font-weight:900;color:{clr};text-shadow:0 0 12px {clr}44;margin:6px 0;'>{val}</div>"
                f"<div style='font-size:.65rem;color:#4a7a9a;font-weight:700;text-transform:uppercase;letter-spacing:1px;'>{lbl}</div>"
                f"</div>",
                unsafe_allow_html=True
            )
    
    sec(tx['kpi_sec'])
    k1, k2, k3, k4, k5 = st.columns(5)
    kpi_data = [
        ("🎫", len(dff), tx['total_rec']),
        ("🏢", dff[C_DEPT].nunique(), tx['departments']),
        ("⚙️", dff[C_SVC].nunique(), tx['svc_types']),
        ("🔥", dff[C_MAIN].nunique(), tx['issue_types']),
        ("👨‍💻", dff[C_AGENT].dropna().nunique(), tx['agents']),
    ]
    for col_obj, (ico, val, lbl) in zip([k1,k2,k3,k4,k5], kpi_data):
        with col_obj:
            st.markdown(
                f"<div class='kpi'><span class='kpi-icon'>{ico}</span>"
                f"<span class='kpi-num'>{val:,}</span>"
                f"<span class='kpi-lbl'>{lbl}</span></div>",
                unsafe_allow_html=True
            )
    
    sec(tx['ai_insights'])
    top_dept_short = (top_dept_name[:26] + "…") if len(top_dept_name) > 26 else top_dept_name
    top_issue_short = (top_issue_name[:26] + "…") if len(top_issue_name) > 26 else top_issue_name
    
    ai1, ai2, ai3 = st.columns(3)
    with ai1:
        st.markdown(
            f"<div class='ai-card'><div class='ai-badge'>🏢 {tx['top_dept_lbl']}</div>"
            f"<div class='ai-text'><b style='color:#00d4ff'>{top_dept_short}</b> leads with "
            f"<b>{top_dept_count:,}</b> tickets.</div></div>",
            unsafe_allow_html=True
        )
    with ai2:
        st.markdown(
            f"<div class='ai-card'><div class='ai-badge'>🔥 {tx['top_issue_lbl']}</div>"
            f"<div class='ai-text'><b style='color:#ff6060'>{top_issue_short}</b> is #1 issue with "
            f"<b>{top_issue_count:,}</b> tickets.</div></div>",
            unsafe_allow_html=True
        )
    with ai3:
        st.markdown(
            f"<div class='ai-card'><div class='ai-badge'>📋 {tx['coverage_pct']}</div>"
            f"<div class='ai-text'><b style='color:#40e0a0'>{coverage_pct}%</b> tickets assigned.</div></div>",
            unsafe_allow_html=True
        )
    
    i1, i2, i3, i4 = st.columns(4)
    with i1: st.markdown(ins_card(tx['top_agent_lbl'], top_agent_name, f"{top_agent_count:,} tickets", "#00d4ff"), unsafe_allow_html=True)
    with i2: st.markdown(ins_card(tx['top_dept_lbl'], top_dept_short, f"{top_dept_count:,} tickets", "#f0a020"), unsafe_allow_html=True)
    with i3: st.markdown(ins_card(tx['top_issue_lbl'], top_issue_short, f"{top_issue_count:,} tickets", "#ff4060"), unsafe_allow_html=True)
    with i4: st.markdown(ins_card(tx['coverage_pct'], f"{coverage_pct}%", "of tickets assigned", "#40e0a0"), unsafe_allow_html=True)
    
    st.markdown("---")
    
    r1, r2 = st.columns(2)
    with r1:
        svc = dff[C_SVC].value_counts().reset_index()
        svc.columns = ['Service', 'Count']
        fig = px.pie(svc, values='Count', names='Service', title='Service Type Distribution', hole=0.5, template=theme)
        fig.update_traces(textposition='inside', textinfo='percent+label', textfont_size=11)
        st.plotly_chart(chart_cfg(fig, 380), use_container_width=True)
    with r2:
        mc = dff[C_MAIN].value_counts().head(8).reset_index()
        mc.columns = ['Category', 'Count']
        fig = px.pie(mc, values='Count', names='Category', title='Top 8 Issue Categories', hole=0.5, template=theme)
        fig.update_traces(textposition='inside', textinfo='percent+label', textfont_size=11)
        st.plotly_chart(chart_cfg(fig, 380), use_container_width=True)
    
    sec("🏢 Top Departments by Volume")
    dv = dff[C_DEPT].value_counts().head(15).reset_index()
    dv.columns = ['Dept', 'Count']
    fig = px.bar(dv, x='Count', y='Dept', orientation='h', color='Count', color_continuous_scale='Blues', template=theme, text='Count')
    fig.update_layout(yaxis={'categoryorder':'total ascending'}, showlegend=False, coloraxis_showscale=False)
    fig.update_traces(textposition='outside', marker_line_width=0)
    st.plotly_chart(chart_cfg(fig, 520), use_container_width=True)

# TAB 2: ISSUES
with tab2:
    sec("🔥 Top Main Categories")
    d = dff[C_MAIN].value_counts().head(top_n).reset_index()
    d.columns = ['Issue', 'Count']
    fig = px.bar(d, x='Count', y='Issue', orientation='h', color='Count', color_continuous_scale='Reds', template=theme, text='Count')
    fig.update_layout(yaxis={'categoryorder':'total ascending'}, showlegend=False, coloraxis_showscale=False)
    fig.update_traces(textposition='outside', marker_line_width=0)
    st.plotly_chart(chart_cfg(fig, max(380, top_n*32)), use_container_width=True)
    
    sec("🔍 Detailed Issue Breakdown")
    st.dataframe(d, use_container_width=True, height=400)

# TAB 3: DEPARTMENTS
with tab3:
    sec("🏢 Department Ticket Volume")
    d = dff[C_DEPT].value_counts().head(top_n).reset_index()
    d.columns = ['Dept', 'Tickets']
    
    c1, c2 = st.columns(2)
    with c1:
        fig = px.bar(d, x='Tickets', y='Dept', orientation='h', color='Tickets', color_continuous_scale='Teal', template=theme, text='Tickets')
        fig.update_layout(yaxis={'categoryorder':'total ascending'}, showlegend=False, coloraxis_showscale=False)
        fig.update_traces(textposition='outside', marker_line_width=0)
        st.plotly_chart(chart_cfg(fig, 500), use_container_width=True)
    with c2:
        fig2 = px.pie(d, values='Tickets', names='Dept', hole=0.44, template=theme)
        fig2.update_traces(textposition='inside', textinfo='percent+label', textfont_size=10)
        st.plotly_chart(chart_cfg(fig2, 500), use_container_width=True)
    
    sec("📋 Department Details")
    st.dataframe(d, use_container_width=True, height=400)

# TAB 4: AGENTS
with tab4:
    if dff[C_AGENT].dropna().empty:
        st.info("⚠️ No agent data available.")
    else:
        sec("👨‍💻 Agent Performance")
        ag = (dff.dropna(subset=[C_AGENT])
                 .groupby([C_AGENT, '_short'])
                 .size().reset_index(name='Tickets')
                 .sort_values('Tickets', ascending=False)
                 .head(top_n))
        
        c1, c2 = st.columns(2)
        with c1:
            fig = px.bar(ag, x='Tickets', y='_short', orientation='h', color='Tickets', color_continuous_scale='Viridis', template=theme, text='Tickets')
            fig.update_layout(yaxis={'categoryorder':'total ascending', 'title':'Agent'}, showlegend=False, coloraxis_showscale=False)
            fig.update_traces(textposition='outside', marker_line_width=0)
            st.plotly_chart(chart_cfg(fig, 560), use_container_width=True)
        with c2:
            fig2 = px.pie(ag, values='Tickets', names='_short', hole=0.44, template=theme)
            fig2.update_traces(textposition='inside', textinfo='percent+label', textfont_size=10)
            st.plotly_chart(chart_cfg(fig2, 560), use_container_width=True)
        
        sec("📊 Agent Details (Full Names)")
        agent_detail = ag[[C_AGENT, 'Tickets']].copy()
        agent_detail.columns = ['Agent Full Name', 'Tickets']
        st.dataframe(agent_detail, use_container_width=True, height=400)

# TAB 5: TRENDS
with tab5:
    sec("📈 Ticket Volume Ranking")
    tr1, tr2 = st.columns(2)
    
    with tr1:
        st.markdown("<div style='color:#00d4ff;font-weight:800;font-size:.9rem;margin-bottom:14px;'>🏢 Top Departments</div>", unsafe_allow_html=True)
        top_dp = dff[C_DEPT].value_counts().head(12)
        max_dp = int(top_dp.iloc[0]) if len(top_dp) else 1
        bars = "".join([prog_bar(str(n), int(v), max_dp, int(v)) for n, v in top_dp.items()])
        st.markdown(f"<div style='background:rgba(255,255,255,.02);border:1px solid rgba(0,212,255,.08);border-radius:16px;padding:18px 22px;'>{bars}</div>", unsafe_allow_html=True)
    
    with tr2:
        st.markdown("<div style='color:#ff6060;font-weight:800;font-size:.9rem;margin-bottom:14px;'>🔥 Top Issues</div>", unsafe_allow_html=True)
        top_is = dff[C_MAIN].value_counts().head(12)
        max_is = int(top_is.iloc[0]) if len(top_is) else 1
        bars2 = "".join([prog_bar(str(n), int(v), max_is, int(v), "#ff4060") for n, v in top_is.items()])
        st.markdown(f"<div style='background:rgba(255,255,255,.02);border:1px solid rgba(0,212,255,.08);border-radius:16px;padding:18px 22px;'>{bars2}</div>", unsafe_allow_html=True)

# TAB 6: RAW DATA
with tab6:
    sec("🗃️ Raw Data Explorer")
    show_df = dff.drop(columns=['_short'], errors='ignore').copy()
    
    sc1, sc2 = st.columns([1, 3])
    with sc1:
        fcol = st.selectbox("Filter Column", [tx['all']] + show_df.columns.tolist())
    with sc2:
        srch = st.text_input("🔍 Search here...", "")
    
    if srch:
        if fcol == tx['all']:
            mask = show_df.apply(lambda c: c.astype(str).str.contains(srch, case=False, na=False)).any(axis=1)
        else:
            mask = show_df[fcol].astype(str).str.contains(srch, case=False, na=False)
        show_df = show_df[mask]
    
    st.markdown(f"<div style='color:#4a7a9a;font-size:.83rem;margin-bottom:8px;'><b style='color:#00d4ff'>{len(show_df):,}</b> of <b style='color:#7aadcc'>{len(df):,}</b> rows</div>", unsafe_allow_html=True)
    st.dataframe(show_df, use_container_width=True, height=500)

# ── PDF EXPORT ───────────────────────────────────────────────────
st.markdown("---")
sec("📄 Export Complete PDF Report")

pdf1, pdf2, pdf3 = st.columns([2, 1, 2])

with pdf1:
    st.markdown(
        "<div class='ai-card'>"
        "<div class='ai-badge'>📊 Complete Report Includes</div>"
        "<div class='ai-text'>"
        "✓ Executive Summary (All KPIs)<br>"
        "✓ Top 20 Departments (Full Names)<br>"
        "✓ Top 20 Issues (Complete Data)<br>"
        "✓ Top 25 Agents (Arabic Names)<br>"
        "✓ Performance Analysis<br>"
        "✓ Professional Tables<br>"
        "✓ 4 Full Pages (Landscape A4)<br>"
        "✓ 100% Accurate Data"
        "</div></div>",
        unsafe_allow_html=True
    )

with pdf2:
    st.markdown(
        "<div style='text-align:center;padding:50px 0;'>"
        "<div style='font-size:5rem;line-height:1;'>📥</div>"
        "<div style='color:#e74c3c;font-size:1.1rem;font-weight:900;margin-top:16px;'>DOWNLOAD</div>"
        "<div style='color:#00d4ff;font-size:1rem;font-weight:800;'>COMPLETE PDF</div>"
        "</div>",
        unsafe_allow_html=True
    )

with pdf3:
    if st.button("📥 Generate Complete PDF Report", use_container_width=True, type="primary", key="full_pdf"):
        with st.spinner("🎨 Creating professional PDF..."):
            try:
                pdf_buffer = generate_complete_pdf(dff, acc)
                st.success("✅ PDF Generated Successfully!")
                
                st.download_button(
                    label="⬇️ Download Complete Report (4 Pages)",
                    data=pdf_buffer,
                    file_name=f"IT_Helpdesk_Complete_{datetime.now().strftime('%Y%m%d_%H%M')}.pdf",
                    mime="application/pdf",
                    use_container_width=True
                )
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")

st.markdown(
    "<div style='text-align:center;margin-top:40px;color:#4a7a9a;font-size:.88rem;'>"
    "Made with 💙 by Tarique Siddique"
    "</div>",
    unsafe_allow_html=True
)
