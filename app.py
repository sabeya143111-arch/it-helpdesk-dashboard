# ============================================================
#   IT HELPDESK ANALYTICS DASHBOARD
#   Author: tarique14321495
#   Data: Arabic Excel with merged/forward-filled cells
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

# ── COLUMN NAMES (Arabic → English) ──────────────────────────
COL_DEPT     = 'إدارة العميل'
COL_SERVICE  = 'الخدمة'
COL_MAIN     = 'التصنيف الرئيسي'
COL_SUB      = 'التصنيف الفرعي'
COL_ASSIGNED = 'مسند الى'
COL_RESOLVED = 'تم حل بواسطة'

EN = {
    COL_DEPT    : 'Department',
    COL_SERVICE : 'Service_Type',
    COL_MAIN    : 'Main_Category',
    COL_SUB     : 'Sub_Category',
    COL_ASSIGNED: 'Assigned_To',
    COL_RESOLVED: 'Resolved_By',
}

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
          <div style='font-size:2.5rem;'>🔥</div><div style='color:white;margin-top:8px;'>Issue Breakdown</div>
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)
    st.stop()

# ── LOAD & CLEAN DATA ─────────────────────────────────────────
@st.cache_data
def load_data(file_bytes):
    # Row 0 = empty, Row 1 = Arabic headers → header=2 (0-indexed row 2)
    raw = pd.read_excel(io.BytesIO(file_bytes), sheet_name=0, header=2)

    # Keep only the 6 known Arabic columns
    cols_present = [c for c in [COL_DEPT, COL_SERVICE, COL_MAIN,
                                 COL_SUB, COL_ASSIGNED, COL_RESOLVED]
                    if c in raw.columns]
    df = raw[cols_present].copy()

    # Forward-fill merged cells (Department, Service, Main Category, Sub Category)
    for c in [COL_DEPT, COL_SERVICE, COL_MAIN, COL_SUB]:
        if c in df.columns:
            df[c] = df[c].replace('', pd.NA).ffill()

    # Drop rows where ALL key cols are empty
    df.dropna(how='all', inplace=True)

    # Clean agent column — remove " - Agent" noise, strip whitespace
    for c in [COL_ASSIGNED, COL_RESOLVED]:
        if c in df.columns:
            df[c] = df[c].astype(str).str.strip()
            df[c] = df[c].replace({'nan': pd.NA, 'Agent': pd.NA, '': pd.NA})

    # Rename to English
    df.rename(columns=EN, inplace=True)
    return df

try:
    file_bytes = uploaded.read()
    df = load_data(file_bytes)
except Exception as e:
    st.error(f"❌ File load error: {e}")
    st.stop()

# ── VALIDATE ──────────────────────────────────────────────────
if df.empty:
    st.error("❌ Data load nahi hua. File check karein.")
    st.stop()

# ── HEADER ────────────────────────────────────────────────────
st.markdown(f"""
<div style='background:linear-gradient(90deg,#1e3a5f,#0a1628);
            padding:20px 30px;border-radius:12px;margin-bottom:20px;'>
  <h1 style='color:#00d4ff;margin:0;'>🖥️ IT Helpdesk Analytics Dashboard</h1>
  <p style='color:#adc6e5;margin:5px 0 0 0;'>
    📄 <b>{uploaded.name}</b> &nbsp;|&nbsp;
    📊 Total Records: <b>{len(df):,}</b> &nbsp;|&nbsp;
    🗂️ Columns: <b>{", ".join(df.columns.tolist())}</b>
  </p>
</div>
""", unsafe_allow_html=True)

# ── TABS ──────────────────────────────────────────────────────
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊 Overview",
    "🔥 Issues",
    "🏢 Departments",
    "👨‍💻 Agents",
    "🗃️ Raw Data"
])

