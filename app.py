# ============================================================
#   IT HELPDESK ANALYTICS DASHBOARD
#   Author: tarique14321495
#   Run: streamlit run app.py
# ============================================================

import streamlit as st
import pandas as pd
import plotly.express as px
import io

# ── PAGE CONFIG ──────────────────────────────────────────────
st.set_page_config(
    page_title="IT Helpdesk Analytics",
    page_icon="🖥️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── CUSTOM CSS ───────────────────────────────────────────────
st.markdown("""
<style>
    .metric-card {
        background: linear-gradient(135deg, #1e3a5f, #2d6a9f);
        border-radius: 12px; padding: 20px;
        text-align: center; color: white;
        margin: 5px; box-shadow: 0 4px 15px rgba(0,0,0,0.3);
    }
    .metric-number { font-size: 2.5rem; font-weight: bold; color: #00d4ff; }
    .metric-label  { font-size: 0.9rem; color: #adc6e5; margin-top: 5px; }
    .section-header {
        background: linear-gradient(90deg, #1e3a5f, transparent);
        padding: 10px 20px;
        border-left: 4px solid #00d4ff;
        border-radius: 5px; margin: 20px 0 10px 0;
        color: white; font-size: 1.2rem; font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# ── ARABIC → ENGLISH MAPPING ─────────────────────────────────
ARABIC_TO_ENGLISH = {
    'إدارة العميل'      : 'Customer_Department',
    'الخدمة'            : 'Service_Type',
    'التصنيف الرئيسي'   : 'Main_Category',
    'التصنيف الفرعي'    : 'Sub_Category',
    'مسند الى'          : 'Assigned_To',
    'تم حل بواسطة'      : 'Resolved_By',
    'رقم التذكرة'       : 'Ticket_ID',
    'تاريخ الفتح'       : 'Open_Date',
    'تاريخ الإغلاق'     : 'Close_Date',
    'الحالة'            : 'Status',
    'الأولوية'          : 'Priority',
    'الوصف'             : 'Description',
    'نوع الطلب'         : 'Request_Type',
    'المجموعة'          : 'Group',
    'القسم'             : 'Department',
    'الموقع'            : 'Location',
    'نوع الجهاز'        : 'Device_Type',
    'اسم الجهاز'        : 'Device_Name',
    'رقم الأصل'         : 'Asset_Number',
    'اسم المستخدم'      : 'Username',
    'المنطقة'           : 'Region',
    'وقت الاستجابة'     : 'Response_Time',
    'تم الإغلاق بواسطة' : 'Closed_By',
    'ملاحظات'           : 'Notes',
    'رقم الطلب'         : 'Request_Number',
    'التاريخ'           : 'Date',
    'الشهر'             : 'Month',
    'السنة'             : 'Year',
}

def rename_cols(df):
    return df.rename(columns={
        c: ARABIC_TO_ENGLISH.get(str(c).strip(), str(c).strip())
        for c in df.columns
    })

def get_col(df, *opts):
    for o in opts:
        if o in df.columns:
            return o
    return None

# ── SIDEBAR ───────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🖥️ IT Helpdesk Analytics")
    st.markdown("---")
    uploaded = st.file_uploader("📂 Excel File Upload Karein", type=["xlsx", "xls"])
    if uploaded:
        st.success(f"✅ {uploaded.name}")
    st.markdown("---")
    top_n = st.slider("Top N Results", 5, 30, 15)
    theme = st.selectbox("Chart Theme", ["plotly_dark", "plotly", "ggplot2"])

# ── WELCOME SCREEN ────────────────────────────────────────────
if not uploaded:
    st.markdown("""
    <div style='text-align:center;padding:80px 20px;'>
      <h1 style='color:#00d4ff;font-size:3rem;'>🖥️ IT Helpdesk Analytics</h1>
      <p style='color:#adc6e5;font-size:1.2rem;'>
        Sidebar se <b>Excel file upload karein</b><br>
        aur poora dashboard automatically ban jaayega!
      </p>
      <br>
      <div style='display:flex;justify-content:center;gap:20px;flex-wrap:wrap;'>
        <div style='background:#1e3a5f;border-radius:12px;padding:25px;width:160px;'>
          <div style='font-size:2.5rem;'>📊</div><div style='color:white;margin-top:8px;'>Charts & Graphs</div>
        </div>
        <div style='background:#1e3a5f;border-radius:12px;padding:25px;width:160px;'>
          <div style='font-size:2.5rem;'>👨‍💻</div><div style='color:white;margin-top:8px;'>Agent Performance</div>
        </div>
        <div style='background:#1e3a5f;border-radius:12px;padding:25px;width:160px;'>
          <div style='font-size:2.5rem;'>🏢</div><div style='color:white;margin-top:8px;'>Department Analysis</div>
        </div>
        <div style='background:#1e3a5f;border-radius:12px;padding:25px;width:160px;'>
          <div style='font-size:2.5rem;'>📅</div><div style='color:white;margin-top:8px;'>Monthly Trends</div>
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)
    st.stop()

# ── LOAD DATA ─────────────────────────────────────────────────
try:
    xl         = pd.ExcelFile(uploaded)
    sheet_list = xl.sheet_names

    with st.sidebar:
        st.markdown("---")
        selected_sheet = st.selectbox("📋 Sheet Select Karein", sheet_list)
        st.markdown("---")

    df_raw = pd.read_excel(uploaded, sheet_name=selected_sheet)
    df     = rename_cols(df_raw.copy())

    # ── COLUMN DEBUG (sidebar) ────────────────────────────────
    with st.sidebar:
        with st.expander("🔍 Column Debug Info"):
            st.caption("Raw column names:")
            for c in df_raw.columns.tolist():
                st.code(repr(c))
            st.caption("Renamed columns:")
            st.write(df.columns.tolist())

except Exception as e:
    st.error(f"❌ File load error: {e}")
    st.stop()

# ── DETECT COLUMNS ────────────────────────────────────────────
col_dept     = get_col(df, 'Customer_Department', 'Department')
col_service  = get_col(df, 'Service_Type')
col_main     = get_col(df, 'Main_Category')
col_sub      = get_col(df, 'Sub_Category')
col_assigned = get_col(df, 'Assigned_To')
col_resolved = get_col(df, 'Resolved_By', 'Closed_By')
col_status   = get_col(df, 'Status')
col_priority = get_col(df, 'Priority')
col_date     = get_col(df, 'Open_Date', 'Date')

# ── HEADER ────────────────────────────────────────────────────
st.markdown(f"""
<div style='background:linear-gradient(90deg,#1e3a5f,#0a1628);
            padding:20px 30px;border-radius:12px;margin-bottom:20px;'>
  <h1 style='color:#00d4ff;margin:0;'>🖥️ IT Helpdesk Analytics Dashboard</h1>
  <p style='color:#adc6e5;margin:5px 0 0 0;'>
    📄 <b>{uploaded.name}</b> &nbsp;|&nbsp;
    📋 Sheet: <b>{selected_sheet}</b> &nbsp;|&nbsp;
    📊 Rows: <b>{len(df):,}</b> &nbsp;|&nbsp;
    🗂️ Columns: <b>{len(df.columns)}</b>
  </p>
</div>
""", unsafe_allow_html=True)

# ── TABS ──────────────────────────────────────────────────────
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "📊 Overview", "🔥 Issues", "🏢 Departments",
    "👨‍💻 Agents", "📅 Trends", "🗃️ Raw Data"
])

