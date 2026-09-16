-- 0. Clean up existing tables (Run this if you ever need to start over)
DROP TABLE IF EXISTS fact_contracts;
DROP TABLE IF EXISTS dim_clients;
DROP TABLE IF EXISTS dim_equipment;

-- 1. Create the Clients Dimension
CREATE TABLE dim_clients (
    Client_ID VARCHAR(20) PRIMARY KEY,
    Client_Industry VARCHAR(50),
    Client_Credit_Score INT
);

-- 2. Create the Equipment Dimension
CREATE TABLE dim_equipment (
    Equipment_ID VARCHAR(20) PRIMARY KEY,
    Equipment_Category VARCHAR(50)
);

-- 3. Create the Contracts Fact Table
CREATE TABLE fact_contracts (
    Contract_ID VARCHAR(20) PRIMARY KEY,
    Client_ID VARCHAR(20),       
    Equipment_ID VARCHAR(20),    
    Origination_Date VARCHAR(50),        
    Asset_Cost_INR DECIMAL(20, 2),       
    Down_Payment_INR DECIMAL(20, 2),     
    Financed_Amount_INR DECIMAL(20, 2),  
    Tenure_Months INT, 
    Interest_Rate_Pct DECIMAL(10, 4),    
    Athena_Risk_Score DECIMAL(10, 4),    
    Athena_Recommendation VARCHAR(50),
    Loan_Status VARCHAR(30),
    
    FOREIGN KEY (Client_ID) REFERENCES dim_clients(Client_ID),
    FOREIGN KEY (Equipment_ID) REFERENCES dim_equipment(Equipment_ID)
);