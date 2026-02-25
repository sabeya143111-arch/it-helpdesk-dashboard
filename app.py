# ============================================================
#   IT HELPDESK ANALYTICS DASHBOARD  v4.0
#   Author  : tarique14321495
#   Data    : 2,494 records | 5 useful columns | Arabic Excel
#   Features: Bilingual (AR/EN), Filters, 15+ Charts
#   Run     : streamlit run app.py
# ============================================================

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import io

# ── PAGE CONFIG ───────────────────────────────────────────────
st.set_page_config(
    page_title="IT Helpdesk Dashboard",
    page_icon="🖥️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── TRANSLATIONS ──────────────────────────────────────────────
T = {
    'AR': {
        'title'         : '🖥️ لوحة تحليلات مكتب الدعم التقني',
        'upload'        : '📂 رفع ملف Excel',
        'filters'       : '🔽 الفلاتر',
        'dept_filter'   : '🏢 الإدارة',
        'svc_filter'    : '⚙️ الخدمة',
        'main_filter'   : '🔥 التصنيف الرئيسي',
        'top_n'         : '🔢 أعلى N نتيجة',
        'theme'         : '🎨 نمط الرسم',
        'all'           : 'الكل',
        'total_rec'     : '🎫 إجمالي السجلات',
        'departments'   : '🏢 الإدارات',
        'svc_types'     : '⚙️ أنواع الخدمات',
        'issue_types'   : '🔥 أنواع المشكلات',
        'agents'        : '👨‍💻 الموظفون',
        'tab_overview'  : '📊 نظرة عامة',
        'tab_issues'    : '🔥 المشكلات',
        'tab_dept'      : '🏢 الإدارات',
        'tab_agents'    : '👨‍💻 الموظفون',
        'tab_raw'       : '🗃️ البيانات الخام',
        'kpi_sec'       : '📌 مؤشرات الأداء الرئيسية',
        'svc_dist'      : '⚙️ توزيع أنواع الخدمات',
        'top8_issues'   : '🔥 أعلى 8 تصنيفات رئيسية',
        'top_dept_vol'  : '🏢 أعلى الإدارات من حيث الطلبات',
        'svc_x_issue'   : '🧩 الخدمة × التصنيف الرئيسي',
        'top_main'      : '🔥 أعلى التصنيفات الرئيسية',
        'top_sub'       : '📂 أعلى التصنيفات الفرعية',
        'treemap'       : '🔗 شجرة التصنيفات',
        'heatmap_svc'   : '🌡️ خريطة حرارية: الخدمة × التصنيف',
        'dept_vol'      : '🏢 حجم الطلبات لكل إدارة',
        'dept_svc'      : '⚙️ الإدارة × نوع الخدمة',
        'dept_issue'    : '🔥 الإدارة × التصنيف الرئيسي',
        'sunburst'      : '☀️ الإدارة ← الخدمة (Sunburst)',
        'agent_wl'      : '👨‍💻 عبء عمل الموظفين',
        'agent_svc'     : '⚙️ الموظف × نوع الخدمة',
        'agent_issue'   : '🔥 الموظف × التصنيف الرئيسي',
        'agent_heatmap' : '🌡️ خريطة: الموظف × الإدارة',
        'raw_explorer'  : '🗃️ مستكشف البيانات الخام',
        'filter_col'    : 'تصفية العمود',
        'search'        : '🔍 بحث',
        'showing'       : 'عرض',
        'of'            : 'من',
        'rows'          : 'سجل',
        'download'      : '⬇️ تنزيل كـ Excel',
        'col_stats'     : '📈 إحصائيات الأعمدة',
        'unique'        : 'قيم فريدة',
        'filtered'      : '🔽 تم التصفية',
        'lang_label'    : 'اللغة / Language',
        'welcome_title' : '🖥️ لوحة تحليلات مكتب الدعم التقني',
        'welcome_sub'   : 'ارفع ملف Excel من القائمة الجانبية وسيتم إنشاء لوحة التحليلات تلقائياً!',
        'dept_share'    : 'نسبة الإدارات %',
        'agent_share'   : 'حصة الموظفين %',
    },
    'EN': {
        'title'         : '🖥️ IT Helpdesk Analytics Dashboard',
        'upload'        : '📂 Upload Excel File',
        'filters'       : '🔽 Filters',
        'dept_filter'   : '🏢 Department',
        'svc_filter'    : '⚙️ Service Type',
        'main_filter'   : '🔥 Main Category',
        'top_n'         : '🔢 Top N Items',
        'theme'         : '🎨 Chart Theme',
        'all'           : 'All',
        'total_rec'     : '🎫 Total Records',
        'departments'   : '🏢 Departments',
        'svc_types'     : '⚙️ Service Types',
        'issue_types'   : '🔥 Issue Types',
        'agents'        : '👨‍💻 Agents',
        'tab_overview'  : '📊 Overview',
        'tab_issues'    : '🔥 Issues',
        'tab_dept'      : '🏢 Departments',
        'tab_agents'    : '👨‍💻 Agents',
        'tab_raw'       : '🗃️ Raw Data',
        'kpi_sec'       : '📌 Key Performance Indicators',
        'svc_dist'      : '⚙️ Service Type Distribution',
        'top8_issues'   : '🔥 Top 8 Issue Categories',
        'top_dept_vol'  : '🏢 Top Departments by Ticket Volume',
        'svc_x_issue'   : '🧩 Service Type × Issue Category',
        'top_main'      : '🔥 Top Main Categories',
        'top_sub'       : '📂 Top Sub Categories',
        'treemap'       : '🔗 Issue Hierarchy Treemap',
        'heatmap_svc'   : '🌡️ Service × Issue Heatmap',
        'dept_vol'      : '🏢 Department Ticket Volume',
        'dept_svc'      : '⚙️ Department × Service Type',
        'dept_issue'    : '🔥 Department × Issue Category',
        'sunburst'      : '☀️ Department → Service Sunburst',
        'agent_wl'      : '👨‍💻 Agent Workload Overview',
        'agent_svc'     : '⚙️ Agent × Service Type',
        'agent_issue'   : '🔥 Agent × Issue Category',
        'agent_heatmap' : '🌡️ Agent × Department Heatmap',
        'raw_explorer'  : '🗃️ Raw Data Explorer',
        'filter_col'    : 'Filter Column',
        'search'        : '🔍 Search value',
        'showing'       : 'Showing',
        'of'            : 'of',
        'rows'          : 'rows',
        'download'      : '⬇️ Download as Excel',
        'col_stats'     : '📈 Column Statistics',
        'unique'        : 'unique values',
        'filtered'      : '🟡 Filter Active',
        'lang_label'    : 'Language / اللغة',
        'welcome_title' : '🖥️ IT Helpdesk Analytics',
        'welcome_sub'   : 'Upload your Excel file from the sidebar and the dashboard will build automatically!',
        'dept_share'    : 'Department Share %',
        'agent_share'   : 'Agent Workload Share %',
    }
}

# Column name keys
C_DEPT  = 'إدارة العميل'
C_SVC   = 'الخدمة'
C_MAIN  = 'التصنيف الرئيسي'
C_SUB   = 'التصنيف الفرعي'
C_AGENT = 'مسند الى'
C_RES   = 'تم حل بواسطة'

# ── CSS ───────────────────────────────────────────────────────
st.markdown("""
<style>
.kpi {
    background: linear-gradient(135deg,#0f2544,#1a4a8a);
    border-radius:14px; padding:18px 8px;
    text-align:center; color:#fff;
    box-shadow:0 4px 18px rgba(0,0,0,.4);
    border-top:3px solid #00d4ff;
    margin-bottom:8px;
}
.kpi-num { font-size:2.1rem; font-weight:800; color:#00d4ff; }
.kpi-lbl { font-size:.8rem; color:#b0cfe8; margin-top:4px; letter-spacing:.4px; }
.sec {
    background:linear-gradient(90deg,#0f2544,transparent);
    border-left:4px solid #00d4ff;
    padding:9px 18px; border-radius:6px;
    margin:22px 0 10px; color:#fff;
    font-size:1.05rem; font-weight:700;
}
[data-testid="stSidebar"] { background:#0a1628 !important; }
.stTabs [data-baseweb="tab"] {
    font-size:.93rem; font-weight:600; padding:8px 18px;
}
</style>
""", unsafe_allow_html=True)

# ── SIDEBAR ───────────────────────────────────────────────────
with st.sidebar:
    # Language toggle — first thing
    lang = st.radio("🌐 Language / اللغة", ["EN", "AR"],
                    horizontal=True, index=0)
    tx = T[lang]

    st.markdown(f"## {tx['title']}")
    st.markdown("---")
    uploaded = st.file_uploader(tx['upload'], type=["xlsx","xls"])
    if uploaded:
        st.success(f"✅ {uploaded.name}")

# ── WELCOME SCREEN ────────────────────────────────────────────
if not uploaded:
    st.markdown(f"""
    <div style='text-align:center;padding:80px 20px'>
      <h1 style='color:#00d4ff;font-size:2.8rem;'>{tx['welcome_title']}</h1>
      <p style='color:#adc6e5;font-size:1.15rem;margin-top:12px;'>{tx['welcome_sub']}</p>
      <div style='display:flex;justify-content:center;gap:16px;
                  flex-wrap:wrap;margin-top:35px'>
        {''.join([f"<div style='background:#1e3a5f;border-radius:12px;padding:22px;width:140px'>"
                  f"<div style='font-size:2.2rem'>{ic}</div>"
                  f"<div style='color:#fff;margin-top:8px;font-size:.88rem'>{lb}</div></div>"
                  for ic,lb in [('📊',tx['tab_overview']),('🔥',tx['tab_issues']),
                                 ('🏢',tx['tab_dept']),('👨‍💻',tx['tab_agents'])]])}
      </div>
    </div>""", unsafe_allow_html=True)
    st.stop()

# ── LOAD DATA ─────────────────────────────────────────────────
@st.cache_data(show_spinner="📊 Loading data...")
def load_data(raw_bytes: bytes) -> pd.DataFrame:
    df = pd.read_excel(io.BytesIO(raw_bytes), sheet_name=0, header=2)

    # Remove Grand Total row if present
    if C_DEPT in df.columns:
        df = df[df[C_DEPT] != 'Grand Total']

    # Keep only useful columns
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

    # Drop fully empty rows
    df.dropna(how='all', inplace=True)
    df.reset_index(drop=True, inplace=True)

    # Short agent name (remove contractor suffix)
    if C_AGENT in df.columns:
        df['_agent_short'] = df[C_AGENT]\
            .str.replace('−متعاقد','',regex=False)\
            .str.replace('-متعاقد','',regex=False).str.strip()

    return df

try:
    raw_bytes = uploaded.read()
    df = load_data(raw_bytes)
except Exception as e:
    st.error(f"❌ Error: {e}")
    st.stop()

if df.empty:
    st.error("❌ Data is empty. Check file.")
    st.stop()

# ── SIDEBAR FILTERS ───────────────────────────────────────────
with st.sidebar:
    st.markdown("---")
    st.markdown(f"### {tx['filters']}")

    all_lbl = tx['all']

    dept_opts = [all_lbl] + sorted(df[C_DEPT].dropna().unique().tolist())
    sel_dept  = st.selectbox(tx['dept_filter'], dept_opts)

    svc_opts  = [all_lbl] + sorted(df[C_SVC].dropna().unique().tolist())
    sel_svc   = st.selectbox(tx['svc_filter'], svc_opts)

    main_opts = [all_lbl] + sorted(df[C_MAIN].dropna().unique().tolist())
    sel_main  = st.selectbox(tx['main_filter'], main_opts)

    st.markdown("---")
    top_n  = st.slider(tx['top_n'], 5, 30, 15)
    theme  = st.selectbox(tx['theme'], ["plotly_dark","plotly","ggplot2"])
    st.markdown("---")
    st.caption(f"📊 Total records: **{len(df):,}**")

# ── APPLY FILTERS ─────────────────────────────────────────────
dff = df.copy()
if sel_dept != all_lbl: dff = dff[dff[C_DEPT] == sel_dept]
if sel_svc  != all_lbl: dff = dff[dff[C_SVC]  == sel_svc]
if sel_main != all_lbl: dff = dff[dff[C_MAIN] == sel_main]

is_filtered = len(dff) < len(df)

# ── HEADER ────────────────────────────────────────────────────
st.markdown(f"""
<div style='background:linear-gradient(90deg,#0f2544,#0a1628);
            padding:16px 26px;border-radius:14px;margin-bottom:16px;
            border-bottom:2px solid #00d4ff;'>
  <h1 style='color:#00d4ff;margin:0;font-size:1.8rem;'>{tx['title']}</h1>
  <p style='color:#b0cfe8;margin:5px 0 0;font-size:.88rem;'>
    📄 <b>{uploaded.name}</b> &nbsp;|&nbsp;
    🗂️ Total: <b>{len(df):,}</b> &nbsp;|&nbsp;
    🔽 Filtered: <b>{len(dff):,}</b>
    {"&nbsp; 🟡 <b>" + tx['filtered'] + "</b>" if is_filtered else ""}
  </p>
</div>
""", unsafe_allow_html=True)

# ── HELPER ────────────────────────────────────────────────────
def sec(label):
    st.markdown(f'<div class="sec">{label}</div>', unsafe_allow_html=True)

# ── TABS ──────────────────────────────────────────────────────
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    tx['tab_overview'],
    tx['tab_issues'],
    tx['tab_dept'],
    tx['tab_agents'],
    tx['tab_raw'],
])

