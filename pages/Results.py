import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import io
import zipfile

st.set_page_config(page_title="Data Analyst Dashboard", layout="wide")
st.title("📊 Data Analyst Dashboard - Results & Insights")

# =========================================================
# SAFE DATA LOAD
# =========================================================
df = st.session_state.get("df_clean")

if df is None or not isinstance(df, pd.DataFrame):
    st.info("👉 Please upload and run Smart Cleaning first to see results.")
    st.stop()

# =========================================================
# KPI DASHBOARD
# =========================================================
rows, cols = df.shape
missing = df.isnull().sum().sum()
duplicates = df.duplicated().sum()

col1, col2, col3, col4 = st.columns(4)

col1.metric("Rows", rows)
col2.metric("Columns", cols)
col3.metric("Missing", int(missing))
col4.metric("Duplicates", int(duplicates))

st.divider()

# =========================================================
# DATA QUALITY SCORE
# =========================================================
total_cells = rows * cols
score = round(100 - (missing / total_cells * 100), 2) if total_cells else 0

st.subheader("📊 Data Quality Score")
st.progress(score / 100)
st.metric("Quality Score (%)", score)

st.divider()

# =========================================================
# NUMERIC ANALYSIS
# =========================================================
st.subheader("🔢 Numeric Analysis")

num_df = df.select_dtypes(include=["int64", "float64"])

if not num_df.empty:
    st.dataframe(num_df.describe())

    for col in num_df.columns:
        st.write(
            f"👉 {col} | Mean: {num_df[col].mean():.2f} | "
            f"Median: {num_df[col].median():.2f} | "
            f"Max: {num_df[col].max()} | Min: {num_df[col].min()}"
        )

# =========================================================
# CATEGORICAL ANALYSIS
# =========================================================
st.subheader("🏷️ Categorical Analysis")

cat_df = df.select_dtypes(include=["object"])

if not cat_df.empty:
    for col in cat_df.columns:
        mode_val = df[col].mode()

        st.write(f"📌 {col}")
        st.write("Unique:", df[col].nunique())
        st.write("Top Value:", mode_val[0] if len(mode_val) > 0 else "N/A")

# =========================================================
# VISUALIZATION
# =========================================================
st.subheader("📊 Visual Analytics")

if not num_df.empty:

    colA, colB = st.columns(2)

    with colA:
        st.write("📊 Histogram")
        fig, ax = plt.subplots()
        num_df.iloc[:, 0].plot(kind="hist", bins=20, ax=ax)
        st.pyplot(fig)

    with colB:
        st.write("📊 Bar Chart")
        fig, ax = plt.subplots()
        num_df.iloc[:, 0].value_counts().head(10).plot(kind="bar", ax=ax)
        st.pyplot(fig)

    if num_df.shape[1] > 1:
        st.write("📊 Correlation Heatmap")
        fig, ax = plt.subplots(figsize=(6, 4))
        sns.heatmap(num_df.corr(), annot=True, cmap="coolwarm", ax=ax)
        st.pyplot(fig)

# =========================================================
# INSIGHTS
# =========================================================
st.subheader("🧠 Business Insights")

insights = [
    f"Dataset has {rows} rows and {cols} columns.",
    f"Missing values: {missing}",
    f"Duplicate rows: {duplicates}",
    f"Data Quality Score: {score}%",
]

for i in insights:
    st.write("✔", i)

# =========================================================
# DOWNLOAD REPORT
# =========================================================
st.subheader("📥 Download Full Analyst Report")

zip_buffer = io.BytesIO()

with zipfile.ZipFile(zip_buffer, "w") as z:

    z.writestr("report.txt", "\n".join(insights))

    if not num_df.empty:

        fig, ax = plt.subplots()
        num_df.iloc[:, 0].plot(kind="hist", bins=20, ax=ax)
        buf = io.BytesIO()
        fig.savefig(buf, format="png")
        z.writestr("histogram.png", buf.getvalue())
        plt.close(fig)

        fig, ax = plt.subplots()
        num_df.iloc[:, 0].value_counts().head(10).plot(kind="bar", ax=ax)
        buf = io.BytesIO()
        fig.savefig(buf, format="png")
        z.writestr("bar_chart.png", buf.getvalue())
        plt.close(fig)

        if num_df.shape[1] > 1:
            fig, ax = plt.subplots()
            sns.heatmap(num_df.corr(), annot=True, ax=ax)
            buf = io.BytesIO()
            fig.savefig(buf, format="png")
            z.writestr("heatmap.png", buf.getvalue())
            plt.close(fig)

zip_buffer.seek(0)

st.download_button(
    label="⬇ Download Full Analysis (ZIP)",
    data=zip_buffer,
    file_name="data_analyst_full_report.zip",
    mime="application/zip"
)