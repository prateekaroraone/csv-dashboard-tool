import streamlit as st
import pandas as pd
import altair as alt

# Page settings
st.set_page_config(page_title="📊 CSV Dashboard Generator", layout="wide")
st.title("📊 CSV Dashboard Generator")
st.markdown("Upload your CSV file to get instant summaries, charts, and insights.")

# Define required schema
REQUIRED_COLUMNS = ["Date", "Amount", "Category"]

# Sample download button
with st.sidebar:
    st.header("📥 Sample CSV")
    sample_df = pd.DataFrame({
        "Date": ["2024-01-10", "2024-02-15", "2024-02-25"],
        "Amount": [1000, 500, 1500],
        "Category": ["Fundraising", "Operations", "Programs"]
    })
    st.download_button("Download Sample CSV", sample_df.to_csv(index=False), file_name="sample.csv", mime="text/csv")

# File uploader
uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])

if uploaded_file:
    try:
        df = pd.read_csv(uploaded_file)

        # Check for required columns
        missing_cols = [col for col in REQUIRED_COLUMNS if col not in df.columns]
        if missing_cols:
            st.error(f"Missing required columns: {missing_cols}")
            st.stop()

        # Convert Date column
        df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
        df = df.dropna(subset=["Date"])

        st.success("✅ File loaded successfully!")
        st.subheader("🔎 Data Preview")
        st.dataframe(df)

        # Summary stats
        st.subheader("📈 Summary Statistics")
        st.metric("Total Transactions", len(df))
        st.metric("Total Amount", f"£{df['Amount'].sum():,.2f}")
        st.metric("Average Amount", f"£{df['Amount'].mean():,.2f}")

        # Visualisation: Amount over time
        st.subheader("📅 Amount Over Time")
        line_chart = alt.Chart(df).mark_line().encode(
            x="Date:T",
            y="Amount:Q",
            tooltip=["Date", "Amount"]
        ).interactive()
        st.altair_chart(line_chart, use_container_width=True)

        # Visualisation: Category breakdown
        st.subheader("📊 Spending by Category")
        category_chart = alt.Chart(df).mark_bar().encode(
            x="Category:N",
            y="sum(Amount):Q",
            tooltip=["Category", "sum(Amount)"]
        ).interactive()
        st.altair_chart(category_chart, use_container_width=True)

    except Exception as e:
        st.error(f"❌ Error reading file: {e}")
else:
    st.info("👈 Upload a CSV file to get started.")