# ════════════ TAB 1: OVERVIEW ════════════
with tab1:
    sec(tx['kpi_sec'])
    k1,k2,k3,k4,k5 = st.columns(5)
    kpis = [
        (len(dff),                              tx['total_rec']),
        (dff[C_DEPT].nunique(),                 tx['departments']),
        (dff[C_SVC].nunique(),                  tx['svc_types']),
        (dff[C_MAIN].nunique(),                 tx['issue_types']),
        (dff[C_AGENT].dropna().nunique()
         if C_AGENT in dff.columns else 0,      tx['agents']),
    ]
    for col_obj,(v,lbl) in zip([k1,k2,k3,k4,k5], kpis):
        with col_obj:
            st.markdown(f"""<div class="kpi">
              <div class="kpi-num">{v:,}</div>
              <div class="kpi-lbl">{lbl}</div>
            </div>""", unsafe_allow_html=True)

    st.markdown("---")

    # Pie: Service Type | Pie: Top 8 Main Issues
    r1, r2 = st.columns(2)
    with r1:
        svc = dff[C_SVC].value_counts().reset_index()
        svc.columns = ['Service','Count']
        fig = px.pie(svc, values='Count', names='Service',
                     title=tx['svc_dist'], hole=0.45, template=theme)
        fig.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig, use_container_width=True)
    with r2:
        mc = dff[C_MAIN].value_counts().head(8).reset_index()
        mc.columns = ['Category','Count']
        fig = px.pie(mc, values='Count', names='Category',
                     title=tx['top8_issues'], hole=0.45, template=theme)
        fig.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig, use_container_width=True)

    # Top Departments bar
    sec(tx['top_dept_vol'])
    dv = dff[C_DEPT].value_counts().head(15).reset_index()
    dv.columns = ['Department','Tickets']
    fig = px.bar(dv, x='Tickets', y='Department', orientation='h',
                 color='Tickets', color_continuous_scale='Blues',
                 template=theme, text='Tickets',
                 title=tx['top_dept_vol'])
    fig.update_layout(height=520,
                      yaxis={'categoryorder':'total ascending'},
                      showlegend=False, coloraxis_showscale=False)
    fig.update_traces(textposition='outside')
    st.plotly_chart(fig, use_container_width=True)

    # Stacked bar: Service × Main Category
    sec(tx['svc_x_issue'])
    top_m = dff[C_MAIN].value_counts().head(8).index.tolist()
    sm = dff[dff[C_MAIN].isin(top_m)]\
         .groupby([C_SVC, C_MAIN]).size().reset_index(name='Count')
    fig = px.bar(sm, x=C_SVC, y='Count', color=C_MAIN,
                 barmode='stack', template=theme,
                 title=tx['svc_x_issue'], text='Count')
    fig.update_layout(height=450, xaxis_tickangle=-25,
                      legend=dict(orientation='h', yanchor='bottom', y=1.01))
    fig.update_traces(textposition='inside')
    st.plotly_chart(fig, use_container_width=True)

