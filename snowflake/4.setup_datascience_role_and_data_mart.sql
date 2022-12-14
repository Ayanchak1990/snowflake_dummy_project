-- USE DEDICATED WAREHOUSE FOR COMPUTE PURPOSES

USE WAREHOUSE CONVEX_INSURANCE;

-- CREATE USER FOR DATASCIENCE 

CREATE USER DATASCIENCE PASSWORD = '***************' COMMENT = 'THIS IS DUMMY DATA SCIENCE USER' MUST_CHANGE_PASSWORD = TRUE;

-- CREATE ROLE FOR DATA SCIENCE

CREATE ROLE "DATASCIENCE" COMMENT = 'ONLY TO SEE DATA MART DATA';
GRANT ROLE "DATASCIENCE" TO ROLE "SYSADMIN";
grant usage on warehouse CONVEX_INSURANCE to role DATASCIENCE;
grant usage on database CONVEX_INSURANCE to role DATASCIENCE;
grant usage on schema CONVEX_INSURANCE.CONVEX_DATAMART to role DATASCIENCE;
grant select on view CONVEX_DATAMART.DATASCIENCE_OUTPUT to role DATASCIENCE;
grant role DATASCIENCE to user DATASCIENCE;

-- CREATE TABLES FOR DATA WAREHOUSE / INFORMATION VAULT

USE "CONVEX_INSURANCE"."CONVEX_DATAMART";

--CREATE DATAMART FOR DATA SCIENTISTS TO ACCESS FINAL DESIRED OUTPUT

-- customer_id	loyalty_score	product_id	product_category	purchase_co
DROP VIEW DDATASCIENCE_OUTPUT

CREATE OR REPLACE VIEW DATASCIENCE_OUTPUT AS
SELECT
    DC.CUSTOMER_BUSINESS_ID AS customer_id,
    DC.LOYALTY_SCORE,
    DP.PRODUCT_BUSINESS_ID AS product_id,
    DP.PRODUCT_CATEGORY,
    COUNT(*) AS purchase_count
FROM
    CONVEX_WAREHOUSE.FACT_TRANSACTIONS FT
    JOIN CONVEX_WAREHOUSE.DIM_CUSTOMER DC
    ON FT.CUSTOMER_ID = DC.CUSTOMER_ID
    JOIN CONVEX_WAREHOUSE.DIM_PRODUCT DP
    ON FT.PRODUCT_ID = DP.PRODUCT_ID
GROUP BY
        1,2,3,4;