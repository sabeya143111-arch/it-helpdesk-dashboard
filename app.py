# ================================================================
#   IT HELPDESK ANALYTICS — ACCURATE FULL DATA EDITION
#   Uses sheet "Data" (full 5,987 tickets) — No row lost
# ================================================================

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import io, os, requests
from datetime import datetime

from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Table, TableStyle,
    Paragraph, Spacer, PageBreak, Image, HRFlowable
)
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# Arabic helpers
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

# -------------------------------------------------
# CONSTANTS (based on your Data sheet) [file:56]
# -------------------------------------------------
C_ID     = "رقم البلاغ"
C_STATUS = "الحالة"
C_CLIENT = "العميل"
C_DEPT   = "إدارة العميل"
C_SUMMARY = "ملخص البلاغ"
C_SVC    = "الخدمة"
C_MAIN   = "التصنيف الرئيسي"
C_SUB    = "التصنيف الفرعي"
C_IMPACT = "التأثير"
C_PRIORITY = "الأهمية"
C_AGENT  = "مسند الى"
C_CREATED = "تاريخ الإنشاء"
C_CLOSED  = "تاريخ ووقت الاغلاق"

# -------------------------------------------------
# Arabic fonts loader
# -------------------------------------------------
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
            "https://fonts.gstatic.com/s/amiri/v27/J7acnpd8CGxBHqUpvrIwGJBEoRdI.ttf",
        ],
    }
    for font_name, urls in font_urls.items():
        path = f"/tmp/{font_name}.ttf"
        if not os.path.exists(path):
            for url in urls:
                try:
                    r = requests.get(url, timeout=15)
                    if r.status_code == 200:
                        open(path, "wb").write(r.content)
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
FONT_OK = FONTS.get("Amiri-Regular", False)
AR_FONT = "Amiri-Regular" if FONT_OK else "Helvetica"
AR_FONT_BOLD = "Amiri-Bold" if FONTS.get("Amiri-Bold", False) else "Helvetica-Bold"

def ar(text, max_len=None):
    """Arabic reshape + bidi + optional truncate."""
    t = str(text).strip()
    if not t or t in ["nan", "None"]:
        return ""
    if max_len and len(t) > max_len:
        t = t[:max_len - 2] + ".."
    if ARABIC_SUPPORT and any("\u0600" <= c <= "\u06FF" for c in t):
        try:
            return get_display(reshape(t))
        except:
            return t
    return t

# -------------------------------------------------
# Simple dark theme CSS (short) 
# -------------------------------------------------
st.markdown("""
<style>
.stApp {background:#050816;}
.main .block-container {padding-top:1rem;max-width:1200px;}
[data-testid="stSidebar"] {background:#0d1117;border-right:1px solid #30363d;}
</style>
""", unsafe_allow_html=True)

# -------------------------------------------------
# Sidebar
# -------------------------------------------------
with st.sidebar:
    st.markdown("### 🖥️ IT Helpdesk Analytics")
    st.markdown(
        f"<small style='color:{'#3fb950' if FONT_OK else '#d29922'}'>"
        f"{'Arabic font: OK' if FONT_OK else 'Arabic font: loading / fallback'}</small>",
        unsafe_allow_html=True
    )
    uploaded = st.file_uploader("📂 Upload Excel (Data sheet)", type=["xlsx", "xls"])
    pdf_lang = st.radio("🌐 PDF Language", ["English", "العربية"], horizontal=True)

if not uploaded:
    st.info("Excel upload karo (sheet name = **Data**).")
    st.stop()

