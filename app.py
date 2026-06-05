import streamlit as st
import pandas as pd

st.markdown("""
    <h1 style='text-align:center; color:#4CAF50;'>
        📊 InsightFlow Analytics Platform
    </h1>
    <p style='text-align:center; color:gray;'>
        Smart Data Cleaning • Analytics • Visualization • Insights
    </p>
""", unsafe_allow_html=True)

# -----------------------------
# SESSION INIT
# -----------------------------
if "df" not in st.session_state:
    st.session_state.df = None

# -----------------------------
# UPLOAD FILE
# -----------------------------
uploaded_file = st.file_uploader("📂 Upload CSV or Excel file", type=["csv", "xlsx"])

if uploaded_file is not None:
    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)

    st.session_state.df = df
    st.session_state.df_raw = df
    st.success("File uploaded successfully")

# -----------------------------
# GET DATA
# -----------------------------
df = st.session_state.df

# -----------------------------
# SHOW ONLY ROWS & COLUMNS
# -----------------------------
if df is not None:

    st.subheader("📊 Dataset Info")

    col1, col2 = st.columns(2)

    col1.metric("Rows", df.shape[0])
    col2.metric("Columns", df.shape[1])

else:
    st.info("Please upload a file to see details")
    st.divider()

if df is not None:

    st.subheader("📊 Data Quality Overview")

    col3, col4 = st.columns(2)

    col3.metric("Missing Values", df.isnull().sum().sum())
    col4.metric("Duplicate Rows", df.duplicated().sum())

    st.divider()

    # =====================================================
    # 📋 DATA PREVIEW (FULL VIEW)
    # =====================================================
    st.subheader("📋 Full Dataset Preview")

    st.dataframe(df, use_container_width=True)

    st.divider()

    # =====================================================
    # 📥 DOWNLOAD ORIGINAL DATA
    # =====================================================
    st.subheader("📥 Download Dataset")

    csv = df.to_csv(index=False).encode('utf-8')

    st.download_button(
        label="⬇ Download CSV",
        data=csv,
        file_name="dataset.csv",
        mime="text/csv"
    )

    st.divider()

    # =====================================================
    # 🧠 QUICK INSIGHT
    # =====================================================
    st.subheader("🧠 Quick Insight")

    st.write(f"✔ Total Rows: {df.shape[0]}")
    st.write(f"✔ Total Columns: {df.shape[1]}")
    st.write(f"✔ Memory Usage: {df.memory_usage().sum() / 1024:.2f} KB")