USE CustomerChurnDB;
GO

SELECT COUNT(*) AS TotalRows
FROM CustomerChurn;

SELECT TOP 5 * FROM CustomerChurn;
----data cleaning
-----Convert MonthlyCharges
ALTER TABLE CustomerChurn
ALTER COLUMN MonthlyCharges DECIMAL(10,2);

-----Convert SeniorCitizen
ALTER TABLE CustomerChurn
ALTER COLUMN SeniorCitizen INT;


----Convert tenure
ALTER TABLE CustomerChurn
ALTER COLUMN tenure INT;


----Check TotalCharges
SELECT *
FROM CustomerChurn
WHERE TotalCharges = '';

-----Check blank values in TotalCharges
SELECT COUNT(*) AS BlankTotalCharges
FROM CustomerChurn
WHERE LTRIM(RTRIM(TotalCharges)) = '';

-----Check for duplicate customers
SELECT
customerID,
COUNT(*) AS TotalCount
FROM CustomerChurn
GROUP BY customerID
HAVING COUNT(*) > 1;


----Check NULL values
SELECT
SUM(CASE WHEN customerID IS NULL THEN 1 ELSE 0 END) AS CustomerID_NULL,
SUM(CASE WHEN gender IS NULL THEN 1 ELSE 0 END) AS Gender_NULL,
SUM(CASE WHEN MonthlyCharges IS NULL THEN 1 ELSE 0 END) AS MonthlyCharges_NULL,
SUM(CASE WHEN TotalCharges IS NULL THEN 1 ELSE 0 END) AS TotalCharges_NULL
FROM CustomerChurn;

-------Replace blank values with NULL

UPDATE CustomerChurn
SET TotalCharges = NULL
WHERE LTRIM(RTRIM(TotalCharges)) = '';

----verify
SELECT COUNT(*) AS NullTotalCharges
FROM CustomerChurn
WHERE TotalCharges IS NULL;
----Fill NULL values
UPDATE CustomerChurn
SET TotalCharges = '0'
WHERE TotalCharges IS NULL;
----Convert TotalCharges to DECIMAL
ALTER TABLE CustomerChurn
ALTER COLUMN TotalCharges DECIMAL(10,2);
---Verify Data Types
EXEC sp_help CustomerChurn;
---to verify both
SELECT
    AVG(MonthlyCharges) AS AvgMonthlyCharges,
    AVG(TotalCharges) AS AvgTotalCharges
FROM CustomerChurn;

----data cleaning over

-----Total Customers
SELECT COUNT(*) AS TotalCustomers
FROM CustomerChurn;

----total churned customers
SELECT COUNT(*) AS ChurnedCustomers
FROM CustomerChurn
WHERE Churn = 'Yes';


----total active customers
SELECT COUNT(*) AS ActiveCustomers
FROM CustomerChurn
WHERE Churn = 'No';


--- churn percentage
SELECT
    ROUND(
        COUNT(CASE WHEN Churn='Yes' THEN 1 END) * 100.0 / COUNT(*),
        2
    ) AS ChurnPercentage
FROM CustomerChurn;



----average montly charges
SELECT
AVG(CAST(MonthlyCharges AS DECIMAL(10,2))) AS AvgMonthlyCharges
FROM CustomerChurn;


-----Churn Rate
SELECT
ROUND(
COUNT(CASE WHEN Churn='Yes' THEN 1 END)*100.0/COUNT(*),2)
AS ChurnRate
FROM CustomerChurn;



----Gender-wise Churn
SELECT
Gender,
COUNT(*) AS Customers,
SUM(CASE WHEN Churn='Yes' THEN 1 ELSE 0 END) AS ChurnedCustomers
FROM CustomerChurn
GROUP BY Gender;


----Contract-wise Churn
SELECT
Contract,
COUNT(*) AS TotalCustomers,
SUM(CASE WHEN Churn='Yes' THEN 1 ELSE 0 END) AS ChurnedCustomers
FROM CustomerChurn
GROUP BY Contract
ORDER BY ChurnedCustomers DESC;



----Payment Method-wise Churn
SELECT
PaymentMethod,
COUNT(*) AS Customers,
SUM(CASE WHEN Churn='Yes' THEN 1 ELSE 0 END) AS Churned
FROM CustomerChurn
GROUP BY PaymentMethod
ORDER BY Churned DESC;


----Internet Service-wise Churn
SELECT
InternetService,
COUNT(*) AS Customers,
SUM(CASE WHEN Churn='Yes' THEN 1 ELSE 0 END) AS Churned
FROM CustomerChurn
GROUP BY InternetService;


-----Average Monthly Charges
SELECT TOP 20 MonthlyCharges
FROM CustomerChurn;
EXEC sp_help CustomerChurn;
-------Highest Paying Customers
SELECT TOP 10
customerID,
MonthlyCharges
FROM CustomerChurn
ORDER BY MonthlyCharges DESC;


---advanced sql query

----Churn Rate by Contract Type
SELECT
    Contract,
    COUNT(*) AS TotalCustomers,
    SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) AS ChurnedCustomers,
    ROUND(
        SUM(CASE WHEN Churn = 'Yes' THEN 1.0 ELSE 0 END) * 100 / COUNT(*),
        2
    ) AS ChurnRate
FROM CustomerChurn
GROUP BY Contract
ORDER BY ChurnRate DESC;

---Revenue by Contract Type
SELECT
    Contract,
    COUNT(*) AS Customers,
    SUM(TotalCharges) AS TotalRevenue
