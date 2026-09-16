import numpy as np
import pandas as pd

# Set seed for reproducible data
np.random.seed(42)
n = 5000

# 1. Dimensions
industries = [
    "Manufacturing",
    "Healthcare",
    "Construction",
    "Logistics & Fleet",
    "IT & Enterprise Tech",
]
equipment_map = {
    "Manufacturing": [
        "CNC Milling Unit",
        "Industrial Robotic Arm",
        "Injection Molding Press",
    ],
    "Healthcare": ["MRI Scanner", "Digital X-Ray System", "Surgical Robot"],
    "Construction": ["Hydraulic Excavator", "Tower Crane", "Bulldozer"],
    "Logistics & Fleet": [
        "Heavy Duty Hauler",
        "Electric Delivery Van",
        "Forklift Fleet",
    ],
    "IT & Enterprise Tech": [
        "Enterprise Server Rack",
        "Edge AI Compute Cluster",
        "Automated Storage Array",
    ],
}

client_industry = np.random.choice(
    industries, size=n, p=[0.25, 0.20, 0.20, 0.20, 0.15]
)
equipment_type = [
    np.random.choice(equipment_map[ind]) for ind in client_industry
]

# 2. Financials
cost_brackets = {
    "Manufacturing": (1500000, 8500000),
    "Healthcare": (4000000, 15000000),
    "Construction": (2500000, 11000000),
    "Logistics & Fleet": (1200000, 5000000),
    "IT & Enterprise Tech": (800000, 6000000),
}

asset_cost = [
    round(
        np.random.uniform(cost_brackets[ind][0], cost_brackets[ind][1]), -3
    )
    for ind in client_industry
]
down_payment_pct = np.random.choice([0.10, 0.15, 0.20, 0.25], size=n)
down_payment_inr = [
    round(cost * pct, 2) for cost, pct in zip(asset_cost, down_payment_pct)
]
financed_amount_inr = [
    round(cost - dp, 2) for cost, dp in zip(asset_cost, down_payment_inr)
]

tenure_months = np.random.choice([24, 36, 48, 60], size=n, p=[0.15, 0.35, 0.35, 0.15])
base_rate = np.random.normal(loc=9.5, scale=1.5, size=n).round(2)
interest_rate_pct = np.clip(base_rate, 7.0, 14.5)

# 3. Credit Scoring & Athena Decision Logic
client_credit_score = np.random.normal(loc=710, scale=65, size=n).astype(int)
client_credit_score = np.clip(client_credit_score, 550, 850)

# Decision Intelligence Risk Score (1-100: higher = riskier)
risk_score = (
    (850 - client_credit_score) * 0.22
    + (interest_rate_pct * 2.2)
    + (tenure_months * 0.3)
    + np.random.normal(0, 5, size=n)
).round(1)
risk_score = np.clip(risk_score, 10.0, 99.0)

# Athena Decision Recommendation
athena_recommendation = []
delinquency_status = []

for r, cs in zip(risk_score, client_credit_score):
  if r < 40 and cs >= 720:
    athena_recommendation.append("AUTO_APPROVE")
    delinquency_status.append(
        np.random.choice(
            ["Performing", "30_Days_Past_Due"], p=[0.96, 0.04]
        )
    )
  elif r < 65 and cs >= 650:
    athena_recommendation.append("STRUCTURED_LEASE")
    delinquency_status.append(
        np.random.choice(
            ["Performing", "30_Days_Past_Due", "60_Days_Past_Due"],
            p=[0.88, 0.09, 0.03],
        )
    )
  elif r < 80:
    athena_recommendation.append("REQUIRE_COLLATERAL")
    delinquency_status.append(
        np.random.choice(
            ["Performing", "30_Days_Past_Due", "60_Days_Past_Due", "Default"],
            p=[0.75, 0.15, 0.07, 0.03],
        )
    )
  else:
    athena_recommendation.append("REJECT")
    delinquency_status.append(
        np.random.choice(
            ["Performing", "60_Days_Past_Due", "Default"], p=[0.50, 0.25, 0.25]
        )
    )

# 4. Dates
dates = pd.date_range(start="2025-01-01", periods=n, freq="90min")

# Construct DataFrame
df = pd.DataFrame({
    "Contract_ID": [f"EQF-2025-{i:05d}" for i in range(1, n + 1)],
    "Origination_Date": dates.strftime("%Y-%m-%d"),
    "Client_Industry": client_industry,
    "Equipment_Category": equipment_type,
    "Asset_Cost_INR": asset_cost,
    "Down_Payment_INR": down_payment_inr,
    "Financed_Amount_INR": financed_amount_inr,
    "Tenure_Months": tenure_months,
    "Interest_Rate_Pct": interest_rate_pct,
    "Client_Credit_Score": client_credit_score,
    "Athena_Risk_Score": risk_score,
    "Athena_Recommendation": athena_recommendation,
    "Loan_Status": delinquency_status,
})

# Export to CSV
df.to_csv("athena_equipment_finance_dataset.csv", index=False)
print("Generated athena_equipment_finance_dataset.csv with 5,000 records.")