# ════════════ TAB 1: OVERVIEW ════════════
with tab1:
    st.markdown('<div class="section-header">📌 Key Metrics</div>', unsafe_allow_html=True)
    c1, c2, c3, c4, c5 = st.columns(5)
    cards = [
        (len(df),                                               "Total Tickets"),
        (df[col_dept].nunique()     if col_dept     else "N/A", "Departments"),
        (df[col_main].nunique()     if col_main     else "N/A", "Issue Types"),
        (df[col_resolved].nunique() if col_resolved else "N/A", "Agents"),
        (df[col_sub].nunique()      if col_sub      else "N/A", "Sub Categories"),
    ]
    for col_obj, (val, label) in zip([c1, c2, c3, c4, c5], cards):
        with col_obj:
            display = f"{val:,}" if isinstance(val, int) else str(val)
            st.markdown(f"""<div class="metric-card">
                <div class="metric-number">{display}</div>
                <div class="metric-label">{label}</div>
            </div>""", unsafe_allow_html=True)

    st.markdown("---")
    r1, r2 = st.columns(2)
    with r1:
        if col_service:
            svc = df[col_service].value_counts().reset_index()
            svc.columns = ['Service', 'Count']
            fig = px.pie(svc, values='Count', names='Service',
                         title='⚙️ Service Type Distribution',
                         hole=0.45, template=theme)
            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("⚠️ Service_Type column nahi mili.")
    with r2:
        if col_priority:
            pri = df[col_priority].value_counts().reset_index()
            pri.columns = ['Priority', 'Count']
            fig = px.pie(pri, values='Count', names='Priority',
                         title='🚨 Priority Distribution',
                         hole=0.45, template=theme,
                         color_discrete_sequence=px.colors.sequential.RdBu)
            st.plotly_chart(fig, use_container_width=True)
        elif col_status:
            sta = df[col_status].value_counts().reset_index()
            sta.columns = ['Status', 'Count']
            fig = px.pie(sta, values='Count', names='Status',
                         title='📌 Status Distribution',
                         hole=0.45, template=theme)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("⚠️ Priority / Status column nahi mili.")