# ════════════ TAB 2: ISSUES ════════════
with tab2:
    # Top Main Issues
    sec(tx['top_main'])
    d = dff[C_MAIN].value_counts().head(top_n).reset_index()
    d.columns = ['Issue','Count']
    fig = px.bar(d, x='Count', y='Issue', orientation='h',
                 color='Count', color_continuous_scale='Reds',
                 template=theme, text='Count',
                 title=f"{tx['top_main']} (Top {top_n})")
    fig.update_layout(height=max(400, top_n*30),
                      yaxis={'categoryorder':'total ascending'},
                      showlegend=False, coloraxis_showscale=False)
    fig.update_traces(textposition='outside')
    st.plotly_chart(fig, use_container_width=True)

    # Top Sub Categories
    sec(tx['top_sub'])
    d2 = dff[C_SUB].dropna().value_counts().head(top_n).reset_index()
    d2.columns = ['Sub','Count']
    fig2 = px.bar(d2, x='Count', y='Sub', orientation='h',
                  color='Count', color_continuous_scale='Oranges',
                  template=theme, text='Count',
                  title=f"{tx['top_sub']} (Top {top_n})")
    fig2.update_layout(height=max(400, top_n*30),
                       yaxis={'categoryorder':'total ascending'},
                       showlegend=False, coloraxis_showscale=False)
    fig2.update_traces(textposition='outside')
    st.plotly_chart(fig2, use_container_width=True)

    # Treemap: Main → Sub
    sec(tx['treemap'])
    tree = dff.dropna(subset=[C_MAIN, C_SUB])\
              .groupby([C_MAIN, C_SUB]).size().reset_index(name='Count')
    fig3 = px.treemap(tree, path=[C_MAIN, C_SUB], values='Count',
                      title=tx['treemap'], template=theme,
                      color='Count', color_continuous_scale='Blues')
    fig3.update_layout(height=650)
    fig3.update_traces(textinfo='label+value+percent root')
    st.plotly_chart(fig3, use_container_width=True)

    # Heatmap: Service × Main Category
    sec(tx['heatmap_svc'])
    top_svcs = dff[C_SVC].value_counts().head(8).index.tolist()
    top_m2   = dff[C_MAIN].value_counts().head(12).index.tolist()
    heat = dff[dff[C_SVC].isin(top_svcs) & dff[C_MAIN].isin(top_m2)]\
           .groupby([C_SVC, C_MAIN]).size().reset_index(name='Count')
    pivot = heat.pivot(index=C_SVC, columns=C_MAIN,
                       values='Count').fillna(0)
    fig4 = go.Figure(go.Heatmap(
        z=pivot.values,
        x=pivot.columns.tolist(),
        y=pivot.index.tolist(),
        colorscale='YlOrRd',
        text=pivot.values.astype(int),
        texttemplate='%{text}',
        hoverongaps=False
    ))
    fig4.update_layout(title=tx['heatmap_svc'], template=theme,
                       height=420, xaxis_tickangle=-35)
    st.plotly_chart(fig4, use_container_width=True)

