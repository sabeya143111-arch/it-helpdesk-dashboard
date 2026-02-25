# ============================================================
#   IT HELPDESK ANALYTICS DASHBOARD  v3.0
#   Author  : tarique14321495
#   Data    : 2,495 records | 5 columns | Arabic Excel
#   Run     : streamlit run app.py
# ============================================================

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import io

# ── PAGE CONFIG ──────────────────────────────────────────────
st.set_page_config(
    page_title="IT Helpdesk Dashboard",
    page_icon="🖥️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── CSS ───────────────────────────────────────────────────────
st.markdown("""
<style>
/* Metric Cards */
.kpi {
    background: linear-gradient(135deg,#0f2544,#1a4a8a);
    border-radius:14px; padding:18px 10px;
    text-align:center; color:#fff;
    box-shadow:0 4px 18px rgba(0,0,0,.4);
    border-top:3px solid #00d4ff;
}
.kpi-num  { font-size:2.2rem; font-weight:800; color:#00d4ff; }
.kpi-lbl  { font-size:.82rem; color:#b0cfe8; margin-top:4px; letter-spacing:.5px; }

/* Section headers */
.sec {
    background:linear-gradient(90deg,#0f2544,transparent);
    border-left:4px solid #00d4ff;
    padding:9px 18px; border-radius:6px;
    margin:22px 0 10px; color:#fff;
    font-size:1.1rem; font-weight:700;
}

/* Sidebar */
[data-testid="stSidebar"] {background:#0a1628;}
</style>
""", unsafe_allow_html=True)

# ── COLUMN KEYS ───────────────────────────────────────────────
C_DEPT    = 'إدارة العميل'
C_SVC     = 'الخدمة'
C_MAIN    = 'التصنيف الرئيسي'
C_SUB     = 'التصنيف الفرعي'
C_AGENT   = 'مسند الى'

EN = {
    C_DEPT  : 'Department',
    C_SVC   : 'Service_Type',
    C_MAIN  : 'Main_Category',
    C_SUB   : 'Sub_Category',
    C_AGENT : 'Agent',
}

# ── SIDEBAR ───────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🖥️ IT Helpdesk")
    st.markdown("---")
    uploaded = st.file_uploader("📂 Excel Upload Karein", type=["xlsx","xls"])
    if uploaded:
        st.success(f"✅ {uploaded.name}")

# ── WELCOME ───────────────────────────────────────────────────
if not uploaded:
    st.markdown("""
    <div style='text-align:center;padding:80px 20px'>
      <h1 style='color:#00d4ff;font-size:3rem;'>🖥️ IT Helpdesk Analytics</h1>
      <p style='color:#adc6e5;font-size:1.2rem;'>
        Sidebar se <b>Excel file upload karein</b><br>
        Dashboard automatically ban jaayega!
      </p>
      <div style='display:flex;justify-content:center;gap:16px;flex-wrap:wrap;margin-top:30px'>
        <div style='background:#1e3a5f;border-radius:12px;padding:22px;width:145px;'>
          <div style='font-size:2.2rem'>📊</div>
          <div style='color:#fff;margin-top:8px;font-size:.9rem'>Overview & KPIs</div>
        </div>
        <div style='background:#1e3a5f;border-radius:12px;padding:22px;width:145px;'>
          <div style='font-size:2.2rem'>🔥</div>
          <div style='color:#fff;margin-top:8px;font-size:.9rem'>Issue Analysis</div>
        </div>
        <div style='background:#1e3a5f;border-radius:12px;padding:22px;width:145px;'>
          <div style='font-size:2.2rem'>🏢</div>
          <div style='color:#fff;margin-top:8px;font-size:.9rem'>Departments</div>
        </div>
        <div style='background:#1e3a5f;border-radius:12px;padding:22px;width:145px;'>
          <div style='font-size:2.2rem'>👨‍💻</div>
          <div style='color:#fff;margin-top:8px;font-size:.9rem'>Agent Stats</div>
        </div>
      </div>
    </div>""", unsafe_allow_html=True)
    st.stop()

# ── LOAD & CLEAN DATA ─────────────────────────────────────────
@st.cache_data(show_spinner="📊 Data load ho raha hai...")
def load_data(raw_bytes):
    # Row 0,1 = empty | Row 2 = Arabic headers
    df = pd.read_excel(io.BytesIO(raw_bytes), sheet_name=0, header=2)

    # Keep only the 5 useful columns
    keep = [c for c in [C_DEPT, C_SVC, C_MAIN, C_SUB, C_AGENT] if c in df.columns]
    df = df[keep].copy()

    # Forward-fill merged cells
    for c in [C_DEPT, C_SVC, C_MAIN, C_SUB]:
        if c in df.columns:
            df[c] = df[c].replace('', pd.NA).ffill()

    # Clean agent column
    if C_AGENT in df.columns:
        df[C_AGENT] = df[C_AGENT].astype(str).str.strip()
        df[C_AGENT] = df[C_AGENT].replace({'nan':pd.NA,'Agent':pd.NA,'':pd.NA})

    # Drop rows where all values are NA
    df.dropna(how='all', inplace=True)
    df.reset_index(drop=True, inplace=True)

    # Rename to English
    df.rename(columns=EN, inplace=True)

    # Short agent names (remove −متعاقد / -متعاقد)
    if 'Agent' in df.columns:
        df['Agent_Short'] = df['Agent']\
            .str.replace('−متعاقد','',regex=False)\
            .str.replace('-متعاقد','',regex=False)\
            .str.strip()

    return df

try:
    raw_bytes = uploaded.read()
    df = load_data(raw_bytes)
except Exception as e:
    st.error(f"❌ Load error: {e}")
    st.stop()

if df.empty:
    st.error("❌ Data empty hai. File check karein.")
    st.stop()

# ── SIDEBAR FILTERS ───────────────────────────────────────────
with st.sidebar:
    st.markdown("---")
    st.markdown("### 🔽 Filters")

    dept_opts = ['All'] + sorted(df['Department'].dropna().unique().tolist())
    sel_dept  = st.selectbox("🏢 Department", dept_opts)

    svc_opts  = ['All'] + sorted(df['Service_Type'].dropna().unique().tolist())
    sel_svc   = st.selectbox("⚙️ Service Type", svc_opts)

    main_opts = ['All'] + sorted(df['Main_Category'].dropna().unique().tolist())
    sel_main  = st.selectbox("🔥 Main Category", main_opts)

    st.markdown("---")
    top_n = st.slider("🔢 Top N Items", 5, 30, 15)
    theme = st.selectbox("🎨 Chart Theme", ["plotly_dark","plotly","ggplot2"])

# ── APPLY FILTERS ─────────────────────────────────────────────
dff = df.copy()
if sel_dept  != 'All': dff = dff[dff['Department']    == sel_dept]
if sel_svc   != 'All': dff = dff[dff['Service_Type']  == sel_svc]
if sel_main  != 'All': dff = dff[dff['Main_Category'] == sel_main]

# ── HEADER ────────────────────────────────────────────────────
st.markdown(f"""
<div style='background:linear-gradient(90deg,#0f2544,#0a1628);
            padding:18px 28px;border-radius:14px;margin-bottom:18px;
            border-bottom:2px solid #00d4ff;'>
  <h1 style='color:#00d4ff;margin:0;font-size:1.9rem;'>
    🖥️ IT Helpdesk Analytics Dashboard
  </h1>
  <p style='color:#b0cfe8;margin:5px 0 0;font-size:.92rem;'>
    📄 <b>{uploaded.name}</b> &nbsp;|&nbsp;
    🗂️ Total: <b>{len(df):,}</b> records &nbsp;|&nbsp;
    🔽 Filtered: <b>{len(dff):,}</b> records
    {"&nbsp;|&nbsp; 🟡 Filter active" if len(dff) < len(df) else ""}
  </p>
</div>
""", unsafe_allow_html=True)

# ── TABS ──────────────────────────────────────────────────────
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊 Overview",
    "🔥 Issues",
    "🏢 Departments",
    "👨‍💻 Agents",
    "🗃️ Raw Data",
])