# -------------------------------------------------
# Data load – ALWAYS from sheet 'Data' [file:56]
# -------------------------------------------------
@st.cache_data(show_spinner="📥 Loading data (Data sheet)...")
def load_data(rb: bytes):
    df = pd.read_excel(io.BytesIO(rb), sheet_name="Data", header=0)

    # Keep only relevant columns
    keep = [c for c in [
        C_ID, C_STATUS, C_CLIENT, C_DEPT, C_SUMMARY,
        C_SVC, C_MAIN, C_SUB, C_IMPACT, C_PRIORITY,
        C_AGENT, C_CREATED, C_CLOSED
    ] if c in df.columns]
    df = df[keep].copy()

    # Agent clean
    if C_AGENT in df.columns:
        df[C_AGENT] = df[C_AGENT].astype(str).str.strip()
        df[C_AGENT] = df[C_AGENT].replace(
            {"nan": pd.NA, "Agent": pd.NA, "مسند الى": pd.NA, "": pd.NA}
        )

    # Short agent (without "−متعاقد")
    if C_AGENT in df.columns:
        df["_AgentShort"] = (
            df[C_AGENT]
            .str.replace("−متعاقد", "", regex=False)
            .str.replace("-متعاقد", "", regex=False)
            .str.strip()
        )
    else:
        df["_AgentShort"] = pd.NA

    # Convert dates (best effort)
    for col in [C_CREATED, C_CLOSED]:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors="coerce")

    df.dropna(how="all", inplace=True)
    df.reset_index(drop=True, inplace=True)

    acc = {
        "total": len(df),
        "dept_fill": round(df[C_DEPT].notna().sum() / len(df) * 100, 1) if C_DEPT in df.columns else 0,
        "svc_fill": round(df[C_SVC].notna().sum() / len(df) * 100, 1) if C_SVC in df.columns else 0,
        "main_fill": round(df[C_MAIN].notna().sum() / len(df) * 100, 1) if C_MAIN in df.columns else 0,
        "agent_fill": round(df[C_AGENT].notna().sum() / len(df) * 100, 1) if C_AGENT in df.columns else 0,
    }
    return df, acc

rb = uploaded.read()
df, acc = load_data(rb)

# yahan tumhe 5987 records dekhne chahiye
total_rows = len(df)

st.markdown(f"**File:** `{uploaded.name}` — **Records (Data sheet):** `{total_rows}`")

# -------------------------------------------------
# Filters (on top of full df)
# -------------------------------------------------
with st.expander("🔎 Filters", expanded=False):
    c1, c2, c3 = st.columns(3)
    ALL = "All"

    with c1:
        vals = [ALL] + sorted(df[C_DEPT].dropna().unique().tolist()) if C_DEPT in df.columns else [ALL]
        f_dept = st.selectbox("Department (إدارة العميل)", vals)
    with c2:
        vals = [ALL] + sorted(df[C_SVC].dropna().unique().tolist()) if C_SVC in df.columns else [ALL]
        f_svc = st.selectbox("Service (الخدمة)", vals)
    with c3:
        vals = [ALL] + sorted(df[C_MAIN].dropna().unique().tolist()) if C_MAIN in df.columns else [ALL]
        f_main = st.selectbox("Main Category (التصنيف الرئيسي)", vals)

dff = df.copy()
if f_dept != ALL and C_DEPT in dff.columns:
    dff = dff[dff[C_DEPT] == f_dept]
if f_svc != ALL and C_SVC in dff.columns:
    dff = dff[dff[C_SVC] == f_svc]
if f_main != ALL and C_MAIN in dff.columns:
    dff = dff[dff[C_MAIN] == f_main]

filtered = len(dff) < len(df)

# -------------------------------------------------
# KPIs
# -------------------------------------------------
st.subheader("📊 Overview (Full Data Accurate)")

c1, c2, c3, c4 = st.columns(4)
with c1:
    st.metric("Total Tickets (Data sheet)", total_rows)
with c2:
    st.metric("Shown after filters", len(dff))
with c3:
    st.metric("Departments", dff[C_DEPT].nunique() if C_DEPT in dff.columns else 0)
with c4:
    st.metric("Agents", dff[C_AGENT].dropna().nunique() if C_AGENT in dff.columns else 0)

# -------------------------------------------------
# Charts (on filtered data)
# -------------------------------------------------
top_n = st.slider("Top N for charts", 5, 30, 15)