# ════════════ TAB 3: DEPARTMENTS ════════════
with tab3:
    sec(tx['dept_vol'])
    d = dff[C_DEPT].value_counts().head(top_n).reset_index()
    d.columns = ['Department','Tickets']

    c1, c2 = st.columns(2)
    with c1:
        fig = px.bar(d, x='Tickets', y='Department', orientation='h',
                     title=tx['dept_vol'],
                     color='Tickets', color_continuous_scale='Teal',
                     template=theme, text='Tickets')
        fig.update_layout(height=550,
                          yaxis={'categoryorder':'total ascending'},
                          showlegend=False, coloraxis_showscale=False)
        fig.update_traces(textposition='outside')
        st.plotly_chart(fig, use_container_width=True)
    with c2:
        fig2 = px.pie(d, values='Tickets', names='Department',
                      title=tx['dept_share'], hole=0.4, template=theme)
        fig2.update_traces(textposition='inside',
                           textinfo='percent+label')
        st.plotly_chart(fig2, use_container_width=True)

    # Dept × Service Type stacked
    sec(tx['dept_svc'])
    top_depts = d['Department'].head(12).tolist()
    ds = dff[dff[C_DEPT].isin(top_depts)]\
         .groupby([C_DEPT, C_SVC]).size().reset_index(name='Count')
    fig3 = px.bar(ds, x=C_DEPT, y='Count', color=C_SVC,
                  barmode='stack', template=theme,
                  title=tx['dept_svc'])
    fig3.update_layout(height=500, xaxis_tickangle=-30,
                       legend=dict(orientation='h',
                                   yanchor='bottom', y=1.01))
    st.plotly_chart(fig3, use_container_width=True)

    # Dept × Main Category stacked
    sec(tx['dept_issue'])
    top_m = dff[C_MAIN].value_counts().head(8).index.tolist()
    cross = dff[dff[C_DEPT].isin(top_depts) &
                dff[C_MAIN].isin(top_m)]\
            .groupby([C_DEPT, C_MAIN]).size().reset_index(name='Count')
    fig4 = px.bar(cross, x=C_DEPT, y='Count', color=C_MAIN,
                  barmode='stack', template=theme,
                  title=tx['dept_issue'])
    fig4.update_layout(height=550, xaxis_tickangle=-30,
                       legend=dict(orientation='h',
                                   yanchor='bottom', y=1.01))
    st.plotly_chart(fig4, use_container_width=True)

    # Sunburst: Dept → Service
    sec(tx['sunburst'])
    sun = dff[dff[C_DEPT].isin(top_depts)]\
          .groupby([C_DEPT, C_SVC]).size().reset_index(name='Count')
    fig5 = px.sunburst(sun, path=[C_DEPT, C_SVC], values='Count',
                       title=tx['sunburst'], template=theme,
                       color='Count', color_continuous_scale='Blues')
    fig5.update_layout(height=620)
    st.plotly_chart(fig5, use_container_width=True)

