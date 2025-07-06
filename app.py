import streamlit as st
import pandas as pd
import altair as alt

# Page configuration
st.set_page_config(page_title="📊 CSV Dashboard Generator", layout="wide")
st.title("📊 CSV Dashboard Generator")
st.markdown("Upload your CSV file from the **sidebar** to instantly explore your data!")

# Required columns for validation
REQUIRED_COLUMNS = ["Date", "Amount", "Category"]

# 🔹 Main Page: Instructions and Sample Download
st.header("📌 How to Prepare Your CSV File")

st.markdown("""
Ensure your file includes the following **three columns**:

- `Date`: e.g., `2024-01-10`  
- `Amount`: e.g., `1000` (in GBP)  
- `Category`: e.g., `Fundraising`, `Operations`, etc.

✅ Format:
- Must be **comma-separated (.csv)**
- Dates must be in **YYYY-MM-DD** format
- No empty rows or unnamed columns

Download an example below:
""")

# Downloadable sample CSV
sample_df = pd.DataFrame({
    "Date": ["2024-01-10", "2024-02-15", "2024-02-25"],
    "Amount": [1000, 500, 1500],
    "Category": ["Fundraising", "Operations", "Programs"]
})
st.download_button("📥 Download Sample CSV", sample_df.to_csv(index=False), file_name="sample.csv", mime="text/csv")

# 🔸 Sidebar: File Upload
with st.sidebar:
    st.header("📂 Upload Your CSV")
    uploaded_file = st.file_uploader("Upload CSV File", type=["csv"])

# 🔍 Data Processing
if uploaded_file:
    try:
        df = pd.read_csv(uploaded_file)

        # Check required columns
        missing_cols = [col for col in REQUIRED_COLUMNS if col not in df.columns]
        if missing_cols:
            st.error(f"❌ Missing required columns: {missing_cols}")
            st.stop()

        # Parse dates
        df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
        df = df.dropna(subset=["Date"])

        # ✅ Success message
        st.success("✅ File loaded successfully!")

        # 🔎 Preview Data
        st.subheader("📋 Data Preview")
        st.dataframe(df)

        # 📊 Summary Metrics
        st.subheader("📊 Summary Metrics")
        st.metric("Total Records", len(df))
        st.metric("Total Amount", f"£{df['Amount'].sum():,.2f}")
        st.metric("Average Amount", f"£{df['Amount'].mean():,.2f}")

        # 📅 Line Chart
        st.subheader("📈 Amount Over Time")
        line_chart = alt.Chart(df).mark_line().encode(
            x="Date:T",
            y="Amount:Q",
            tooltip=["Date", "Amount"]
        ).interactive()
        st.altair_chart(line_chart, use_container_width=True)

        # 📂 Bar Chart
        st.subheader("📊 Category Breakdown")
        bar_chart = alt.Chart(df).mark_bar().encode(
            x="Category:N",
            y="sum(Amount):Q",
            tooltip=["Category", "sum(Amount)"]
        ).interactive()
        st.altair_chart(bar_chart, use_container_width=True)

    except Exception as e:
        st.error(f"❌ Error processing file: {e}")
else:
    st.info("👈 Please upload a valid CSV file using the sidebar.")
