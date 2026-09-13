from pathlib import Path
import pandas as pd
import streamlit as st

DATA_PATH = Path(__file__).resolve().parent / "data" / "walmart_retail_data.csv"

# High-contrast colors chosen to remain readable in both light and dark themes.
PLOTLY_COLORS = ["#4C78A8", "#2A9D8F", "#8E6BBE", "#E69F00", "#D55E00", "#0072B2"]

@st.cache_data
def load_data():
    df = pd.read_csv(DATA_PATH)
    df["Order Date"] = pd.to_datetime(df["Order Date"], errors="coerce")
    df["Ship Date"] = pd.to_datetime(df["Ship Date"], errors="coerce")
    df["Year"] = df["Order Date"].dt.year
    df["Month"] = df["Order Date"].dt.to_period("M").dt.to_timestamp()
    return df

def apply_filters(df):
    with st.sidebar:
        st.markdown("### Filters")
        regions = st.multiselect("Region", sorted(df["Region"].dropna().unique()))
        categories = st.multiselect(
            "Product Category", sorted(df["Product Category"].dropna().unique())
        )

    out = df.copy()
    if regions:
        out = out[out["Region"].isin(regions)]
    if categories:
        out = out[out["Product Category"].isin(categories)]
    return out

def setup(title, subtitle):
    st.set_page_config(page_title=title, page_icon="📊", layout="wide")
    st.markdown("""
    <style>
      [data-testid="stSidebar"] { background:#10243f; }
      [data-testid="stSidebar"] * { color:white !important; }
      .block-container { padding-top:1.25rem; }
      .kpi { border:1px solid rgba(120,145,175,.45); border-radius:9px; padding:15px 17px;
             background:rgba(128,150,175,.10); min-height:105px; }
      .kpi-title { color:inherit; font-size:13px; font-weight:600; }
      .kpi-value { color:inherit; font-size:27px; font-weight:700; margin-top:5px; }
      .kpi-sub { color:#2A9D8F; font-size:12px; margin-top:4px; }
    </style>
    """, unsafe_allow_html=True)
    with st.sidebar:
        st.markdown("## 📊 Retail Business")
        st.markdown("### Analytics")
        st.divider()
        st.caption("Use the page navigation to explore the analysis.")
        st.divider()
        st.caption("Data-driven insights for better decisions")
    st.title(title)
    st.caption(subtitle)

def kpi_row(items):
    cols = st.columns(len(items))
    for col, (title, value, sub) in zip(cols, items):
        col.markdown(
            f'<div class="kpi"><div class="kpi-title">{title}</div>'
            f'<div class="kpi-value">{value}</div>'
            f'<div class="kpi-sub">{sub}</div></div>',
            unsafe_allow_html=True,
        )
