# 📊 Customer Churn Analysis

An end-to-end Data Analytics portfolio project analyzing customer churn
for a telecom company using SQL, Python, and Streamlit.

---

## 🎯 Business Problem

> A telecom company is losing ~26.5% of its customers every year.
> This project identifies **who is churning**, **why they are churning**,
> and **which customers are at highest risk** right now.

---

## 🛠️ Tools & Technologies

| Layer | Tools |
|---|---|
| Data Storage | SQLite + SQLAlchemy |
| Data Analysis | Python, pandas, numpy |
| Visualization | Plotly, seaborn, matplotlib |
| Dashboard | Streamlit |
| Environment | VS Code, virtualenv |
| Version Control | Git + GitHub |

---

## 📁 Project Structure
customer-churn-analysis/

│

├── app/

│   ├── app.py                  ← Streamlit home page

│   └── pages/

│       ├── 01_overview.py      ← KPIs + summary charts

│       └── 02_analysis.py      ← Deep dive + filters

│

├── data/

│   ├── raw/

│   │   └── WA_Fn-UseC_-Telco-Customer-Churn.csv

│   ├── processed/

│   └── setup_db.py             ← Builds churn.db from CSV

│

├── sql/

│   ├── schema.sql              ← Table structure

│   └── queries.sql             ← Business queries

│

├── notebooks/

│   ├── 01_data_loading_sql.ipynb

│   ├── 02_sql_queries.ipynb

│   └── 03_eda_visualizations.ipynb

│

├── requirements.txt

├── .gitignore

└── README.md

---

## ⚡ How to Run This Project

### 1. Clone the repository
```bash
git clone https://github.com/YOUR_USERNAME/customer-churn-analysis.git
cd customer-churn-analysis
```

### 2. Create virtual environment
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Download the dataset
Download from Kaggle:
[IBM Telco Customer Churn Dataset](https://www.kaggle.com/datasets/blastchar/telco-customer-churn)

Place it in: data/raw/WA_Fn-UseC_-Telco-Customer-Churn.csv

### 5. Build the database
```bash
python data/setup_db.py
```

### 6. Run the dashboard
```bash
streamlit run app/app.py
```

Open your browser at `http://localhost:8501`

---

## 📊 Dashboard Features

### 📈 Overview Page
- Total customers KPI
- Churn rate KPI with baseline comparison
- Monthly revenue lost KPI
- Average tenure KPI
- Churn distribution pie chart
- Churn by contract type bar chart
- Revenue waterfall chart
- Churn by internet service chart

### 🔍 Analysis Page
- Monthly charges vs churn histogram
- Churn rate by tenure group
- Churn rate by payment method
- Tenure vs monthly charges scatter plot
- High-risk customer table

### 🔧 Interactive Filters
- Gender
- Contract type
- Internet service
- Monthly charges range slider

---

## 🔑 Key Business Insights

| # | Insight | Impact |
|---|---|---|
| 1 | Overall churn rate is **26.5%** | 1 in 4 customers leave |
| 2 | Month-to-month contracts churn at **42%** | Contract type is #1 risk factor |
| 3 | Most churn happens in **first 12 months** | Onboarding experience is critical |
| 4 | Fiber optic users churn at **2x DSL rate** | Service quality issue |
| 5 | Electronic check payers churn at **~45%** | Payment friction = churn signal |
| 6 | Churned customers pay **$15 more/month** | High bill = high churn risk |

---

## 💡 Business Recommendations

1. **Offer incentives** to convert month-to-month customers to annual contracts
2. **Focus retention efforts** on customers in their first 12 months
3. **Investigate fiber optic** service quality and pricing
4. **Promote auto-pay** options to replace electronic checks
5. **Target high-risk segment** — month-to-month + tenure < 12mo + charges > $65

---

## 📂 Dataset

- **Name:** IBM Telco Customer Churn
- **Source:** [Kaggle](https://www.kaggle.com/datasets/blastchar/telco-customer-churn)
- **Size:** 7,043 customers · 21 features
- **Target variable:** `Churn` (Yes / No)

---

## 👤 Author

**Your Name**
- GitHub: [@your_username](https://github.com/your_username)
- LinkedIn: [your_linkedin](https://linkedin.com/in/your_linkedin)

---