# ════════════ TAB 1: OVERVIEW ════════════
with tab1:
    st.markdown('<div class="section-header">📌 Key Metrics</div>', unsafe_allow_html=True)
    c1, c2, c3, c4, c5, c6 = st.columns(6)
    metrics = [
        (len(df),                                                        "🎫 Total Records"),
        (df['Department'].nunique()    if 'Department'    in df else "—", "🏢 Departments"),
        (df['Service_Type'].nunique()  if 'Service_Type'  in df else "—", "⚙️ Service Types"),
        (df['Main_Category'].nunique() if 'Main_Category' in df else "—", "🔥 Main Issues"),
        (df['Sub_Category'].nunique()  if 'Sub_Category'  in df else "—", "📂 Sub Categories"),
        (df['Resolved_By'].nunique()   if 'Resolved_By'   in df else "—", "👨‍💻 Agents"),
    ]
    for col_obj, (val, label) in zip([c1, c2, c3, c4, c5, c6], metrics):
        with col_obj:
            display = f"{val:,}" if isinstance(val, int) else str(val)
            st.markdown(f"""<div class="metric-card">
                <div class="metric-number">{display}</div>
                <div class="metric-label">{label}</div>
            </div>""", unsafe_allow_html=True)

    st.markdown("---")

    # Service Type pie
    r1, r2 = st.columns(2)
    with r1:
        if 'Service_Type' in df.columns:
            svc = df['Service_Type'].value_counts().reset_index()
            svc.columns = ['Service', 'Count']
            fig = px.pie(svc, values='Count', names='Service',
                         title='⚙️ Service Type Distribution',
                         hole=0.45, template=theme)
            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig, use_container_width=True)

    with r2:
        if 'Main_Category' in df.columns:
            mc = df['Main_Category'].value_counts().head(8).reset_index()
            mc.columns = ['Category', 'Count']
            fig = px.pie(mc, values='Count', names='Category',
                         title='🔥 Top Main Issue Categories',
                         hole=0.45, template=theme)
            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig, use_container_width=True)

    # Department bar
    if 'Department' in df.columns:
        st.markdown('<div class="section-header">🏢 Top Departments Overview</div>', unsafe_allow_html=True)
        dept_ov = df['Department'].value_counts().head(10).reset_index()
        dept_ov.columns = ['Department', 'Tickets']
        fig = px.bar(dept_ov, x='Tickets', y='Department', orientation='h',
                     title='Top 10 Departments by Ticket Count',
                     color='Tickets', color_continuous_scale='Blues',
                     template=theme, text='Tickets')
        fig.update_layout(height=450, yaxis={'categoryorder': 'total ascending'}, showlegend=False)
        fig.update_traces(textposition='outside')
        st.plotly_chart(fig, use_container_width=True)

# ════════════ TAB 2: ISSUES ════════════
with tab2:
    if 'Main_Category' in df.columns:
        st.markdown('<div class="section-header">🔥 Top Main Issue Categories</div>', unsafe_allow_html=True)
        d = df['Main_Category'].value_counts().head(top_n).reset_index()
        d.columns = ['Issue', 'Count']
        fig = px.bar(d, x='Count', y='Issue', orientation='h',
                     title=f'Top {top_n} Main Issues',
                     color='Count', color_continuous_scale='Blues',
                     template=theme, text='Count')
        fig.update_layout(height=600, yaxis={'categoryorder': 'total ascending'}, showlegend=False)
        fig.update_traces(textposition='outside')
        st.plotly_chart(fig, use_container_width=True)

    if 'Sub_Category' in df.columns:
        st.markdown('<div class="section-header">📂 Sub Categories</div>', unsafe_allow_html=True)
        d2 = df['Sub_Category'].dropna().value_counts().head(top_n).reset_index()
        d2.columns = ['Sub Category', 'Count']
        fig2 = px.bar(d2, x='Count', y='Sub Category', orientation='h',
                      title=f'Top {top_n} Sub Categories',
                      color='Count', color_continuous_scale='Oranges',
                      template=theme, text='Count')
        fig2.update_layout(height=600, yaxis={'categoryorder': 'total ascending'}, showlegend=False)
        fig2.update_traces(textposition='outside')
        st.plotly_chart(fig2, use_container_width=True)

    if 'Main_Category' in df.columns and 'Sub_Category' in df.columns:
        st.markdown('<div class="section-header">🔗 Main → Sub Category Treemap</div>', unsafe_allow_html=True)
        tree = df.dropna(subset=['Main_Category', 'Sub_Category'])
        tree = tree.groupby(['Main_Category', 'Sub_Category']).size().reset_index(name='Count')
        fig3 = px.treemap(tree, path=['Main_Category', 'Sub_Category'], values='Count',
                          title='Issue Category Treemap', template=theme,
                          color='Count', color_continuous_scale='Blues')
        fig3.update_layout(height=650)
        st.plotly_chart(fig3, use_container_width=True)

    if 'Service_Type' in df.columns and 'Main_Category' in df.columns:
        st.markdown('<div class="section-header">🧩 Service Type × Main Category Heatmap</div>', unsafe_allow_html=True)
        heat = df.groupby(['Service_Type', 'Main_Category']).size().reset_index(name='Count')
        top_svcs  = df['Service_Type'].value_counts().head(8).index.tolist()
        top_mains = df['Main_Category'].value_counts().head(10).index.tolist()
        heat = heat[heat['Service_Type'].isin(top_svcs) & heat['Main_Category'].isin(top_mains)]
        pivot = heat.pivot(index='Service_Type', columns='Main_Category', values='Count').fillna(0)
        import plotly.graph_objects as go
        fig4 = go.Figure(data=go.Heatmap(
            z=pivot.values,
            x=pivot.columns.tolist(),
            y=pivot.index.tolist(),
            colorscale='Blues', text=pivot.values.astype(int),
            texttemplate='%{text}', hoverongaps=False
        ))
        fig4.update_layout(title='Service Type × Issue Category',
                           template=theme, height=450,
                           xaxis_tickangle=-35)
        st.plotly_chart(fig4, use_container_width=True)

