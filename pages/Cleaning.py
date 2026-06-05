import streamlit as st
import pandas as pd

st.title("🧹 Smart Data Cleaning")

# -----------------------------
# GET DATA
# -----------------------------
df = st.session_state.get("df")

if df is None:
    st.error("❌ No data found. Please upload file in app.py first")
    st.stop()

# -----------------------------
# ORIGINAL DATA
# -----------------------------
st.subheader("Original Data")
st.dataframe(df)

st.divider()

# =========================================================
# SMART CLEANING
# =========================================================
if st.button("Run Smart Cleaning"):

    clean_df = df.copy()

    for col in clean_df.columns:

        if pd.api.types.is_numeric_dtype(clean_df[col]):

            skew = clean_df[col].skew()

            if abs(skew) > 1:
                clean_df[col] = clean_df[col].fillna(clean_df[col].median())
            else:
                clean_df[col] = clean_df[col].fillna(clean_df[col].mean())

        else:
            if clean_df[col].isnull().sum() > 0:
                clean_df[col] = clean_df[col].fillna(clean_df[col].mode()[0])

    clean_df = clean_df.drop_duplicates()

    st.session_state.df = clean_df
    st.session_state.df_clean = clean_df

    st.success("Smart Cleaning Completed ✔")

# -----------------------------
# CLEANED DATA
# -----------------------------
st.subheader("📊 Cleaned Data")
st.dataframe(st.session_state.get("df_clean", df))

# -----------------------------
# 📥 DOWNLOAD BUTTON
# -----------------------------
st.subheader("📥 Download Cleaned Dataset")

clean_df = st.session_state.get("df_clean")

if clean_df is not None:
    csv = clean_df.to_csv(index=False).encode('utf-8')

    st.download_button(
        label="⬇ Download CSV",
        data=csv,
        file_name="cleaned_data.csv",
        mime="text/csv"
    )