# ════════════ TAB 2: ISSUES ════════════
with tab2:
    st.markdown('<div class="section-header">🔥 Top Issue Categories</div>', unsafe_allow_html=True)
    if col_main:
        d = df[col_main].value_counts().head(top_n).reset_index()
        d.columns = ['Issue', 'Count']
        fig = px.bar(d, x='Count', y='Issue', orientation='h',
                     title=f'Top {top_n} Main Issues', color='Count',
                     color_continuous_scale='Blues', template=theme, text='Count')
        fig.update_layout(height=600, yaxis={'categoryorder': 'total ascending'}, showlegend=False)
        fig.update_traces(textposition='outside')
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("⚠️ Main_Category column nahi mili.")

    st.markdown('<div class="section-header">📂 Sub Categories</div>', unsafe_allow_html=True)
    if col_sub:
        d2 = df[col_sub].value_counts().head(top_n).reset_index()
        d2.columns = ['Sub Category', 'Count']
        fig2 = px.bar(d2, x='Count', y='Sub Category', orientation='h',
                      title=f'Top {top_n} Sub Categories', color='Count',
                      color_continuous_scale='Oranges', template=theme, text='Count')
        fig2.update_layout(height=600, yaxis={'categoryorder': 'total ascending'}, showlegend=False)
        fig2.update_traces(textposition='outside')
        st.plotly_chart(fig2, use_container_width=True)
    else:
        st.info("⚠️ Sub_Category column nahi mili.")

    if col_main and col_sub:
        st.markdown('<div class="section-header">🔗 Main → Sub Category Treemap</div>', unsafe_allow_html=True)
        tree = df.groupby([col_main, col_sub]).size().reset_index(name='Count')
        fig3 = px.treemap(tree, path=[col_main, col_sub], values='Count',
                          title='Issue Category Treemap', template=theme,
                          color='Count', color_continuous_scale='Blues')
        fig3.update_layout(height=600)
        st.plotly_chart(fig3, use_container_width=True)

# ════════════ TAB 3: DEPARTMENTS ════════════
with tab3:
    st.markdown('<div class="section-header">🏢 Department-wise Analysis</div>', unsafe_allow_html=True)
    if col_dept:
        d = df[col_dept].value_counts().head(top_n).reset_index()
        d.columns = ['Department', 'Tickets']
        c1, c2 = st.columns(2)
        with c1:
            fig = px.bar(d, x='Tickets', y='Department', orientation='h',
                         title='Tickets by Department', color='Tickets',
                         color_continuous_scale='Teal', template=theme, text='Tickets')
            fig.update_layout(height=500, yaxis={'categoryorder': 'total ascending'}, showlegend=False)
            fig.update_traces(textposition='outside')
            st.plotly_chart(fig, use_container_width=True)
        with c2:
            fig2 = px.pie(d, values='Tickets', names='Department',
                          title='Department Share', hole=0.4, template=theme)
            fig2.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig2, use_container_width=True)

        if col_main:
            st.markdown('<div class="section-header">🔥 Issues by Department</div>', unsafe_allow_html=True)
            top_depts = d['Department'].head(10).tolist()
            cross = df[df[col_dept].isin(top_depts)].groupby(
                [col_dept, col_main]).size().reset_index(name='Count')
            fig3 = px.bar(cross, x=col_dept, y='Count', color=col_main,
                          title='Issue Type by Department', template=theme,
                          barmode='stack')
            fig3.update_layout(height=500, xaxis_tickangle=-30)
            st.plotly_chart(fig3, use_container_width=True)
    else:
        st.info("⚠️ Department column nahi mili.")