# ════════════ TAB 3: DEPARTMENTS ════════════
with tab3:
    if 'Department' in df.columns:
        st.markdown('<div class="section-header">🏢 Department-wise Ticket Volume</div>', unsafe_allow_html=True)
        d = df['Department'].value_counts().head(top_n).reset_index()
        d.columns = ['Department', 'Tickets']

        c1, c2 = st.columns(2)
        with c1:
            fig = px.bar(d, x='Tickets', y='Department', orientation='h',
                         title='Tickets by Department',
                         color='Tickets', color_continuous_scale='Teal',
                         template=theme, text='Tickets')
            fig.update_layout(height=550, yaxis={'categoryorder': 'total ascending'}, showlegend=False)
            fig.update_traces(textposition='outside')
            st.plotly_chart(fig, use_container_width=True)
        with c2:
            fig2 = px.pie(d, values='Tickets', names='Department',
                          title='Department Share (%)',
                          hole=0.4, template=theme)
            fig2.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig2, use_container_width=True)

        if 'Main_Category' in df.columns:
            st.markdown('<div class="section-header">📊 Department × Issue Type (Stacked)</div>', unsafe_allow_html=True)
            top_depts  = d['Department'].head(10).tolist()
            top_issues = df['Main_Category'].value_counts().head(8).index.tolist()
            cross = df[df['Department'].isin(top_depts) &
                       df['Main_Category'].isin(top_issues)].groupby(
                ['Department', 'Main_Category']).size().reset_index(name='Count')
            fig3 = px.bar(cross, x='Department', y='Count', color='Main_Category',
                          title='Department vs Issue Type',
                          template=theme, barmode='stack', text='Count')
            fig3.update_layout(height=550, xaxis_tickangle=-30,
                               legend=dict(orientation='h', yanchor='bottom', y=1.02))
            fig3.update_traces(textposition='inside')
            st.plotly_chart(fig3, use_container_width=True)

        if 'Service_Type' in df.columns:
            st.markdown('<div class="section-header">⚙️ Department × Service Type</div>', unsafe_allow_html=True)
            svc_cross = df[df['Department'].isin(top_depts)].groupby(
                ['Department', 'Service_Type']).size().reset_index(name='Count')
            fig4 = px.bar(svc_cross, x='Department', y='Count', color='Service_Type',
                          title='Department vs Service Type',
                          template=theme, barmode='group')
            fig4.update_layout(height=500, xaxis_tickangle=-30,
                               legend=dict(orientation='h', yanchor='bottom', y=1.02))
            st.plotly_chart(fig4, use_container_width=True)
    else:
        st.info("⚠️ Department column data mein nahi mili.")

