# Customer Churn Prediction Dashboard

An end-to-end **Customer Churn Prediction system** built on real Telco customer data, combining **Python, MySQL, Machine Learning, and Power BI** into a complete data analytics pipeline.

> Built as a portfolio project targeting Data Analyst roles. Demonstrates the full DA workflow: data sourcing → SQL analysis → ML modelling → interactive dashboard.

---

## Dashboard Pages

| Page | What it shows |
|------|--------------|
| **Overview** | Total customers, churn rate, revenue at risk, churn by contract and payment method |
| **Customer Analysis** | Churn by internet service, senior vs non-senior comparison, risk segment distribution |
| **ML Performance** | Model accuracy, AUC score, confusion matrix, feature importance chart |
| **Risk Segments** | High risk customer table, churn probability by contract type |
| **AI Insights** | Key findings summary, revenue impact, senior citizen churn comparison |

---

## SQL Queries Used

All queries were run in **MySQL Workbench** against the `churn_db` database.

### 1. Overall Churn Rate
```sql
SELECT 
    COUNT(*) as total_customers,
    SUM(Churn_Binary) as churned,
    ROUND(AVG(Churn_Binary) * 100, 2) as churn_rate_pct
FROM customers;
```

### 2. Churn Rate by Contract Type
```sql
SELECT 
    Contract,
    COUNT(*) as total,
    SUM(Churn_Binary) as churned,
    ROUND(AVG(Churn_Binary) * 100, 2) as churn_rate_pct
FROM customers
GROUP BY Contract
ORDER BY churn_rate_pct DESC;
```

### 3. Churn Rate by Internet Service
```sql
SELECT 
    InternetService,
    COUNT(*) as total,
    SUM(Churn_Binary) as churned,
    ROUND(AVG(Churn_Binary) * 100, 2) as churn_rate_pct
FROM customers
GROUP BY InternetService
ORDER BY churn_rate_pct DESC;
```

### 4. Churn Rate by Payment Method
```sql
SELECT 
    PaymentMethod,
    COUNT(*) as total,
    SUM(Churn_Binary) as churned,
    ROUND(AVG(Churn_Binary) * 100, 2) as churn_rate_pct
FROM customers
GROUP BY PaymentMethod
ORDER BY churn_rate_pct DESC;
```

### 5. Avg Charges — Churned vs Retained
```sql
SELECT 
    Churn,
    ROUND(AVG(MonthlyCharges), 2) as avg_monthly_charges,
    ROUND(AVG(tenure), 1) as avg_tenure_months,
    ROUND(AVG(TotalCharges), 2) as avg_total_charges
FROM customers
GROUP BY Churn;
```

### 6. Senior vs Non-Senior Churn
```sql
SELECT 
    CASE WHEN SeniorCitizen = 1 THEN 'Senior' ELSE 'Non-Senior' END as customer_type,
    COUNT(*) as total,
    SUM(Churn_Binary) as churned,
    ROUND(AVG(Churn_Binary) * 100, 2) as churn_rate_pct
FROM customers
GROUP BY SeniorCitizen;
```

### 7. Revenue Impact of Churn
```sql
SELECT 
    ROUND(SUM(MonthlyCharges), 2) as total_monthly_revenue,
    ROUND(SUM(CASE WHEN Churn_Binary = 1 
               THEN MonthlyCharges ELSE 0 END), 2) as revenue_lost,
    ROUND(SUM(CASE WHEN Churn_Binary = 1 
               THEN MonthlyCharges ELSE 0 END) / SUM(MonthlyCharges) * 100, 2) as pct_at_risk
FROM customers;
```

---

## DAX Measures Used in Power BI

```dax
Total Customers = COUNTROWS(churn_predictions)
```

```dax
Churned Customers = 
    COUNTROWS(FILTER(churn_predictions, churn_predictions[Churn] = "Yes"))
```

```dax
Churn Rate = DIVIDE([Churned Customers], [Total Customers]) * 100
```

```dax
High Risk Customers = 
    COUNTROWS(FILTER(churn_predictions, churn_predictions[risk_segment] = "High Risk"))
```

```dax
Avg Churn Probability = AVERAGE(churn_predictions[churn_probability])
```

```dax
Monthly Revenue at Risk = 
    SUMX(
        FILTER(churn_predictions, churn_predictions[Churn] = "Yes"),
        churn_predictions[MonthlyCharges]
    )
```

---

## Machine Learning Model

**Algorithm:** Random Forest Classifier

| Metric | Value |
|--------|-------|
| Accuracy | 74.98% |
| AUC Score | 0.8295 |
| True Positives (churners caught) | 283 |
| False Negatives (churners missed) | 91 |

### Top Churn Drivers

| Rank | Feature | Importance |
|------|---------|-----------|
| 1 | Contract type | 0.1580 |
| 2 | Tenure | 0.1490 |
| 3 | TotalCharges | 0.1286 |
| 4 | MonthlyCharges | 0.1246 |
| 5 | OnlineSecurity | 0.0795 |
| 6 | TechSupport | 0.0715 |

---

## Key Insights

- **26.5% overall churn rate**
- **Electronic check users churn at 45.29%** — highest of all payment methods
- **Month-to-month contracts** have the highest churn probability (~58%)
- **Senior citizens churn at 41.68%** vs 23.65% for non-seniors
- **$139,130/month revenue at risk** — 30.53% of total monthly revenue
- **2,196 customers** identified as High Risk

---

## Tech Stack

| Tool | Purpose |
|------|---------|
| Python (pandas, numpy) | Data cleaning and processing |
| MySQL + MySQL Workbench | Database creation and SQL analysis |
| scikit-learn | Random Forest ML model |
| matplotlib + seaborn | Model performance charts |
| Power BI Desktop | Interactive dashboard |
| DAX | KPI measures |
| Kaggle | Real-world dataset source |
| Git + GitHub | Version control |

---

## How to Run

```bash
# 1. Install dependencies
pip install pandas numpy scikit-learn matplotlib seaborn mysql-connector-python

# 2. Clean the data
python explore_data.py

# 3. Load into MySQL (make sure MySQL is running)
python load_to_mysql.py

# 4. Train the ML model
python train_model.py

# 5. Open churn_dashboard.pbix in Power BI Desktop
```

---

## Business Impact

> "By identifying 2,196 High Risk customers before they churn, the business can proactively offer targeted retention incentives — potentially saving $41,700+ in monthly recurring revenue."

---

## Author

**Priyanshi** — B.Tech Computer Science (Blockchain), Presidency University Bangalore
GitHub: [@priyanshihihi](https://github.com/priyanshihihi)

## Preview

[View Dashboard Preview (PDF)](./churn_dashboard.pdf)