# ════════════ TAB 4: AGENTS ════════════
with tab4:
    st.markdown('<div class="section-header">👨‍💻 Agent Performance</div>', unsafe_allow_html=True)
    agent_col = col_resolved or col_assigned
    if agent_col:
        ag = df[agent_col].value_counts().head(top_n).reset_index()
        ag.columns = ['Agent', 'Tickets']
        c1, c2 = st.columns(2)
        with c1:
            fig = px.bar(ag, x='Tickets', y='Agent', orientation='h',
                         title=f'Top {top_n} Agents by Tickets Resolved',
                         color='Tickets', color_continuous_scale='Viridis',
                         template=theme, text='Tickets')
            fig.update_layout(height=500, yaxis={'categoryorder': 'total ascending'}, showlegend=False)
            fig.update_traces(textposition='outside')
            st.plotly_chart(fig, use_container_width=True)
        with c2:
            fig2 = px.pie(ag, values='Tickets', names='Agent',
                          title='Agent Workload Share', hole=0.4, template=theme)
            fig2.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig2, use_container_width=True)

        if col_status:
            st.markdown('<div class="section-header">📊 Agent × Status Breakdown</div>', unsafe_allow_html=True)
            top_agents = ag['Agent'].head(10).tolist()
            ag_status = df[df[agent_col].isin(top_agents)].groupby(
                [agent_col, col_status]).size().reset_index(name='Count')
            fig3 = px.bar(ag_status, x=agent_col, y='Count', color=col_status,
                          title='Agent Performance by Status', template=theme,
                          barmode='group')
            fig3.update_layout(height=450, xaxis_tickangle=-30)
            st.plotly_chart(fig3, use_container_width=True)
    else:
        st.info("⚠️ Agent column (Assigned_To / Resolved_By) nahi mili.")

# ════════════ TAB 5: TRENDS ════════════
with tab5:
    st.markdown('<div class="section-header">📅 Monthly Ticket Trends</div>', unsafe_allow_html=True)
    if col_date:
        try:
            df['_date'] = pd.to_datetime(df[col_date], errors='coerce', dayfirst=True)
            df['_month'] = df['_date'].dt.to_period('M').astype(str)

            parsed_count = df['_date'].notna().sum()
            st.caption(f"📅 {parsed_count:,} / {len(df):,} rows mein date successfully parse hui")

            monthly = df.groupby('_month').size().reset_index(name='Tickets')
            monthly = monthly.sort_values('_month')

            fig = px.line(monthly, x='_month', y='Tickets',
                          title='Monthly Ticket Volume', template=theme,
                          markers=True, line_shape='spline')
            fig.update_layout(height=400, xaxis_title='Month',
                               yaxis_title='Tickets', xaxis_tickangle=-45)
            st.plotly_chart(fig, use_container_width=True)

            fig2 = px.bar(monthly, x='_month', y='Tickets',
                          title='Monthly Tickets (Bar)', template=theme,
                          color='Tickets', color_continuous_scale='Blues', text='Tickets')
            fig2.update_layout(height=400, xaxis_tickangle=-45)
            fig2.update_traces(textposition='outside')
            st.plotly_chart(fig2, use_container_width=True)

            if col_main:
                st.markdown('<div class="section-header">📈 Issue Category Trend</div>',
                            unsafe_allow_html=True)
                top_issues = df[col_main].value_counts().head(5).index.tolist()
                trend_df = df[df[col_main].isin(top_issues)].groupby(
                    ['_month', col_main]).size().reset_index(name='Count')
                fig3 = px.line(trend_df, x='_month', y='Count', color=col_main,
                               title='Top 5 Issue Trends Over Time',
                               template=theme, markers=True)
                fig3.update_layout(height=450, xaxis_tickangle=-45)
                st.plotly_chart(fig3, use_container_width=True)

        except Exception as e:
            st.error(f"❌ Date processing error: {e}")
    else:
        st.info("⚠️ Date column (Open_Date / Date) nahi mili.")

# ════════════ TAB 6: RAW DATA ════════════
with tab6:
    st.markdown('<div class="section-header">🗃️ Raw Data Explorer</div>', unsafe_allow_html=True)

    search_term = st.text_input("🔍 Search in data", "")
    if search_term:
        mask = df.apply(lambda col: col.astype(str).str.contains(search_term, case=False, na=False))
        filtered_df = df[mask.any(axis=1)]
    else:
        filtered_df = df

    st.markdown(f"**Showing {len(filtered_df):,} of {len(df):,} rows**")
    st.dataframe(filtered_df, use_container_width=True, height=500)

    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        filtered_df.to_excel(writer, index=False, sheet_name='Data')
    st.download_button(
        label="⬇️ Download Filtered Data as Excel",
        data=output.getvalue(),
        file_name="helpdesk_filtered.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
