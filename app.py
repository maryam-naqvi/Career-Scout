

import os
import io
import joblib
import pandas as pd
import streamlit as st

try:
    from fpdf import FPDF
    FPDF_AVAILABLE = True
except ImportError:
    FPDF_AVAILABLE = False

# ==============================================================================
# PAGE CONFIG  –  must be the very first Streamlit call
# ==============================================================================

st.set_page_config(
    page_title="CareerScout",
    page_icon=None,
    layout="wide",
    initial_sidebar_state="expanded",
)

# ==============================================================================
# CUSTOM CSS  -  GitHub-style professional dark mode
# ==============================================================================

st.markdown("""
<style>
/* Inter from Google Fonts */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

/* Design tokens - GitHub dark palette */
:root {
    --bg:           #0d1117;
    --bg-card:      #161b22;
    --bg-overlay:   #1c2128;
    --border:       #30363d;
    --border-muted: #21262d;
    --text-primary: #e6edf3;
    --text-secondary:#8b949e;
    --text-disabled:#484f58;
    --accent:       #58a6ff;
    --accent-green: #3fb950;
    --accent-orange:#d29922;
    --accent-red:   #f85149;
    --font:         'Inter', system-ui, -apple-system, sans-serif;
    --radius:       6px;
    --radius-md:    8px;
}

/* Global */
html, body, [class*="css"] {
    font-family: var(--font) !important;
    background-color: var(--bg) !important;
    color: var(--text-primary) !important;
}

.stApp {
    background-color: var(--bg) !important;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background-color: var(--bg-card) !important;
    border-right: 1px solid var(--border) !important;
}
[data-testid="stSidebar"] * {
    color: var(--text-primary) !important;
}

/* Tabs - GitHub underline style */
.stTabs [data-baseweb="tab-list"] {
    background: transparent !important;
    border-bottom: 1px solid var(--border) !important;
    border-radius: 0 !important;
    padding: 0 !important;
    gap: 0 !important;
}
.stTabs [data-baseweb="tab"] {
    background: transparent !important;
    color: var(--text-secondary) !important;
    border-radius: 0 !important;
    font-family: var(--font) !important;
    font-weight: 500 !important;
    font-size: 0.875rem !important;
    padding: 8px 16px !important;
    border: none !important;
    border-bottom: 2px solid transparent !important;
    transition: color 0.15s ease !important;
}
.stTabs [data-baseweb="tab"]:hover {
    color: var(--text-primary) !important;
    border-bottom-color: var(--border) !important;
}
.stTabs [aria-selected="true"] {
    background: transparent !important;
    color: var(--text-primary) !important;
    border-bottom: 2px solid var(--accent) !important;
    font-weight: 600 !important;
}

/* Form inputs */
[data-testid="stSelectbox"] > div > div,
[data-baseweb="select"] > div {
    background: var(--bg-card) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--radius) !important;
    color: var(--text-primary) !important;
    font-family: var(--font) !important;
    font-size: 0.875rem !important;
}
[data-baseweb="select"]:focus-within > div {
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 3px rgba(88, 166, 255, 0.12) !important;
}

/* Primary button */
.stButton > button {
    background: var(--accent) !important;
    color: #0d1117 !important;
    font-family: var(--font) !important;
    font-weight: 600 !important;
    font-size: 0.875rem !important;
    border: 1px solid rgba(88,166,255,0.3) !important;
    border-radius: var(--radius) !important;
    padding: 10px 20px !important;
    width: 100% !important;
    letter-spacing: 0 !important;
    text-transform: none !important;
    transition: background 0.15s ease, opacity 0.15s ease !important;
    box-shadow: none !important;
}
.stButton > button:hover {
    background: #79c0ff !important;
    transform: none !important;
    box-shadow: none !important;
}

/* Download button */
[data-testid="stDownloadButton"] > button {
    background: var(--bg-overlay) !important;
    color: var(--text-primary) !important;
    font-family: var(--font) !important;
    font-weight: 500 !important;
    font-size: 0.875rem !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--radius) !important;
    padding: 10px 20px !important;
    width: 100% !important;
    letter-spacing: 0 !important;
    text-transform: none !important;
    box-shadow: none !important;
    transition: background 0.15s ease !important;
}
[data-testid="stDownloadButton"] > button:hover {
    background: #30363d !important;
    transform: none !important;
    box-shadow: none !important;
}

/* Alert / info boxes */
[data-testid="stAlert"] {
    background: var(--bg-card) !important;
    border-radius: var(--radius) !important;
    border: 1px solid var(--border) !important;
    font-family: var(--font) !important;
}

/* Metric cards */
[data-testid="stMetric"] {
    background: var(--bg-card) !important;
    border: 1px solid var(--border-muted) !important;
    border-radius: var(--radius-md) !important;
    padding: 16px !important;
}
[data-testid="stMetricLabel"] {
    color: var(--text-secondary) !important;
    font-family: var(--font) !important;
    font-size: 0.75rem !important;
    font-weight: 500 !important;
}
[data-testid="stMetricValue"] {
    color: var(--text-primary) !important;
    font-family: var(--font) !important;
    font-size: 1.25rem !important;
    font-weight: 600 !important;
}

/* Slider */
[data-testid="stSlider"] [role="slider"] {
    background: var(--accent) !important;
    border-color: var(--accent) !important;
}

/* Scrollbar */
::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: var(--bg); }
::-webkit-scrollbar-thumb { background: var(--border); border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: #484f58; }

/* Image containers */
[data-testid="stImage"] {
    border-radius: var(--radius-md) !important;
    overflow: hidden !important;
    border: 1px solid var(--border-muted) !important;
}

/* Dataframe */
[data-testid="stDataFrame"] {
    border: 1px solid var(--border-muted) !important;
    border-radius: var(--radius-md) !important;
    overflow: hidden !important;
}
</style>
""", unsafe_allow_html=True)