# ════════════════════════════════════════════
# TAB 1 ─ OVERVIEW
# ════════════════════════════════════════════
with tab1:
    # KPI Cards
    st.markdown('<div class="sec">📌 Key Performance Indicators</div>',
                unsafe_allow_html=True)
    k1,k2,k3,k4,k5 = st.columns(5)
    kpis = [
        (len(dff),                              "🎫 Total Records"),
        (dff['Department'].nunique(),            "🏢 Departments"),
        (dff['Service_Type'].nunique(),          "⚙️ Service Types"),
        (dff['Main_Category'].nunique(),         "🔥 Issue Types"),
        (dff['Agent'].dropna().nunique()
         if 'Agent' in dff.columns else 0,      "👨‍💻 Agents"),
    ]
    for c, (v, lbl) in zip([k1,k2,k3,k4,k5], kpis):
        with c:
            st.markdown(f"""<div class="kpi">
              <div class="kpi-num">{v:,}</div>
              <div class="kpi-lbl">{lbl}</div>
            </div>""", unsafe_allow_html=True)

    st.markdown("---")

    # Row 1: Service Type pie | Main Category pie
    r1, r2 = st.columns(2)
    with r1:
        svc = dff['Service_Type'].value_counts().reset_index()
        svc.columns = ['Service','Count']
        fig = px.pie(svc, values='Count', names='Service',
                     title='⚙️ Service Type Distribution',
                     hole=0.45, template=theme)
        fig.update_traces(textposition='inside', textinfo='percent+label')
        fig.update_layout(showlegend=True,
                          legend=dict(orientation='v', x=1.02, y=0.5))
        st.plotly_chart(fig, use_container_width=True)

    with r2:
        mc = dff['Main_Category'].value_counts().head(8).reset_index()
        mc.columns = ['Category','Count']
        fig = px.pie(mc, values='Count', names='Category',
                     title='🔥 Top 8 Issue Categories',
                     hole=0.45, template=theme)
        fig.update_traces(textposition='inside', textinfo='percent+label')
        fig.update_layout(showlegend=True,
                          legend=dict(orientation='v', x=1.02, y=0.5))
        st.plotly_chart(fig, use_container_width=True)

    # Row 2: Top Departments bar
    st.markdown('<div class="sec">🏢 Top Departments by Ticket Volume</div>',
                unsafe_allow_html=True)
    dept_ov = dff['Department'].value_counts().head(15).reset_index()
    dept_ov.columns = ['Department','Tickets']
    fig = px.bar(dept_ov, x='Tickets', y='Department', orientation='h',
                 color='Tickets', color_continuous_scale='Blues',
                 template=theme, text='Tickets',
                 title='Tickets per Department (Top 15)')
    fig.update_layout(height=500,
                      yaxis={'categoryorder':'total ascending'},
                      showlegend=False,
                      coloraxis_showscale=False)
    fig.update_traces(textposition='outside')
    st.plotly_chart(fig, use_container_width=True)

    # Row 3: Service × Main Category stacked bar
    st.markdown('<div class="sec">🧩 Service Type × Issue Category</div>',
                unsafe_allow_html=True)
    top_mains = dff['Main_Category'].value_counts().head(8).index.tolist()
    sm = dff[dff['Main_Category'].isin(top_mains)]\
         .groupby(['Service_Type','Main_Category']).size().reset_index(name='Count')
    fig = px.bar(sm, x='Service_Type', y='Count', color='Main_Category',
                 barmode='stack', template=theme,
                 title='Service Type vs Top 8 Issue Categories',
                 text='Count')
    fig.update_layout(height=450, xaxis_tickangle=-25,
                      legend=dict(orientation='h', yanchor='bottom', y=1.01))
    fig.update_traces(textposition='inside')
    st.plotly_chart(fig, use_container_width=True)

