import streamlit as st

st.title("📊 Insights Dashboard")

# -----------------------------
# GET CLEANED DATA
# -----------------------------
df = st.session_state.get("df_clean")

if df is None:
    st.error("❌ No cleaned data found. Please upload + clean first.")
    st.stop()

# =========================================================
# BASIC INFO
# =========================================================
st.subheader("📌 Dataset Overview")

st.write(f"📊 Total Rows: {df.shape[0]}")
st.write(f"📊 Total Columns: {df.shape[1]}")

missing = df.isnull().sum().sum()
st.write(f"❗ Missing Values: {missing}")

duplicates = df.duplicated().sum()
st.write(f"🔁 Duplicate Rows: {duplicates}")

st.divider()

# =========================================================
# COLUMN TYPES
# =========================================================
st.subheader("📊 Column Types")

st.write(df.dtypes)

st.divider()

# =========================================================
# NUMERIC INSIGHTS
# =========================================================
num_df = df.select_dtypes(include=["int64", "float64"])

if len(num_df.columns) > 0:
    st.subheader("🔢 Numeric Insights")

    st.write("📈 Statistical Summary")
    st.dataframe(num_df.describe())

    st.write("📊 Highest Value Columns")

    for col in num_df.columns:
        st.write(f"👉 {col} max: {num_df[col].max()} | min: {num_df[col].min()}")

else:
    st.warning("No numeric columns found")

st.divider()

# =========================================================
# CATEGORICAL INSIGHTS
# =========================================================
cat_df = df.select_dtypes(include=["object"])

if len(cat_df.columns) > 0:
    st.subheader("🏷️ Categorical Insights")

    for col in cat_df.columns:
        mode_val = df[col].mode()

        st.write(f"📌 Column: {col}")
        st.write(f"- Unique values: {df[col].nunique()}")
        st.write(f"- Most common: {mode_val[0] if len(mode_val) > 0 else 'N/A'}")
        st.write("")

else:
    st.warning("No categorical columns found")

st.divider()

# =========================================================
# FINAL SUMMARY
# =========================================================
st.subheader("🧠 Auto Summary")

summary = []

summary.append(f"This dataset contains {df.shape[0]} rows and {df.shape[1]} columns.")

if missing > 0:
    summary.append(f"There are {missing} missing values that may need attention.")
else:
    summary.append("No missing values found in the dataset.")

if duplicates > 0:
    summary.append(f"There are {duplicates} duplicate rows that should be reviewed.")
else:
    summary.append("No duplicate rows detected.")

if len(num_df.columns) > 0:
    summary.append("Numeric data is available for statistical analysis and visualization.")

if len(cat_df.columns) > 0:
    summary.append("Categorical data is available for grouping and segmentation.")

for line in summary:
    st.write("• " + line)