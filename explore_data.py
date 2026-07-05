"""
Step 1: Data Exploration and Cleaning
Telco Customer Churn Dataset
Run this first to understand the data before building the ML model
"""

import pandas as pd
import numpy as np

# ── LOAD DATA ──
df = pd.read_csv("telco_churn.csv")

print("=" * 55)
print("TELCO CHURN DATASET - EXPLORATION REPORT")
print("=" * 55)

# Basic shape
print(f"\nTotal Customers : {df.shape[0]}")
print(f"Total Columns   : {df.shape[1]}")

# Column names
print("\nColumns:")
for col in df.columns:
    print(f"  - {col}")

# Data types
print("\nData Types:")
print(df.dtypes)

# Missing values
print("\nMissing Values:")
print(df.isnull().sum())

# Churn distribution
print("\nChurn Distribution:")
print(df['Churn'].value_counts())
print(f"Churn Rate: {df['Churn'].value_counts(normalize=True)['Yes']*100:.1f}%")

# Basic stats for numeric columns
print("\nNumeric Column Stats:")
print(df.describe())

# ── CLEANING ──
print("\n" + "=" * 55)
print("CLEANING THE DATA")
print("=" * 55)

# TotalCharges has spaces instead of nulls — fix it
df['TotalCharges'] = pd.to_numeric(df['TotalCharges'], errors='coerce')
print(f"Rows with blank TotalCharges: {df['TotalCharges'].isnull().sum()}")

# Drop those rows (only 11 — very few, safe to drop)
df = df.dropna(subset=['TotalCharges'])
print(f"Rows after dropping blanks: {len(df)}")

# Convert Churn to binary (Yes=1, No=0) for ML
df['Churn_Binary'] = (df['Churn'] == 'Yes').astype(int)
print(f"\nChurn column converted to binary (1=Yes, 0=No)")

# Drop customerID — not useful for ML
df = df.drop(columns=['customerID'])
print("customerID column dropped (not useful for ML)")

# Save cleaned version
df.to_csv("telco_churn_cleaned.csv", index=False)
print("\nCleaned data saved to telco_churn_cleaned.csv")
print("\nDone! Ready for SQL loading and ML model building.")
