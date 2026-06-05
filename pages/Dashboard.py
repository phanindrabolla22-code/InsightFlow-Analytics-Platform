import streamlit as st
import matplotlib.pyplot as plt

st.title("📊 Dashboard - Charts & Graphs")

# -----------------------------
# GET CLEANED DATA
# -----------------------------
df = st.session_state.get("df_clean")

if df is None:
    st.error("❌ No cleaned data found. Please upload + clean data first.")
    st.stop()

# -----------------------------
# NUMERIC COLUMNS ONLY
# -----------------------------
num_cols = df.select_dtypes(include=["int64", "float64"]).columns

if len(num_cols) == 0:
    st.warning("⚠ No numeric columns available for charts")
    st.stop()

# =========================================================
# BAR CHART
# =========================================================
st.subheader("📊 Bar Chart")

bar_col = st.selectbox("Select column for Bar Chart", num_cols, key="bar")

fig1, ax1 = plt.subplots()
df[bar_col].value_counts().head(10).plot(kind="bar", ax=ax1)

st.pyplot(fig1)

st.divider()

# =========================================================
# LINE CHART
# =========================================================
st.subheader("📈 Line Chart")

line_col = st.selectbox("Select column for Line Chart", num_cols, key="line")

fig2, ax2 = plt.subplots()
df[line_col].sort_index().plot(kind="line", ax=ax2)

st.pyplot(fig2)

st.divider()

# =========================================================
# HISTOGRAM
# =========================================================
st.subheader("📊 Histogram")

hist_col = st.selectbox("Select column for Histogram", num_cols, key="hist")

fig3, ax3 = plt.subplots()
df[hist_col].plot(kind="hist", bins=20, ax=ax3)

st.pyplot(fig3)

st.divider()

# =========================================================
# PIE CHART
# =========================================================
st.subheader("🥧 Pie Chart")

pie_col = st.selectbox("Select column for Pie Chart", num_cols, key="pie")

fig4, ax4 = plt.subplots()
df[pie_col].value_counts().head(5).plot(kind="pie", autopct="%1.1f%%", ax=ax4)

st.pyplot(fig4)