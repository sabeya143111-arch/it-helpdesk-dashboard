# ================================================================
#   IT HELPDESK ANALYTICS — ADVANCED RESOLUTION TIME v21.0
#   Complete Manager Dashboard with SLA & Performance Metrics
#   Author: tarique14321495
# ================================================================

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import io, os, requests
from datetime import datetime, timedelta
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
            return get_display(reshape(t))
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
[data-testid="stSidebar"]{background:linear-gradient(180deg,#0d1117,#161b22,#0d1117)!important;border-right:2px solid rgba(88,166,255,.2)!important}
.kpi-premium{background:linear-gradient(145deg,#1a1f3a,#2d3561);border:2px solid rgba(88,166,255,.2);border-top:4px solid #58a6ff;border-radius:20px;padding:20px 14px 18px;text-align:center;box-shadow:0 8px 32px rgba(0,0,0,.4);transition:all .4s;margin-bottom:14px}
.kpi-premium:hover{transform:translateY(-8px);box-shadow:0 16px 48px rgba(88,166,255,.3)}
.kpi-icon{font-size:1.6rem;margin-bottom:8px;display:block}
.kpi-num{font-size:2rem;font-weight:900;color:#58a6ff;line-height:1;display:block}
.kpi-lbl{font-size:.68rem;color:#7d8590;margin-top:8px;display:block;letter-spacing:1.2px;text-transform:uppercase;font-weight:800}
.sec-premium{background:linear-gradient(90deg,rgba(88,166,255,.15),transparent);border-left:4px solid #58a6ff;border-radius:0 16px 16px 0;padding:12px 24px;margin:28px 0 18px;color:#c9d1d9;font-size:1.05rem;font-weight:900}
.insight-card{background:linear-gradient(135deg,#161b22,#1c2128);border:2px solid rgba(88,166,255,.2);border-left:5px solid #58a6ff;border-radius:18px;padding:18px 22px;margin-bottom:14px;transition:all .3s ease}
.insight-card:hover{box-shadow:0 8px 32px rgba(88,166,255,.2);transform:translateX(4px)}
.insight-badge{display:inline-block;background:rgba(88,166,255,.15);color:#58a6ff;padding:4px 12px;border-radius:20px;font-size:.68rem;font-weight:900;letter-spacing:1px;text-transform:uppercase;margin-bottom:8px}
.insight-text{color:#c9d1d9;font-size:.88rem;line-height:1.7;font-weight:400}
.stDownloadButton>button{background:linear-gradient(135deg,#1f6feb,#58a6ff)!important;color:white!important;border:none!important;border-radius:16px!important;padding:14px 32px!important;font-weight:900!important;font-size:.95rem!important;box-shadow:0 8px 32px rgba(31,111,235,.4)!important;transition:all .4s!important}
.stDownloadButton>button:hover{box-shadow:0 12px 48px rgba(31,111,235,.6)!important;transform:translateY(-4px)!important}
</style>""", unsafe_allow_html=True)

# ── COLUMN NAMES ─────────────────────────────────────────────────
COLUMN_MAP = {
    'إدارة العميل': 'Department',
    'الخدمة': 'Service',
    'التصنيف الرئيسي': 'Main Category',
    'التصنيف الفرعي': 'Sub Category',
    'مسند الى': 'Assigned To',
    'تاريخ الفتح': 'Open Date',
    'تاريخ الإغلاق': 'Close Date',
    'الأولوية': 'Priority',
    'السبب': 'Reason'
}

C_DEPT = 'Department'
C_SVC = 'Service'
C_MAIN = 'Main Category'
C_SUB = 'Sub Category'
C_AGENT = 'Assigned To'
C_OPEN = 'Open Date'
C_CLOSE = 'Close Date'
C_PRIORITY = 'Priority'
C_REASON = 'Reason'

# ── SIDEBAR ──────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("<div style='text-align:center;padding:18px 0 10px'>"
                "<div style='background:linear-gradient(135deg,#1f6feb,#58a6ff);display:inline-block;"
                "border-radius:18px;padding:14px 18px;font-size:2.2rem;box-shadow:0 8px 32px rgba(31,111,235,.4)'>🖥️</div>"
                "</div>", unsafe_allow_html=True)
    st.markdown(f"<h3 style='text-align:center;color:#58a6ff;margin:6px 0 12px;font-size:.95rem;"
                f"font-weight:900'>IT Helpdesk Analytics</h3>", unsafe_allow_html=True)
    st.markdown(f"<div style='text-align:center;font-size:.75rem;font-weight:700;color:{'#3fb950' if FONT_OK else '#d29922'}'>"
                f"{'✅ Ready' if FONT_OK else '⚠️ Loading'}</div>", unsafe_allow_html=True)
    st.markdown("---")
    uploaded = st.file_uploader("📂 Upload Excel", type=["xlsx","xls"])
    if uploaded: st.success(f"✅ {uploaded.name}")

if not uploaded:
    st.markdown(
        "<div style='min-height:88vh;display:flex;flex-direction:column;align-items:center;"
        "justify-content:center;text-align:center;padding:48px'>"
        "<div style='background:linear-gradient(135deg,#1f6feb,#58a6ff);border-radius:32px;"
        "padding:28px;font-size:4rem;margin-bottom:32px;box-shadow:0 20px 60px rgba(31,111,235,.4)'>🖥️</div>"
        "<h1 style='color:#58a6ff;font-size:2.8rem;font-weight:900;margin:0 0 16px'>IT Helpdesk Analytics</h1>"
        "<p style='color:#7d8590;font-size:1.05rem;font-weight:500'>Upload Excel to begin analysis</p></div>",
        unsafe_allow_html=True)
    st.stop()

# ── LOAD DATA WITH DATES ─────────────────────────────────────────
@st.cache_data(show_spinner="⚙️ Processing data...")
def load_data(rb):
    bh = 2
    for h in [0,1,2,3]:
        try:
            t = pd.read_excel(io.BytesIO(rb), sheet_name=0, header=h)
            if 'إدارة العميل' in t.columns: bh=h; break
        except: pass
    
    df = pd.read_excel(io.BytesIO(rb), sheet_name=0, header=bh)
    
    # Remove totals
    for col in df.columns:
        if df[col].dtype == 'object':
            df = df[~df[col].astype(str).str.contains('Grand Total|المجموع|الإجمالي', na=False, case=False)]
    
    # Rename columns
    df = df.rename(columns=COLUMN_MAP)
    
    # Keep relevant columns
    keep = [c for c in [C_DEPT, C_SVC, C_MAIN, C_SUB, C_AGENT, C_OPEN, C_CLOSE, C_PRIORITY, C_REASON] if c in df.columns]
    df = df[keep].copy()
    
    # Forward fill merged cells
    for c in [C_DEPT, C_SVC, C_MAIN, C_SUB]:
        if c in df.columns:
            df[c] = df[c].replace('', pd.NA).ffill()
    
    # Clean agent names
    if C_AGENT in df.columns:
        df[C_AGENT] = df[C_AGENT].astype(str).str.strip()
        df[C_AGENT] = df[C_AGENT].replace({'nan':pd.NA,'Agent':pd.NA,'مسند الى':pd.NA,'':pd.NA})
        df['_short'] = (df[C_AGENT].str.replace('−متعاقد','',regex=False)
                        .str.replace('-متعاقد','',regex=False).str.strip())
    
    # Parse dates
    if C_OPEN in df.columns:
        df[C_OPEN] = pd.to_datetime(df[C_OPEN], errors='coerce')
    if C_CLOSE in df.columns:
        df[C_CLOSE] = pd.to_datetime(df[C_CLOSE], errors='coerce')
    
    # Calculate resolution time in hours
    if C_OPEN in df.columns and C_CLOSE in df.columns:
        df['Resolution_Hours'] = (df[C_CLOSE] - df[C_OPEN]).dt.total_seconds() / 3600
        df['Resolution_Days'] = df['Resolution_Hours'] / 24
    else:
        df['Resolution_Hours'] = pd.NA
        df['Resolution_Days'] = pd.NA
    
    # Clean priority
    if C_PRIORITY in df.columns:
        df[C_PRIORITY] = df[C_PRIORITY].astype(str).str.strip().replace({'nan':pd.NA,'':pd.NA})
    
    # Clean reason
    if C_REASON in df.columns:
        df[C_REASON] = df[C_REASON].astype(str).str.strip().replace({'nan':pd.NA,'':pd.NA})
    
    # Extract month from open date
    if C_OPEN in df.columns:
        df['Month'] = df[C_OPEN].dt.to_period('M').astype(str)
    
    # Remove empty rows
    df.dropna(how='all', inplace=True)
    df.reset_index(drop=True, inplace=True)
    
    # Calculate stats
    acc = {
        'total': len(df),
        'with_dates': df[['Resolution_Hours']].notna().sum()[0] if 'Resolution_Hours' in df.columns else 0,
        'avg_resolution_hours': df['Resolution_Hours'].mean() if 'Resolution_Hours' in df.columns else 0,
        'avg_resolution_days': df['Resolution_Days'].mean() if 'Resolution_Days' in df.columns else 0,
    }
    
    return df, acc

try:
    rb = uploaded.read()
    df, acc = load_data(rb)
except Exception as e:
    st.error(f"❌ {e}"); st.stop()

if df.empty:
    st.error("❌ No data"); st.stop()

# ── SIDEBAR FILTERS ──────────────────────────────────────────────
with st.sidebar:
    st.markdown("---")
    pdf_lang = st.radio("🌐 PDF Language", ["English","العربية"], horizontal=True)
    st.markdown("---")
    
    ALL = "All"
    s_dep = st.selectbox("🏢 Department", [ALL]+sorted(df[C_DEPT].dropna().unique().tolist()))
    s_pri = st.selectbox("⚡ Priority", [ALL]+sorted(df[C_PRIORITY].dropna().unique().tolist())) if C_PRIORITY in df.columns else ALL
    
    st.markdown("---")
    top_n = st.slider("🔢 Top N", 5, 30, 15)

dff = df.copy()
if s_dep != ALL: dff = dff[dff[C_DEPT]==s_dep]
if s_pri != ALL and C_PRIORITY in df.columns: dff = dff[dff[C_PRIORITY]==s_pri]

def sec(l):
    st.markdown(f"<div class='sec-premium'>{l}</div>", unsafe_allow_html=True)

def ccfg(fig, h=450):
    fig.update_layout(
        height=h, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        font=dict(family='Inter, sans-serif', size=11, color='#c9d1d9'),
        margin=dict(l=10,r=10,t=40,b=10))
    return fig

def fmt_time(hours):
    if pd.isna(hours) or hours == 0:
        return "—"
    days = int(hours // 24)
    hrs = int(hours % 24)
    if days > 0:
        return f"{days}d {hrs}h"
    return f"{hrs}h"

# ══════════════════════════════════════════════════════════════════
# DASHBOARD
# ══════════════════════════════════════════════════════════════════

st.markdown(
    "<div style='background:linear-gradient(135deg,#1a1f3a,#2d3561);padding:24px 32px;border-radius:22px;"
    "margin-bottom:20px;border:2px solid rgba(88,166,255,.25)'>"
    "<div style='display:flex;align-items:center;gap:20px'>"
    "<div style='background:linear-gradient(135deg,#1f6feb,#58a6ff);border-radius:20px;"
    "padding:16px 20px;font-size:2.4rem;box-shadow:0 8px 32px rgba(31,111,235,.4)'>🖥️</div>"
    "<div style='flex:1'>"
    "<h1 style='color:#58a6ff;margin:0;font-size:1.9rem;font-weight:900'>IT Helpdesk Analytics</h1>"
    "<div style='color:#7d8590;margin-top:5px;font-size:.8rem;font-weight:600'>Advanced Resolution Time & SLA Analysis</div>"
    f"<div style='color:#7d8590;margin-top:8px;font-size:.8rem'>"
    f"📄 {uploaded.name} • 🗂️ {len(df):,} total • 🔽 {len(dff):,} shown</div>"
    "</div></div></div>",
    unsafe_allow_html=True)

# ── TABS ─────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "📊 Overview", "⏱️ Resolution Time", "⚡ Priority Analysis",
    "👨‍💻 Agent Performance", "📈 Monthly Trends", "🗃️ Raw Data"])

# ══════════════════════════════════════════════════════════════════
# TAB 1: OVERVIEW
# ══════════════════════════════════════════════════════════════════
with tab1:
    sec("📌 KEY PERFORMANCE INDICATORS")
    
    k1,k2,k3,k4,k5 = st.columns(5)
    
    with k1:
        st.markdown(
            f"<div class='kpi-premium'><span class='kpi-icon'>🎫</span>"
            f"<span class='kpi-num'>{len(dff):,}</span>"
            f"<span class='kpi-lbl'>Total Tickets</span></div>",
            unsafe_allow_html=True)
    
    with k2:
        avg_hrs = dff['Resolution_Hours'].mean()
        st.markdown(
            f"<div class='kpi-premium'><span class='kpi-icon'>⏱️</span>"
            f"<span class='kpi-num'>{fmt_time(avg_hrs)}</span>"
            f"<span class='kpi-lbl'>Avg Resolution</span></div>",
            unsafe_allow_html=True)
    
    with k3:
        st.markdown(
            f"<div class='kpi-premium'><span class='kpi-icon'>🏢</span>"
            f"<span class='kpi-num'>{dff[C_DEPT].nunique()}</span>"
            f"<span class='kpi-lbl'>Departments</span></div>",
            unsafe_allow_html=True)
    
    with k4:
        st.markdown(
            f"<div class='kpi-premium'><span class='kpi-icon'>👨‍💻</span>"
            f"<span class='kpi-num'>{dff[C_AGENT].dropna().nunique()}</span>"
            f"<span class='kpi-lbl'>Agents</span></div>",
            unsafe_allow_html=True)
    
    with k5:
        if C_PRIORITY in dff.columns:
            high_pct = round(len(dff[dff[C_PRIORITY]=='High'])/len(dff)*100,1) if len(dff) > 0 else 0
        else:
            high_pct = 0
        st.markdown(
            f"<div class='kpi-premium'><span class='kpi-icon'>⚡</span>"
            f"<span class='kpi-num'>{high_pct}%</span>"
            f"<span class='kpi-lbl'>High Priority</span></div>",
            unsafe_allow_html=True)
    
    sec("🎯 SLA COMPLIANCE")
    
    total_with_time = dff['Resolution_Hours'].notna().sum()
    sla_24h = len(dff[dff['Resolution_Hours'] <= 24]) if total_with_time > 0 else 0
    sla_3d = len(dff[dff['Resolution_Days'] > 3]) if total_with_time > 0 else 0
    sla_7d = len(dff[dff['Resolution_Days'] > 7]) if total_with_time > 0 else 0
    
    pct_24h = round(sla_24h/total_with_time*100,1) if total_with_time > 0 else 0
    pct_3d = round(sla_3d/total_with_time*100,1) if total_with_time > 0 else 0
    pct_7d = round(sla_7d/total_with_time*100,1) if total_with_time > 0 else 0
    
    s1,s2,s3 = st.columns(3)
    
    with s1:
        st.markdown(
            f"<div class='insight-card'><div class='insight-badge'>✅ WITHIN 24H</div>"
            f"<div class='insight-text'><b style='color:#3fb950;font-size:1.8rem'>{pct_24h}%</b><br>"
            f"{sla_24h:,} tickets resolved within 24 hours</div></div>",
            unsafe_allow_html=True)
    
    with s2:
        st.markdown(
            f"<div class='insight-card'><div class='insight-badge'>⚠️ MORE THAN 3 DAYS</div>"
            f"<div class='insight-text'><b style='color:#d29922;font-size:1.8rem'>{pct_3d}%</b><br>"
            f"{sla_3d:,} tickets took more than 3 days</div></div>",
            unsafe_allow_html=True)
    
    with s3:
        st.markdown(
            f"<div class='insight-card'><div class='insight-badge'>🔴 MORE THAN 7 DAYS</div>"
            f"<div class='insight-text'><b style='color:#f85149;font-size:1.8rem'>{pct_7d}%</b><br>"
            f"{sla_7d:,} tickets took more than 7 days</div></div>",
            unsafe_allow_html=True)
    
    st.markdown("---")
    
    c1, c2 = st.columns(2)
    
    with c1:
        dept_data = dff[C_DEPT].value_counts().head(10).reset_index()
        dept_data.columns = ['Department', 'Count']
        fig = px.bar(dept_data, x='Count', y='Department', orientation='h',
                     color='Count', color_continuous_scale='Teal',
                     title='Top 10 Departments by Ticket Volume')
        fig.update_layout(yaxis={'categoryorder':'total ascending'}, showlegend=False, coloraxis_showscale=False)
        fig.update_traces(textposition='outside', text=dept_data['Count'])
        st.plotly_chart(ccfg(fig, 450), use_container_width=True)
    
    with c2:
        if C_PRIORITY in dff.columns:
            pri_data = dff[C_PRIORITY].value_counts().reset_index()
            pri_data.columns = ['Priority', 'Count']
            fig = px.pie(pri_data, values='Count', names='Priority', hole=0.45,
                         title='Priority Distribution',
                         color_discrete_sequence=['#f85149','#d29922','#3fb950'])
            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(ccfg(fig, 450), use_container_width=True)

# ══════════════════════════════════════════════════════════════════
# TAB 2: RESOLUTION TIME
# ══════════════════════════════════════════════════════════════════
with tab2:
    sec("⏱️ AVERAGE RESOLUTION TIME ANALYSIS")
    
    r1, r2, r3 = st.columns(3)
    
    with r1:
        overall_avg = dff['Resolution_Hours'].mean()
        st.markdown(
            f"<div class='insight-card'><div class='insight-badge'>📊 OVERALL AVERAGE</div>"
            f"<div class='insight-text'><b style='color:#58a6ff;font-size:2rem'>{fmt_time(overall_avg)}</b><br>"
            f"Average resolution time for all tickets</div></div>",
            unsafe_allow_html=True)
    
    with r2:
        median_hrs = dff['Resolution_Hours'].median()
        st.markdown(
            f"<div class='insight-card'><div class='insight-badge'>📈 MEDIAN TIME</div>"
            f"<div class='insight-text'><b style='color:#3fb950;font-size:2rem'>{fmt_time(median_hrs)}</b><br>"
            f"50% of tickets resolved faster than this</div></div>",
            unsafe_allow_html=True)
    
    with r3:
        max_hrs = dff['Resolution_Hours'].max()
        st.markdown(
            f"<div class='insight-card'><div class='insight-badge'>⚠️ LONGEST TIME</div>"
            f"<div class='insight-text'><b style='color:#f85149;font-size:2rem'>{fmt_time(max_hrs)}</b><br>"
            f"Maximum resolution time recorded</div></div>",
            unsafe_allow_html=True)
    
    st.markdown("---")
    
    # By Priority
    if C_PRIORITY in dff.columns:
        sec("⚡ AVERAGE RESOLUTION TIME BY PRIORITY")
        pri_time = dff.groupby(C_PRIORITY)['Resolution_Hours'].mean().sort_values(ascending=False).reset_index()
        pri_time.columns = ['Priority', 'Avg Hours']
        pri_time['Avg Time'] = pri_time['Avg Hours'].apply(fmt_time)
        
        fig = px.bar(pri_time, x='Avg Hours', y='Priority', orientation='h',
                     color='Avg Hours', color_continuous_scale='Reds',
                     text='Avg Time', title='Average Resolution Time by Priority')
        fig.update_layout(yaxis={'categoryorder':'total ascending'}, showlegend=False, coloraxis_showscale=False)
        fig.update_traces(textposition='outside')
        st.plotly_chart(ccfg(fig, 400), use_container_width=True)
        
        st.dataframe(pri_time[['Priority', 'Avg Time']], use_container_width=True, height=200)
    
    # By Department
    sec("🏢 AVERAGE RESOLUTION TIME BY DEPARTMENT (Top 15)")
    dept_time = dff.groupby(C_DEPT).agg({
        'Resolution_Hours': 'mean',
        C_DEPT: 'count'
    }).rename(columns={C_DEPT: 'Count'}).reset_index()
    dept_time = dept_time.sort_values('Resolution_Hours', ascending=False).head(15)
    dept_time['Avg Time'] = dept_time['Resolution_Hours'].apply(fmt_time)
    
    fig = px.bar(dept_time, x='Resolution_Hours', y=C_DEPT, orientation='h',
                 color='Resolution_Hours', color_continuous_scale='Oranges',
                 text='Avg Time', title='Average Resolution Time by Department')
    fig.update_layout(yaxis={'categoryorder':'total ascending'}, showlegend=False, coloraxis_showscale=False)
    fig.update_traces(textposition='outside')
    st.plotly_chart(ccfg(fig, 550), use_container_width=True)
    
    st.dataframe(dept_time[[C_DEPT, 'Count', 'Avg Time']], use_container_width=True, height=400)
    
    # By Reason
    if C_REASON in dff.columns:
        sec("🔍 AVERAGE RESOLUTION TIME BY REASON (Top 10)")
        reason_time = dff.groupby(C_REASON).agg({
            'Resolution_Hours': 'mean',
            C_REASON: 'count'
        }).rename(columns={C_REASON: 'Count'}).reset_index()
        reason_time = reason_time.sort_values('Resolution_Hours', ascending=False).head(10)
        reason_time['Avg Time'] = reason_time['Resolution_Hours'].apply(fmt_time)
        
        fig = px.bar(reason_time, x='Resolution_Hours', y=C_REASON, orientation='h',
                     color='Resolution_Hours', color_continuous_scale='Purples',
                     text='Avg Time', title='Top 10 Reasons by Average Resolution Time')
        fig.update_layout(yaxis={'categoryorder':'total ascending'}, showlegend=False, coloraxis_showscale=False)
        fig.update_traces(textposition='outside')
        st.plotly_chart(ccfg(fig, 450), use_container_width=True)
        
        st.dataframe(reason_time[[C_REASON, 'Count', 'Avg Time']], use_container_width=True, height=350)

# ══════════════════════════════════════════════════════════════════
# TAB 3: PRIORITY ANALYSIS
# ══════════════════════════════════════════════════════════════════
with tab3:
    if C_PRIORITY not in dff.columns:
        st.info("⚠️ Priority column not available in data")
    else:
        sec("⚡ PRIORITY DISTRIBUTION & ANALYSIS")
        
        total = len(dff)
        high_cnt = len(dff[dff[C_PRIORITY]=='High'])
        med_cnt = len(dff[dff[C_PRIORITY]=='Medium'])
        low_cnt = len(dff[dff[C_PRIORITY]=='Low'])
        
        high_pct = round(high_cnt/total*100,1) if total > 0 else 0
        med_pct = round(med_cnt/total*100,1) if total > 0 else 0
        low_pct = round(low_cnt/total*100,1) if total > 0 else 0
        
        p1, p2, p3 = st.columns(3)
        
        with p1:
            st.markdown(
                f"<div class='insight-card' style='border-left-color:#f85149'>"
                f"<div class='insight-badge' style='background:rgba(248,81,73,.15);color:#f85149'>HIGH PRIORITY</div>"
                f"<div class='insight-text'><b style='color:#f85149;font-size:2.2rem'>{high_pct}%</b><br>"
                f"{high_cnt:,} tickets • High priority cases</div></div>",
                unsafe_allow_html=True)
        
        with p2:
            st.markdown(
                f"<div class='insight-card' style='border-left-color:#d29922'>"
                f"<div class='insight-badge' style='background:rgba(210,153,34,.15);color:#d29922'>MEDIUM PRIORITY</div>"
                f"<div class='insight-text'><b style='color:#d29922;font-size:2.2rem'>{med_pct}%</b><br>"
                f"{med_cnt:,} tickets • Medium priority cases</div></div>",
                unsafe_allow_html=True)
        
        with p3:
            st.markdown(
                f"<div class='insight-card' style='border-left-color:#3fb950'>"
                f"<div class='insight-badge' style='background:rgba(63,185,80,.15);color:#3fb950'>LOW PRIORITY</div>"
                f"<div class='insight-text'><b style='color:#3fb950;font-size:2.2rem'>{low_pct}%</b><br>"
                f"{low_cnt:,} tickets • Low priority cases</div></div>",
                unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Priority by Department
        sec("🏢 HIGH PRIORITY PERCENTAGE BY DEPARTMENT (Top 15)")
        
        dept_pri = dff.groupby(C_DEPT).apply(lambda x: pd.Series({
            'Total': len(x),
            'High': len(x[x[C_PRIORITY]=='High']),
            'High %': round(len(x[x[C_PRIORITY]=='High'])/len(x)*100,1) if len(x) > 0 else 0
        })).reset_index()
        dept_pri = dept_pri.sort_values('High %', ascending=False).head(15)
        
        fig = px.bar(dept_pri, x='High %', y=C_DEPT, orientation='h',
                     color='High %', color_continuous_scale='Reds',
                     text='High %', title='High Priority % by Department')
        fig.update_layout(yaxis={'categoryorder':'total ascending'}, showlegend=False, coloraxis_showscale=False)
        fig.update_traces(textposition='outside')
        st.plotly_chart(ccfg(fig, 550), use_container_width=True)
        
        st.dataframe(dept_pri, use_container_width=True, height=400)

# ══════════════════════════════════════════════════════════════════
# TAB 4: AGENT PERFORMANCE
# ══════════════════════════════════════════════════════════════════
with tab4:
    if dff[C_AGENT].dropna().empty:
        st.info("⚠️ No agent data available")
    else:
        sec("👨‍💻 AGENT PERFORMANCE ANALYSIS")
        
        agent_stats = dff.dropna(subset=[C_AGENT]).groupby(C_AGENT).agg({
            C_AGENT: 'count',
            'Resolution_Hours': 'mean'
        }).rename(columns={C_AGENT: 'Tickets', 'Resolution_Hours': 'Avg Hours'}).reset_index()
        
        if C_PRIORITY in dff.columns:
            agent_high = dff[dff[C_PRIORITY]=='High'].groupby(C_AGENT).size().reset_index(name='High Count')
            agent_stats = agent_stats.merge(agent_high, on=C_AGENT, how='left').fillna(0)
            agent_stats['High Count'] = agent_stats['High Count'].astype(int)
        
        agent_stats = agent_stats.sort_values('Tickets', ascending=False).head(top_n)
        agent_stats['Avg Time'] = agent_stats['Avg Hours'].apply(fmt_time)
        agent_stats['Agent Short'] = agent_stats[C_AGENT].str.replace('−متعاقد','').str.replace('-متعاقد','').str.strip()
        
        # Table
        sec(f"📋 TOP {top_n} AGENTS — DETAILED STATS")
        if C_PRIORITY in dff.columns:
            display_cols = ['Agent Short', 'Tickets', 'Avg Time', 'High Count']
        else:
            display_cols = ['Agent Short', 'Tickets', 'Avg Time']
        st.dataframe(agent_stats[display_cols], use_container_width=True, height=500)
        
        st.markdown("---")
        
        # Charts
        c1, c2 = st.columns(2)
        
        with c1:
            fig = px.bar(agent_stats, x='Tickets', y='Agent Short', orientation='h',
                         color='Tickets', color_continuous_scale='Viridis',
                         text='Tickets', title=f'Top {top_n} Agents by Ticket Count')
            fig.update_layout(yaxis={'categoryorder':'total ascending'}, showlegend=False, coloraxis_showscale=False)
            fig.update_traces(textposition='outside')
            st.plotly_chart(ccfg(fig, 500), use_container_width=True)
        
        with c2:
            fig = px.bar(agent_stats, x='Avg Hours', y='Agent Short', orientation='h',
                         color='Avg Hours', color_continuous_scale='Oranges',
                         text=agent_stats['Avg Time'], title=f'Top {top_n} Agents by Avg Resolution Time')
            fig.update_layout(yaxis={'categoryorder':'total ascending'}, showlegend=False, coloraxis_showscale=False)
            fig.update_traces(textposition='outside')
            st.plotly_chart(ccfg(fig, 500), use_container_width=True)

# ══════════════════════════════════════════════════════════════════
# TAB 5: MONTHLY TRENDS
# ══════════════════════════════════════════════════════════════════
with tab5:
    if 'Month' not in dff.columns or dff['Month'].isna().all():
        st.info("⚠️ Date information not available")
    else:
        sec("📈 MONTHLY TRENDS ANALYSIS")
        
        monthly = dff.groupby('Month').agg({
            'Month': 'count',
            'Resolution_Hours': 'mean'
        }).rename(columns={'Month': 'Tickets', 'Resolution_Hours': 'Avg Hours'}).reset_index()
        monthly['Avg Time'] = monthly['Avg Hours'].apply(fmt_time)
        
        if C_PRIORITY in dff.columns:
            monthly_high = dff[dff[C_PRIORITY]=='High'].groupby('Month').size().reset_index(name='High Count')
            monthly = monthly.merge(monthly_high, on='Month', how='left').fillna(0)
            monthly['High Count'] = monthly['High Count'].astype(int)
            monthly['High %'] = round(monthly['High Count']/monthly['Tickets']*100,1)
        
        monthly = monthly.sort_values('Month')
        
        # Line charts
        fig = make_subplots(rows=2, cols=1,
                           subplot_titles=('Monthly Ticket Volume', 'Monthly Avg Resolution Time'),
                           vertical_spacing=0.15)
        
        fig.add_trace(go.Scatter(x=monthly['Month'], y=monthly['Tickets'],
                                mode='lines+markers', name='Tickets',
                                line=dict(color='#58a6ff', width=3),
                                marker=dict(size=8)),
                     row=1, col=1)
        
        fig.add_trace(go.Scatter(x=monthly['Month'], y=monthly['Avg Hours'],
                                mode='lines+markers', name='Avg Hours',
                                line=dict(color='#d29922', width=3),
                                marker=dict(size=8)),
                     row=2, col=1)
        
        fig.update_layout(height=700, showlegend=False,
                         paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                         font=dict(color='#c9d1d9'))
        fig.update_xaxes(showgrid=True, gridcolor='rgba(125,133,144,.1)')
        fig.update_yaxes(showgrid=True, gridcolor='rgba(125,133,144,.1)')
        
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("---")
        
        # Monthly table
        sec("📊 MONTHLY DETAILED STATISTICS")
        if C_PRIORITY in dff.columns:
            display_cols = ['Month', 'Tickets', 'Avg Time', 'High Count', 'High %']
        else:
            display_cols = ['Month', 'Tickets', 'Avg Time']
        st.dataframe(monthly[display_cols], use_container_width=True, height=450)

# ══════════════════════════════════════════════════════════════════
# TAB 6: RAW DATA
# ══════════════════════════════════════════════════════════════════
with tab6:
    sec("🗃️ RAW DATA EXPLORER")
    
    display_df = dff.copy()
    if 'Resolution_Hours' in display_df.columns:
        display_df['Resolution Time'] = display_df['Resolution_Hours'].apply(fmt_time)
    
    c1, c2 = st.columns([1, 3])
    with c1:
        search_col = st.selectbox("Column", ["All"] + display_df.columns.tolist())
    with c2:
        search_val = st.text_input("🔍 Search", "")
    
    if search_val:
        if search_col == "All":
            mask = display_df.apply(lambda c: c.astype(str).str.contains(search_val, case=False, na=False)).any(axis=1)
        else:
            mask = display_df[search_col].astype(str).str.contains(search_val, case=False, na=False)
        display_df = display_df[mask]
    
    st.markdown(f"<div style='color:#7d8590;margin-bottom:8px'>"
                f"<b style='color:#58a6ff'>{len(display_df):,}</b> of {len(df):,} records</div>",
                unsafe_allow_html=True)
    
    st.dataframe(display_df, use_container_width=True, height=550)

# ══════════════════════════════════════════════════════════════════
# FOOTER
# ══════════════════════════════════════════════════════════════════
st.markdown("---")
st.markdown(
    "<div style='text-align:center;margin-top:40px;padding-top:20px;border-top:1px solid rgba(88,166,255,.1)'>"
    "<div style='color:#7d8590;font-size:.88rem;font-weight:600'>Advanced IT Helpdesk Analytics Platform</div>"
    "<div style='color:#58a6ff;font-size:.78rem;margin-top:6px;font-weight:500'>Crafted by Tarique Siddique 💙</div>"
    "</div>",
    unsafe_allow_html=True)
