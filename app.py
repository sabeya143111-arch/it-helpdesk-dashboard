# ================================================================
#   IT HELPDESK ANALYTICS — FULL FEATURED VERSION
#   With PDF Export + Excel Download + All Original Features
# ================================================================

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import io, os
from datetime import datetime, timedelta
from fpdf import FPDF

# ================================================================
#  PAGE CONFIG
# ================================================================
st.set_page_config(
    page_title="IT Helpdesk Analytics",
    page_icon="🖥️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ================================================================
#  CSS (ORIGINAL PREMIUM STYLE)
# ================================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700;800;900&display=swap');
*{font-family:'Inter',sans-serif!important;box-sizing:border-box}
.stApp{background:linear-gradient(135deg,#0a0e27 0%,#1a1f3a 50%,#0a0e27 100%)!important}
.main .block-container{background:transparent!important;padding-top:.8rem!important;max-width:100%!important}
[data-testid="stSidebar"]{background:linear-gradient(180deg,#0d1117,#161b22,#0d1117)!important;border-right:2px solid rgba(88,166,255,.2)!important;}

/* KPIs */
.kpi-premium{background:linear-gradient(145deg,#1a1f3a,#2d3561);border:2px solid rgba(88,166,255,.2);border-top:4px solid #58a6ff;border-radius:20px;padding:20px 14px 18px;text-align:center;box-shadow:0 8px 32px rgba(0,0,0,.4);transition:all .4s;margin-bottom:14px}
.kpi-premium:hover{transform:translateY(-8px);box-shadow:0 16px 48px rgba(88,166,255,.3)}
.kpi-icon{font-size:1.6rem;margin-bottom:8px;display:block}
.kpi-num{font-size:2rem;font-weight:900;color:#58a6ff;line-height:1;display:block}
.kpi-lbl{font-size:.68rem;color:#7d8590;margin-top:8px;display:block;letter-spacing:1.2px;text-transform:uppercase;font-weight:800}

/* Section header */
.sec-premium{background:linear-gradient(90deg,rgba(88,166,255,.15),transparent);border-left:4px solid #58a6ff;border-radius:0 16px 16px 0;padding:12px 24px;margin:28px 0 18px;color:#c9d1d9;font-size:1.05rem;font-weight:900}

/* Insight cards */
.insight-card{background:linear-gradient(135deg,#161b22,#1c2128);border:2px solid rgba(88,166,255,.2);border-left:5px solid #58a6ff;border-radius:18px;padding:18px 22px;margin-bottom:14px;transition:all .3s ease}
.insight-card:hover{box-shadow:0 8px 32px rgba(88,166,255,.2);transform:translateX(4px)}
.insight-badge{display:inline-block;background:rgba(88,166,255,.15);color:#58a6ff;padding:4px 12px;border-radius:20px;font-size:.68rem;font-weight:900;letter-spacing:1px;text-transform:uppercase;margin-bottom:8px}
.insight-text{color:#c9d1d9;font-size:.88rem;line-height:1.7;font-weight:400}

/* Download buttons */
.stDownloadButton>button{
    background:linear-gradient(135deg,#1f6feb,#58a6ff)!important;
    color:white!important;border:none!important;border-radius:16px!important;
    padding:14px 32px!important;font-weight:900!important;font-size:.95rem!important;
    box-shadow:0 8px 32px rgba(31,111,235,.4)!important;transition:all .4s!important
}
.stDownloadButton>button:hover{
    box-shadow:0 12px 48px rgba(31,111,235,.6)!important;
    transform:translateY(-4px)!important
}
</style>
""", unsafe_allow_html=True)

# ================================================================
#  ARABIC COLUMN DEFINITIONS
# ================================================================
AR_COL_ID       = 'رقم البلاغ'
AR_COL_STATUS   = 'الحالة'
AR_COL_CLIENT   = 'العميل'
AR_COL_DEPT     = 'إدارة العميل'
AR_COL_SUMMARY  = 'ملخص البلاغ'
AR_COL_SERVICE  = 'الخدمة'
AR_COL_MAIN     = 'التصنيف الرئيسي'
AR_COL_SUB      = 'التصنيف الفرعي'
AR_COL_IMPACT   = 'التأثير'
AR_COL_URGENCY  = 'الأهمية'
AR_COL_AGENT    = 'مسند الى'
AR_COL_OPEN     = 'تاريخ الإنشاء'
AR_COL_UPDATE   = 'تاريخ التعديل'
AR_COL_RESOLVE  = 'تاريخ حل البلاغ'
AR_COL_CLOSE    = 'تاريخ ووقت الاغلاق'
AR_COL_RESP_SLA = 'تم خرق اتفاقية الاستجابة'
AR_COL_RES_SLA  = 'تم خرق اتفاقية الحل'
AR_COL_SOLUTION = 'الحل'
AR_COL_RESOLVED_BY = 'تم حل بواسطة'

# Internal English labels
C_ID        = 'Ticket ID'
C_STATUS    = 'Status'
C_CLIENT    = 'Client'
C_DEPT      = 'Department'
C_SUMMARY   = 'Summary'
C_SERVICE   = 'Service'
C_MAIN      = 'Main Category'
C_SUB       = 'Sub Category'
C_IMPACT    = 'Impact'
C_URGENCY   = 'Urgency'
C_PRIORITY  = 'Priority'
C_AGENT     = 'Assigned To'
C_OPEN      = 'Open Date'
C_UPDATE    = 'Update Date'
C_RESOLVE   = 'Resolved Date'
C_CLOSE     = 'Close Date'
C_RESP_SLA  = 'Resp SLA Breach'
C_RES_SLA   = 'Resol SLA Breach'
C_REASON    = 'Reason'
C_RESOLVED_BY = 'Resolved By'

# ================================================================
#  SIDEBAR
# ================================================================
with st.sidebar:
    st.markdown(
        "<div style='text-align:center;padding:18px 0 10px'>"
        "<div style='background:linear-gradient(135deg,#1f6feb,#58a6ff);display:inline-block;"
        "border-radius:18px;padding:14px 18px;font-size:2.2rem;box-shadow:0 8px 32px rgba(31,111,235,.4)'>🖥️</div>"
        "</div>",
        unsafe_allow_html=True,
    )
    st.markdown(
        "<h3 style='text-align:center;color:#58a6ff;margin:6px 0 12px;"
        "font-size:.95rem;font-weight:900'>IT Helpdesk Analytics</h3>",
        unsafe_allow_html=True,
    )
    st.markdown("---")
    uploaded = st.file_uploader("📂 Upload Helpdesk Excel", type=["xlsx", "xls"])
    if uploaded:
        st.success(f"✅ {uploaded.name}")

if not uploaded:
    st.markdown(
        "<div style='min-height:88vh;display:flex;flex-direction:column;align-items:center;"
        "justify-content:center;text-align:center;padding:48px'>"
        "<div style='background:linear-gradient(135deg,#1f6feb,#58a6ff);border-radius:32px;"
        "padding:28px;font-size:4rem;margin-bottom:32px;box-shadow:0 20px 60px rgba(31,111,235,.4)'>🖥️</div>"
        "<h1 style='color:#58a6ff;font-size:2.8rem;font-weight:900;margin:0 0 16px'>IT Helpdesk Analytics</h1>"
        "<p style='color:#7d8590;font-size:1.05rem;font-weight:500'>Upload the Arabic report Excel file to start</p></div>",
        unsafe_allow_html=True,
    )
    st.stop()

# ================================================================
#  DATA LOADER
# ================================================================
@st.cache_data(show_spinner="⚙️ Processing data...")
def load_data(raw_bytes: bytes):
    # Detect header row
    best_header = 0
    for h in [0, 1, 2, 3, 4, 5]:
        try:
            tmp = pd.read_excel(io.BytesIO(raw_bytes), sheet_name=0, header=h)
            if AR_COL_ID in tmp.columns:
                best_header = h
                break
        except Exception:
            continue

    df = pd.read_excel(io.BytesIO(raw_bytes), sheet_name=0, header=best_header)

    # Remove total rows
    for col in df.columns:
        if df[col].dtype == 'object':
            df = df[~df[col].astype(str).str.contains(
                'Grand Total|المجموع|الإجمالي', na=False, case=False
            )]

    # Arabic → internal rename
    rename_map = {
        AR_COL_ID: C_ID,
        AR_COL_STATUS: C_STATUS,
        AR_COL_CLIENT: C_CLIENT,
        AR_COL_DEPT: C_DEPT,
        AR_COL_SUMMARY: C_SUMMARY,
        AR_COL_SERVICE: C_SERVICE,
        AR_COL_MAIN: C_MAIN,
        AR_COL_SUB: C_SUB,
        AR_COL_IMPACT: C_IMPACT,
        AR_COL_URGENCY: C_URGENCY,
        AR_COL_AGENT: C_AGENT,
        AR_COL_OPEN: C_OPEN,
        AR_COL_UPDATE: C_UPDATE,
        AR_COL_RESOLVE: C_RESOLVE,
        AR_COL_CLOSE: C_CLOSE,
        AR_COL_RESP_SLA: C_RESP_SLA,
        AR_COL_RES_SLA: C_RES_SLA,
        AR_COL_SOLUTION: C_REASON,
        AR_COL_RESOLVED_BY: C_RESOLVED_BY,
    }
    df = df.rename(columns=rename_map)

    # Keep relevant columns
    keep_cols = [c for c in [
        C_ID, C_STATUS, C_CLIENT, C_DEPT, C_SUMMARY, C_SERVICE,
        C_MAIN, C_SUB, C_IMPACT, C_URGENCY, C_AGENT,
        C_OPEN, C_UPDATE, C_RESOLVE, C_CLOSE,
        C_RESP_SLA, C_RES_SLA, C_REASON, C_RESOLVED_BY
    ] if c in df.columns]
    df = df[keep_cols].copy()

    # Forward fill merged columns
    for c in [C_DEPT, C_SERVICE, C_MAIN, C_SUB]:
        if c in df.columns:
            df[c] = df[c].replace('', pd.NA).ffill()

    # Clean Agent
    if C_AGENT in df.columns:
        df[C_AGENT] = df[C_AGENT].astype(str).str.strip()
        df[C_AGENT] = df[C_AGENT].replace(
            {'nan': pd.NA, '': pd.NA, 'Agent': pd.NA, 'مسند الى': pd.NA}
        )
        df['_Agent Short'] = (
            df[C_AGENT]
            .str.replace('−متعاقد', '', regex=False)
            .str.replace('-متعاقد', '', regex=False)
            .str.strip()
        )
    else:
        df['_Agent Short'] = pd.NA

    # Parse dates
    for col in [C_OPEN, C_UPDATE, C_RESOLVE, C_CLOSE]:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors='coerce')

    # Resolution time
    if C_OPEN in df.columns and C_CLOSE in df.columns:
        delta = df[C_CLOSE] - df[C_OPEN]
        df['Resolution_Hours'] = delta.dt.total_seconds() / 3600
        df['Resolution_Days'] = df['Resolution_Hours'] / 24
    else:
        df['Resolution_Hours'] = pd.NA
        df['Resolution_Days'] = pd.NA

    # Month
    if C_OPEN in df.columns:
        df['Month'] = df[C_OPEN].dt.to_period('M').astype(str)

    # Priority from numeric column
    if C_PRIORITY not in df.columns:
        pri_col = None
        for col in df.columns:
            if col in [C_ID, C_OPEN, C_CLOSE, C_STATUS, C_AGENT, C_DEPT]:
                continue
            try:
                num_frac = df[col].dropna().astype(str).str.match(r'^[0-9]+(\.0)?$').mean()
            except Exception:
                num_frac = 0
            if num_frac > 0.9:
                pri_col = col
                break

        if pri_col:
            tmp = pd.to_numeric(df[pri_col], errors='coerce')
            pr = []
            for v in tmp:
                if v == 1:
                    pr.append('High')
                elif v in [3, 4]:
                    pr.append('Medium')
                elif v == 5:
                    pr.append('Low')
                else:
                    pr.append(pd.NA)
            df[C_PRIORITY] = pr
        else:
            df[C_PRIORITY] = 'Low'

    df[C_PRIORITY] = df[C_PRIORITY].astype(str).str.strip().replace({'nan': pd.NA, '': pd.NA})

    # Reason
    if C_REASON in df.columns:
        df[C_REASON] = df[C_REASON].astype(str).str.strip().replace({'nan': pd.NA, '': pd.NA})
    else:
        df[C_REASON] = df.get(C_SUMMARY, pd.NA)

    # SLA columns
    for col in [C_RESP_SLA, C_RES_SLA]:
        if col in df.columns:
            df[col] = df[col].astype(str).str.strip().replace({'nan': '', '': ''})

    df.dropna(how='all', inplace=True)
    df.reset_index(drop=True, inplace=True)

    return df

try:
    raw_bytes = uploaded.read()
    df = load_data(raw_bytes)
except Exception as e:
    st.error(f"❌ Error: {e}")
    st.stop()

if df.empty:
    st.error("❌ No data.")
    st.stop()

# ================================================================
#  SIDEBAR FILTERS
# ================================================================
with st.sidebar:
    st.markdown("---")
    ALL = "All"
    dep_opts = [ALL] + sorted(df[C_DEPT].dropna().unique().tolist()) if C_DEPT in df.columns else [ALL]
    pri_opts = [ALL] + sorted(df[C_PRIORITY].dropna().unique().tolist()) if C_PRIORITY in df.columns else [ALL]
    s_dep = st.selectbox("🏢 Department", dep_opts)
    s_pri = st.selectbox("⚡ Priority", pri_opts)
    st.markdown("---")
    top_n = st.slider("🔢 Top N", 5, 30, 15)

dff = df.copy()
if s_dep != ALL and C_DEPT in dff.columns:
    dff = dff[dff[C_DEPT] == s_dep]
if s_pri != ALL and C_PRIORITY in dff.columns:
    dff = dff[dff[C_PRIORITY] == s_pri]

# ================================================================
#  HELPER FUNCTIONS
# ================================================================
def sec(title: str):
    st.markdown(f"<div class='sec-premium'>{title}</div>", unsafe_allow_html=True)

def fmt_time(hours):
    try:
        if pd.isna(hours) or hours == 0:
            return "—"
    except Exception:
        return "—"
    days = int(hours // 24)
    hrs = int(hours % 24)
    if days > 0:
        return f"{days}d {hrs}h"
    return f"{hrs}h"

def ccfg(fig, h=450):
    fig.update_layout(
        height=h,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(family='Inter, sans-serif', size=11, color='#c9d1d9'),
        margin=dict(l=10, r=10, t=40, b=10),
    )
    return fig

# ================================================================
#  PDF GENERATION FUNCTION
# ================================================================
def generate_pdf_report(dff, uploaded_name):
    """Generate executive summary PDF"""
    pdf = FPDF()
    pdf.add_page()
    
    # Title
    pdf.set_font('Arial', 'B', 20)
    pdf.cell(0, 15, 'IT Helpdesk Analytics', ln=True, align='C')
    pdf.set_font('Arial', 'I', 10)
    pdf.cell(0, 8, f'Executive Summary Report', ln=True, align='C')
    pdf.cell(0, 6, f'Generated: {datetime.now().strftime("%Y-%m-%d %H:%M")}', ln=True, align='C')
    pdf.ln(10)
    
    # KPIs Section
    pdf.set_font('Arial', 'B', 14)
    pdf.cell(0, 10, 'KEY PERFORMANCE INDICATORS', ln=True)
    pdf.set_font('Arial', '', 10)
    
    total_tickets = len(dff)
    avg_hours = dff['Resolution_Hours'].mean()
    dept_count = dff[C_DEPT].nunique() if C_DEPT in dff.columns else 0
    agent_count = dff[C_AGENT].dropna().nunique() if C_AGENT in dff.columns else 0
    
    pdf.cell(0, 6, f'Total Tickets: {total_tickets:,}', ln=True)
    pdf.cell(0, 6, f'Average Resolution Time: {fmt_time(avg_hours)}', ln=True)
    pdf.cell(0, 6, f'Active Departments: {dept_count}', ln=True)
    pdf.cell(0, 6, f'Active Agents: {agent_count}', ln=True)
    pdf.ln(8)
    
    # Priority Distribution
    if C_PRIORITY in dff.columns:
        pdf.set_font('Arial', 'B', 14)
        pdf.cell(0, 10, 'PRIORITY DISTRIBUTION', ln=True)
        pdf.set_font('Arial', '', 10)
        
        pri_counts = dff[C_PRIORITY].value_counts()
        for pri, cnt in pri_counts.items():
            pct = round(cnt / len(dff) * 100, 1)
            pdf.cell(0, 6, f'{pri}: {cnt:,} tickets ({pct}%)', ln=True)
        pdf.ln(8)
    
    # SLA Compliance
    pdf.set_font('Arial', 'B', 14)
    pdf.cell(0, 10, 'SLA COMPLIANCE', ln=True)
    pdf.set_font('Arial', '', 10)
    
    total_with_time = dff['Resolution_Hours'].notna().sum()
    if total_with_time > 0:
        sla_24h = len(dff[dff['Resolution_Hours'] <= 24])
        sla_3d = len(dff[dff['Resolution_Days'] > 3])
        sla_7d = len(dff[dff['Resolution_Days'] > 7])
        
        pdf.cell(0, 6, f'Within 24 Hours: {sla_24h:,} ({round(sla_24h/total_with_time*100,1)}%)', ln=True)
        pdf.cell(0, 6, f'Beyond 3 Days: {sla_3d:,} ({round(sla_3d/total_with_time*100,1)}%)', ln=True)
        pdf.cell(0, 6, f'Beyond 7 Days: {sla_7d:,} ({round(sla_7d/total_with_time*100,1)}%)', ln=True)
    pdf.ln(8)
    
    # Top Departments
    if C_DEPT in dff.columns:
        pdf.set_font('Arial', 'B', 14)
        pdf.cell(0, 10, 'TOP 5 DEPARTMENTS BY VOLUME', ln=True)
        pdf.set_font('Arial', '', 10)
        
        top_dept = dff[C_DEPT].value_counts().head(5)
        for dept, cnt in top_dept.items():
            dept_str = str(dept)[:50]  # Truncate long names
            pdf.cell(0, 6, f'{dept_str}: {cnt:,} tickets', ln=True)
        pdf.ln(8)
    
    # Top Agents
    if C_AGENT in dff.columns:
        pdf.set_font('Arial', 'B', 14)
        pdf.cell(0, 10, 'TOP 5 AGENTS BY VOLUME', ln=True)
        pdf.set_font('Arial', '', 10)
        
        top_agents = dff[C_AGENT].value_counts().head(5)
        for agent, cnt in top_agents.items():
            agent_str = str(agent)[:50]
            pdf.cell(0, 6, f'{agent_str}: {cnt:,} tickets', ln=True)
    
    # Footer
    pdf.ln(15)
    pdf.set_font('Arial', 'I', 8)
    pdf.cell(0, 10, f'Source: {uploaded_name}', ln=True, align='C')
    
    return pdf.output(dest='S').encode('latin1')

# ================================================================
#  HEADER WITH DOWNLOAD BUTTONS
# ================================================================
col_head1, col_head2 = st.columns([3, 1])

with col_head1:
    st.markdown(
        f"<div style='background:linear-gradient(135deg,#1a1f3a,#2d3561);padding:24px 32px;border-radius:22px;"
        f"border:2px solid rgba(88,166,255,.25)'>"
        f"<div style='display:flex;align-items:center;gap:20px'>"
        f"<div style='background:linear-gradient(135deg,#1f6feb,#58a6ff);border-radius:20px;"
        f"padding:16px 20px;font-size:2.4rem;box-shadow:0 8px 32px rgba(31,111,235,.4)'>🖥️</div>"
        f"<div style='flex:1'>"
        f"<h1 style='color:#58a6ff;margin:0;font-size:1.9rem;font-weight:900'>IT Helpdesk Analytics Dashboard</h1>"
        f"<div style='color:#7d8590;margin-top:5px;font-size:.8rem;font-weight:600'>Complete Analysis with PDF Export</div>"
        f"<div style='color:#7d8590;margin-top:8px;font-size:.8rem'>"
        f"📄 {uploaded.name} • 🗂️ {len(df):,} tickets • 🔽 {len(dff):,} filtered"
        f"</div></div></div></div>",
        unsafe_allow_html=True,
    )

with col_head2:
    st.markdown("<div style='margin-top:20px'>", unsafe_allow_html=True)
    
    # PDF Download
    pdf_bytes = generate_pdf_report(dff, uploaded.name)
    st.download_button(
        label="📄 Download PDF Report",
        data=pdf_bytes,
        file_name=f"helpdesk_report_{datetime.now().strftime('%Y%m%d_%H%M')}.pdf",
        mime="application/pdf",
        use_container_width=True,
    )
    
    # Excel Download
    excel_buffer = io.BytesIO()
    with pd.ExcelWriter(excel_buffer, engine='openpyxl') as writer:
        dff.to_excel(writer, index=False, sheet_name='Filtered Data')
    excel_bytes = excel_buffer.getvalue()
    
    st.download_button(
        label="📊 Download Excel Data",
        data=excel_bytes,
        file_name=f"helpdesk_data_{datetime.now().strftime('%Y%m%d_%H%M')}.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        use_container_width=True,
    )
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ================================================================
#  TABS
# ================================================================
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "📊 Overview",
    "⏱️ Resolution Time",
    "⚡ Priority & Reasons",
    "👨‍💻 Agents & Departments",
    "📈 Monthly Trends",
    "🗃️ Raw Data",
])

# ================== TAB 1: OVERVIEW ===================
with tab1:
    sec("📌 KEY KPIs")

    k1, k2, k3, k4, k5 = st.columns(5)

    with k1:
        st.markdown(
            f"<div class='kpi-premium'><span class='kpi-icon'>🎫</span>"
            f"<span class='kpi-num'>{len(dff):,}</span>"
            f"<span class='kpi-lbl'>TOTAL TICKETS</span></div>",
            unsafe_allow_html=True,
        )

    with k2:
        avg_hrs = dff['Resolution_Hours'].mean()
        st.markdown(
            f"<div class='kpi-premium'><span class='kpi-icon'>⏱️</span>"
            f"<span class='kpi-num'>{fmt_time(avg_hrs)}</span>"
            f"<span class='kpi-lbl'>AVG RESOLUTION</span></div>",
            unsafe_allow_html=True,
        )

    with k3:
        dept_count = dff[C_DEPT].nunique() if C_DEPT in dff.columns else 0
        st.markdown(
            f"<div class='kpi-premium'><span class='kpi-icon'>🏢</span>"
            f"<span class='kpi-num'>{dept_count}</span>"
            f"<span class='kpi-lbl'>DEPARTMENTS</span></div>",
            unsafe_allow_html=True,
        )

    with k4:
        agent_count = dff[C_AGENT].dropna().nunique() if C_AGENT in dff.columns else 0
        st.markdown(
            f"<div class='kpi-premium'><span class='kpi-icon'>👨‍💻</span>"
            f"<span class='kpi-num'>{agent_count}</span>"
            f"<span class='kpi-lbl'>AGENTS</span></div>",
            unsafe_allow_html=True,
        )

    with k5:
        if C_PRIORITY in dff.columns and len(dff) > 0:
            high_pct = round(len(dff[dff[C_PRIORITY] == 'High']) / len(dff) * 100, 1)
        else:
            high_pct = 0
        st.markdown(
            f"<div class='kpi-premium'><span class='kpi-icon'>⚡</span>"
            f"<span class='kpi-num'>{high_pct}%</span>"
            f"<span class='kpi-lbl'>HIGH PRIORITY</span></div>",
            unsafe_allow_html=True,
        )

    # SLA Compliance
    sec("🎯 SLA COMPLIANCE (24H / 3D / 7D)")

    total_with_time = dff['Resolution_Hours'].notna().sum()
    if total_with_time > 0:
        sla_24h_cnt = len(dff[dff['Resolution_Hours'] <= 24])
        sla_3d_cnt = len(dff[dff['Resolution_Days'] > 3])
        sla_7d_cnt = len(dff[dff['Resolution_Days'] > 7])
    else:
        sla_24h_cnt = sla_3d_cnt = sla_7d_cnt = 0

    pct_24h = round(sla_24h_cnt / total_with_time * 100, 1) if total_with_time else 0
    pct_3d = round(sla_3d_cnt / total_with_time * 100, 1) if total_with_time else 0
    pct_7d = round(sla_7d_cnt / total_with_time * 100, 1) if total_with_time else 0

    s1, s2, s3 = st.columns(3)

    with s1:
        st.markdown(
            f"<div class='insight-card'><div class='insight-badge'>✅ WITHIN 24H</div>"
            f"<div class='insight-text'><b style='color:#3fb950;font-size:2rem'>{pct_24h}%</b><br>"
            f"{sla_24h_cnt:,} tickets resolved within 24 hours</div></div>",
            unsafe_allow_html=True,
        )

    with s2:
        st.markdown(
            f"<div class='insight-card'><div class='insight-badge'>⚠️ &gt; 3 DAYS</div>"
            f"<div class='insight-text'><b style='color:#d29922;font-size:2rem'>{pct_3d}%</b><br>"
            f"{sla_3d_cnt:,} tickets took more than 3 days</div></div>",
            unsafe_allow_html=True,
        )

    with s3:
        st.markdown(
            f"<div class='insight-card'><div class='insight-badge'>🔴 &gt; 7 DAYS</div>"
            f"<div class='insight-text'><b style='color:#f85149;font-size:2rem'>{pct_7d}%</b><br>"
            f"{sla_7d_cnt:,} tickets exceeded 7 days</div></div>",
            unsafe_allow_html=True,
        )

    st.markdown("---")

    # Charts
    c1, c2 = st.columns(2)

    with c1:
        if C_DEPT in dff.columns:
            dept_vol = dff[C_DEPT].value_counts().head(10).reset_index()
            dept_vol.columns = [C_DEPT, 'Count']
            fig = px.bar(
                dept_vol, x='Count', y=C_DEPT, orientation='h',
                color='Count', color_continuous_scale='Teal',
                title='Top 10 Departments by Volume'
            )
            fig.update_layout(yaxis={'categoryorder': 'total ascending'}, showlegend=False, coloraxis_showscale=False)
            fig.update_traces(text=dept_vol['Count'], textposition='outside')
            st.plotly_chart(ccfg(fig, 450), use_container_width=True)

    with c2:
        if C_PRIORITY in dff.columns:
            pri_data = dff[C_PRIORITY].value_counts().reset_index()
            pri_data.columns = ['Priority', 'Count']
            fig = px.pie(
                pri_data, values='Count', names='Priority', hole=0.45,
                title='Priority Distribution',
                color_discrete_sequence=['#f85149', '#d29922', '#3fb950'],
            )
            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(ccfg(fig, 450), use_container_width=True)

# ================== TAB 2: RESOLUTION TIME ===================
with tab2:
    sec("⏱️ RESOLUTION TIME ANALYSIS")

    r1, r2, r3 = st.columns(3)

    with r1:
        overall_avg = dff['Resolution_Hours'].mean()
        st.markdown(
            f"<div class='insight-card'><div class='insight-badge'>📊 OVERALL AVG</div>"
            f"<div class='insight-text'><b style='color:#58a6ff;font-size:2rem'>{fmt_time(overall_avg)}</b><br>"
            f"Average resolution time</div></div>",
            unsafe_allow_html=True,
        )

    with r2:
        median_hrs = dff['Resolution_Hours'].median()
        st.markdown(
            f"<div class='insight-card'><div class='insight-badge'>📈 MEDIAN</div>"
            f"<div class='insight-text'><b style='color:#3fb950;font-size:2rem'>{fmt_time(median_hrs)}</b><br>"
            f"50% resolved faster</div></div>",
            unsafe_allow_html=True,
        )

    with r3:
        max_hrs = dff['Resolution_Hours'].max()
        st.markdown(
            f"<div class='insight-card'><div class='insight-badge'>⚠️ MAX</div>"
            f"<div class='insight-text'><b style='color:#f85149;font-size:2rem'>{fmt_time(max_hrs)}</b><br>"
            f"Longest resolution time</div></div>",
            unsafe_allow_html=True,
        )

    st.markdown("---")

    # By Priority
    if C_PRIORITY in dff.columns:
        sec("⚡ BY PRIORITY")
        pri_time = (
            dff.groupby(C_PRIORITY)['Resolution_Hours']
            .mean()
            .sort_values(ascending=False)
            .reset_index()
        )
        pri_time.columns = ['Priority', 'Avg Hours']
        pri_time['Avg Time'] = pri_time['Avg Hours'].apply(fmt_time)

        fig = px.bar(
            pri_time, x='Avg Hours', y='Priority', orientation='h',
            color='Avg Hours', color_continuous_scale='Reds',
            text='Avg Time', title='Avg Resolution Time by Priority'
        )
        fig.update_layout(yaxis={'categoryorder': 'total ascending'}, showlegend=False, coloraxis_showscale=False)
        fig.update_traces(textposition='outside')
        st.plotly_chart(ccfg(fig, 400), use_container_width=True)

    # By Department
    if C_DEPT in dff.columns:
        sec("🏢 BY DEPARTMENT (Top 15)")
        dept_time = (
            dff.groupby(C_DEPT)
            .agg(Avg_Hours=('Resolution_Hours', 'mean'), Tickets=(C_DEPT, 'count'))
            .reset_index()
        )
        dept_time['Avg Time'] = dept_time['Avg_Hours'].apply(fmt_time)
        dept_time = dept_time.sort_values('Avg_Hours', ascending=False).head(15)

        fig = px.bar(
            dept_time, x='Avg_Hours', y=C_DEPT, orientation='h',
            color='Avg_Hours', color_continuous_scale='Oranges',
            text='Avg Time', title='Avg Resolution by Department'
        )
        fig.update_layout(yaxis={'categoryorder': 'total ascending'}, showlegend=False, coloraxis_showscale=False)
        fig.update_traces(textposition='outside')
        st.plotly_chart(ccfg(fig, 500), use_container_width=True)

# ================== TAB 3: PRIORITY & REASONS ===================
with tab3:
    if C_PRIORITY in dff.columns:
        sec("⚡ PRIORITY DISTRIBUTION")

        total = len(dff)
        high_cnt = len(dff[dff[C_PRIORITY] == 'High'])
        med_cnt = len(dff[dff[C_PRIORITY] == 'Medium'])
        low_cnt = len(dff[dff[C_PRIORITY] == 'Low'])

        high_pct = round(high_cnt / total * 100, 1) if total else 0
        med_pct = round(med_cnt / total * 100, 1) if total else 0
        low_pct = round(low_cnt / total * 100, 1) if total else 0

        c1, c2, c3 = st.columns(3)
        with c1:
            st.markdown(
                f"<div class='insight-card' style='border-left-color:#f85149'>"
                f"<div class='insight-badge' style='background:rgba(248,81,73,.15);color:#f85149'>HIGH</div>"
                f"<div class='insight-text'><b style='color:#f85149;font-size:2.1rem'>{high_pct}%</b><br>"
                f"{high_cnt:,} tickets</div></div>",
                unsafe_allow_html=True,
            )
        with c2:
            st.markdown(
                f"<div class='insight-card' style='border-left-color:#d29922'>"
                f"<div class='insight-badge' style='background:rgba(210,153,34,.15);color:#d29922'>MEDIUM</div>"
                f"<div class='insight-text'><b style='color:#d29922;font-size:2.1rem'>{med_pct}%</b><br>"
                f"{med_cnt:,} tickets</div></div>",
                unsafe_allow_html=True,
            )
        with c3:
            st.markdown(
                f"<div class='insight-card' style='border-left-color:#3fb950'>"
                f"<div class='insight-badge' style='background:rgba(63,185,80,.15);color:#3fb950'>LOW</div>"
                f"<div class='insight-text'><b style='color:#3fb950;font-size:2.1rem'>{low_pct}%</b><br>"
                f"{low_cnt:,} tickets</div></div>",
                unsafe_allow_html=True,
            )

    # Top Reasons
    if C_REASON in dff.columns:
        sec(f"📌 TOP {top_n} REASONS")
        reason_counts = dff[C_REASON].value_counts().head(top_n).reset_index()
        reason_counts.columns = [C_REASON, 'Count']
        reason_counts['% of Total'] = round(reason_counts['Count'] / len(df) * 100, 2)

        avg_per_reason = (
            dff.groupby(C_REASON)['Resolution_Hours']
            .mean()
            .reset_index()
            .rename(columns={'Resolution_Hours': 'Avg Hours'})
        )
        merged = reason_counts.merge(avg_per_reason, on=C_REASON, how='left')
        merged['Avg Time'] = merged['Avg Hours'].apply(fmt_time)

        st.dataframe(
            merged[[C_REASON, 'Count', '% of Total', 'Avg Time']],
            use_container_width=True,
            height=450,
        )

# ================== TAB 4: AGENTS & DEPARTMENTS ===================
with tab4:
    sec("👨‍💻 AGENT PERFORMANCE")

    if C_AGENT in dff.columns and not dff[C_AGENT].dropna().empty:
        agent_stats = (
            dff.dropna(subset=[C_AGENT])
            .groupby(C_AGENT)
            .agg(
                Tickets=(C_AGENT, 'count'),
                Avg_Hours=('Resolution_Hours', 'mean'),
            )
            .reset_index()
        )

        if C_PRIORITY in dff.columns:
            agent_high = dff[dff[C_PRIORITY] == 'High'].groupby(C_AGENT).size().reset_index(name='High Count')
            agent_stats = agent_stats.merge(agent_high, on=C_AGENT, how='left').fillna(0)
            agent_stats['High Count'] = agent_stats['High Count'].astype(int)
        else:
            agent_stats['High Count'] = 0

        agent_stats['Avg Time'] = agent_stats['Avg_Hours'].apply(fmt_time)
        agent_stats['_Agent Short'] = (
            agent_stats[C_AGENT].astype(str)
            .str.replace('−متعاقد', '', regex=False)
            .str.replace('-متعاقد', '', regex=False)
            .str.strip()
        )

        agent_stats = agent_stats.sort_values('Tickets', ascending=False).head(top_n)

        st.dataframe(
            agent_stats[['_Agent Short', 'Tickets', 'High Count', 'Avg Time']],
            use_container_width=True,
            height=400,
        )

    # Department Stats
    if C_DEPT in dff.columns:
        sec("🏢 DEPARTMENT PERFORMANCE")
        dept_stats = (
            dff.groupby(C_DEPT)
            .agg(
                Tickets=(C_DEPT, 'count'),
                Avg_Hours=('Resolution_Hours', 'mean'),
            )
            .reset_index()
        )
        
        if C_PRIORITY in dff.columns:
            dept_high = (
                dff[dff[C_PRIORITY] == 'High']
                .groupby(C_DEPT)
                .size()
                .reset_index(name='High Count')
            )
            dept_stats = dept_stats.merge(dept_high, on=C_DEPT, how='left').fillna(0)
            dept_stats['High Count'] = dept_stats['High Count'].astype(int)
            dept_stats['High %'] = round(dept_stats['High Count'] / dept_stats['Tickets'] * 100, 1)
        else:
            dept_stats['High %'] = 0.0

        dept_stats['Avg Time'] = dept_stats['Avg_Hours'].apply(fmt_time)
        dept_stats = dept_stats.sort_values('Tickets', ascending=False)

        st.dataframe(
            dept_stats[[C_DEPT, 'Tickets', 'High Count', 'High %', 'Avg Time']],
            use_container_width=True,
            height=450,
        )

# ================== TAB 5: MONTHLY TRENDS ===================
with tab5:
    if 'Month' in dff.columns and not dff['Month'].isna().all():
        sec("📈 MONTHLY TRENDS")

        monthly = dff.groupby('Month').agg(
            Tickets=('Month', 'count'),
            Avg_Hours=('Resolution_Hours', 'mean'),
        ).reset_index()
        monthly['Avg Time'] = monthly['Avg_Hours'].apply(fmt_time)

        if C_PRIORITY in dff.columns:
            monthly_high = (
                dff[dff[C_PRIORITY] == 'High']
                .groupby('Month').size().reset_index(name='High Count')
            )
            monthly = monthly.merge(monthly_high, on='Month', how='left').fillna(0)
            monthly['High Count'] = monthly['High Count'].astype(int)
            monthly['High %'] = round(monthly['High Count'] / monthly['Tickets'] * 100, 1)
        else:
            monthly['High %'] = 0.0

        monthly = monthly.sort_values('Month')

        fig = make_subplots(
            rows=2, cols=1,
            subplot_titles=('Monthly Volume', 'Avg Resolution Time (Hours)'),
            vertical_spacing=0.15,
        )

        fig.add_trace(
            go.Scatter(
                x=monthly['Month'], y=monthly['Tickets'],
                mode='lines+markers', name='Tickets',
                line=dict(color='#58a6ff', width=3), marker=dict(size=7),
            ),
            row=1, col=1,
        )

        fig.add_trace(
            go.Scatter(
                x=monthly['Month'], y=monthly['Avg_Hours'],
                mode='lines+markers', name='Avg Hours',
                line=dict(color='#d29922', width=3), marker=dict(size=7),
            ),
            row=2, col=1,
        )

        fig.update_layout(
            height=700,
            showlegend=False,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#c9d1d9'),
        )
        fig.update_xaxes(showgrid=True, gridcolor='rgba(125,133,144,.1)')
        fig.update_yaxes(showgrid=True, gridcolor='rgba(125,133,144,.1)')

        st.plotly_chart(fig, use_container_width=True)

        st.dataframe(
            monthly[['Month', 'Tickets', 'Avg Time', 'High Count', 'High %']],
            use_container_width=True,
            height=400,
        )

# ================== TAB 6: RAW DATA ===================
with tab6:
    sec("🗃️ RAW DATA (FILTERED)")

    display_df = dff.copy()
    if 'Resolution_Hours' in display_df.columns:
        display_df['Resolution Time'] = display_df['Resolution_Hours'].apply(fmt_time)

    c1, c2 = st.columns([1, 3])
    with c1:
        search_col = st.selectbox("Search in", ["All"] + display_df.columns.tolist())
    with c2:
        search_val = st.text_input("🔍 Search", "")

    if search_val:
        if search_col == "All":
            mask = display_df.apply(
                lambda c: c.astype(str).str.contains(search_val, case=False, na=False)
            ).any(axis=1)
        else:
            mask = display_df[search_col].astype(str).str.contains(search_val, case=False, na=False)
        display_df = display_df[mask]

    st.markdown(
        f"<div style='color:#7d8590;margin-bottom:8px'>"
        f"Showing <b style='color:#58a6ff'>{len(display_df):,}</b> of {len(df):,} records</div>",
        unsafe_allow_html=True,
    )
    st.dataframe(display_df, use_container_width=True, height=600)

# ================================================================
#  FOOTER
# ================================================================
st.markdown("---")
st.markdown(
    "<div style='text-align:center;margin-top:40px;padding-top:20px'>"
    "<div style='color:#7d8590;font-size:.88rem;font-weight:600'>IT Helpdesk Analytics Dashboard</div>"
    "<div style='color:#58a6ff;font-size:.78rem;margin-top:6px'>Full Featured with PDF & Excel Export</div>"
    "</div>",
    unsafe_allow_html=True,
)
