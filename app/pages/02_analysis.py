import streamlit as st
import pandas as pd
from sqlalchemy import create_engine, text
import plotly.express as px

st.set_page_config(
    page_title="Analysis",
    page_icon="🔍",
    layout="wide"
)

@st.cache_data
def load_data():
    engine = create_engine("sqlite:///churn.db")
    with engine.connect() as conn:
        df = pd.read_sql(text("SELECT * FROM customers"), conn)
    df["totalcharges"] = pd.to_numeric(df["totalcharges"], errors="coerce")
    df = df.dropna(subset=["totalcharges"])
    df["churn_binary"] = (df["churn"] == "Yes").astype(int)
    df["tenure_group"] = pd.cut(
        df["tenure"],
        bins=[0, 12, 24, 48, 60, 72],
        labels=["0-12 mo", "13-24 mo", "25-48 mo", "49-60 mo", "61-72 mo"]
    )
    return df

df = load_data()

# Sidebar filters
st.sidebar.header("🔧 Filters")

gender_filter = st.sidebar.multiselect(
    "Gender", options=df["gender"].unique(),
    default=df["gender"].unique()
)
contract_filter = st.sidebar.multiselect(
    "Contract Type", options=df["contract"].unique(),
    default=df["contract"].unique()
)
internet_filter = st.sidebar.multiselect(
    "Internet Service", options=df["internetservice"].unique(),
    default=df["internetservice"].unique()
)
charge_range = st.sidebar.slider(
    "Monthly Charges ($)",
    float(df["monthlycharges"].min()),
    float(df["monthlycharges"].max()),
    (float(df["monthlycharges"].min()), float(df["monthlycharges"].max()))
)

filtered_df = df[
    (df["gender"].isin(gender_filter)) &
    (df["contract"].isin(contract_filter)) &
    (df["internetservice"].isin(internet_filter)) &
    (df["monthlycharges"].between(charge_range[0], charge_range[1]))
]

# Page
st.title("🔍 Churn Deep Dive Analysis")
st.markdown(f"Analysing **{len(filtered_df):,}** customers")
st.markdown("---")

# Chart 1: Monthly charges histogram
st.subheader("Monthly Charges vs Churn")
fig = px.histogram(
    filtered_df, x="monthlycharges", color="churn",
    nbins=40, barmode="overlay", opacity=0.7,
    color_discrete_map={"Yes": "#e74c3c", "No": "#2ecc71"},
    labels={"monthlycharges": "Monthly Charges ($)", "churn": "Churn"}
)
fig.update_layout(height=360, margin=dict(t=20, b=0))
st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# Chart 2 + 3
col1, col2 = st.columns(2)

with col1:
    st.subheader("Churn Rate by Tenure Group")
    tenure_data = (
        filtered_df.groupby("tenure_group", observed=True)["churn_binary"]
        .mean().reset_index()
    )
    tenure_data["churn_pct"] = (tenure_data["churn_binary"] * 100).round(1)
    fig = px.bar(
        tenure_data, x="tenure_group", y="churn_pct",
        color="churn_pct",
        color_continuous_scale=["#2ecc71", "#e67e22", "#e74c3c"],
        text="churn_pct",
        labels={"tenure_group": "Tenure Group", "churn_pct": "Churn Rate (%)"}
    )
    fig.update_traces(texttemplate="%{text:.1f}%", textposition="outside")
    fig.update_layout(coloraxis_showscale=False, height=360, margin=dict(t=20))
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("Churn Rate by Payment Method")
    pay_data = (
        filtered_df.groupby("paymentmethod")["churn_binary"]
        .mean().reset_index()
    )
    pay_data["churn_pct"] = (pay_data["churn_binary"] * 100).round(1)
    pay_data = pay_data.sort_values("churn_pct", ascending=True)
    fig = px.bar(
        pay_data, x="churn_pct", y="paymentmethod",
        orientation="h",
        color="churn_pct",
        color_continuous_scale=["#2ecc71", "#e74c3c"],
        text="churn_pct",
        labels={"paymentmethod": "", "churn_pct": "Churn Rate (%)"}
    )
    fig.update_traces(texttemplate="%{text:.1f}%", textposition="outside")
    fig.update_layout(coloraxis_showscale=False, height=360, margin=dict(t=20))
    st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# Chart 4: Scatter plot
st.subheader("Tenure vs Monthly Charges — Churn Pattern")
fig = px.scatter(
    filtered_df, x="tenure", y="monthlycharges", color="churn",
    color_discrete_map={"Yes": "#e74c3c", "No": "#2ecc71"},
    opacity=0.5,
    labels={
        "tenure": "Tenure (Months)",
        "monthlycharges": "Monthly Charges ($)",
        "churn": "Churn"
    }
)
fig.update_layout(height=420, margin=dict(t=20, b=0))
st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# High risk table
st.subheader("🚨 High-Risk Customers")
high_risk = filtered_df[
    (filtered_df["churn"] == "No") &
    (filtered_df["contract"] == "Month-to-month") &
    (filtered_df["tenure"] < 12) &
    (filtered_df["monthlycharges"] > 65)
][["customerid", "contract", "tenure",
   "monthlycharges", "internetservice", "paymentmethod"]]\
  .sort_values("monthlycharges", ascending=False)\
  .head(20)

st.markdown(f"**{len(high_risk)} customers** match high-risk criteria")
st.dataframe(high_risk, use_container_width=True)
st.caption("Criteria: Month-to-month · tenure < 12 mo · charges > $65")