c1, c2 = st.columns(2)
if C_MAIN in dff.columns:
    with c1:
        st.markdown("#### 🔥 Top Issue Categories")
        d = dff[C_MAIN].value_counts().head(top_n).reset_index()
        d.columns = ["Issue", "Count"]
        fig = px.bar(d, x="Count", y="Issue", orientation="h",
                     text="Count", color="Count", color_continuous_scale="Reds")
        fig.update_layout(yaxis={"categoryorder": "total ascending"},
                          showlegend=False, height=400)
        st.plotly_chart(fig, use_container_width=True)

if C_DEPT in dff.columns:
    with c2:
        st.markdown("#### 🏢 Top Departments")
        d = dff[C_DEPT].value_counts().head(top_n).reset_index()
        d.columns = ["Department", "Tickets"]
        fig = px.bar(d, x="Tickets", y="Department", orientation="h",
                     text="Tickets", color="Tickets", color_continuous_scale="Blues")
        fig.update_layout(yaxis={"categoryorder": "total ascending"},
                          showlegend=False, height=400)
        st.plotly_chart(fig, use_container_width=True)

if C_AGENT in dff.columns:
    st.markdown("#### 👨‍💻 Top Agents (by ticket volume)")
    ag = (dff.dropna(subset=[C_AGENT])
            .groupby([C_AGENT, "_AgentShort"]).size()
            .reset_index(name="Tickets")
            .sort_values("Tickets", ascending=False)
            .head(top_n))
    fig = px.bar(ag, x="Tickets", y="_AgentShort", orientation="h",
                 text="Tickets", color="Tickets", color_continuous_scale="Viridis")
    fig.update_layout(yaxis={"categoryorder": "total ascending"},
                      showlegend=False, height=450)
    st.plotly_chart(fig, use_container_width=True)

# -------------------------------------------------
# Helper: fig → PNG for PDF
# -------------------------------------------------
def fig_to_png(fig, w=900, h=420):
    try:
        return fig.to_image(format="png", width=w, height=h, scale=2)
    except Exception:
        return None

