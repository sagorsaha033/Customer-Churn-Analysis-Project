import streamlit as st
import pandas as pd
from sqlalchemy import create_engine, text
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(
    page_title="Overview",
    page_icon="📊",
    layout="wide"
)

# Load data
@st.cache_data
def load_data():
    engine = create_engine("sqlite:///churn.db")
    with engine.connect() as conn:
        df = pd.read_sql(text("SELECT * FROM customers"), conn)
    df["totalcharges"] = pd.to_numeric(df["totalcharges"], errors="coerce")
    df = df.dropna(subset=["totalcharges"])
    df["churn_binary"] = (df["churn"] == "Yes").astype(int)
    return df

df = load_data()

# Sidebar filters
st.sidebar.header("🔧 Filters")

gender_filter = st.sidebar.multiselect(
    "Gender",
    options=df["gender"].unique(),
    default=df["gender"].unique()
)
contract_filter = st.sidebar.multiselect(
    "Contract Type",
    options=df["contract"].unique(),
    default=df["contract"].unique()
)
internet_filter = st.sidebar.multiselect(
    "Internet Service",
    options=df["internetservice"].unique(),
    default=df["internetservice"].unique()
)

filtered_df = df[
    (df["gender"].isin(gender_filter)) &
    (df["contract"].isin(contract_filter)) &
    (df["internetservice"].isin(internet_filter))
]

# Page title
st.title("📊 Churn Overview")
st.markdown(f"Showing **{len(filtered_df):,}** customers")
st.markdown("---")

# KPI Cards
churned      = filtered_df[filtered_df["churn"] == "Yes"]
retained     = filtered_df[filtered_df["churn"] == "No"]
churn_rate   = len(churned) / len(filtered_df) * 100
rev_lost     = churned["monthlycharges"].sum()
avg_tenure_c = churned["tenure"].mean()
avg_tenure_r = retained["tenure"].mean()

col1, col2, col3, col4 = st.columns(4)
col1.metric("👥 Total Customers",    f"{len(filtered_df):,}")
col2.metric("🚨 Churn Rate",         f"{churn_rate:.1f}%",
            delta=f"{churn_rate - 26.5:.1f}% vs baseline",
            delta_color="inverse")
col3.metric("💸 Monthly Rev Lost",   f"${rev_lost:,.0f}")
col4.metric("📅 Avg Tenure Churned", f"{avg_tenure_c:.1f} mo",
            delta=f"{avg_tenure_c - avg_tenure_r:.1f} mo vs retained",
            delta_color="inverse")

st.markdown("---")

# Row 1: Pie + Contract bar
col1, col2 = st.columns(2)

with col1:
    st.subheader("Churn Distribution")
    churn_counts = filtered_df["churn"].value_counts().reset_index()
    churn_counts.columns = ["Churn", "Count"]
    fig = px.pie(
        churn_counts, values="Count", names="Churn",
        color="Churn",
        color_discrete_map={"Yes": "#e74c3c", "No": "#2ecc71"},
        hole=0.45
    )
    fig.update_layout(height=320, margin=dict(t=0, b=0))
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("Churn Rate by Contract Type")
    contract_data = (
        filtered_df.groupby("contract")["churn_binary"]
        .mean().reset_index()
    )
    contract_data["churn_pct"] = (contract_data["churn_binary"] * 100).round(1)
    fig = px.bar(
        contract_data, x="contract", y="churn_pct",
        color="churn_pct",
        color_continuous_scale=["#2ecc71", "#e67e22", "#e74c3c"],
        text="churn_pct",
        labels={"contract": "Contract Type", "churn_pct": "Churn Rate (%)"}
    )
    fig.update_traces(texttemplate="%{text:.1f}%", textposition="outside")
    fig.update_layout(coloraxis_showscale=False, height=320, margin=dict(t=20))
    st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# Row 2: Revenue waterfall + Internet service
col1, col2 = st.columns(2)

with col1:
    st.subheader("💰 Revenue Waterfall")
    total_rev = filtered_df["monthlycharges"].sum()
    lost_rev  = churned["monthlycharges"].sum()

    fig = go.Figure(go.Waterfall(
        orientation="v",
        measure=["absolute", "relative", "total"],
        x=["Total Revenue", "Lost to Churn", "Retained Revenue"],
        y=[total_rev, -lost_rev, 0],
        decreasing={"marker": {"color": "#e74c3c"}},
        increasing={"marker": {"color": "#2ecc71"}},
        totals={"marker":    {"color": "#3498db"}}
    ))
    fig.update_layout(height=340, margin=dict(t=20, b=0))
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("Churn by Internet Service")
    inet = (
        filtered_df.groupby("internetservice")["churn_binary"]
        .mean().reset_index()
    )
    inet["churn_pct"] = (inet["churn_binary"] * 100).round(1)
    fig = px.bar(
        inet, x="churn_pct", y="internetservice",
        orientation="h",
        color="churn_pct",
        color_continuous_scale=["#2ecc71", "#e74c3c"],
        text="churn_pct",
        labels={"internetservice": "", "churn_pct": "Churn Rate (%)"}
    )
    fig.update_traces(texttemplate="%{text:.1f}%", textposition="outside")
    fig.update_layout(coloraxis_showscale=False, height=340, margin=dict(t=20))
    st.plotly_chart(fig, use_container_width=True)

st.markdown("---")
st.caption("IBM Telco Customer Churn Dataset · Built with Streamlit + Plotly")