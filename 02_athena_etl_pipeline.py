import pandas as pd

print("🚀 Starting Athena ETL Pipeline...")

# ==========================================
# 1. EXTRACT
# ==========================================
print("Extracting raw data...")
raw_df = pd.read_csv("athena_equipment_finance_dataset.csv")

# ==========================================
# 2. TRANSFORM (Normalization)
# ==========================================
print("Transforming and normalizing data...")

# A. Create Dimension Table: dim_equipment
# Get unique equipment categories and assign an ID
unique_equipment = raw_df[['Equipment_Category']].drop_duplicates().reset_index(drop=True)
unique_equipment['Equipment_ID'] = ['EQ-' + str(i).zfill(3) for i in range(1, len(unique_equipment) + 1)]
dim_equipment = unique_equipment[['Equipment_ID', 'Equipment_Category']]

# B. Create Dimension Table: dim_clients
# Generate unique Client IDs (assuming each contract in this mock data is a new client)
raw_df['Client_ID'] = ['CUST-' + str(i).zfill(5) for i in range(1, len(raw_df) + 1)]
dim_clients = raw_df[['Client_ID', 'Client_Industry', 'Client_Credit_Score']]

# C. Create Fact Table: fact_contracts
# Merge the Equipment_ID into the main dataframe
merged_df = raw_df.merge(dim_equipment, on='Equipment_Category', how='left')
# Force date into standard SQL YYYY-MM-DD format
merged_df['Origination_Date'] = pd.to_datetime(merged_df['Origination_Date']).dt.strftime('%Y-%m-%d')

# Select only the columns needed for the fact table (using IDs instead of text names)
fact_contracts = merged_df[[
    'Contract_ID', 'Client_ID', 'Equipment_ID', 'Origination_Date', 
    'Asset_Cost_INR', 'Down_Payment_INR', 'Financed_Amount_INR', 
    'Tenure_Months', 'Interest_Rate_Pct', 'Athena_Risk_Score', 
    'Athena_Recommendation', 'Loan_Status'
]]

# ==========================================
# 3. LOAD
# ==========================================
print("Loading data into normalized files...")
dim_equipment.to_csv("dim_equipment.csv", index=False)
dim_clients.to_csv("dim_clients.csv", index=False)
fact_contracts.to_csv("fact_contracts.csv", index=False)

print("✅ ETL Complete! Three normalized tables generated.")