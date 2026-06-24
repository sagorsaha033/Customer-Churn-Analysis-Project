# Run this once to create churn.db from the CSV
import pandas as pd
from sqlalchemy import create_engine
import os

# Load CSV
df = pd.read_csv('data/raw/WA_Fn-UseC_-Telco-Customer-Churn.csv')

# Normalize column names
df.columns = (
    df.columns
    .str.strip()
    .str.lower()
    .str.replace(' ', '_', regex=False)
)

# Fix totalcharges
df['totalcharges'] = pd.to_numeric(df['totalcharges'], errors='coerce')
df = df.dropna(subset=['totalcharges'])

# Create DB
engine = create_engine('sqlite:///churn.db')
df.to_sql('customers', engine, if_exists='replace', index=False)

print(f"✅ churn.db created — {len(df)} rows, {df.shape[1]} columns")
print(f"Columns: {df.columns.tolist()}")