# ════════════════════════════════════════════
# TAB 2 ─ ISSUES
# ════════════════════════════════════════════
with tab2:
    # Top Main Issues bar
    st.markdown('<div class="sec">🔥 Top Main Issue Categories</div>',
                unsafe_allow_html=True)
    d = dff['Main_Category'].value_counts().head(top_n).reset_index()
    d.columns = ['Issue','Count']
    fig = px.bar(d, x='Count', y='Issue', orientation='h',
                 title=f'Top {top_n} Main Issues',
                 color='Count', color_continuous_scale='Reds',
                 template=theme, text='Count')
    fig.update_layout(height=600,
                      yaxis={'categoryorder':'total ascending'},
                      showlegend=False, coloraxis_showscale=False)
    fig.update_traces(textposition='outside')
    st.plotly_chart(fig, use_container_width=True)

    # Sub Category bar
    st.markdown('<div class="sec">📂 Top Sub Categories</div>',
                unsafe_allow_html=True)
    d2 = dff['Sub_Category'].dropna().value_counts().head(top_n).reset_index()
    d2.columns = ['Sub Category','Count']
    fig2 = px.bar(d2, x='Count', y='Sub Category', orientation='h',
                  title=f'Top {top_n} Sub Categories',
                  color='Count', color_continuous_scale='Oranges',
                  template=theme, text='Count')
    fig2.update_layout(height=600,
                       yaxis={'categoryorder':'total ascending'},
                       showlegend=False, coloraxis_showscale=False)
    fig2.update_traces(textposition='outside')
    st.plotly_chart(fig2, use_container_width=True)

    # Treemap: Main → Sub
    st.markdown('<div class="sec">🔗 Issue Hierarchy Treemap</div>',
                unsafe_allow_html=True)
    tree = dff.dropna(subset=['Main_Category','Sub_Category'])\
              .groupby(['Main_Category','Sub_Category'])\
              .size().reset_index(name='Count')
    fig3 = px.treemap(tree, path=['Main_Category','Sub_Category'],
                      values='Count',
                      title='Main → Sub Category Hierarchy',
                      template=theme, color='Count',
                      color_continuous_scale='Blues')
    fig3.update_layout(height=650)
    fig3.update_traces(textinfo='label+value+percent root')
    st.plotly_chart(fig3, use_container_width=True)

    # Heatmap: Service × Main Category
    st.markdown('<div class="sec">🌡️ Service × Issue Heatmap</div>',
                unsafe_allow_html=True)
    top_svcs  = dff['Service_Type'].value_counts().head(8).index.tolist()
    top_main2 = dff['Main_Category'].value_counts().head(12).index.tolist()
    heat = dff[dff['Service_Type'].isin(top_svcs) &
               dff['Main_Category'].isin(top_main2)]\
           .groupby(['Service_Type','Main_Category'])\
           .size().reset_index(name='Count')
    pivot = heat.pivot(index='Service_Type',
                       columns='Main_Category', values='Count').fillna(0)
    fig4 = go.Figure(go.Heatmap(
        z=pivot.values,
        x=pivot.columns.tolist(),
        y=pivot.index.tolist(),
        colorscale='YlOrRd',
        text=pivot.values.astype(int),
        texttemplate='%{text}',
        hoverongaps=False
    ))
    fig4.update_layout(title='Service Type × Issue Category Count',
                       template=theme, height=420, xaxis_tickangle=-35)
    st.plotly_chart(fig4, use_container_width=True)