# ════════════ TAB 4: AGENTS ════════════
with tab4:
    agent_col = 'Resolved_By' if 'Resolved_By' in df.columns else (
                'Assigned_To' if 'Assigned_To' in df.columns else None)

    if agent_col:
        st.markdown('<div class="section-header">👨‍💻 Agent Performance</div>', unsafe_allow_html=True)
        ag = df[agent_col].dropna().value_counts().head(top_n).reset_index()
        ag.columns = ['Agent', 'Tickets']

        # Clean agent names (remove -متعاقد suffix for display)
        ag['Agent_Short'] = ag['Agent'].str.replace('−متعاقد', '', regex=False)\
                                       .str.replace('-متعاقد', '', regex=False).str.strip()

        c1, c2 = st.columns(2)
        with c1:
            fig = px.bar(ag, x='Tickets', y='Agent_Short', orientation='h',
                         title=f'Top {top_n} Agents by Tickets',
                         color='Tickets', color_continuous_scale='Viridis',
                         template=theme, text='Tickets')
            fig.update_layout(height=600, yaxis={'categoryorder': 'total ascending'}, showlegend=False)
            fig.update_traces(textposition='outside')
            st.plotly_chart(fig, use_container_width=True)
        with c2:
            fig2 = px.pie(ag, values='Tickets', names='Agent_Short',
                          title='Agent Workload Share',
                          hole=0.4, template=theme)
            fig2.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig2, use_container_width=True)

        if 'Main_Category' in df.columns:
            st.markdown('<div class="section-header">🔥 Agent × Issue Type</div>', unsafe_allow_html=True)
            top_agents = df[agent_col].dropna().value_counts().head(10).index.tolist()
            top_issues = df['Main_Category'].value_counts().head(6).index.tolist()
            ag_issue = df[df[agent_col].isin(top_agents) &
                         df['Main_Category'].isin(top_issues)].copy()
            ag_issue['Agent_Short'] = ag_issue[agent_col]\
                .str.replace('−متعاقد', '', regex=False)\
                .str.replace('-متعاقد', '', regex=False).str.strip()
            ag_grp = ag_issue.groupby(['Agent_Short', 'Main_Category'])\
                             .size().reset_index(name='Count')
            fig3 = px.bar(ag_grp, x='Agent_Short', y='Count', color='Main_Category',
                          title='Agent Workload by Issue Type',
                          template=theme, barmode='stack')
            fig3.update_layout(height=500, xaxis_tickangle=-30,
                               legend=dict(orientation='h', yanchor='bottom', y=1.02))
            st.plotly_chart(fig3, use_container_width=True)

        if 'Department' in df.columns:
            st.markdown('<div class="section-header">🏢 Agent × Department Coverage</div>', unsafe_allow_html=True)
            top_agents = df[agent_col].dropna().value_counts().head(10).index.tolist()
            top_depts  = df['Department'].value_counts().head(10).index.tolist()
            cov = df[df[agent_col].isin(top_agents) &
                     df['Department'].isin(top_depts)].copy()
            cov['Agent_Short'] = cov[agent_col]\
                .str.replace('−متعاقد', '', regex=False)\
                .str.replace('-متعاقد', '', regex=False).str.strip()
            cov_grp = cov.groupby(['Agent_Short', 'Department'])\
                         .size().reset_index(name='Count')
            import plotly.graph_objects as go
            pivot_cov = cov_grp.pivot(index='Agent_Short',
                                      columns='Department', values='Count').fillna(0)
            fig4 = go.Figure(data=go.Heatmap(
                z=pivot_cov.values,
                x=pivot_cov.columns.tolist(),
                y=pivot_cov.index.tolist(),
                colorscale='Viridis',
                text=pivot_cov.values.astype(int),
                texttemplate='%{text}',
            ))
            fig4.update_layout(title='Agent Coverage by Department (Heatmap)',
                               template=theme, height=500,
                               xaxis_tickangle=-35)
            st.plotly_chart(fig4, use_container_width=True)
    else:
        st.info("⚠️ Agent column (Resolved_By / Assigned_To) nahi mili.")

# ════════════ TAB 5: RAW DATA ════════════
with tab5:
    st.markdown('<div class="section-header">🗃️ Raw Data Explorer</div>', unsafe_allow_html=True)

    col_filter, col_val = st.columns([1, 3])
    with col_filter:
        filter_col = st.selectbox("Column filter", ["All"] + df.columns.tolist())
    with col_val:
        search_term = st.text_input("🔍 Search value", "")

    if search_term:
        if filter_col == "All":
            mask = df.apply(lambda c: c.astype(str).str.contains(
                search_term, case=False, na=False)).any(axis=1)
        else:
            mask = df[filter_col].astype(str).str.contains(
                search_term, case=False, na=False)
        filtered_df = df[mask]
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
