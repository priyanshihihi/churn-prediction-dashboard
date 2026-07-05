"""
Churn Prediction Model
Author: Priyanshi
Description: I'm using a Random Forest model to predict which customers
are likely to churn. The idea is simple - look at past customer behavior
and learn patterns that lead to churn, then use those patterns to predict
future churn.
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report, roc_auc_score
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns

# ── Step 1: Load the cleaned data ──
# I already cleaned this in explore_data.py so just loading it here
df = pd.read_csv("telco_churn_cleaned.csv")
print(f"Loaded data: {len(df)} customers")

# ── Step 2: Convert text columns to numbers ──
# Machine learning models only understand numbers, not text like "Yes"/"No"
# So I need to convert every text column to a number
# For example: "Male" -> 0, "Female" -> 1

le = LabelEncoder()

# Get all columns that have text values
text_columns = df.select_dtypes(include=['object']).columns.tolist()

# Remove the target column (Churn) since we handle that separately
text_columns = [col for col in text_columns if col != 'Churn']

df_model = df.copy()
for col in text_columns:
    df_model[col] = le.fit_transform(df[col])

print(f"Converted {len(text_columns)} text columns to numbers")

# ── Step 3: Separate features (X) and target (y) ──
# X = all the customer info we use to make predictions (the inputs)
# y = whether the customer churned or not (what we want to predict)
# I'm dropping Churn (text version) and keeping Churn_Binary (0 or 1)

X = df_model.drop(columns=['Churn', 'Churn_Binary'])
y = df_model['Churn_Binary']

print(f"\nInput features ({len(X.columns)} total):")
for col in X.columns:
    print(f"  - {col}")
print(f"\nTarget: Churn_Binary (0 = stayed, 1 = churned)")

# ── Step 4: Split into training and testing data ──
# I'm using 80% of data to train the model
# and keeping 20% aside to test how well it works
# stratify=y makes sure both splits have same churn ratio

X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.2,       # 20% goes to testing
    random_state=42,     # so results are same every time I run it
    stratify=y           # keeps churn ratio balanced in both splits
)

print(f"\nTraining data: {len(X_train)} customers")
print(f"Testing data : {len(X_test)} customers")

# ── Step 5: Train the Random Forest model ──
# Random Forest works by building many decision trees and combining their results
# Think of it like asking 100 different experts and taking the majority vote
# n_estimators = 100 means I'm building 100 decision trees
# class_weight='balanced' helps because we have more non-churners than churners

print("\nTraining the model... (this might take a moment)")

model = RandomForestClassifier(
    n_estimators=100,
    max_depth=10,
    random_state=42,
    class_weight='balanced'
)

model.fit(X_train, y_train)
print("Model training complete!")

# ── Step 6: Test how well the model performs ──
# Now I use the 20% test data (model has never seen this)
# to check if predictions are accurate

y_pred = model.predict(X_test)
y_prob = model.predict_proba(X_test)[:, 1]  # probability of churning (0 to 1)

accuracy = accuracy_score(y_test, y_pred)
auc = roc_auc_score(y_test, y_prob)
cm = confusion_matrix(y_test, y_pred)

print("\n" + "="*50)
print("HOW WELL DID THE MODEL DO?")
print("="*50)
print(f"Accuracy  : {accuracy*100:.2f}%")
print(f"AUC Score : {auc:.4f}  (closer to 1.0 = better)")
print(f"\nOut of {len(y_test)} test customers:")
print(f"  Correctly predicted NOT churn : {cm[0][0]}")
print(f"  Correctly predicted churn     : {cm[1][1]}")
print(f"  Wrongly predicted churn       : {cm[0][1]}")
print(f"  Missed actual churners        : {cm[1][0]}")
print("\nDetailed report:")
print(classification_report(y_test, y_pred))

# ── Step 7: Which factors matter most for predicting churn? ──
# Random Forest tells us which customer features were most useful
# for making churn predictions - this is called feature importance

feature_importance = pd.DataFrame({
    'feature': X.columns,
    'importance': model.feature_importances_
}).sort_values('importance', ascending=False)

print("\n" + "="*50)
print("TOP FACTORS THAT PREDICT CHURN")
print("="*50)
print(feature_importance.head(10).to_string(index=False))

# ── Step 8: Score ALL customers with churn probability ──
# Now I apply the model to all 7032 customers
# Each customer gets a churn probability from 0% to 100%
# and a risk label: Low / Medium / High

all_probs = model.predict_proba(X)[:, 1]

df_output = df.copy()
df_output['churn_probability'] = (all_probs * 100).round(2)
df_output['churn_prediction'] = model.predict(X)

# Segment customers into risk groups
def get_risk(prob):
    if prob >= 60:
        return 'High Risk'
    elif prob >= 30:
        return 'Medium Risk'
    else:
        return 'Low Risk'

df_output['risk_segment'] = df_output['churn_probability'].apply(get_risk)

print("\nRisk Segment Breakdown:")
print(df_output['risk_segment'].value_counts())

# ── Step 9: Save everything to CSV for Power BI ──
df_output.to_csv("churn_predictions.csv", index=False)
print("\nSaved: churn_predictions.csv")

# Save model performance metrics
perf_df = pd.DataFrame({
    'metric': ['Accuracy', 'AUC Score'],
    'value': [round(accuracy*100, 2), round(auc*100, 2)]
})
perf_df.to_csv("model_performance.csv", index=False)
print("Saved: model_performance.csv")

# Save confusion matrix
cm_df = pd.DataFrame({
    'category': ['True Negative', 'False Positive', 'False Negative', 'True Positive'],
    'count': [cm[0][0], cm[0][1], cm[1][0], cm[1][1]],
    'meaning': [
        'Correctly said: will NOT churn',
        'Wrongly said: will churn',
        'Missed: actually did churn',
        'Correctly said: will churn'
    ]
})
cm_df.to_csv("confusion_matrix.csv", index=False)
print("Saved: confusion_matrix.csv")

# Save feature importance
feature_importance.to_csv("feature_importance.csv", index=False)
print("Saved: feature_importance.csv")

# ── Step 10: Save charts ──
# Confusion matrix heatmap
plt.figure(figsize=(6, 5))
sns.heatmap(cm, annot=True, fmt='d', cmap='Greens',
            xticklabels=['Not Churn', 'Churn'],
            yticklabels=['Not Churn', 'Churn'])
plt.title('Confusion Matrix')
plt.ylabel('Actual')
plt.xlabel('Predicted')
plt.tight_layout()
plt.savefig("confusion_matrix_plot.png", dpi=150)
print("Saved: confusion_matrix_plot.png")

# Feature importance bar chart
plt.figure(figsize=(8, 6))
top10 = feature_importance.head(10)
sns.barplot(x='importance', y='feature', data=top10, palette='Greens_r')
plt.title('Top 10 Factors That Predict Churn')
plt.xlabel('Importance Score')
plt.tight_layout()
plt.savefig("feature_importance_plot.png", dpi=150)
print("Saved: feature_importance_plot.png")

print("\n" + "="*50)
print("ALL DONE!")
print("Files ready to load into Power BI:")
print("  churn_predictions.csv")
print("  model_performance.csv")
print("  confusion_matrix.csv")
print("  feature_importance.csv")
print("="*50)