FROM CustomerChurn
GROUP BY Contract
ORDER BY TotalRevenue DESC;

---Churn by Internet Service
SELECT
    InternetService,
    COUNT(*) AS Customers,
    SUM(CASE WHEN Churn='Yes' THEN 1 ELSE 0 END) AS ChurnedCustomers
FROM CustomerChurn
GROUP BY InternetService;

---Average Monthly Charges by Churn Status
SELECT
    Churn,
    AVG(MonthlyCharges) AS AvgMonthlyCharges
FROM CustomerChurn
GROUP BY Churn;

---Top 10 Highest Revenue Customers
SELECT TOP 10
    customerID,
    TotalCharges
FROM CustomerChurn
ORDER BY TotalCharges DESC;




-----Customer Segmentation using CASE
SELECT
    customerID,
    MonthlyCharges,
    CASE
        WHEN MonthlyCharges < 35 THEN 'Low Spending'
        WHEN MonthlyCharges BETWEEN 35 AND 70 THEN 'Medium Spending'
        ELSE 'High Spending'
    END AS CustomerSegment
FROM CustomerChurn;


----Rank Customers by Total Charges
SELECT
    customerID,
    TotalCharges,
    RANK() OVER(ORDER BY TotalCharges DESC) AS CustomerRank
FROM CustomerChurn;


----Dense Rank
SELECT
    customerID,
    TotalCharges,
    DENSE_RANK() OVER(ORDER BY TotalCharges DESC) AS DenseRank
FROM CustomerChurn;

-----Row Number
SELECT
    customerID,
    TotalCharges,
    ROW_NUMBER() OVER(ORDER BY TotalCharges DESC) AS RowNum
FROM CustomerChurn;

----CTE (High Revenue Customers)
WITH HighRevenueCustomers AS
(
    SELECT
        customerID,
        TotalCharges
    FROM CustomerChurn
    WHERE TotalCharges > 5000
)
SELECT *
FROM HighRevenueCustomers;

----Create a View
USE CustomerChurnDB;
GO

IF OBJECT_ID('vw_ChurnCustomers', 'V') IS NOT NULL
DROP VIEW vw_ChurnCustomers;
GO

CREATE VIEW vw_ChurnCustomers
AS
SELECT *
FROM CustomerChurn
WHERE Churn = 'Yes';
GO
SELECT *
FROM vw_ChurnCustomers;

----Top 5 Customers by Revenue
SELECT TOP 5
    customerID,
    TotalCharges
FROM CustomerChurn
ORDER BY TotalCharges DESC;

----Create Business KPIs
---Total Customers
SELECT COUNT(*) AS TotalCustomers
FROM CustomerChurn;

----Churned Customers
SELECT COUNT(*) AS ChurnedCustomers
FROM CustomerChurn
WHERE Churn = 'Yes';

----Active Customers
SELECT COUNT(*) AS ActiveCustomers
FROM CustomerChurn
WHERE Churn = 'No';

----Churn Rate
SELECT
ROUND(
    COUNT(CASE WHEN Churn='Yes' THEN 1 END) * 100.0 / COUNT(*),
    2
) AS ChurnRate
FROM CustomerChurn;

----Total Revenue
SELECT
SUM(TotalCharges) AS TotalRevenue
FROM CustomerChurn;

----Average Monthly Charge
SELECT
AVG(MonthlyCharges) AS AvgMonthlyCharge
FROM CustomerChurn;

--------------------Business Analysis Queries
----Contract-wise Churn
SELECT
    Contract,
    COUNT(*) AS TotalCustomers,
    SUM(CASE WHEN Churn='Yes' THEN 1 ELSE 0 END) AS ChurnedCustomers,
    ROUND(
        SUM(CASE WHEN Churn='Yes' THEN 1.0 ELSE 0 END) * 100 / COUNT(*),
        2
    ) AS ChurnRate
FROM CustomerChurn
GROUP BY Contract
ORDER BY ChurnRate DESC;


-----Gender-wise Churn
SELECT
    Gender,
    COUNT(*) AS Customers,
    SUM(CASE WHEN Churn='Yes' THEN 1 ELSE 0 END) AS ChurnedCustomers
FROM CustomerChurn
GROUP BY Gender;


----Internet Service-wise Churn
SELECT
    InternetService,
    COUNT(*) AS Customers,
    SUM(CASE WHEN Churn='Yes' THEN 1 ELSE 0 END) AS ChurnedCustomers
FROM CustomerChurn
GROUP BY InternetService;

----Payment Method-wise Churn
SELECT
    PaymentMethod,
    COUNT(*) AS Customers,
    SUM(CASE WHEN Churn='Yes' THEN 1 ELSE 0 END) AS ChurnedCustomers
FROM CustomerChurn
GROUP BY PaymentMethod
ORDER BY ChurnedCustomers DESC;


---Senior Citizen Churn
SELECT
    SeniorCitizen,
    COUNT(*) AS Customers,
    SUM(CASE WHEN Churn='Yes' THEN 1 ELSE 0 END) AS ChurnedCustomers
FROM CustomerChurn
GROUP BY SeniorCitizen;

----Tenure-wise Churn
SELECT
    tenure,
    COUNT(*) AS Customers,
    SUM(CASE WHEN Churn='Yes' THEN 1 ELSE 0 END) AS ChurnedCustomers
FROM CustomerChurn
GROUP BY tenure
ORDER BY tenure;

