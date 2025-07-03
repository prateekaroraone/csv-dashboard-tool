import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Charity CSV Dashboard", layout="wide")
st.title("📊 Charity Donation Dashboard")

uploaded_file = st.file_uploader("Upload your donation CSV", type="csv")

if uploaded_file:
    df = pd.read_csv(uploaded_file, parse_dates=["Date"])

    st.subheader("Raw Data")
    st.dataframe(df) 

    st.subheader("Key Metrics")
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Raised", f"£{df['Amount'].sum():,.2f}")
    col2.metric("Unique Donors", df['Donor'].nunique())
    col3.metric("Campaigns", df['Campaign'].nunique())

    st.subheader("Monthly Donations")
    df["Month"] = df["Date"].dt.to_period("M").astype(str)
    monthly = df.groupby("Month")["Amount"].sum().reset_index()
    fig = px.bar(monthly, x="Month", y="Amount", title="Donations Over Time", labels={"Amount": "£ Raised"})
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Top Donors")
    top_donors = df.groupby("Donor")["Amount"].sum().reset_index().sort_values(by="Amount", ascending=False)
    st.dataframe(top_donors.head(5))

    st.subheader("Donations by Campaign")
    fig2 = px.pie(df, names="Campaign", values="Amount", title="Donations by Campaign")
    st.plotly_chart(fig2, use_container_width=True)

else:
    st.info("👆 Upload a CSV file to get started.")
