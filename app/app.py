import streamlit as st

st.set_page_config(
    page_title="Customer Churn Analysis",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Sidebar
st.sidebar.title("📊 Churn Analysis")
st.sidebar.markdown("---")

# ✅ Clickable Navigation Buttons
st.sidebar.markdown("### 🗺️ Navigation")

if st.sidebar.button("📊 Overview — KPIs & Summary"):
    st.switch_page("pages/01_overview.py")

if st.sidebar.button("🔍 Analysis — Deep Dive"):
    st.switch_page("pages/02_analysis.py")

st.sidebar.markdown("---")
st.sidebar.markdown("**Dataset:** IBM Telco Churn")
st.sidebar.markdown("**Records:** 7,032 customers")
st.sidebar.markdown("**Built with:** Python + Streamlit")

# Home Page
st.title("📊 Customer Churn Analysis Dashboard")
st.markdown("##### Telecom Customer Retention Intelligence System")
st.markdown("---")

col1, col2, col3 = st.columns(3)
col1.info("📊 **Overview Page**\nKPI metrics + churn summary")
col2.warning("🔍 **Analysis Page**\nCharts, filters, segments")
col3.error("🚨 **High Risk**\nCustomers likely to churn")

st.markdown("---")

st.markdown("""
### 📌 Business Question
> *Which customers are most likely to churn — and what can the business do about it?*

### 📁 Dataset
- **Source:** IBM Telco Customer Churn Dataset
- **Size:** 7,032 customers · 21 features
- **Target:** Churn (Yes / No)

### 🔑 Key Insights
| # | Insight |
|---|---|
| 1 | Overall churn rate is **~26.5%** |
| 2 | Month-to-month contracts churn at **~42%** |
| 3 | Most churn happens in **first 12 months** |
| 4 | Fiber optic users churn at **2x DSL rate** |
| 5 | Electronic check payers churn at **~45%** |

### 💡 Business Recommendations
| # | Recommendation |
|---|---|
| 1 | Offer incentives to convert month-to-month customers to annual contracts |
| 2 | Focus retention efforts on customers in first 12 months |
| 3 | Investigate fiber optic service quality and pricing |
| 4 | Promote auto-pay to replace electronic check payments |
| 5 | Target high-risk segment — month-to-month + tenure < 12mo + charges > $65 |
""")

st.markdown("---")
st.caption("IBM Telco Customer Churn Dataset · Built with Streamlit + Plotly")