# ==============================================================================
# DATA & MODEL LOADING  (cached for performance)
# ==============================================================================

@st.cache_data
def load_data() -> pd.DataFrame:
    """Load and return the clean salary dataset."""
    return pd.read_csv("clean_salary_dataset.csv")


@st.cache_resource
def load_model():
    """Load and return the trained RandomForest model."""
    return joblib.load("salary_predictor.pkl")


@st.cache_resource
def load_model_columns() -> list:
    """Load and return the list of encoded feature columns the model expects."""
    return joblib.load("model_columns.pkl")


df            = load_data()
model         = load_model()
model_columns = load_model_columns()

# Pre-compute reusable values
JOB_TITLES     = sorted(df["job_title"].unique().tolist())
EXP_LEVEL_MAP  = {
    "EN - Entry Level":    "EN",
    "MI - Mid Level":      "MI",
    "SE - Senior Level":   "SE",
    "EX - Executive Level":"EX",
}
REMOTE_MAP      = {0: "On-Site (0%)", 50: "Hybrid (50%)", 100: "Fully Remote (100%)"}
REMOTE_MAP_EMOJI = {0: "On-Site (0%)", 50: "Hybrid (50%)", 100: "Fully Remote (100%)"}


# ==============================================================================
# PDF GENERATION
# ==============================================================================

