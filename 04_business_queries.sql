SELECT 
	c.Client_ID,
    c.Client_Industry,
    c.Client_Credit_Score,
    f.Athena_Risk_Score
FROM fact_contracts AS f
INNER JOIN  dim_clients AS c
	ON f.Client_ID = c.Client_ID
WHERE f.Athena_Risk_Score > 80
ORDER BY f.Athena_Risk_Score DESC;


SELECT 
	e.Equipment_ID,
	e.Equipment_Category,
    SUM(Financed_Amount_INR) AS Total_Financed_Amount
FROM fact_contracts AS f
INNER JOIN dim_equipment AS e
	ON f.Equipment_ID = e.Equipment_ID
GROUP BY e.Equipment_Category, e.Equipment_ID
ORDER BY Total_Financed_Amount DESC;


SELECT 
	Athena_Recommendation,
    Loan_Status,
    COUNT(*) AS Total_Contracts
FROM fact_contracts
GROUP BY Athena_Recommendation, Loan_Status;
