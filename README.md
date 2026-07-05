# 📉 Customer Churn Prediction Dashboard

An end-to-end **Customer Churn Prediction system** built on real Telco customer data, combining **Python, MySQL, Machine Learning, and Power BI** into a complete data analytics pipeline — with AI-powered insights to identify customers at risk of leaving before they actually do.

> Built as a portfolio project targeting Data Analyst roles. Demonstrates the full DA workflow: data sourcing → SQL analysis → ML modelling → interactive dashboard.

---

## 📊 Dashboard Pages

| Page | What it shows |
|------|--------------|
| **Overview** | Total customers, churn rate, revenue at risk, churn by contract and payment method |
| **Customer Analysis** | Churn by internet service, senior vs non-senior comparison, risk segment distribution |
| **ML Performance** | Model accuracy, AUC score, confusion matrix, feature importance chart |
| **Risk Segments** | High risk customer table, churn probability by contract type |
| **AI Insights** | Key findings summary, revenue impact, senior citizen churn comparison |

---

## 🤖 Machine Learning Model

**Algorithm:** Random Forest Classifier

**Why Random Forest?**
- Builds 100 decision trees and combines their votes (majority wins)
- Handles both numeric and categorical data well
- Provides feature importance — tells us which factors drive churn most
- Works well on imbalanced datasets (more non-churners than churners)

**Training approach:**
- 80% of data used for training (5,625 customers)
- 20% held out for testing (1,407 customers)
- `class_weight='balanced'` used to handle churn/non-churn imbalance

### Model Results

| Metric | Value |
|--------|-------|
| Accuracy | 74.98% |
| AUC Score | 0.8295 |
| True Positives (churners caught) | 283 |
| False Negatives (churners missed) | 91 |

### Top Churn Drivers (Feature Importance)

| Rank | Feature | Importance |
|------|---------|-----------|
| 1 | Contract type | 0.1580 |
| 2 | Tenure | 0.1490 |
| 3 | TotalCharges | 0.1286 |
| 4 | MonthlyCharges | 0.1246 |
| 5 | OnlineSecurity | 0.0795 |
| 6 | TechSupport | 0.0715 |

---

## 🔍 Key Insights from SQL Analysis

- **26.5% overall churn rate** — 1,869 out of 7,032 customers churned
- **Electronic check users churn at 45.29%** — highest of all payment methods
- **Month-to-month contracts** have the highest churn probability (~58%)
- **Senior citizens churn at 41.68%** vs 23.65% for non-seniors
- **$139,130/month revenue at risk** — 30.53% of total monthly revenue
- **2,196 customers** identified as High Risk (churn probability >60%)
- Churned customers pay **more per month** ($74.44 avg) but stay **less time** (18 months avg)

---

## 🛠️ Tech Stack

| Tool | Purpose |
|------|---------|
| Python (pandas, numpy) | Data cleaning and processing |
| MySQL + MySQL Workbench | Database creation and SQL analysis |
| scikit-learn | Random Forest ML model |
| matplotlib + seaborn | Model performance charts |
| Power BI Desktop | Interactive dashboard |
| DAX | KPI measures |
| Kaggle | Real-world dataset source |
| Git + GitHub | Version control and portfolio hosting |

---

## 📁 Project Structure

```
churn_prediction_project/
│
├── explore_data.py              ← Step 1: data exploration and cleaning
├── load_to_mysql.py             ← Step 2: MySQL database + SQL queries
├── train_model.py               ← Step 3: Random Forest ML model
├── churn_dashboard.pbix         ← Power BI dashboard file
├── churn_dashboard_preview.pdf  ← Dashboard PDF preview
│
├── telco_churn.csv              ← original Kaggle dataset
├── telco_churn_cleaned.csv      ← cleaned dataset
│
├── churn_predictions.csv        ← all customers with churn probability scores
├── model_performance.csv        ← accuracy and AUC metrics
├── confusion_matrix.csv         ← model prediction breakdown
├── feature_importance.csv       ← churn driver rankings
│
├── churn_by_contract.csv        ← SQL: churn rate by contract type
├── churn_by_internet.csv        ← SQL: churn rate by internet service
├── churn_by_payment.csv         ← SQL: churn rate by payment method
├── churn_by_senior.csv          ← SQL: senior vs non-senior churn
└── revenue_impact.csv           ← SQL: monthly revenue at risk
```

---

## ⚙️ How to Run

### 1. Get the dataset
Download from Kaggle: [Telco Customer Churn](https://www.kaggle.com/datasets/blastchar/telco-customer-churn)
Rename to `telco_churn.csv` and place in the project folder.

### 2. Clean the data
```bash
pip install pandas numpy
python explore_data.py
```

### 3. Load into MySQL
```bash
pip install mysql-connector-python
# Make sure MySQL is running
python load_to_mysql.py
```

### 4. Train the ML model
```bash
pip install scikit-learn matplotlib seaborn
python train_model.py
```

### 5. Open the dashboard
Open `churn_dashboard.pbix` in Power BI Desktop.

---

## 💡 Business Impact

> "By identifying the 2,196 High Risk customers before they churn, the business can proactively offer targeted retention incentives. Even retaining 30% of High Risk customers would save approximately $41,700 in monthly recurring revenue."

---

## 📈 Pipeline Overview

```
Kaggle Dataset (real data)
        ↓
   Python (clean + explore)
        ↓
   MySQL Database (SQL analysis)
        ↓
   Random Forest ML Model
        ↓
   Churn Probability Scores (per customer)
        ↓
   Power BI Dashboard (5 pages)
```

---

## 👩‍💻 Author

**Priyanshi** — B.Tech Computer Science (Blockchain), Presidency University Bangalore
GitHub: [@priyanshihihi](https://github.com/priyanshihihi)

---

## 📄 Preview

📊 [View Dashboard Preview (PDF)](./churn_dashboard_preview.pdf)