# ════════════ TAB 4: AGENTS ════════════
with tab4:
    if C_AGENT not in dff.columns or dff[C_AGENT].dropna().empty:
        st.info("⚠️ Agent data not available.")
    else:
        sec(tx['agent_wl'])
        ag = dff.dropna(subset=[C_AGENT])\
                .groupby([C_AGENT, '_agent_short'])\
                .size().reset_index(name='Tickets')\
                .sort_values('Tickets', ascending=False)\
                .head(top_n)

        c1, c2 = st.columns(2)
        with c1:
            fig = px.bar(ag, x='Tickets', y='_agent_short',
                         orientation='h', title=tx['agent_wl'],
                         color='Tickets',
                         color_continuous_scale='Viridis',
                         template=theme, text='Tickets')
            fig.update_layout(height=580,
                              yaxis={'categoryorder':'total ascending'},
                              showlegend=False, coloraxis_showscale=False,
                              yaxis_title='Agent')
            fig.update_traces(textposition='outside')
            st.plotly_chart(fig, use_container_width=True)
        with c2:
            fig2 = px.pie(ag, values='Tickets', names='_agent_short',
                          title=tx['agent_share'], hole=0.4,
                          template=theme)
            fig2.update_traces(textposition='inside',
                               textinfo='percent+label')
            st.plotly_chart(fig2, use_container_width=True)

        top_agents = ag[C_AGENT].tolist()

        # Agent × Service Type
        sec(tx['agent_svc'])
        ag_sv = dff[dff[C_AGENT].isin(top_agents)]\
                .groupby(['_agent_short', C_SVC])\
                .size().reset_index(name='Count')
        fig3 = px.bar(ag_sv, x='_agent_short', y='Count',
                      color=C_SVC, barmode='stack',
                      title=tx['agent_svc'], template=theme)
        fig3.update_layout(height=480, xaxis_tickangle=-30,
                           xaxis_title='Agent',
                           legend=dict(orientation='h',
                                       yanchor='bottom', y=1.01))
        st.plotly_chart(fig3, use_container_width=True)

        # Agent × Main Category
        sec(tx['agent_issue'])
        top_m = dff[C_MAIN].value_counts().head(8).index.tolist()
        ag_is = dff[dff[C_AGENT].isin(top_agents) &
                    dff[C_MAIN].isin(top_m)]\
                .groupby(['_agent_short', C_MAIN])\
                .size().reset_index(name='Count')
        fig4 = px.bar(ag_is, x='_agent_short', y='Count',
                      color=C_MAIN, barmode='stack',
                      title=tx['agent_issue'], template=theme)
        fig4.update_layout(height=480, xaxis_tickangle=-30,
                           xaxis_title='Agent',
                           legend=dict(orientation='h',
                                       yanchor='bottom', y=1.01))
        st.plotly_chart(fig4, use_container_width=True)

        # Agent × Department Heatmap
        sec(tx['agent_heatmap'])
        top_d2 = dff[C_DEPT].value_counts().head(12).index.tolist()
        cov = dff[dff[C_AGENT].isin(top_agents) &
                  dff[C_DEPT].isin(top_d2)]\
              .groupby(['_agent_short', C_DEPT])\
              .size().reset_index(name='Count')
        pivot_c = cov.pivot(index='_agent_short',
                            columns=C_DEPT,
                            values='Count').fillna(0)
        fig5 = go.Figure(go.Heatmap(
            z=pivot_c.values,
            x=pivot_c.columns.tolist(),
            y=pivot_c.index.tolist(),
            colorscale='Teal',
            text=pivot_c.values.astype(int),
            texttemplate='%{text}',
            hoverongaps=False
        ))
        fig5.update_layout(title=tx['agent_heatmap'],
                           template=theme, height=520,
                           xaxis_tickangle=-35)
        st.plotly_chart(fig5, use_container_width=True)