# -------------------------------------------------
# PDF generator — full accurate data (df_full passed)
# -------------------------------------------------
def generate_pdf(df_data, stats, language="English", filename="report.pdf"):
    buffer = io.BytesIO()
    total = len(df_data)
    is_ar = (language == "العربية")

    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        rightMargin=0.75 * inch,
        leftMargin=0.75 * inch,
        topMargin=0.75 * inch,
        bottomMargin=0.6 * inch,
    )
    story = []

    PRIMARY = colors.HexColor("#1f6feb")
    ACCENT = colors.HexColor("#58a6ff")
    DANGER = colors.HexColor("#f85149")
    SUCCESS = colors.HexColor("#3fb950")
    BG = colors.HexColor("#f6f8fa")
    WHITE = colors.white

    base_font = AR_FONT if is_ar else "Helvetica"
    bold_font = AR_FONT_BOLD if is_ar else "Helvetica-Bold"
    leading_mul = 1.8 if is_ar else 1.3

    cover_title = ParagraphStyle(
        "CT",
        fontSize=28,
        textColor=PRIMARY,
        alignment=TA_CENTER,
        fontName=bold_font,
        leading=28 * leading_mul,
        spaceAfter=14,
    )
    cover_sub = ParagraphStyle(
        "CS",
        fontSize=14,
        textColor=ACCENT,
        alignment=TA_CENTER,
        fontName=base_font,
        leading=14 * leading_mul,
        spaceAfter=10,
    )
    body = ParagraphStyle(
        "BD",
        fontSize=10,
        textColor=colors.HexColor("#24292f"),
        alignment=TA_RIGHT if is_ar else TA_JUSTIFY,
        fontName=base_font,
        leading=10 * leading_mul,
        spaceBefore=6,
        spaceAfter=6,
    )
    h1 = ParagraphStyle(
        "H1",
        fontSize=16,
        textColor=PRIMARY,
        fontName=bold_font,
        leading=16 * leading_mul,
        spaceBefore=16,
        spaceAfter=10,
        alignment=TA_RIGHT if is_ar else TA_LEFT,
    )
    h2 = ParagraphStyle(
        "H2",
        fontSize=13,
        textColor=ACCENT,
        fontName=bold_font,
        leading=13 * leading_mul,
        spaceBefore=12,
        spaceAfter=8,
        alignment=TA_RIGHT if is_ar else TA_LEFT,
    )
    footer = ParagraphStyle(
        "FT",
        fontSize=8,
        textColor=colors.HexColor("#6e7681"),
        alignment=TA_CENTER,
        fontName="Helvetica",
        leading=11,
    )

    def tbl(data, widths, hdr_color):
        processed = []
        for row in data:
            r2 = []
            for cell in row:
                s = str(cell)
                if is_ar and any("\u0600" <= c <= "\u06FF" for c in s):
                    r2.append(ar(s, max_len=50))
                else:
                    r2.append(s[:50] if len(s) > 50 else s)
            processed.append(r2)
        t = Table(processed, colWidths=widths, repeatRows=1)
        t.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, 0), hdr_color),
                    ("TEXTCOLOR", (0, 0), (-1, 0), WHITE),
                    ("FONTNAME", (0, 0), (-1, 0), bold_font),
                    ("FONTSIZE", (0, 0), (-1, 0), 9),
                    ("FONTNAME", (0, 1), (-1, -1), base_font),
                    ("FONTSIZE", (0, 1), (-1, -1), 8.5),
                    ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#d0d7de")),
                    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                    ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                    ("LEFTPADDING", (0, 0), (-1, -1), 6),
                    ("RIGHTPADDING", (0, 0), (-1, -1), 6),
                    ("TOPPADDING", (0, 0), (-1, 0), 10),
                    ("BOTTOMPADDING", (0, 0), (-1, 0), 10),
                    ("TOPPADDING", (0, 1), (-1, -1), 8 if is_ar else 6),
                    ("BOTTOMPADDING", (0, 1), (-1, -1), 8 if is_ar else 6),
                ]
            )
        )
        return t

    # Cover
    story.append(Spacer(1, 0.8 * inch))
    story.append(
        Paragraph(
            ar("تحليلات مكتب الدعم التقني") if is_ar else "IT HELP DESK ANALYTICS",
            cover_title,
        )
    )
    story.append(
        Paragraph(
            ar("تقرير الأداء الشامل") if is_ar else "COMPREHENSIVE PERFORMANCE REPORT",
            cover_sub,
        )
    )
    story.append(Spacer(1, 0.3 * inch))
    story.append(
        HRFlowable(width="50%", thickness=2, color=PRIMARY, spaceBefore=6, spaceAfter=14)
    )

    now = datetime.now()
    meta_lines = [
        f"Report Date: {now.strftime('%B %d, %Y')}",
        f"Generated: {now.strftime('%I:%M %p')}",
        f"Total Tickets (Data sheet): {total}",
        f"Source File: {uploaded.name}",
    ]
    for line in meta_lines:
        story.append(Paragraph(line, footer))

    story.append(Spacer(1, 0.6 * inch))
    story.append(
        Paragraph(
            ar(
                f"هذا التقرير يعتمد على جميع السجلات الموجودة في ورقة البيانات دون أي استبعاد لضمان دقة التحليل."
            )
            if is_ar
            else "This report is based on all records from the Data sheet with no exclusions, ensuring fully accurate analysis.",
            body,
        )
    )
    story.append(PageBreak())

    # KPIs
    story.append(
        Paragraph(
            ar("مؤشرات الأداء الرئيسية") if is_ar else "KEY PERFORMANCE INDICATORS", h1
        )
    )
    story.append(Spacer(1, 0.1 * inch))

    kpi_data = [
        [ar("المؤشر") if is_ar else "Metric",
         ar("القيمة") if is_ar else "Value"],
        [ar("إجمالي التذاكر") if is_ar else "Total Tickets", f"{total}"],
        [ar("الإدارات") if is_ar else "Departments",
         f"{df_data[C_DEPT].nunique() if C_DEPT in df_data.columns else 0}"],
        [ar("الخدمات") if is_ar else "Service Types",
         f"{df_data[C_SVC].nunique() if C_SVC in df_data.columns else 0}"],
        [ar("فئات المشكلات") if is_ar else "Issue Categories",
         f"{df_data[C_MAIN].nunique() if C_MAIN in df_data.columns else 0}"],
        [ar("عدد الموظفين") if is_ar else "Agents",
         f"{df_data[C_AGENT].dropna().nunique() if C_AGENT in df_data.columns else 0}"],
    ]
    story.append(tbl(kpi_data, [3.2 * inch, 3.2 * inch], PRIMARY))
    story.append(PageBreak())

    # Top issues table
    story.append(
        Paragraph(
            ar("أعلى فئات المشكلات") if is_ar else "TOP ISSUE CATEGORIES", h2
        )
    )
    if C_MAIN in df_data.columns:
        vc = df_data[C_MAIN].value_counts().head(20)
        rows = [[ar("فئة المشكلة") if is_ar else "Issue Category",
                 ar("العدد") if is_ar else "Count"]]
        for name, cnt in vc.items():
            rows.append([ar(name, max_len=50), str(int(cnt))])
        story.append(tbl(rows, [4.2 * inch, 2.2 * inch], DANGER))
    story.append(PageBreak())

    # Top departments table
    story.append(
        Paragraph(
            ar("أعلى الإدارات حملاً") if is_ar else "TOP DEPARTMENTS", h2
        )
    )
    if C_DEPT in df_data.columns:
        vc = df_data[C_DEPT].value_counts().head(20)
        rows = [[ar("الإدارة") if is_ar else "Department",
                 ar("التذاكر") if is_ar else "Tickets"]]
        for name, cnt in vc.items():
            rows.append([ar(name, max_len=50), str(int(cnt))])
        story.append(tbl(rows, [4.2 * inch, 2.2 * inch], ACCENT))
    story.append(PageBreak())

    # Agents table
    if C_AGENT in df_data.columns:
        story.append(
            Paragraph(
                ar("أداء الموظفين") if is_ar else "AGENT PERFORMANCE", h2
            )
        )
        vc = df_data[C_AGENT].dropna().value_counts().head(25)
        rows = [[ar("الموظف") if is_ar else "Agent",
                 ar("التذاكر") if is_ar else "Tickets"]]
        for name, cnt in vc.items():
            rows.append([ar(name, max_len=50), str(int(cnt))])
        story.append(tbl(rows, [4.2 * inch, 2.2 * inch], SUCCESS))

    # Footer
    story.append(Spacer(1, 0.5 * inch))
    story.append(
        HRFlowable(width="100%", thickness=0.5, color=colors.HexColor("#d0d7de"))
    )
    story.append(
        Paragraph(
            f"IT Helpdesk Analytics • {now.strftime('%B %Y')} • Generated by Streamlit",
            footer,
        )
    )

    doc.build(story)
    buffer.seek(0)
    return buffer

# -------------------------------------------------
# PDF Export (IMPORTANT: use FULL df, not filtered)
# -------------------------------------------------
st.markdown("---")
st.subheader("📄 Export Full Accurate PDF (All 5,987 tickets)")

col1, col2 = st.columns([2, 1])
with col1:
    st.write(
        "PDF mein **poora Data sheet** (jitne bhi tickets hai, e.g. 5,987) ka summary jaayega, "
        "koi row filter se drop nahi hogi."
    )

with col2:
    if st.button("📥 Generate PDF (Full Data)", type="primary", use_container_width=True):
        with st.spinner(f"Generating {pdf_lang} PDF from full Data sheet…"):
            buf = generate_pdf(df, acc, pdf_lang)
        st.success("PDF ready — niche se download karo.")
        st.download_button(
            label=f"⬇️ Download {pdf_lang} PDF",
            data=buf,
            file_name=f"IT_Helpdesk_Full_{pdf_lang}_{datetime.now().strftime('%Y%m%d_%H%M')}.pdf",
            mime="application/pdf",
            use_container_width=True,
        )