def generate_pdf_report(
    job_title: str,
    experience: str,
    remote_ratio: int,
    predicted_salary: float,
) -> bytes:
    """
    Build a multi-page PDF report with the user's salary prediction on page 1
    and the four market analysis charts on the subsequent pages.
    Returns the PDF as raw bytes for st.download_button.
    """

    if not FPDF_AVAILABLE:
        return b"PDF generation requires fpdf2. Run: pip install fpdf2"

    def safe_text(text: str) -> str:
        """Strip/replace any character outside latin-1 so Helvetica never throws."""
        replacements = {
            "–": "-",   # en dash  –
            "—": "-",   # em dash  —
            "’": "'",   # right single quote
            "‘": "'",   # left single quote
            "“": '"',   # left double quote
            "”": '"',   # right double quote
            "•": "*",   # bullet
            "·": "*",   # middle dot
            "→": "->",  # arrow right
            "←": "<-",  # arrow left
            "×": "x",   # multiplication sign
            "…": "...", # ellipsis
        }
        for char, replacement in replacements.items():
            text = text.replace(char, replacement)
        # Final safety net: encode to latin-1, drop anything that still fails
        return text.encode("latin-1", errors="replace").decode("latin-1")

    class PDF(FPDF):
        def header(self):
            # Dark top bar
            self.set_fill_color(7, 11, 20)
            self.rect(0, 0, 210, 18, "F")
            self.set_font("Helvetica", "B", 9)
            self.set_text_color(0, 212, 180)
            self.set_xy(10, 5)
            self.cell(0, 8, "CAREERSCOUT  -  DATA SCIENCE SALARY INTELLIGENCE", ln=0)
            self.set_text_color(100, 116, 139)
            self.set_font("Helvetica", "", 8)
            self.set_xy(0, 5)
            self.cell(200, 8, "carerescout.ai", ln=0, align="R")

        def footer(self):
            self.set_y(-14)
            self.set_fill_color(7, 11, 20)
            self.rect(0, self.get_y(), 210, 20, "F")
            self.set_font("Helvetica", "", 8)
            self.set_text_color(100, 116, 139)
            self.cell(0, 8, f"Page {self.page_no()}  -  Generated by CareerScout  -  Powered by RandomForest ML", align="C")

    pdf = PDF()
    pdf.set_auto_page_break(auto=True, margin=20)
    pdf.set_margins(left=15, top=22, right=15)

    # ── PAGE 1 : Prediction Report ────────────────────────────────────────────
    pdf.add_page()

    # Hero title block
    pdf.set_fill_color(14, 21, 37)
    pdf.rect(15, 24, 180, 42, "F")
    pdf.set_draw_color(0, 212, 180)
    pdf.set_line_width(0.5)
    pdf.rect(15, 24, 180, 42)
    pdf.set_font("Helvetica", "B", 22)
    pdf.set_text_color(0, 212, 180)
    pdf.set_xy(15, 31)
    pdf.cell(180, 10, safe_text("CareerScout Salary Report"), ln=1, align="C")
    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(100, 116, 139)
    pdf.set_xy(15, 45)
    pdf.cell(180, 8, safe_text("Data Science Market Intelligence  -  2025 Dataset"), ln=1, align="C")

    # Section: Your Profile
    pdf.set_xy(15, 74)
    pdf.set_font("Helvetica", "B", 11)
    pdf.set_text_color(0, 212, 180)
    pdf.cell(0, 8, safe_text("YOUR INPUT PROFILE"), ln=1)
    pdf.set_draw_color(0, 212, 180)
    pdf.set_line_width(0.3)
    pdf.line(15, pdf.get_y(), 195, pdf.get_y())
    pdf.ln(4)

    # Render profile rows properly
    exp_labels = {'EN':'Entry Level','MI':'Mid Level','SE':'Senior Level','EX':'Executive / Director'}
    profile_data = [
        ("Job Title",        safe_text(job_title)),
        ("Experience Level", f"{experience}  -  {exp_labels.get(experience, experience)}"),
        ("Remote Ratio",     f"{remote_ratio}%  -  {REMOTE_MAP.get(remote_ratio, str(remote_ratio))}"),
    ]
    for label, value in profile_data:
        x = pdf.get_x()
        y = pdf.get_y()
        pdf.set_fill_color(11, 17, 30)
        pdf.rect(15, y, 180, 11, "F")
        pdf.set_font("Helvetica", "B", 9)
        pdf.set_text_color(100, 116, 139)
        pdf.set_xy(20, y + 1.5)
        pdf.cell(50, 8, label.upper())
        pdf.set_font("Helvetica", "", 10)
        pdf.set_text_color(226, 232, 240)
        pdf.set_xy(70, y + 1.5)
        pdf.cell(120, 8, value)
        pdf.set_xy(15, y + 12)

    # Predicted Salary hero box
    pdf.ln(10)
    y_salary = pdf.get_y()
    pdf.set_fill_color(7, 11, 20)
    pdf.rect(15, y_salary, 180, 48, "F")
    pdf.set_draw_color(245, 158, 11)
    pdf.set_line_width(1.0)
    pdf.rect(15, y_salary, 180, 48)

    pdf.set_font("Helvetica", "B", 10)
    pdf.set_text_color(100, 116, 139)
    pdf.set_xy(15, y_salary + 8)
    pdf.cell(180, 8, safe_text("PREDICTED ANNUAL SALARY (USD)"), ln=1, align="C")

    pdf.set_font("Helvetica", "B", 34)
    pdf.set_text_color(245, 158, 11)
    pdf.set_xy(15, y_salary + 17)
    pdf.cell(180, 18, safe_text(f"${predicted_salary:,.0f}"), ln=1, align="C")

    pdf.set_font("Helvetica", "", 9)
    pdf.set_text_color(100, 116, 139)
    pdf.set_xy(15, y_salary + 37)
    pdf.cell(180, 8, safe_text("Estimated by RandomForestRegressor trained on 93,392 real-world records"), ln=1, align="C")

    # Confidence range
    pdf.ln(8)
    low  = predicted_salary * 0.85
    high = predicted_salary * 1.15
    pdf.set_font("Helvetica", "B", 10)
    pdf.set_text_color(0, 212, 180)
    pdf.cell(0, 8, safe_text("ESTIMATED MARKET RANGE  (± 15%)"), ln=1)
    pdf.set_line_width(0.3)
    pdf.line(15, pdf.get_y(), 195, pdf.get_y())
    pdf.ln(4)

    range_data = [
        ("Conservative (Low)",  f"${low:,.0f}"),
        ("Predicted (Mid)",     f"${predicted_salary:,.0f}"),
        ("Optimistic (High)",   f"${high:,.0f}"),
    ]
    col_w = 57
    x_start = 18
    for i, (label, val) in enumerate(range_data):
        bx = x_start + i * (col_w + 3)
        by = pdf.get_y()
        fill = (14, 21, 37) if i != 1 else (7, 11, 20)
        border_c = (0, 212, 180) if i == 1 else (30, 45, 69)
        pdf.set_fill_color(*fill)
        pdf.rect(bx, by, col_w, 22, "F")
        pdf.set_draw_color(*border_c)
        pdf.set_line_width(0.5 if i != 1 else 1.0)
        pdf.rect(bx, by, col_w, 22)
        pdf.set_font("Helvetica", "", 7)
        pdf.set_text_color(100, 116, 139)
        pdf.set_xy(bx, by + 3)
        pdf.cell(col_w, 6, safe_text(label), align="C")
        c = (245, 158, 11) if i == 1 else (0, 212, 180)
        pdf.set_font("Helvetica", "B", 11)
        pdf.set_text_color(*c)
        pdf.set_xy(bx, by + 10)
        pdf.cell(col_w, 8, val, align="C")

    # Disclaimer
    pdf.ln(32)
    pdf.set_font("Helvetica", "I", 8)
    pdf.set_text_color(51, 65, 85)
    pdf.multi_cell(
        0, 5,
        safe_text("Disclaimer: This prediction is generated by a machine learning"
                  " model trained on historical data. Actual salaries vary based"
                  " on company, location, negotiation, and individual factors."
                  " Use this as a market reference, not a guarantee."),
    )

    # ── PAGES 2–5 : Market Analysis Charts ───────────────────────────────────
    charts = [
        ("fig1_salary_distribution.png",  "Salary Distribution",           "Distribution of salaries across the dataset after removing outliers (>$500K)."),
        ("fig2_experience_level_count.png","Experience Level Distribution", "Breakdown of the number of professionals at each experience level."),
        ("fig3_top10_jobs.png",            "Top 10 Highest-Paying Roles",   "Average salary by job title - top 10 earners in the data science field."),
        ("fig4_salary_vs_experience.png",  "Salary vs. Experience Level",   "Salary spread by experience level, showing medians, IQR, and outliers."),
    ]

    for img_path, chart_title, chart_desc in charts:
        pdf.add_page()
        pdf.set_font("Helvetica", "B", 14)
        pdf.set_text_color(0, 212, 180)
        pdf.set_xy(15, 26)
        pdf.cell(0, 10, safe_text(f"MARKET ANALYSIS  -  {chart_title.upper()}"), ln=1)
        pdf.set_draw_color(0, 212, 180)
        pdf.set_line_width(0.3)
        pdf.line(15, pdf.get_y(), 195, pdf.get_y())
        pdf.ln(3)
        pdf.set_font("Helvetica", "", 9)
        pdf.set_text_color(100, 116, 139)
        pdf.cell(0, 6, safe_text(chart_desc), ln=1)
        pdf.ln(4)

        if os.path.exists(img_path):
            pdf.image(img_path, x=15, y=pdf.get_y(), w=180)
        else:
            pdf.set_fill_color(14, 21, 37)
            pdf.rect(15, pdf.get_y(), 180, 80, "F")
            pdf.set_font("Helvetica", "I", 10)
            pdf.set_text_color(100, 116, 139)
            pdf.set_xy(15, pdf.get_y() + 36)
            pdf.cell(180, 8, safe_text(f"[Chart file '{img_path}' not found in working directory]"), align="C")

    return bytes(pdf.output())