# ════════════════════════════════════════════
# TAB 3 ─ DEPARTMENTS
# ════════════════════════════════════════════
with tab3:
    st.markdown('<div class="sec">🏢 Department Ticket Volume</div>',
                unsafe_allow_html=True)
    d = dff['Department'].value_counts().head(top_n).reset_index()
    d.columns = ['Department','Tickets']

    c1, c2 = st.columns(2)
    with c1:
        fig = px.bar(d, x='Tickets', y='Department', orientation='h',
                     title=f'Top {top_n} Departments',
                     color='Tickets', color_continuous_scale='Teal',
                     template=theme, text='Tickets')
        fig.update_layout(height=550,
                          yaxis={'categoryorder':'total ascending'},
                          showlegend=False, coloraxis_showscale=False)
        fig.update_traces(textposition='outside')
        st.plotly_chart(fig, use_container_width=True)
    with c2:
        fig2 = px.pie(d, values='Tickets', names='Department',
                      title='Department Share %',
                      hole=0.4, template=theme)
        fig2.update_traces(textposition='inside',
                           textinfo='percent+label')
        st.plotly_chart(fig2, use_container_width=True)

    # Dept × Service Type
    st.markdown('<div class="sec">⚙️ Department × Service Type</div>',
                unsafe_allow_html=True)
    top_depts = d['Department'].head(12).tolist()
    svc_x_dept = dff[dff['Department'].isin(top_depts)]\
                 .groupby(['Department','Service_Type'])\
                 .size().reset_index(name='Count')
    fig3 = px.bar(svc_x_dept, x='Department', y='Count',
                  color='Service_Type', barmode='stack',
                  title='Department vs Service Type',
                  template=theme)
    fig3.update_layout(height=500, xaxis_tickangle=-30,
                       legend=dict(orientation='h',
                                   yanchor='bottom', y=1.01))
    st.plotly_chart(fig3, use_container_width=True)

    # Dept × Main Category
    st.markdown('<div class="sec">🔥 Department × Issue Category</div>',
                unsafe_allow_html=True)
    top_mains = dff['Main_Category'].value_counts().head(8).index.tolist()
    cross = dff[dff['Department'].isin(top_depts) &
                dff['Main_Category'].isin(top_mains)]\
            .groupby(['Department','Main_Category'])\
            .size().reset_index(name='Count')
    fig4 = px.bar(cross, x='Department', y='Count',
                  color='Main_Category', barmode='stack',
                  title='Department × Top 8 Issue Types',
                  template=theme)
    fig4.update_layout(height=550, xaxis_tickangle=-30,
                       legend=dict(orientation='h',
                                   yanchor='bottom', y=1.01))
    st.plotly_chart(fig4, use_container_width=True)

    # Sunburst: Dept → Service
    st.markdown('<div class="sec">☀️ Department → Service Sunburst</div>',
                unsafe_allow_html=True)
    sun = dff[dff['Department'].isin(top_depts)]\
          .groupby(['Department','Service_Type'])\
          .size().reset_index(name='Count')
    fig5 = px.sunburst(sun, path=['Department','Service_Type'],
                       values='Count',
                       title='Department → Service Type Breakdown',
                       template=theme, color='Count',
                       color_continuous_scale='Blues')
    fig5.update_layout(height=600)
    st.plotly_chart(fig5, use_container_width=True)

