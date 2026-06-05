import streamlit as st
st.title("📊 Data Overview")
# -----------------------------
# GET DATA SAFELY
# -----------------------------
df = st.session_state.get("df")

if df is None:
    st.error("❌ No data found. Please upload file in app.py first.")
    st.stop()

# -----------------------------
# DATA INFORMATION
# -----------------------------
st.subheader("📌 Dataset Information")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Rows", df.shape[0])
col2.metric("Columns", df.shape[1])
col3.metric("Missing Values", int(df.isnull().sum().sum()))
col4.metric("Duplicates", int(df.duplicated().sum()))

st.divider()

# -----------------------------
# EXTRA DATA DETAILS
# -----------------------------
st.subheader("📊 Column Details")

st.write("Column Names:")
st.write(list(df.columns))

st.write("Data Types:")
st.write(df.dtypes)

st.write("Basic Description:")
st.dataframe(df.describe(include="all"))

st.divider()

# -----------------------------
# FULL DATA
# -----------------------------
st.subheader("📋 Full Dataset")

st.dataframe(df, use_container_width=True)