# ════════════ TAB 5: RAW DATA ════════════
with tab5:
    sec(tx['raw_explorer'])

    show_df = dff.drop(columns=['_agent_short'], errors='ignore').copy()

    sc1, sc2 = st.columns([1, 3])
    with sc1:
        filter_col = st.selectbox(tx['filter_col'],
                                  [tx['all']] + show_df.columns.tolist())
    with sc2:
        search_term = st.text_input(tx['search'], "")

    if search_term:
        if filter_col == tx['all']:
            mask = show_df.apply(lambda c: c.astype(str).str.contains(
                search_term, case=False, na=False)).any(axis=1)
        else:
            mask = show_df[filter_col].astype(str).str.contains(
                search_term, case=False, na=False)
        show_df = show_df[mask]

    st.markdown(
        f"**{tx['showing']} `{len(show_df):,}` {tx['of']}"
        f" `{len(df):,}` {tx['rows']}**"
    )
    st.dataframe(show_df, use_container_width=True, height=520)

    # Column stats expander
    with st.expander(tx['col_stats']):
        for col in show_df.columns:
            vc = show_df[col].dropna().value_counts()
            st.markdown(f"**{col}** — {len(vc):,} {tx['unique']}")
            st.dataframe(
                vc.head(10).rename('Count').reset_index(),
                use_container_width=True, hide_index=True
            )

    # Download button
    out = io.BytesIO()
    with pd.ExcelWriter(out, engine='openpyxl') as w:
        show_df.to_excel(w, index=False, sheet_name='Data')
    st.download_button(
        label=tx['download'],
        data=out.getvalue(),
        file_name="helpdesk_filtered.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