# ════════════════════════════════════════════
# TAB 4 ─ AGENTS
# ════════════════════════════════════════════
with tab4:
    if 'Agent' not in dff.columns or dff['Agent'].dropna().empty:
        st.info("⚠️ Agent data available nahi hai.")
    else:
        st.markdown('<div class="sec">👨‍💻 Agent Workload Overview</div>',
                    unsafe_allow_html=True)
        ag = dff.dropna(subset=['Agent'])\
                .groupby(['Agent','Agent_Short'])\
                .size().reset_index(name='Tickets')\
                .sort_values('Tickets', ascending=False)\
                .head(top_n)

        c1, c2 = st.columns(2)
        with c1:
            fig = px.bar(ag, x='Tickets', y='Agent_Short',
                         orientation='h',
                         title=f'Top {top_n} Agents by Tickets Assigned',
                         color='Tickets',
                         color_continuous_scale='Viridis',
                         template=theme, text='Tickets')
            fig.update_layout(height=580,
                              yaxis={'categoryorder':'total ascending'},
                              showlegend=False,
                              coloraxis_showscale=False)
            fig.update_traces(textposition='outside')
            st.plotly_chart(fig, use_container_width=True)
        with c2:
            fig2 = px.pie(ag, values='Tickets', names='Agent_Short',
                          title='Agent Workload Share %',
                          hole=0.4, template=theme)
            fig2.update_traces(textposition='inside',
                               textinfo='percent+label')
            st.plotly_chart(fig2, use_container_width=True)

        # Agent × Service Type
        st.markdown('<div class="sec">⚙️ Agent × Service Type</div>',
                    unsafe_allow_html=True)
        top_agent_keys = ag['Agent'].tolist()
        ag_svc = dff[dff['Agent'].isin(top_agent_keys)]\
                 .groupby(['Agent_Short','Service_Type'])\
                 .size().reset_index(name='Count')
        fig3 = px.bar(ag_svc, x='Agent_Short', y='Count',
                      color='Service_Type', barmode='stack',
                      title='Agent vs Service Type',
                      template=theme)
        fig3.update_layout(height=480, xaxis_tickangle=-30,
                           legend=dict(orientation='h',
                                       yanchor='bottom', y=1.01))
        st.plotly_chart(fig3, use_container_width=True)

        # Agent × Main Category
        st.markdown('<div class="sec">🔥 Agent × Issue Category</div>',
                    unsafe_allow_html=True)
        top_mains = dff['Main_Category'].value_counts().head(8).index.tolist()
        ag_issue = dff[dff['Agent'].isin(top_agent_keys) &
                       dff['Main_Category'].isin(top_mains)]\
                   .groupby(['Agent_Short','Main_Category'])\
                   .size().reset_index(name='Count')
        fig4 = px.bar(ag_issue, x='Agent_Short', y='Count',
                      color='Main_Category', barmode='stack',
                      title='Agent Workload by Issue Type',
                      template=theme)
        fig4.update_layout(height=480, xaxis_tickangle=-30,
                           legend=dict(orientation='h',
                                       yanchor='bottom', y=1.01))
        st.plotly_chart(fig4, use_container_width=True)

        # Agent × Department Heatmap
        st.markdown('<div class="sec">🌡️ Agent × Department Coverage Heatmap</div>',
                    unsafe_allow_html=True)
        top_depts_ag = dff['Department'].value_counts().head(12).index.tolist()
        cov = dff[dff['Agent'].isin(top_agent_keys) &
                  dff['Department'].isin(top_depts_ag)]\
              .groupby(['Agent_Short','Department'])\
              .size().reset_index(name='Count')
        pivot_cov = cov.pivot(index='Agent_Short',
                              columns='Department',
                              values='Count').fillna(0)
        fig5 = go.Figure(go.Heatmap(
            z=pivot_cov.values,
            x=pivot_cov.columns.tolist(),
            y=pivot_cov.index.tolist(),
            colorscale='Teal',
            text=pivot_cov.values.astype(int),
            texttemplate='%{text}',
            hoverongaps=False
        ))
        fig5.update_layout(title='Which Agent Covers Which Department',
                           template=theme, height=520,
                           xaxis_tickangle=-35)
        st.plotly_chart(fig5, use_container_width=True)