# ==============================================================================
# SIDEBAR
# ==============================================================================

with st.sidebar:
    # Brand
    st.markdown("""
    <div style="padding: 4px 0 20px 0;">
        <div style="font-family: 'Inter', system-ui, sans-serif; font-size: 1.1rem;
                    font-weight: 700; color: #e6edf3; letter-spacing: -0.01em;">
            CareerScout
        </div>
        <div style="font-size: 0.72rem; color: #484f58; margin-top: 3px; font-weight: 400;">
            Data Science Salary Intelligence
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<hr style="border: none; border-top: 1px solid #21262d; margin: 0 0 16px 0;">', unsafe_allow_html=True)

    # Dataset stats
    st.markdown('<p style="font-size:0.7rem; font-weight:600; color:#484f58; letter-spacing:0.05em; margin-bottom:10px; text-transform:uppercase;">Dataset</p>', unsafe_allow_html=True)
    col_a, col_b = st.columns(2)
    with col_a:
        st.metric("Records",    f"{len(df):,}")
        st.metric("Job Titles", f"{df['job_title'].nunique()}")
    with col_b:
        st.metric("Avg Salary", f"${df['salary_in_usd'].mean():,.0f}")
        st.metric("Countries",  f"{df['company_location'].nunique()}")

    st.markdown('<hr style="border: none; border-top: 1px solid #21262d; margin: 16px 0;">', unsafe_allow_html=True)

    # Experience legend
    st.markdown("""
    <p style="font-size:0.7rem; font-weight:600; color:#484f58; letter-spacing:0.05em;
              margin-bottom:10px; text-transform:uppercase;">Experience Codes</p>
    <table style="width:100%; border-collapse:collapse; font-size:0.8rem; color:#8b949e;">
        <tr><td style="padding:3px 0;"><code style="background:#1c2128; color:#58a6ff; padding:1px 5px; border-radius:3px; font-size:0.72rem;">EN</code></td><td style="padding:3px 8px;">Entry Level</td></tr>
        <tr><td style="padding:3px 0;"><code style="background:#1c2128; color:#58a6ff; padding:1px 5px; border-radius:3px; font-size:0.72rem;">MI</code></td><td style="padding:3px 8px;">Mid Level</td></tr>
        <tr><td style="padding:3px 0;"><code style="background:#1c2128; color:#58a6ff; padding:1px 5px; border-radius:3px; font-size:0.72rem;">SE</code></td><td style="padding:3px 8px;">Senior Level</td></tr>
        <tr><td style="padding:3px 0;"><code style="background:#1c2128; color:#58a6ff; padding:1px 5px; border-radius:3px; font-size:0.72rem;">EX</code></td><td style="padding:3px 8px;">Executive</td></tr>
    </table>
    """, unsafe_allow_html=True)

    st.markdown('<hr style="border: none; border-top: 1px solid #21262d; margin: 16px 0;">', unsafe_allow_html=True)

    # Top 5 roles
    st.markdown('<p style="font-size:0.7rem; font-weight:600; color:#484f58; letter-spacing:0.05em; margin-bottom:10px; text-transform:uppercase;">Top Paying Roles</p>', unsafe_allow_html=True)
    top5 = (
        df.groupby("job_title")["salary_in_usd"]
        .mean()
        .sort_values(ascending=False)
        .head(5)
    )
    for title, sal in top5.items():
        short = title if len(title) <= 24 else title[:22] + "..."
        st.markdown(f"""
        <div style="display:flex; justify-content:space-between; align-items:center;
                    padding:5px 0; border-bottom:1px solid #21262d;">
            <span style="font-size:0.75rem; color:#8b949e; font-family:'Inter',system-ui,sans-serif;">{short}</span>
            <span style="font-size:0.75rem; color:#e6edf3; font-weight:600;
                         font-family:'Inter',system-ui,sans-serif;">${sal:,.0f}</span>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('<br>', unsafe_allow_html=True)
    st.markdown("""
    <div style="font-size:0.7rem; color:#484f58; line-height:1.7;">
        Model: RandomForestRegressor<br>
        Features: 320 encoded columns<br>
        Training set: 74,713 records
    </div>
    """, unsafe_allow_html=True)


# ==============================================================================
# MAIN CONTENT
# ==============================================================================

# ── Page Header ───────────────────────────────────────────────────────────────
st.markdown("""
<div style="padding: 8px 0 24px 0; border-bottom: 1px solid #21262d; margin-bottom: 24px;">
    <h1 style="font-family: 'Inter', system-ui, sans-serif; font-size: 1.5rem;
               font-weight: 700; color: #e6edf3; margin: 0; line-height: 1.3;
               letter-spacing: -0.02em;">
        Data Science Salary Intelligence
    </h1>
    <p style="font-family: 'Inter', system-ui, sans-serif; font-size: 0.8rem;
              color: #8b949e; margin: 6px 0 0 0; font-weight: 400;">
        93,392 records &nbsp;&middot;&nbsp; 317 job titles &nbsp;&middot;&nbsp; RandomForest model
    </p>
</div>
""", unsafe_allow_html=True)

# ── Tabs ──────────────────────────────────────────────────────────────────────
tab_dashboard, tab_predictor = st.tabs(["Market Dashboard", "Salary Predictor"])


# ==============================================================================
# TAB 1 : MARKET DASHBOARD
# ==============================================================================

with tab_dashboard:

    st.markdown('<p style="font-size:0.72rem; font-weight:600; color:#484f58; letter-spacing:0.06em; text-transform:uppercase; margin:0 0 12px 0; padding-bottom:8px; border-bottom:1px solid #21262d;">Market Overview</p>', unsafe_allow_html=True)

    # KPI row
    kpi1, kpi2, kpi3, kpi4, kpi5 = st.columns(5)
    with kpi1:
        st.metric("Median Salary",   f"${df['salary_in_usd'].median():,.0f}")
    with kpi2:
        st.metric("Average Salary",  f"${df['salary_in_usd'].mean():,.0f}")
    with kpi3:
        st.metric("Max Salary",      f"${df['salary_in_usd'].max():,.0f}")
    with kpi4:
        st.metric("Min Salary",      f"${df['salary_in_usd'].min():,.0f}")
    with kpi5:
        remote_pct = (df["remote_ratio"] == 100).mean() * 100
        st.metric("Fully Remote",    f"{remote_pct:.1f}%")

    st.markdown("<br>", unsafe_allow_html=True)

    # Charts row 1
    st.markdown('<p style="font-size:0.72rem; font-weight:600; color:#484f58; letter-spacing:0.06em; text-transform:uppercase; margin:0 0 12px 0; padding-bottom:8px; border-bottom:1px solid #21262d;">Salary & Workforce Distribution</p>', unsafe_allow_html=True)

    chart_col1, chart_col2 = st.columns(2, gap="large")

    with chart_col1:
        st.markdown('<p style="font-size:0.72rem; font-weight:500; color:#484f58; margin-bottom:6px;">Fig 1 - Salary Distribution</p>', unsafe_allow_html=True)
        if os.path.exists("fig1_salary_distribution.png"):
            st.image("fig1_salary_distribution.png", use_container_width=True)
        else:
            st.warning("fig1_salary_distribution.png not found")

    with chart_col2:
        st.markdown('<p style="font-size:0.72rem; font-weight:500; color:#484f58; margin-bottom:6px;">Fig 2 - Experience Level Distribution</p>', unsafe_allow_html=True)
        if os.path.exists("fig2_experience_level_count.png"):
            st.image("fig2_experience_level_count.png", use_container_width=True)
        else:
            st.warning("fig2_experience_level_count.png not found")

    st.markdown("<br>", unsafe_allow_html=True)

    # Charts row 2
    st.markdown('<p style="font-size:0.72rem; font-weight:600; color:#484f58; letter-spacing:0.06em; text-transform:uppercase; margin:0 0 12px 0; padding-bottom:8px; border-bottom:1px solid #21262d;">Role & Experience Analysis</p>', unsafe_allow_html=True)

    chart_col3, chart_col4 = st.columns(2, gap="large")

    with chart_col3:
        st.markdown('<p style="font-size:0.72rem; font-weight:500; color:#484f58; margin-bottom:6px;">Fig 3 - Top 10 Highest-Paying Job Titles</p>', unsafe_allow_html=True)
        if os.path.exists("fig3_top10_jobs.png"):
            st.image("fig3_top10_jobs.png", use_container_width=True)
        else:
            st.warning("fig3_top10_jobs.png not found")

    with chart_col4:
        st.markdown('<p style="font-size:0.72rem; font-weight:500; color:#484f58; margin-bottom:6px;">Fig 4 - Salary Range by Experience Level</p>', unsafe_allow_html=True)
        if os.path.exists("fig4_salary_vs_experience.png"):
            st.image("fig4_salary_vs_experience.png", use_container_width=True)
        else:
            st.warning("fig4_salary_vs_experience.png not found")

    # Bonus: live data table with filters
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<p style="font-size:0.72rem; font-weight:600; color:#484f58; letter-spacing:0.06em; text-transform:uppercase; margin:0 0 12px 0; padding-bottom:8px; border-bottom:1px solid #21262d;">Data Explorer</p>', unsafe_allow_html=True)

    filter_col1, filter_col2, filter_col3 = st.columns(3)
    with filter_col1:
        filter_exp = st.multiselect(
            "Filter by Experience Level",
            options=sorted(df["experience_level"].unique()),
            default=sorted(df["experience_level"].unique()),
        )
    with filter_col2:
        filter_remote = st.multiselect(
            "Filter by Remote Ratio",
            options=sorted(df["remote_ratio"].unique()),
            default=sorted(df["remote_ratio"].unique()),
        )
    with filter_col3:
        salary_range = st.slider(
            "Salary Range (USD)",
            min_value=int(df["salary_in_usd"].min()),
            max_value=int(df["salary_in_usd"].max()),
            value=(int(df["salary_in_usd"].min()), int(df["salary_in_usd"].max())),
            step=5000,
        )

    filtered_df = df[
        df["experience_level"].isin(filter_exp) &
        df["remote_ratio"].isin(filter_remote) &
        df["salary_in_usd"].between(salary_range[0], salary_range[1])
    ][["job_title", "experience_level", "remote_ratio", "salary_in_usd", "company_location", "work_year"]]

    st.caption(f"{len(filtered_df):,} records matching filters")

    st.dataframe(
        filtered_df.sort_values("salary_in_usd", ascending=False).head(200),
        use_container_width=True,
        hide_index=True,
        column_config={
            "salary_in_usd": st.column_config.NumberColumn("Salary (USD)", format="$%d"),
            "remote_ratio":  st.column_config.NumberColumn("Remote %",     format="%d%%"),
        },
    )


# ==============================================================================
# TAB 2 : SALARY PREDICTOR
# ==============================================================================

with tab_predictor:

    pred_left, pred_right = st.columns([1, 1], gap="large")

    # ── LEFT : Input Form ─────────────────────────────────────────────────────
    with pred_left:
        st.markdown('<p style="font-size:0.72rem; font-weight:600; color:#484f58; letter-spacing:0.06em; text-transform:uppercase; margin:0 0 14px 0;">Input Profile</p>', unsafe_allow_html=True)

        # Experience level
        exp_label = st.selectbox(
            "Experience Level",
            options=list(EXP_LEVEL_MAP.keys()),
            index=2,
            help="Select the experience level that best describes your seniority.",
        )
        experience_code = EXP_LEVEL_MAP[exp_label]

        # Job title
        job_title = st.selectbox(
            "Job Title",
            options=JOB_TITLES,
            index=JOB_TITLES.index("Data Scientist") if "Data Scientist" in JOB_TITLES else 0,
            help=f"Choose from {len(JOB_TITLES)} unique job titles in the dataset.",
        )

        # Remote ratio
        remote_ratio = st.select_slider(
            "Work Arrangement",
            options=[0, 50, 100],
            value=100,
            format_func=lambda v: REMOTE_MAP_EMOJI[v],
            help="0 = fully on-site  ·  50 = hybrid  ·  100 = fully remote",
        )

        st.markdown("<br>", unsafe_allow_html=True)

        # Market context for chosen experience level
        avg_for_exp = df[df["experience_level"] == experience_code]["salary_in_usd"].mean()
        avg_for_title = df[df["job_title"] == job_title]["salary_in_usd"].mean()
        median_overall = df["salary_in_usd"].median()

        ctx1, ctx2, ctx3 = st.columns(3)
        with ctx1:
            st.metric(
                f"{experience_code} Avg",
                f"${avg_for_exp:,.0f}",
                help="Average salary for your selected experience level across all jobs.",
            )
        with ctx2:
            st.metric(
                "Role Avg",
                f"${avg_for_title:,.0f}" if not pd.isna(avg_for_title) else "N/A",
                help="Average salary for this specific job title.",
            )
        with ctx3:
            st.metric(
                "Market Median",
                f"${median_overall:,.0f}",
                help="Overall median salary in the dataset.",
            )

        st.markdown("<br>", unsafe_allow_html=True)
        predict_clicked = st.button("Predict Salary", use_container_width=True)

    # ── RIGHT : Results ───────────────────────────────────────────────────────
    with pred_right:
        st.markdown('<p style="font-size:0.72rem; font-weight:600; color:#484f58; letter-spacing:0.06em; text-transform:uppercase; margin:0 0 14px 0;">Prediction Result</p>', unsafe_allow_html=True)

        if not predict_clicked:
            # Placeholder state
            st.markdown("""
            <div style="background:#161b22; border:1px solid #21262d; border-radius:8px;
                        padding:48px 24px; text-align:center; margin-top:8px;">
                <div style="font-size:1.5rem; color:#30363d; margin-bottom:12px; font-weight:300;">&#11835;</div>
                <div style="font-family:'Inter',system-ui,sans-serif; font-size:0.9rem;
                            font-weight:500; color:#484f58; margin-bottom:6px;">
                    No prediction yet
                </div>
                <div style="font-family:'Inter',system-ui,sans-serif; font-size:0.8rem; color:#30363d;">
                    Select your profile and click Predict Salary
                </div>
            </div>
            """, unsafe_allow_html=True)

        else:
            # ── PREDICTION PIPELINE ───────────────────────────────────────────
            with st.spinner("Running model inference..."):

                # 1. Build 1-row input DataFrame
                input_df = pd.DataFrame([{
                    "experience_level": experience_code,
                    "job_title":        job_title,
                    "remote_ratio":     remote_ratio,
                }])

                # 2. Encode categoricals (same transform as training)
                input_encoded = pd.get_dummies(input_df, drop_first=True)

                # 3. Align to the exact column schema the model was trained on
                #    Missing columns → 0, extra columns → dropped
                input_encoded = input_encoded.reindex(columns=model_columns, fill_value=0)

                # 4. Run inference
                predicted_salary = model.predict(input_encoded)[0]

            # ── RESULT DISPLAY ─────────────────────────────────────────────────
            low   = predicted_salary * 0.85
            high  = predicted_salary * 1.15

            # Main salary card
            st.markdown(f"""
            <div style="background:#161b22; border:1px solid #30363d; border-radius:8px;
                        padding:28px 24px; text-align:center; margin-bottom:12px;">
                <div style="font-family:'Inter',system-ui,sans-serif; font-size:0.72rem;
                            font-weight:500; color:#8b949e; letter-spacing:0.05em;
                            text-transform:uppercase; margin-bottom:10px;">
                    Predicted Annual Salary
                </div>
                <div style="font-family:'Inter',system-ui,sans-serif; font-size:2.4rem;
                            font-weight:700; color:#e6edf3; line-height:1;
                            letter-spacing:-0.02em; margin-bottom:4px;">
                    ${predicted_salary:,.0f}
                </div>
                <div style="font-size:0.75rem; color:#484f58;">USD per year</div>
            </div>
            """, unsafe_allow_html=True)

            # Range cards
            r1, r2, r3 = st.columns(3)
            for col, label, val, is_mid in [
                (r1, "Low (-15%)",  low,              False),
                (r2, "Predicted",   predicted_salary, True),
                (r3, "High (+15%)", high,             False),
            ]:
                with col:
                    border = "#58a6ff" if is_mid else "#21262d"
                    val_color = "#e6edf3" if is_mid else "#8b949e"
                    st.markdown(f"""
                    <div style="background:#161b22; border:1px solid {border};
                                border-radius:6px; padding:12px 8px; text-align:center;">
                        <div style="font-size:0.65rem; font-weight:500; color:#484f58;
                                    text-transform:uppercase; letter-spacing:0.04em; margin-bottom:5px;">
                            {label}
                        </div>
                        <div style="font-size:0.95rem; font-weight:600; color:{val_color};
                                    font-family:'Inter',system-ui,sans-serif;">
                            ${val:,.0f}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)

            # Market comparison bar
            market_avg = df["salary_in_usd"].mean()
            pct_vs_market = ((predicted_salary - market_avg) / market_avg) * 100
            direction     = "above" if pct_vs_market >= 0 else "below"
            badge_color   = "#3fb950" if pct_vs_market >= 0 else "#f85149"
            arrow         = "+" if pct_vs_market >= 0 else "-"

            badge_bg = "#1a2b1f" if pct_vs_market >= 0 else "#2b1a1f"
            st.markdown(f"""
            <div style="background:#161b22; border:1px solid #21262d; border-radius:6px;
                        padding:14px 16px; margin-bottom:12px; display:flex;
                        align-items:center; gap:12px;">
                <span style="display:inline-block; background:{badge_bg}; color:{badge_color};
                             font-size:0.8rem; font-weight:600; padding:3px 10px;
                             border-radius:4px; white-space:nowrap;">
                    {arrow} {abs(pct_vs_market):.1f}% vs market
                </span>
                <span style="font-size:0.8rem; color:#8b949e;">
                    {direction} market average of ${market_avg:,.0f}
                </span>
            </div>
            """, unsafe_allow_html=True)

            # Input summary card
            exp_display = exp_label.split(" - ")[1].strip() if " - " in exp_label else exp_label
            st.markdown(f"""
            <div style="background:#161b22; border:1px solid #21262d; border-radius:6px;
                        padding:14px 16px; margin-bottom:14px;">
                <p style="font-size:0.65rem; font-weight:600; color:#484f58;
                          letter-spacing:0.05em; text-transform:uppercase; margin:0 0 10px 0;">
                    Input Summary
                </p>
                <table style="width:100%; border-collapse:collapse; font-size:0.8rem;">
                    <tr><td style="color:#484f58; padding:3px 0; width:80px;">Role</td>
                        <td style="color:#e6edf3;">{job_title}</td></tr>
                    <tr><td style="color:#484f58; padding:3px 0;">Level</td>
                        <td style="color:#e6edf3;">{experience_code} &mdash; {exp_display}</td></tr>
                    <tr><td style="color:#484f58; padding:3px 0;">Remote</td>
                        <td style="color:#e6edf3;">{REMOTE_MAP[remote_ratio]}</td></tr>
                </table>
            </div>
            """, unsafe_allow_html=True)

            # PDF download
            if not FPDF_AVAILABLE:
                st.warning("PDF export requires fpdf2. Install it with: pip install fpdf2")
            else:
                pdf_bytes = generate_pdf_report(
                job_title        = job_title,
                experience       = experience_code,
                remote_ratio     = remote_ratio,
                predicted_salary = predicted_salary,
            )

                st.download_button(
                    label="Download PDF Report",
                    data=pdf_bytes,
                    file_name="CareerScout_Report.pdf",
                    mime="application/pdf",
                    use_container_width=True,
                )