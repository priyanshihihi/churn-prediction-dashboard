"""
Step 3: Load cleaned churn data into MySQL and run SQL queries
Make sure MySQL server is running before executing this script
"""

import pandas as pd
import mysql.connector

# ── CONNECT TO MYSQL ──
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root123",
    database="churn_db"
)
cursor = conn.cursor()
print("Connected to MySQL successfully!")

# ── CREATE TABLE ──
cursor.execute("DROP TABLE IF EXISTS customers;")
cursor.execute("""
CREATE TABLE customers (
    gender VARCHAR(10),
    SeniorCitizen INT,
    Partner VARCHAR(5),
    Dependents VARCHAR(5),
    tenure INT,
    PhoneService VARCHAR(5),
    MultipleLines VARCHAR(20),
    InternetService VARCHAR(20),
    OnlineSecurity VARCHAR(20),
    OnlineBackup VARCHAR(20),
    DeviceProtection VARCHAR(20),
    TechSupport VARCHAR(20),
    StreamingTV VARCHAR(20),
    StreamingMovies VARCHAR(20),
    Contract VARCHAR(20),
    PaperlessBilling VARCHAR(5),
    PaymentMethod VARCHAR(40),
    MonthlyCharges FLOAT,
    TotalCharges FLOAT,
    Churn VARCHAR(5),
    Churn_Binary INT
);
""")
print("Table 'customers' created!")

# ── LOAD CSV DATA ──
df = pd.read_csv("telco_churn_cleaned.csv")
df = df.where(pd.notnull(df), None)  # replace NaN with None for MySQL

rows_inserted = 0
for _, row in df.iterrows():
    cursor.execute("""
        INSERT INTO customers VALUES (
            %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,
            %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s
        )
    """, tuple(row))
    rows_inserted += 1

conn.commit()
print(f"Inserted {rows_inserted} rows into MySQL!")

# ── SQL QUERIES ──
print("\n" + "="*55)
print("SQL QUERY RESULTS")
print("="*55)

queries = {
    "1. Overall Churn Rate": """
        SELECT 
            COUNT(*) as total_customers,
            SUM(Churn_Binary) as churned,
            ROUND(AVG(Churn_Binary) * 100, 2) as churn_rate_pct
        FROM customers
    """,
    "2. Churn by Contract Type": """
        SELECT Contract,
            COUNT(*) as total,
            SUM(Churn_Binary) as churned,
            ROUND(AVG(Churn_Binary)*100, 2) as churn_rate_pct
        FROM customers
        GROUP BY Contract
        ORDER BY churn_rate_pct DESC
    """,
    "3. Churn by Internet Service": """
        SELECT InternetService,
            COUNT(*) as total,
            SUM(Churn_Binary) as churned,
            ROUND(AVG(Churn_Binary)*100, 2) as churn_rate_pct
        FROM customers
        GROUP BY InternetService
        ORDER BY churn_rate_pct DESC
    """,
    "4. Churn by Payment Method": """
        SELECT PaymentMethod,
            COUNT(*) as total,
            SUM(Churn_Binary) as churned,
            ROUND(AVG(Churn_Binary)*100, 2) as churn_rate_pct
        FROM customers
        GROUP BY PaymentMethod
        ORDER BY churn_rate_pct DESC
    """,
    "5. Avg Charges - Churned vs Retained": """
        SELECT Churn,
            ROUND(AVG(MonthlyCharges), 2) as avg_monthly_charges,
            ROUND(AVG(tenure), 1) as avg_tenure_months,
            ROUND(AVG(TotalCharges), 2) as avg_total_charges
        FROM customers
        GROUP BY Churn
    """,
    "6. Senior vs Non-Senior Churn": """
        SELECT 
            CASE WHEN SeniorCitizen=1 THEN 'Senior' ELSE 'Non-Senior' END as type,
            COUNT(*) as total,
            SUM(Churn_Binary) as churned,
            ROUND(AVG(Churn_Binary)*100, 2) as churn_rate_pct
        FROM customers
        GROUP BY SeniorCitizen
    """,
    "7. Revenue Impact of Churn": """
        SELECT 
            ROUND(SUM(MonthlyCharges), 2) as total_monthly_revenue,
            ROUND(SUM(CASE WHEN Churn_Binary=1 THEN MonthlyCharges ELSE 0 END), 2) as revenue_lost,
            ROUND(SUM(CASE WHEN Churn_Binary=1 THEN MonthlyCharges ELSE 0 END)/SUM(MonthlyCharges)*100, 2) as pct_at_risk
        FROM customers
    """
}

# Run each query, print result, save to CSV
csv_names = [
    "overall_churn", "churn_by_contract", "churn_by_internet",
    "churn_by_payment", "churn_by_charges", "churn_by_senior", "revenue_impact"
]

for (title, query), csv_name in zip(queries.items(), csv_names):
    print(f"\n{title}:")
    result_df = pd.read_sql(query, conn)
    print(result_df.to_string(index=False))
    result_df.to_csv(f"{csv_name}.csv", index=False)

conn.close()
print("\n\nAll query results saved as CSVs!")
print("Done. Ready to build the ML model!")