# ════════════════════════════════════════════
# TAB 5 ─ RAW DATA
# ════════════════════════════════════════════
with tab5:
    st.markdown('<div class="sec">🗃️ Raw Data Explorer</div>',
                unsafe_allow_html=True)

    sc1, sc2 = st.columns([1, 3])
    with sc1:
        filter_col = st.selectbox("Filter Column",
                                  ["All"] + df.columns.tolist())
    with sc2:
        search_term = st.text_input("🔍 Search value", "")

    show_df = dff.drop(columns=['Agent_Short'], errors='ignore').copy()

    if search_term:
        if filter_col == "All":
            mask = show_df.apply(lambda c: c.astype(str).str.contains(
                search_term, case=False, na=False)).any(axis=1)
        else:
            mask = show_df[filter_col].astype(str).str.contains(
                search_term, case=False, na=False)
        show_df = show_df[mask]

    st.markdown(f"**Showing `{len(show_df):,}` of `{len(df):,}` rows**")
    st.dataframe(show_df, use_container_width=True, height=520)

    # Column-wise stats
    with st.expander("📈 Column Statistics"):
        for col in show_df.columns:
            vc = show_df[col].dropna().value_counts()
            st.markdown(f"**{col}** — {len(vc)} unique values")
            st.dataframe(vc.head(10).rename('Count').reset_index(),
                         use_container_width=True, hide_index=True)

    # Download
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        show_df.to_excel(writer, index=False, sheet_name='FilteredData')
    st.download_button(
        label="⬇️ Download as Excel",
        data=output.getvalue(),
        file_name="helpdesk_filtered.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
